# 📧 EmailCleaner Pro - AI-Powered Email Automation System

<div align="center">

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![CrewAI](https://img.shields.io/badge/CrewAI-Enabled-orange)
![Gmail](https://img.shields.io/badge/Gmail-Integrated-red)

**স্বয়ংক্রিয়ভাবে emails পড়ে, বুঝে, এবং reply পাঠায়!**

[Quick Start (Bangla)](#-quick-start-bangla) • [Features](#-features) • [Setup Guide](#-setup-guide) • [Documentation](#-documentation)

</div>

---

## 🎯 What is EmailCleaner Pro?

EmailCleaner Pro একটি intelligent email automation system যা:

- ✅ **Automatic email processing** - Inbox monitor করে এবং নতুন email detect করে
- ✅ **AI-powered intent detection** - Email এর উদ্দেশ্য বোঝে (refund, complaint, support, etc.)
- ✅ **Smart classification** - সিদ্ধান্ত নেয় কী action নিতে হবে
- ✅ **Auto-reply generation** - সহজ queries এ automatically reply পাঠায়
- ✅ **Human escalation** - জটিল issues মানুষের কাছে পাঠায়
- ✅ **Gmail integration** - আপনার Gmail এর সাথে সরাসরি কাজ করে

---

## 🚀 Quick Start (Bangla)

### মাত্র 5 মিনিটে চালু করুন!

#### 1️⃣ Gmail App Password তৈরি করুন
```
1. https://myaccount.google.com/apppasswords এ যান
2. 2-Step Verification চালু করুন
3. App Password generate করুন
4. 16 digit password copy করুন
```

#### 2️⃣ Environment Configure করুন
```bash
# .env file edit করুন
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-16-digit-app-password
```

#### 3️⃣ Dependencies Install করুন
```bash
pip install -r requirements.txt
```

#### 4️⃣ LM Studio চালু করুন
```
1. LM Studio খুলুন
2. Model load করুন (phi-2 or mistral)
3. Local Server start করুন (port 1234)
```

#### 5️⃣ Test করুন
```bash
# Email পাঠানো test করুন
python test_email_send.py

# Server চালু করুন
uvicorn app.main:app --reload --port 8000

# Email monitor চালু করুন (নতুন terminal এ)
python email_monitor.py
```

#### 6️⃣ নিজেকে email পাঠিয়ে test করুন!
```
Subject: Need refund
Body: I want to return my product
→ আপনি auto-reply পাবেন! 🎉
```

**📚 বিস্তারিত guide:** [`QUICK_START_BANGLA.md`](QUICK_START_BANGLA.md)

---

## ✨ Features

### 🤖 AI-Powered Processing
- **Intent Detection:** Email এর মূল উদ্দেশ্য identify করে
- **Smart Classification:** Automatic, Tag, অথবা Escalate - সঠিক action নেয়
- **Context-Aware Replies:** Company policies এবং knowledge base ব্যবহার করে reply তৈরি করে

### 📧 Gmail Integration
- **IMAP Support:** Automatic inbox monitoring
- **SMTP Support:** Secure email sending with TLS
- **Real-time Processing:** নতুন emails instantly detect করে

### 🎯 Action Types
1. **AUTO_REPLY** ✉️ - সহজ queries এ automatically reply
2. **TAG_ARCHIVE** 🏷️ - ট্যাগ করে সংরক্ষণ
3. **ESCALATE** 🚨 - Complex issues মানুষের কাছে পাঠায়

### 🔐 Security
- App Password authentication
- TLS/SSL encryption
- Environment-based configuration
- No credentials in code

---

## 🏗️ Architecture

```
Email Arrives → Email Monitor → CrewAI Processing → Action Execution
                                    │
                    ┌───────────────┼───────────────┐
                    ↓               ↓               ↓
              Intent Agent   Classification   Auto Reply
                                  Agent          Agent
```

**Full architecture:** [`VISUAL_GUIDE.md`](VISUAL_GUIDE.md)

---

## 📁 Project Structure

```
Email Cleaner Agentic CrewAI/
├── 📄 Configuration
│   ├── .env                        # Your settings (create from .env.example)
│   └── .env.example                # Template
│
├── 🧪 Testing
│   ├── test_emails.py              # Pytest unit tests (FIXED!)
│   └── test_email_send.py          # Manual email test
│
├── 🤖 Core Application
│   ├── email_monitor.py            # Automatic inbox checker (NEW!)
│   └── app/
│       ├── main.py                 # FastAPI application
│       ├── api/                    # API endpoints
│       ├── crew/                   # AI agents
│       ├── services/               # Business logic
│       │   └── email_service.py    # Gmail integration (REWRITTEN!)
│       ├── schemas/                # Data models
│       └── utils/                  # Utilities
│
└── 📚 Documentation
    ├── README.md                   # This file
    ├── QUICK_START_BANGLA.md       # 5-minute setup guide
    ├── EMAIL_SETUP_COMPLETE_GUIDE.md # Detailed setup
    ├── VISUAL_GUIDE.md             # Visual diagrams
    └── SUMMARY_REPORT.md           # What was fixed
```

---

## 🔧 Recent Updates (January 2025)

### ✅ Issues Fixed:
1. **Pytest Error** - Fixed fixture and status code issues
2. **Email Service** - Implemented full Gmail SMTP/IMAP integration
3. **Auto-reply** - Now actually sends emails!

### ✅ New Features:
1. **`email_monitor.py`** - Automatic inbox monitoring
2. **`test_email_send.py`** - Easy email testing
3. **Complete documentation** - Bangla guides for easy setup

### ✅ Improvements:
- Error handling with detailed logging
- TLS encryption for security
- Configurable check intervals
- Comprehensive test coverage

**Full changelog:** [`SUMMARY_REPORT.md`](SUMMARY_REPORT.md)

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Gmail account with App Password
- LM Studio (for local LLM)

### Step 1: Clone & Install
```bash
git clone <your-repo>
cd "Email Cleaner Agentic CrewAI"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env and set:
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Step 3: Setup LM Studio
```
1. Download from https://lmstudio.ai/
2. Install and open
3. Download a model (e.g., phi-2, mistral-7b)
4. Start Local Server (port 1234)
```

### Step 4: Test
```bash
# Test email sending
python test_email_send.py

# Should output:
# ✅ Email sent successfully!
# 📬 Check your inbox
```

---

## 🎮 Usage

### Method 1: Automatic Monitoring (Recommended)
```bash
# Terminal 1: Start FastAPI server
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start email monitor
python email_monitor.py
```

Email monitor will:
- Check inbox every 60 seconds
- Process new emails automatically
- Send auto-replies for simple queries
- Escalate complex issues

### Method 2: API Endpoint
```bash
# Send email data to webhook
curl -X POST "http://localhost:8000/api/email/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "customer@example.com",
    "subject": "Need refund",
    "body": "I want to return my product",
    "received_at": "2025-01-14T10:00:00Z"
  }'
```

### Method 3: Dashboard
```bash
streamlit run dashboard/app.py
```
- View all processed emails
- See statistics and metrics
- Manual actions

---

## 📊 Intent Types & Actions

### Intent Detection
| Intent | Description | Typical Action |
|--------|-------------|----------------|
| `refund_request` | Customer wants refund | AUTO_REPLY |
| `support_request` | Needs help/support | AUTO_REPLY |
| `complaint` | Unhappy customer | ESCALATE |
| `general_inquiry` | General questions | AUTO_REPLY |
| `spam` | Promotional/spam | TAG_ARCHIVE |

### Action Execution
| Action | What Happens | When Used |
|--------|-------------|-----------|
| AUTO_REPLY | AI generates and sends reply | Simple queries |
| TAG_ARCHIVE | Tags email and archives | Informational |
| ESCALATE | Creates summary, notifies human | Complex/sensitive |

---

## 🧪 Testing

### Unit Tests (Pytest)
```bash
# Run all tests
pytest test_emails.py -v

# Expected output:
# test_emails.py::test_email[Refund Request] PASSED
# test_emails.py::test_email[Shipping Question] PASSED
# test_emails.py::test_email[Complaint] PASSED
# test_emails.py::test_email[General Inquiry] PASSED
# ====== 4 passed in 5.23s ======
```

### Manual Email Test
```bash
python test_email_send.py
```

### Live Testing
1. Start email_monitor.py
2. Send yourself an email
3. Wait 60 seconds
4. Check for auto-reply

---

## 📈 Performance & Monitoring

### Logs
```bash
# View logs
tail -f logs/email_cleaner.log

# Sample log output:
# 2025-01-14 11:45:00 - INFO - 📬 Found 1 unread email(s)
# 2025-01-14 11:45:01 - INFO - 📧 Processing: Need refund
# 2025-01-14 11:45:05 - INFO - ✅ Sent auto-reply
```

### Metrics to Track
- Emails processed per day
- Auto-reply success rate
- Escalation rate
- Average response time
- Error rate

---

## 🔐 Security Best Practices

### ✅ DO:
- Use Gmail App Password (not regular password)
- Enable 2-Step Verification
- Keep `.env` file in `.gitignore`
- Use HTTPS in production
- Rotate App Passwords periodically

### ❌ DON'T:
- Commit credentials to Git
- Use regular Gmail password
- Share `.env` file
- Disable TLS/SSL
- Store passwords in code

---

## 🐛 Troubleshooting

### Issue: "SMTPAuthenticationError"
**Cause:** Wrong email credentials

**Solution:**
```
1. Check EMAIL_USER in .env
2. Verify EMAIL_PASSWORD is App Password (16 digits)
3. Ensure 2-Step Verification is enabled
```

### Issue: "Connection refused on port 1234"
**Cause:** LM Studio not running

**Solution:**
```
1. Open LM Studio
2. Load a model
3. Start Local Server
4. Verify port is 1234
```

### Issue: "No unread emails found"
**Cause:** All emails are already read

**Solution:**
```
1. Send a new email to yourself
2. Or mark existing emails as unread in Gmail
```

### Issue: Pytest fails
**Solution:**
```bash
# Clear cache
pytest --cache-clear

# Ensure server is running
uvicorn app.main:app --reload --port 8000
```

**Full troubleshooting guide:** [`EMAIL_SETUP_COMPLETE_GUIDE.md`](EMAIL_SETUP_COMPLETE_GUIDE.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [`QUICK_START_BANGLA.md`](QUICK_START_BANGLA.md) | 5-minute setup guide (Bangla) |
| [`EMAIL_SETUP_COMPLETE_GUIDE.md`](EMAIL_SETUP_COMPLETE_GUIDE.md) | Detailed setup & troubleshooting |
| [`VISUAL_GUIDE.md`](VISUAL_GUIDE.md) | Architecture & workflow diagrams |
| [`SUMMARY_REPORT.md`](SUMMARY_REPORT.md) | Recent fixes & updates |
| [`SETUP_GUIDE_BANGLA.md`](SETUP_GUIDE_BANGLA.md) | Original setup guide |

---

## 🚀 Deployment

### Docker (Recommended)
```bash
docker-compose up -d
```

### Manual Deployment
1. Use PostgreSQL for production:
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```

2. Set environment variables on server

3. Use process manager (PM2, systemd):
   ```bash
   pm2 start email_monitor.py --name email-monitor
   ```

4. Enable HTTPS with reverse proxy (Nginx)

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more intent types
- [ ] Improve reply generation
- [ ] Add support for attachments
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with more email providers

---

## 📝 License

MIT License - Feel free to use for personal or commercial projects.

---

## 💬 Support

যদি কোনো সমস্যা হয় বা help দরকার হয়:

1. **Check logs:** `logs/email_cleaner.log`
2. **Read docs:** Especially troubleshooting sections
3. **Test components:** Run `test_email_send.py`
4. **Verify config:** Check `.env` file

---

## 🎉 Success!

আপনার AI-powered Email Assistant এখন ready! 

**Next Steps:**
1. ✅ Send a test email to yourself
2. ✅ Watch it get auto-replied
3. ✅ Customize for your business needs
4. ✅ Deploy to production

**Happy Automating! 🚀**

---

<div align="center">

Made with ❤️ using FastAPI, CrewAI, and Gmail

**Star ⭐ this repo if you find it helpful!**

</div>
