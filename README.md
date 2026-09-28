# Telegram AI Assistant

این پروژه یک کلاینت تلگرام مبتنی بر Telethon است که با حساب کاربری تلگرام اجرا می‌شود و چند قابلیت هوش مصنوعی برای پردازش پیام‌ها، پیام‌های صوتی و فایل‌ها ارائه می‌دهد.

## قابلیت‌ها

- تبدیل پیام صوتی فارسی تلگرام به متن با Google Speech Recognition
- خلاصه‌سازی پیام‌های اخیر یک گفت‌وگو
- گفت‌وگوی مستقیم با یک مدل زبانی از طریق API سازگار با OpenAI
- ارسال فایل تلگرامی به Google Gemini و دریافت خلاصه فارسی
- مدیریت کاربران مجاز برای استفاده از دستور `/chat`
- ذخیره کاربران مجاز در پایگاه داده SQLite

## ساختار پروژه

```text
python1telbot/
├── telethonmain.py             # Telegram client and message handlers
├── Database.py                 # SQLite permission management
├── Voice_to_text_google.py     # Voice conversion and speech recognition
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── LLm_openai/
│   ├── AI_sum.py               # OpenAI-compatible chat completion client
│   └── AI_withgoogle.py        # Google Gemini file analysis client
├── voice_downloads/            # Temporary voice files
└── pdf_downloads/              # Temporary downloaded files
```

فایل‌های `bot_session.session`، `permissions.db`، پوشه‌های موقت، محیط مجازی و فایل‌های `.env` محلی هستند و نباید در GitHub منتشر شوند.

## پیش‌نیازها

