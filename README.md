# 🛠️ RESUME BUILDER AI — Blue-Collar Resume Platform

An **AI-powered resume builder** designed specifically for **blue-collar workers in India**. The platform supports **13 Indian languages**, AI-enhanced text, voice input, and intelligent job recommendations — making professional resume creation accessible to everyone.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Multi-Language Support** | English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Odia, Assamese |
| **AI Text Enhancement** | Powered by Google Gemini to improve user-written descriptions |
| **Voice Input** | Speech-to-text for hands-free form filling |
| **Job Recommendations** | AI-driven job matching based on profession, skills, and location |
| **PDF Resume Generation** | Four professional templates — Modern, Classic, Compact, Executive |
| **OTP Authentication** | Mobile number login with SMS OTP verification |
| **AI Chatbot Assistant** | Conversational guidance with text-to-speech support |
| **Profession Verification** | Profession-specific form fields for 12 trades |
| **ID Verification** | Document upload for identity proof |
| **Auto-Save** | Form data persisted via `localStorage` |

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | MySQL |
| AI / ML | Google Gemini API |
| PDF Generation | ReportLab |
| Translation | Google Generative AI, Deep Translator |
| Speech | pyttsx3 (TTS), SpeechRecognition (STT) |
| SMS | Twilio |
| Frontend | HTML, CSS, JavaScript |
| Auth | JWT, SHA-256 hashing |

---

## 📁 Project Structure

```
RESUME_BUILDER_AI/
├── app.py                      # Main Flask application
├── config.py                   # Application configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not tracked)
│
├── database/
│   ├── config.py               # Database configuration
│   ├── init_db.py              # Database initialisation script
│   └── schema.sql              # MySQL schema (users, jobs, sessions, OTPs)
│
├── services/
│   ├── assistant_service.py    # Gemini-based AI chatbot
│   ├── file_upload.py          # File upload handler
│   └── sms_service.py          # Twilio SMS / OTP service
│
├── utils/
│   ├── ai_helper.py            # AI text enhancement & resume sections
│   ├── auth.py                 # Authentication, OTP, JWT, validation
│   ├── job_recommender.py      # AI job recommendations
│   ├── resume_generator.py     # PDF resume generation (4 templates)
│   ├── speech_recognition.py   # Audio transcription
│   └── translation.py          # Multi-language translation engine
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html
│   ├── language.html
│   ├── login.html
│   ├── verify_otp.html
│   ├── passkey_login.html
│   ├── profession.html
│   ├── verification.html
│   ├── profile.html
│   ├── id_verification.html
│   ├── stay_signed_in.html
│   ├── resume.html
│   └── jobs.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── responsive.css
│   └── js/
│       ├── main.js
│       ├── chatbot.js
│       ├── translation.js
│       └── voice-input.js
│
└── uploads/                    # User-generated files (not tracked)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/BhartiKumarii/RESUME_BUILDER_AI.git
cd RESUME_BUILDER_AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
PORT=5000

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=bluecollar

UPLOAD_FOLDER=uploads

GEMINI_API_KEY=your-gemini-api-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

### 5. Initialise the Database

```bash
python database/init_db.py
```

### 6. Run the Application

```bash
python app.py
```

The app will be available at **http://localhost:5000**.

---

## 🔄 Application Flow

1. **Language Selection** → Choose from 13 supported languages
2. **Login** → Enter mobile number and receive OTP
3. **OTP Verification** → Verify the one-time password
4. **Profession Selection** → Pick from 12 blue-collar professions
5. **Professional Verification** → Fill profession-specific details
6. **Profile** → Enter personal information
7. **ID Verification** → Upload identity documents
8. **Stay Signed In** → Optional passkey setup
9. **Resume Generation** → Choose a template and generate a PDF
10. **Job Recommendations** → View AI-matched job listings

---

## 👷 Supported Professions

Driver · Electrician · Plumber · Carpenter · Mechanic · Welder · Construction Worker · Painter · Mason · Gardener · Security Guard · Cleaner

---

## 🌐 Supported Languages

English · हिन्दी · தமிழ் · తెలుగు · বাংলা · मराठी · ગુજરાતી · ಕನ್ನಡ · മലയാളം · ਪੰਜਾਬੀ · اردو · ଓଡ଼ିଆ · অসমীয়া

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Bharti Kumari**
B.Tech CSE — Einstein Academy of Technology and Management, Bhubaneswar

- GitHub: [@BhartiKumarii](https://github.com/BhartiKumarii)
