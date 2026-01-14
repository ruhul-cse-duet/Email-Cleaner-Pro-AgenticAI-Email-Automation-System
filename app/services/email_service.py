"""
Email Service - Gmail Integration
Handles sending and receiving emails through Gmail IMAP/SMTP
"""
import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

from app.schemas.email_schema import EmailInbound

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for Gmail integration"""
    
    def __init__(self):
        # Gmail configuration from environment variables
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_host = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
        self.imap_host = os.getenv("EMAIL_IMAP_HOST", "imap.gmail.com")
        
        # Validate configuration
        if not self.email_user or not self.email_password:
            logger.warning("Email credentials not configured. Email sending will be disabled.")
    
    def send_reply(self, email: EmailInbound, reply_text: str) -> None:
        """
        Send reply email using Gmail SMTP
        
        Args:
            email: Original email to reply to
            reply_text: Reply message text
        """
        if not self.email_user or not self.email_password:
            logger.error("Cannot send email - credentials not configured")
            return
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = email.from_address
            msg['Subject'] = f"Re: {email.subject}"
            
            # Add reply text
            msg.attach(MIMEText(reply_text, 'plain'))
            
            # Connect to Gmail SMTP
            logger.info(f"Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            
            # Login
            logger.info(f"Logging in as: {self.email_user}")
            server.login(self.email_user, self.email_password)
            
            # Send email
            logger.info(f"Sending reply to: {email.from_address}")
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Successfully sent reply to {email.from_address}")
            
        except smtplib.SMTPAuthenticationError:
            logger.error("❌ SMTP Authentication failed! Check your email credentials.")
            logger.error("Make sure you're using Gmail App Password, not your regular password")
            raise
            
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            raise
    
    def fetch_unread(self) -> list[EmailInbound]:
        """
        Fetch unread emails from Gmail IMAP
        
        Returns:
            List of unread emails
        """
        if not self.email_user or not self.email_password:
            logger.error("Cannot fetch emails - credentials not configured")
            return []
        
        emails = []
        
        try:
            # Connect to Gmail IMAP
            logger.info(f"Connecting to IMAP server: {self.imap_host}")
            mail = imaplib.IMAP4_SSL(self.imap_host)
            
            # Login
            logger.info(f"Logging in as: {self.email_user}")
            mail.login(self.email_user, self.email_password)
            
            # Select inbox
            mail.select("INBOX")
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != "OK":
                logger.error("Failed to search for emails")
                return []
            
            email_ids = messages[0].split()
            logger.info(f"Found {len(email_ids)} unread emails")
            
            # Fetch each email
            for email_id in email_ids:
                try:
                    status, msg_data = mail.fetch(email_id, "(RFC822)")
                    
                    if status != "OK":
                        continue
                    
                    # Parse email
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Extract fields
                    from_address = msg.get("From", "")
                    subject = msg.get("Subject", "")
                    
                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    # Create EmailInbound object
                    email_obj = EmailInbound(
                        from_address=from_address,
                        subject=subject,
                        body=body,
                        received_at=datetime.now().isoformat()
                    )
                    
                    emails.append(email_obj)
                    logger.info(f"Fetched email: {subject}")
                    
                except Exception as e:
                    logger.error(f"Error parsing email {email_id}: {e}")
                    continue
            
            # Close connection
            mail.close()
            mail.logout()
            
            logger.info(f"✅ Successfully fetched {len(emails)} emails")
            return emails
            
        except imaplib.IMAP4.error as e:
            logger.error(f"❌ IMAP error: {e}")
            return []
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch emails: {e}")
            return []
