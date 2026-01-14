# 📧 Complete Email Auto-Reply Setup Guide (Bangla)

## 🎯 এই Guide এ যা যা শিখবেন:

1. ✅ **Gmail App Password তৈরি করা**
2. ✅ **Environment Variables Configure করা**
3. ✅ **Email পাঠানো Test করা**
4. ✅ **Automatic Email Checking সেটআপ করা**
5. ✅ **Pytest Fix করা**

---

## 🔐 Step 1: Gmail App Password তৈরি করুন

### কেন App Password দরকার?
Gmail এর normal password দিয়ে third-party apps access করা যায় না। Security এর জন্য Google এ "App Password" ব্যবহার করতে হয়।

### কীভাবে App Password তৈরি করবেন:

#### 1. Google Account Settings এ যান
- যান: https://myaccount.google.com/
- অথবা: Google Account → Security

#### 2. 2-Step Verification চালু করুন (যদি না থাকে)
```
Google Account → Security → 2-Step Verification → Get Started
```
- আপনার phone number দিয়ে verify করুন
- এটা **একবার** করতে হবে

#### 3. App Password তৈরি করুন
```
Google Account → Security → 2-Step Verification → App passwords
```

অথবা সরাসরি: https://myaccount.google.com/apppasswords

**Steps:**
1. "Select app" → **Other (Custom name)**
2. নাম দিন: `EmailCleaner Pro`
3. **Generate** click করুন
4. একটা **16 digit password** পাবেন (যেমন: `abcd efgh ijkl mnop`)
5. এটা **copy করে safe জায়গায় রাখুন** - এটা আর দেখা যাবে না!

---

## ⚙️ Step 2: Environment Variables Configure করুন

`.env` file খুলুন এবং এই values দিন:

```env
# Application Settings
APP_ENV=local
LOG_LEVEL=INFO

# Database (শুরুতে SQLite দিয়েই চালান)
DATABASE_URL=sqlite:///./emailcleaner.db

# LLM Configuration (LM Studio)
LLM_PROVIDER=lmstudio
LLM_BASE_URL=http://localhost:1234/v1
LLM_MODEL=liquid/lfm2-1.2b
LLM_API_KEY=
LLM_TEMPERATURE=0.2
LLM_TIMEOUT=300

# ⭐ Email Settings (এখানে আপনার info দিন)
EMAIL_PROVIDER=gmail
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USER=your-email@gmail.com          # আপনার Gmail address
EMAIL_PASSWORD=abcd efgh ijkl mnop        # আপনার 16 digit App Password

TENANT_HEADER=X-Tenant-Id
```

### ⚠️ Important Notes:
- `EMAIL_USER`: আপনার Gmail address (যেমন: `ruhul.cse.duet@gmail.com`)
- `EMAIL_PASSWORD`: 16 digit App Password (spaces সহ বা ছাড়া - দুটোই কাজ করবে)
- **Normal Gmail password দেবেন না!** শুধু App Password!

---

## 🧪 Step 3: Email পাঠানো Test করুন

### Test 1: Python Script দিয়ে Test করুন

একটা নতুন file তৈরি করুন: `test_email_send.py`

```python
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
    print("\nCheck your inbox - you should receive a test email.")
    
except Exception as e:
    print(f"❌ Failed to send email: {e}")
    print("\nPossible issues:")
    print("1. Check if EMAIL_USER and EMAIL_PASSWORD are correct in .env")
    print("2. Make sure you're using App Password, not regular password")
    print("3. Check if 2-Step Verification is enabled on Google Account")
```

**চালান:**
```bash
python test_email_send.py
```

**Expected Output:**
```
🔄 Sending test email...
From: your-email@gmail.com
To: your-email@gmail.com
✅ Email sent successfully!

Check your inbox - you should receive a test email.
```

---

## 🤖 Step 4: Automatic Email Checking সেটআপ করুন

