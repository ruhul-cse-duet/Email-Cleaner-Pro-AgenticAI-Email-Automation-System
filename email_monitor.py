"""
Email Monitor - Automatically checks inbox and processes emails.
"""
import logging
import time

from dotenv import load_dotenv

from app.crew.crew import build_crew
from app.services.email_service import EmailService
from app.services.escalation_service import EscalationService
from app.services.tagging_service import TaggingService
from app.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

load_dotenv()


def process_unread_emails() -> None:
    """Fetch and process unread emails."""
    logger.info("Checking for unread emails...")

    email_service = EmailService()
    unread_emails = email_service.fetch_unread()

    if not unread_emails:
        logger.info("No unread emails found")
        return

    logger.info("Found %s unread email(s)", len(unread_emails))

    for email in unread_emails:
        try:
            logger.info("Processing email: %s", email.subject)

            crew = build_crew()
            result = crew.kickoff(inputs={
                "subject": email.subject,
                "body": email.body,
            })

            action = result.get("action")
            logger.info("Action decided: %s", action)

            if action == "AUTO_REPLY":
                reply = result.get("reply", "")
                if reply:
                    email_service.send_reply(email, reply)
                    logger.info("Sent auto-reply for: %s", email.subject)
                else:
                    logger.warning("Auto-reply action but no reply generated")

            elif action == "TAG_ARCHIVE":
                tags = result.get("tags", [])
                TaggingService().tag_and_archive(email, tags)
                logger.info("Tagged email with: %s", tags)

            elif action == "ESCALATE":
                summary = result.get("summary", "No summary available")
                EscalationService().notify_human(email, summary)
                logger.info("Escalated email: %s", email.subject)

            else:
                logger.warning("Unknown action: %s", action)

            logger.info("Completed processing: %s", email.subject)

        except Exception as exc:
            logger.error("Error processing email: %s", exc)
            continue


def main() -> None:
    """Main monitoring loop."""
    logger.info("Email Monitor Started")
    logger.info("=" * 50)

    check_interval = 60
    logger.info("Checking inbox every %s seconds", check_interval)
    logger.info("Press Ctrl+C to stop")

    try:
        while True:
            process_unread_emails()
            logger.info("Waiting %s seconds...", check_interval)
            logger.info("=" * 50)
            time.sleep(check_interval)

    except KeyboardInterrupt:
        logger.info("Email Monitor Stopped")
        logger.info("Goodbye!")


if __name__ == "__main__":
    main()
