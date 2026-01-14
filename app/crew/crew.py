from __future__ import annotations

import re
import logging
from pathlib import Path

from app.services.llm import LLMClient, LLMError

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def _load_prompt(filename: str) -> str:
    """Load prompt from file with error handling"""
    path = PROMPTS_DIR / filename
    if not path.exists():
        logger.warning(f"Prompt file not found: {filename}")
        return ""
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as e:
        logger.error(f"Failed to read prompt file {filename}: {e}")
        return ""


def _extract_label(text: str, default: str = "general") -> str:
    """Extract alphanumeric label from text"""
    if not text:
        return default
    match = re.search(r"[A-Za-z0-9_]+", text)
    return match.group(0) if match else default


def _normalize_action(text: str) -> str:
    """Normalize action from LLM response"""
    if not text:
        return "TAG_ARCHIVE"
    upper = text.upper()
    if "AUTO_REPLY" in upper or "REPLY" in upper or "AUTO" in upper:
        return "AUTO_REPLY"
    if "ESCALATE" in upper:
        return "ESCALATE"
    if "TAG" in upper or "ARCHIVE" in upper:
        return "TAG_ARCHIVE"
    return "TAG_ARCHIVE"


def _fallback_classification(intent: str, subject: str, body: str) -> str:
    """
    Fallback classification based on intent when LLM classification is unclear.
    Provides rule-based classification as safety net.
    """
    # Convert to lowercase for matching
    intent_lower = intent.lower()
    subject_lower = subject.lower()
    body_lower = body.lower()
    combined_text = subject_lower + " " + body_lower
    
    # Strong complaint indicators - ESCALATE
    strong_complaint_words = ['angry', 'furious', 'outraged', 'disgusted']
    demand_words = ['demand', 'unacceptable', 'manager', 'supervisor', 'lawsuit', 'legal']
    
    if intent_lower == 'complaint':
        # Check if it's a strong complaint
        if any(word in combined_text for word in strong_complaint_words + demand_words):
            return "ESCALATE"
        # Mild complaint might still get auto-reply
        return "AUTO_REPLY"
    
    # Strong escalation indicators in text
    if any(word in combined_text for word in ['terrible', 'horrible', 'worst', 'never again']):
        # Check if it's really angry or just expressing disappointment
        if any(word in combined_text for word in demand_words):
            return "ESCALATE"
    
    # Simple queries - AUTO_REPLY (expanded list)
    auto_reply_intents = [
        'refund_request', 'shipping_inquiry', 'product_inquiry', 
        'general_inquiry', 'support_request', 'order_status',
        'shipping', 'delivery', 'order', 'product', 'warranty',
        'return', 'exchange', 'tracking'
    ]
    
    # Check intent or keywords in text
    if intent_lower in auto_reply_intents:
        return "AUTO_REPLY"
    
    # Check for shipping/delivery keywords
    shipping_keywords = ['shipping', 'delivery', 'arrive', 'ship', 'delivered', 'tracking', 'when will']
    if any(keyword in combined_text for keyword in shipping_keywords):
        return "AUTO_REPLY"
    
    # Check for refund/return keywords
    refund_keywords = ['refund', 'return', 'money back', 'exchange']
    if any(keyword in combined_text for keyword in refund_keywords):
        return "AUTO_REPLY"
    
    # Spam/informational - TAG_ARCHIVE  
    archive_intents = ['spam', 'newsletter', 'notification', 'confirmation']
    if intent_lower in archive_intents:
        return "TAG_ARCHIVE"
    
    # Default to AUTO_REPLY for customer questions
    return "AUTO_REPLY"


def _parse_tags(text: str) -> list[str]:
    """Parse comma/newline separated tags"""
    if not text:
        return []
    parts = re.split(r"[,\n]+", text)
    return [part.strip() for part in parts if part.strip()]


class CrewError(Exception):
    """Base exception for Crew errors"""
    pass