আপনার inbox automatically check করার জন্য একটা script তৈরি করুন:


### একটা Email Monitor Script তৈরি করুন: `email_monitor.py`

```python
"""
Email Monitor - Automatically checks inbox and processes emails
"""
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

from app.services.email_service import EmailService
from app.crew.crew import build_crew

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()


def process_unread_emails():
    """Fetch and process unread emails"""
    
    logger.info("🔍 Checking for unread emails...")
    
    # Fetch unread emails
    email_service = EmailService()
    unread_emails = email_service.fetch_unread()
    
    if not unread_emails:
        logger.info("📭 No unread emails found")
        return
    
    logger.info(f"📬 Found {len(unread_emails)} unread email(s)")
    
    # Process each email
    for email in unread_emails:
        try:
            logger.info(f"📧 Processing: {email.subject}")
            
            # Build crew and process
            crew = build_crew()
            result = crew.kickoff(inputs={
                "subject": email.subject,
                "body": email.body
            })
            
            action = result.get("action")
            logger.info(f"🎯 Action decided: {action}")
            
            # Execute action
            if action == "AUTO_REPLY":
                reply = result.get("reply", "")
                if reply:
                    email_service.send_reply(email, reply)
                    logger.info(f"✅ Sent auto-reply to: {email.from_address}")
                else:
                    logger.warning("⚠️ No reply generated")
                    
            elif action == "TAG_ARCHIVE":
                tags = result.get("tags", [])
                logger.info(f"🏷️ Tagged with: {tags}")
                
            elif action == "ESCALATE":
                logger.info(f"🚨 Escalated to human")
            
            logger.info(f"✅ Completed processing: {email.subject}\n")
            
        except Exception as e:
            logger.error(f"❌ Error processing email: {e}\n")
            continue


def main():
    """Main monitoring loop"""
    
    logger.info("🚀 Email Monitor Started")
    logger.info("=" * 50)
    
    # Check interval in seconds
    CHECK_INTERVAL = 60  # Check every 1 minute (আপনি এটা change করতে পারেন)
    
    logger.info(f"⏰ Checking inbox every {CHECK_INTERVAL} seconds")
    logger.info(f"Press Ctrl+C to stop\n")
    
    try:
        while True:
            process_unread_emails()
            
            # Wait before next check
            logger.info(f"⏸️ Waiting {CHECK_INTERVAL} seconds...")
            logger.info("=" * 50 + "\n")
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\n🛑 Email Monitor Stopped")
        logger.info("Goodbye! 👋")


if __name__ == "__main__":
    main()
```

**এই Script চালান:**
```bash
python email_monitor.py
```

**Output দেখাবে:**
```
🚀 Email Monitor Started
==================================================
⏰ Checking inbox every 60 seconds
Press Ctrl+C to stop

🔍 Checking for unread emails...
📬 Found 2 unread email(s)
📧 Processing: Need refund for order #12345
🎯 Action decided: AUTO_REPLY
✅ Sent auto-reply to: customer@example.com
✅ Completed processing: Need refund for order #12345

📧 Processing: How long does shipping take?
🎯 Action decided: AUTO_REPLY
✅ Sent auto-reply to: buyer@example.com
✅ Completed processing: How long does shipping take?

⏸️ Waiting 60 seconds...
==================================================
```

---

## 🧪 Step 5: Pytest Fix করুন

আপনার pytest error fix হয়ে গেছে! এখন test চালান:

### Test চালানোর আগে:

1. **Server চালু করুন** (নতুন terminal এ):
```bash
uvicorn app.main:app --reload --port 8000
```

2. **LM Studio চালু করুন** এবং local server start করুন

3. **Test চালান**:
```bash
pytest test_emails.py -v
```

**Expected Output:**
```
test_emails.py::test_email[Refund Request] PASSED
test_emails.py::test_email[Shipping Question] PASSED
test_emails.py::test_email[Complaint] PASSED
test_emails.py::test_email[General Inquiry] PASSED

====== 4 passed in 5.23s ======
```

