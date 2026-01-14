# ⚡ Email Auto-Reply Quick Start (5 মিনিটে সেটআপ!)

## 🎯 আপনি যা করবেন:
আপনার Gmail inbox automatically check করে customer emails এ AI দিয়ে reply পাঠাবে!

---

## 📝 Step 1: Gmail App Password তৈরি করুন (2 মিনিট)

### অপশন A: সরাসরি লিঙ্ক দিয়ে
1. এই link এ যান: https://myaccount.google.com/apppasswords
2. যদি বলে "2-Step Verification চালু করুন" - তাহলে চালু করুন
3. **Select app** → **Other (Custom name)**
4. নাম দিন: `EmailCleaner`
5. **Generate** click করুন
6. 16 digit password copy করুন (যেমন: `abcd efgh ijkl mnop`)

### অপশন B: Manual Steps
```
Google Account → Security → 2-Step Verification → Enable করুন
↓
Security → App passwords → Other (Custom name) → Generate
↓
16 digit password copy করুন
```

---

## ⚙️ Step 2: .env File Configure করুন (1 মিনিট)

`.env` file খুলুন এবং এই দুইটা লাইন পরিবর্তন করুন:

```env
EMAIL_USER=your-email@gmail.com          # ← আপনার Gmail
EMAIL_PASSWORD=abcd efgh ijkl mnop        # ← আপনার 16 digit App Password
```

**Example:**
```env
EMAIL_USER=ruhul.cse.duet@gmail.com
EMAIL_PASSWORD=wxyz abcd efgh 1234
```

---

## 🧪 Step 3: Test করুন (30 সেকেন্ড)

### Terminal এ চালান:
```bash
python test_email_send.py
```

### Expected Output:
```
🔄 Sending test email...
From: your-email@gmail.com
To: your-email@gmail.com
✅ Email sent successfully!

📬 Check your inbox - you should receive a test email.
```

### আপনার inbox check করুন!
- একটা test email পাবেন
- Subject: "Re: Test Email"
- এর মানে email sending কাজ করছে! ✅

---

## 🚀 Step 4: Email Monitor চালু করুন (1 মিনিট)

### প্রথমে LM Studio চালু করুন:
1. LM Studio খুলুন
2. একটা model load করুন (যেমন: `phi-2` বা `mistral`)
3. **Local Server** tab → **Start Server**
4. Port: `1234` (default)

### FastAPI Server চালু করুন (Terminal 1):
```bash
uvicorn app.main:app --reload --port 8000
```

### Email Monitor চালু করুন (Terminal 2):
```bash
python email_monitor.py
```

### Output দেখাবে:
```
🚀 Email Monitor Started
==================================================
⏰ Checking inbox every 60 seconds
Press Ctrl+C to stop

🔍 Checking for unread emails...
📭 No unread emails found
⏸️ Waiting 60 seconds...
```

---

## ✅ Test করুন - Email পাঠান!

### নিজেকে একটা email পাঠান:
1. আপনার Gmail খুলুন
2. নিজেকে email করুন (your-email@gmail.com)
3. Subject: "Need refund for my order"
4. Body: "I want to return my product and get a refund"
5. Send করুন!

### Monitor দেখবে:
```
🔍 Checking for unread emails...
📬 Found 1 unread email(s)
📧 Processing: Need refund for my order
🎯 Action decided: AUTO_REPLY
✅ Sent auto-reply to: your-email@gmail.com
✅ Completed processing: Need refund for my order
```

### আপনি একটা auto-reply পাবেন! 🎉

---

## 🔧 যদি কোনো সমস্যা হয়:

### ❌ "SMTPAuthenticationError"
**Solution:** 
- `.env` এ EMAIL_PASSWORD সঠিক আছে কিনা check করুন
- App Password ব্যবহার করছেন, normal password নয়

### ❌ "Connection refused on port 1234"
**Solution:** 
- LM Studio খুলুন এবং Local Server চালু করুন

### ❌ "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📊 কীভাবে কাজ করে - সহজ ব্যাখ্যা

```
1. কেউ আপনাকে email পাঠায়
        ↓
2. email_monitor.py প্রতি 60 সেকেন্ডে inbox check করে
        ↓
3. নতুন email পেলে AI তে পাঠায়
        ↓
4. AI বুঝে নেয়: এটা refund, complaint, নাকি support request
        ↓
5. AI সিদ্ধান্ত নেয়: Auto-reply পাঠাবো, নাকি human এর কাছে পাঠাবো
        ↓
6. Automatically reply পাঠায় (যদি সহজ প্রশ্ন হয়)
```

---

## 🎯 এখন কী করবেন?

### ✅ আপনার সেটআপ সম্পূর্ণ!

এখন থেকে:
- প্রতি মিনিটে inbox check হবে
- নতুন email এলে automatically process হবে
- সহজ প্রশ্নে auto-reply যাবে
- জটিল ক্ষেত্রে আপনাকে notify করবে

### 📈 পরবর্তী পদক্ষেপ:

1. **Knowledge Base যোগ করুন:**
   - `data/kb_docs/` folder এ আপনার company policies রাখুন
   - Replies আরও accurate হবে

2. **Customize করুন:**
   - `app/crew/agents.py` এ intent এবং actions customize করুন
   - আপনার business needs অনুযায়ী change করুন

3. **Dashboard দেখুন:**
   ```bash
   streamlit run dashboard/app.py
   ```
   - সব emails এক জায়গায় দেখুন
   - Statistics track করুন

---

## 🆘 আরও Help দরকার?

বিস্তারিত guide দেখুন: `EMAIL_SETUP_COMPLETE_GUIDE.md`

---

**Congratulations! আপনার AI Email Assistant এখন live! 🎉**