- Python 3.10 یا بالاتر
- یک حساب کاربری تلگرام؛ این پروژه با Session حساب کاربری Telethon اجرا می‌شود
- Telegram API ID و API Hash از [my.telegram.org](https://my.telegram.org)
- یک API سازگار با OpenAI برای قابلیت‌های متنی
- یک Google Gemini API Key برای تحلیل فایل
- FFmpeg برای تبدیل پیام‌های صوتی

## نصب

### ۱. دریافت پروژه

```bash
git clone https://github.com/Mhmdone/Telegram-userbot-assistant.git
cd Telegram-userbot-assistant
```

### ۲. ساخت محیط مجازی

در Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

در Linux یا macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### ۳. نصب وابستگی‌های Python

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### ۴. نصب FFmpeg

FFmpeg یک وابستگی سیستمی است و در `requirements.txt` نصب نمی‌شود.

پس از نصب FFmpeg، باید دستور زیر بدون خطا اجرا شود:

```bash
ffmpeg -version
```

اگر این دستور شناخته نشد، مسیر پوشه `bin` مربوط به FFmpeg را به `PATH` سیستم اضافه کنید.

## تنظیم فایل `.env`

فایل `.env.example` را به `.env` در ریشه پروژه کپی کنید:

```text
python1telbot/.env
```

سپس مقادیر واقعی را وارد کنید:

```env
# Telegram API credentials
API_ID=YOUR_TELEGRAM_API_ID
API_HASH=YOUR_TELEGRAM_API_HASH
session_name=bot_session

# OpenAI-compatible LLM endpoint
api_key_openai=YOUR_LLM_API_KEY
base_url_openai=https://YOUR_PROVIDER/v1

# Google Gemini API credential
api_key_google=YOUR_GOOGLE_API_KEY
```

نام متغیرها باید دقیقاً مطابق نمونه باشد. کد از این نام‌ها استفاده می‌کند:

- `API_ID`
- `API_HASH`
- `session_name`
- `api_key_openai`
- `base_url_openai`
- `api_key_google`

فقط یک فایل `.env` در ریشه پروژه استفاده می‌شود. فایل `LLm_openai/.env` لازم نیست.

### API متنی

`AI_sum.py` از رابط `AsyncOpenAI` استفاده می‌کند. سرویس انتخاب‌شده باید API سازگار با OpenAI و endpoint زیر را پشتیبانی کند:

```text
POST /chat/completions
```

اگر سرویس شما OpenAI نیست، مقدار `base_url_openai` و نام مدل در `LLm_openai/AI_sum.py` باید با همان سرویس سازگار باشند. مدل فعلی در کد:

```text
gemini-2.5-flash
```

## اجرای برنامه

از ریشه پروژه اجرا کنید:

```bash
python telethonmain.py
```

در اولین اجرا، Telethon ممکن است شماره تلفن، کد تأیید تلگرام و در صورت فعال بودن، رمز دومرحله‌ای را درخواست کند. پس از ورود موفق، فایل Session ساخته می‌شود و در اجراهای بعدی دوباره ورود لازم نیست.

فایل Session را محرمانه نگه دارید و آن را در GitHub منتشر نکنید.

## دستورات ربات

### تبدیل صوت به متن

روی یک پیام صوتی ریپلای کنید و دستور زیر را ارسال کنید:

```text
/voice
```

ربات فایل صوتی را دانلود، به WAV تبدیل و گفتار فارسی را به متن تبدیل می‌کند.

### خلاصه‌سازی چت

```text
/sumtext MESSAGE_COUNT MAX_TOKENS
```

مثال:

```text
/sumtext 100 1000
```

ربات پیام‌های متنی اخیر را می‌خواند و آن‌ها را با ترتیب قدیمی به جدید برای مدل ارسال می‌کند.

### گفت‌وگو با مدل زبانی

```text
/chat YOUR_MESSAGE
```

مثال:

```text
/chat درباره یادگیری ماشین توضیح بده
```

صاحب حساب متصل می‌تواند از این دستور استفاده کند. سایر کاربران باید ابتدا با `/allow` مجاز شوند.

### مجاز کردن کاربر

روی پیام کاربر ریپلای کنید و دستور زیر را ارسال کنید:

```text
/allow
```

شناسه کاربر در جدول `allowed_users` ذخیره می‌شود.

### حذف دسترسی کاربر

روی پیام کاربر ریپلای کنید و دستور زیر را ارسال کنید:

```text
/ban
```

### خلاصه‌سازی فایل

روی فایل موردنظر، ترجیحاً PDF، ریپلای کنید و دستور زیر را ارسال کنید:

```text
/Askfile
```

فایل به Gemini ارسال می‌شود و خلاصه آن به زبان فارسی در تلگرام برگردانده می‌شود. فایل دانلودشده پس از پردازش از سیستم حذف می‌شود.

## پایگاه داده

پایگاه داده SQLite در کنار `Database.py` با نام زیر ساخته می‌شود:

```text
permissions.db
```

در شروع برنامه، جدول زیر به‌صورت خودکار ایجاد می‌شود:

```text
allowed_users(user_id)
```

برای حفظ فهرست کاربران مجاز، فایل `permissions.db` را حذف نکنید.

## فایل‌های موقت

فایل‌های صوتی در `voice_downloads/` و فایل‌های ارسالی در `pdf_downloads/` ذخیره می‌شوند. این فایل‌ها بعد از پردازش حذف می‌شوند و در `.gitignore` قرار دارند.

## خطاهای رایج

### خطای نبودن API ID یا API Hash

نام متغیرها و خالی نبودن مقادیر زیر را بررسی کنید:

```env
API_ID=
API_HASH=
```

### خطای تبدیل صدا

بررسی کنید که FFmpeg نصب شده و دستور زیر در ترمینال قابل اجرا باشد:

```bash
ffmpeg -version
```

### خطای سرویس مدل زبانی

مقدارهای زیر را بررسی کنید:

```env
api_key_openai=
base_url_openai=
```

همچنین مطمئن شوید سرویس موردنظر از `/chat/completions` و مدل تعریف‌شده در کد پشتیبانی می‌کند.

### خطای Gemini

معتبر بودن کلید زیر و فعال بودن دسترسی Gemini را بررسی کنید:

```env
api_key_google=
```

### کاربر نمی‌تواند از `/chat` استفاده کند

روی پیام همان کاربر ریپلای کنید و `/allow` را اجرا کنید. اطلاعات مجوز در `permissions.db` ذخیره می‌شود.