---

## 🎯 Complete Workflow - এক নজরে

```
┌─────────────────────────┐
│  1. Email আসে           │
│  (Gmail Inbox)          │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│  2. email_monitor.py    │
│  (Every 60 seconds)     │
│  - Fetches unread       │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│  3. CrewAI Processing   │
│  - Intent Detection     │
│  - Classification       │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│  4. Action Execution    │
│  - AUTO_REPLY ✉️        │
│  - TAG_ARCHIVE 🏷️      │
│  - ESCALATE 🚨          │
└─────────────────────────┘
```

---

## ✅ Final Checklist

এই steps সব complete করুন:

- [ ] Google Account এ 2-Step Verification চালু করেছেন
- [ ] Gmail App Password তৈরি করেছেন
- [ ] `.env` file এ EMAIL_USER এবং EMAIL_PASSWORD দিয়েছেন
- [ ] `test_email_send.py` চালিয়ে test email পেয়েছেন
- [ ] LM Studio চালু করেছেন এবং model load করেছেন
- [ ] FastAPI server চালু করেছেন (`uvicorn app.main:app --reload`)
- [ ] `email_monitor.py` চালু করেছেন
- [ ] pytest test pass করেছে

---

## 🔧 Troubleshooting Common Issues

### Issue 1: "SMTPAuthenticationError"
**Problem:** Email credentials wrong
**Solution:**
- Check `.env` file এ EMAIL_USER এবং EMAIL_PASSWORD সঠিক আছে কিনা
- App Password ব্যবহার করছেন, normal password নয়
- 2-Step Verification চালু আছে কিনা check করুন

### Issue 2: "Connection refused on port 1234"
**Problem:** LM Studio চালু নেই
**Solution:**
- LM Studio খুলুন
- একটা model load করুন
- "Local Server" start করুন
- Port 1234 check করুন

### Issue 3: "No unread emails found" কিন্তু inbox এ email আছে
**Problem:** Email already marked as read
**Solution:**
- Gmail এ যান এবং একটা email কে "Mark as unread" করুন
- অথবা নতুন email পাঠান

### Issue 4: Pytest fails with "fixture 'email_data' not found"
**Problem:** Pytest cache issue
**Solution:**
```bash
# Clear pytest cache
pytest --cache-clear

# অথবা cache folder delete করুন
rm -rf .pytest_cache
```

### Issue 5: "Unable to open database file"
**Problem:** SQLite database file create করতে পারছে না
**Solution:**
```bash
# Database file manually তৈরি করুন
touch emailcleaner.db

# অথবা .env এ path সঠিক করুন
DATABASE_URL=sqlite:///./emailcleaner.db
```

---

## 🚀 Next Steps (পরবর্তী কাজ)

1. **Knowledge Base যোগ করুন**
   - `data/kb_docs/` তে আপনার company policies, FAQs যোগ করুন
   - এতে replies আরও accurate হবে

2. **Custom Intent যোগ করুন**
   - `app/crew/agents.py` তে নতুন intent types যোগ করুন
   - আপনার business needs অনুযায়ী customize করুন

3. **Dashboard ব্যবহার করুন**
   ```bash
   streamlit run dashboard/app.py
   ```
   - সব emails দেখুন
   - Statistics দেখুন
   - Manual actions করুন

4. **Production Deploy করুন**
   - Docker দিয়ে containerize করুন
   - AWS/Azure/DigitalOcean এ deploy করুন
   - Domain setup করুন

---

## 📞 Support & Help

যদি আরও help দরকার হয়:
1. Logs check করুন: `logs/email_cleaner.log`
2. API docs দেখুন: `http://localhost:8000/docs`
3. LM Studio console check করুন

---

**শুভকামনা! এখন আপনার AI Email Assistant সম্পূর্ণ ready! 🎉**