class SimpleCrew:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm = llm_client
        self.intent_prompt = _load_prompt("intent.txt")
        self.classify_prompt = _load_prompt("classify.txt")
        self.autoreply_prompt = _load_prompt("autoreply.txt")
        self.escalate_prompt = _load_prompt("escalate.txt")

    def kickoff(self, inputs: dict) -> dict:
        """
        Process email through the crew workflow with error handling.
        
        Args:
            inputs: Dictionary with 'subject' and 'body'
            
        Returns:
            Dictionary with processing results
            
        Raises:
            CrewError: If critical processing fails
        """
        subject = inputs.get("subject", "")
        body = inputs.get("body", "")

        if not subject and not body:
            logger.error("Empty email provided to crew")
            return {
                "intent": "unknown",
                "action": "ESCALATE",
                "error": "Empty email content",
                "summary": "Email has no content"
            }

        # Step 1: Intent Detection
        try:
            intent_prompt = (
                f"Subject: {subject}\n"
                f"Body: {body}\n"
                "Return a single snake_case intent label."
            )
            intent_raw = self.llm.generate(
                intent_prompt, 
                system_prompt=self.intent_prompt, 
                max_tokens=32
            )
            intent = _extract_label(intent_raw).lower()
            logger.info(f"Detected intent: {intent}")
        except LLMError as e:
            logger.error(f"Intent detection failed: {e}")
            intent = "unknown"

        # Step 2: Classification
        try:
            classify_prompt = (
                f"Subject: {subject}\n"
                f"Body: {body}\n"
                f"Intent: {intent}\n\n"
                "Based on the email content and intent, return only one label: AUTO_REPLY, TAG_ARCHIVE, or ESCALATE."
            )
            action_raw = self.llm.generate(
                classify_prompt, 
                system_prompt=self.classify_prompt, 
                max_tokens=32
            )
            action = _normalize_action(action_raw)
            
            # Apply intelligent fallback logic
            fallback_action = _fallback_classification(intent, subject, body)
            
            # If LLM and fallback disagree, log and use fallback for customer queries
            if action != fallback_action:
                logger.info(f"LLM classified as {action}, fallback suggests {fallback_action}")
                
                # Trust fallback for AUTO_REPLY suggestions (it's keyword-based and reliable)
                if fallback_action == "AUTO_REPLY":
                    logger.info(f"Using fallback classification: {fallback_action}")
                    action = fallback_action
                # For ESCALATE, check if LLM has good reason
                elif action == "ESCALATE" and fallback_action != "ESCALATE":
                    # Only escalate if there are strong indicators
                    strong_escalate = any(word in (subject + " " + body).lower() 
                                        for word in ['lawsuit', 'legal', 'lawyer', 'attorney', 'sue'])
                    if not strong_escalate:
                        logger.info(f"Overriding ESCALATE with fallback: {fallback_action}")
                        action = fallback_action
            
            logger.info(f"Final classified action: {action}")
        except LLMError as e:
            logger.error(f"Classification failed: {e}, using fallback")
            action = _fallback_classification(intent, subject, body)

        result = {"intent": intent, "action": action}

        # Step 3: Execute Action
        try:
            if action == "AUTO_REPLY":
                reply_prompt = (
                    f"Subject: {subject}\n"
                    f"Body: {body}\n"
                    f"Intent: {intent}\n"
                    "Write a concise, helpful reply."
                )
                reply = self.llm.generate(
                    reply_prompt, 
                    system_prompt=self.autoreply_prompt, 
                    max_tokens=256
                )
                result["reply"] = reply
                result["tags"] = [intent]
                logger.info(f"Generated auto-reply ({len(reply)} chars)")
                
            elif action == "TAG_ARCHIVE":
                tags_prompt = f"Intent: {intent}\nReturn 1-3 short tags, comma-separated."
                tags_raw = self.llm.generate(
                    tags_prompt, 
                    system_prompt="You assign mailbox tags."
                )
                tags = _parse_tags(tags_raw)
                result["tags"] = tags or [intent]
                logger.info(f"Assigned tags: {result['tags']}")
                
            elif action == "ESCALATE":
                summary_prompt = (
                    f"Subject: {subject}\n"
                    f"Body: {body}\n"
                    "Summarize the issue for a human agent."
                )
                summary = self.llm.generate(
                    summary_prompt, 
                    system_prompt=self.escalate_prompt, 
                    max_tokens=256
                )
                result["summary"] = summary
                logger.info(f"Generated escalation summary")
                
        except LLMError as e:
            logger.error(f"Action execution failed: {e}")
            result["error"] = str(e)
            result["action"] = "ESCALATE"
            result["summary"] = f"Processing failed: {str(e)}"

        return result


def build_crew() -> SimpleCrew:
    """Factory function to create SimpleCrew instance"""
    try:
        return SimpleCrew(LLMClient())
    except Exception as e:
        logger.error(f"Failed to build crew: {e}")
        raise CrewError(f"Crew initialization failed: {e}") from e
