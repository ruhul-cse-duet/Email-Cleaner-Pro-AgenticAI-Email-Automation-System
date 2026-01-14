from fastapi import APIRouter, HTTPException, status
import logging

from app.schemas.email_schema import EmailInbound
from app.crew.crew import build_crew, CrewError
from app.services.email_service import EmailService
from app.services.tagging_service import TaggingService
from app.services.escalation_service import EscalationService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/email/webhook")
def process_email(payload: EmailInbound) -> dict:
    """
    Process incoming email through the AI workflow.
    
    Args:
        payload: Email data
        
    Returns:
        Processing result
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Processing email: {payload.subject}")
        
        # Initialize crew
        crew = build_crew()
        
        # Process email through crew
        result = crew.kickoff(inputs={
            "subject": payload.subject, 
            "body": payload.body
        })

        action = result.get("action")
        
        # Execute appropriate action
        try:
            if action == "AUTO_REPLY":
                reply = result.get("reply", "")
                if reply:
                    EmailService().send_reply(payload, reply)
                    logger.info(f"Sent auto-reply for: {payload.subject}")
                else:
                    logger.warning("Auto-reply action but no reply generated")
                    
            elif action == "TAG_ARCHIVE":
                tags = result.get("tags", [])
                TaggingService().tag_and_archive(payload, tags)
                logger.info(f"Tagged email with: {tags}")
                
            elif action == "ESCALATE":
                summary = result.get("summary", "No summary available")
                EscalationService().notify_human(payload, summary)
                logger.info(f"Escalated email: {payload.subject}")
                
        except Exception as e:
            logger.error(f"Action execution failed: {e}")
            result["action_error"] = str(e)

        return {
            "status": "processed", 
            "action": action,
            "intent": result.get("intent", "unknown"),
            "details": result
        }
        
    except CrewError as e:
        logger.error(f"Crew processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Email processing failed: {str(e)}"
        )
        
    except Exception as e:
        logger.error(f"Unexpected error processing email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during email processing"
        )
