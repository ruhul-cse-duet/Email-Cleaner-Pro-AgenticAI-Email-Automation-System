"""
Simple test to check if email sending works
"""
import os
from dotenv import load_dotenv
from app.services.email_service import EmailService
from app.schemas.email_schema import EmailInbound

# Load environment variables
load_dotenv()

# Create test email
test_email = EmailInbound(
    from_address="test@example.com",  # Dummy sender
    subject="Test Email",
    body="This is a test email from EmailCleaner Pro"
)

# Test reply message
reply_text = """
Hello!

This is an automatic test reply from EmailCleaner Pro.

If you receive this email, it means the email system is working correctly! ✅

Best regards,
EmailCleaner Pro
"""

# Send email
print("🔄 Sending test email...")
print(f"From: {os.getenv('EMAIL_USER')}")
print(f"To: {os.getenv('EMAIL_USER')}")  # Send to yourself for testing

try:
    service = EmailService()
    
    # Send to yourself for testing
    test_email.from_address = os.getenv("EMAIL_USER")
    
    service.send_reply(test_email, reply_text)
    print("✅ Email sent successfully!")
    print("\n📬 Check your inbox - you should receive a test email.")
    
except Exception as e:
    print(f"❌ Failed to send email: {e}")
    print("\n⚠️ Possible issues:")
    print("1. Check if EMAIL_USER and EMAIL_PASSWORD are correct in .env")
    print("2. Make sure you're using App Password, not regular password")
    print("3. Check if 2-Step Verification is enabled on Google Account")
