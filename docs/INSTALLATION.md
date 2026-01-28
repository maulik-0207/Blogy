# 🔧 Blogy - Installation Guide

This guide provides detailed, step-by-step instructions for setting up the Blogy Django blogging platform on your local machine.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

| Software | Minimum Version | Download Link |
|----------|----------------|---------------|
| **Python** | 3.10+ | [python.org](https://www.python.org/downloads/) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/downloads) |
| **Redis** | 7.0+ | [redis.io](https://redis.io/download) (Linux/Mac) |
| **Memurai** | Latest | [memurai.com](https://www.memurai.com/) (Windows alternative to Redis) |

### Optional but Recommended
- **Virtual Environment**: `venv` or `virtualenv` (included with Python 3.3+)
- **Code Editor**: VS Code, PyCharm, or your preferred IDE

---

## 🚀 Installation Steps

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/maulik-0207/Blogy.git
cd Blogy
```

---

### 2️⃣ Create Virtual Environment

Creating a virtual environment isolates project dependencies from your system Python installation.

#### 🐧 Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 🪟 Windows (Command Prompt)

```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### 🪟 Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> **⚠️ PowerShell Execution Policy Error?**
>
> If you see an error like `execution of scripts is disabled on this system`, run PowerShell as Administrator and execute:
> ```powershell
> Set-ExecutionPolicy RemoteSigned
> ```
> Then try activating the virtual environment again.

**Verify Activation**: Your terminal prompt should now show `(.venv)` at the beginning.

---

### 3️⃣ Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements/development.txt
```

> **For Production**: Use `pip install -r requirements/production.txt`

**Expected Output**: You should see packages being downloaded and installed. This may take a few minutes.

---

### 4️⃣ Configure Environment Variables

#### Create .env File

```bash
# Copy the example file
cp src/config/.env.example src/config/.env
```

> **Windows (if `cp` doesn't work)**:
> ```cmd
> copy src\config\.env.example src\config\.env
> ```

#### Edit .env File

Open `src/config/.env` in your text editor and configure the following variables:

```env
# Django Secret Key (REQUIRED)
SECRET_KEY=your-secret-key-here

# Allowed Hosts (REQUIRED)
ALLOWED_HOSTS=localhost,127.0.0.1

# Debug Mode (set to False in production)
DEBUG=True

# Email Configuration (OPTIONAL - for password reset emails)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Generate a Secret Key

Run this command to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as the value for `SECRET_KEY` in your `.env` file.

#### Email Configuration (Optional)

If you want password reset functionality:

1. **Gmail Users**:
   - Enable 2-Factor Authentication on your Google account
   - Generate an [App Password](https://myaccount.google.com/apppasswords)
   - Use the app password (not your regular password) in `EMAIL_HOST_PASSWORD`

2. **Other Email Providers**: Update `EMAIL_HOST` and `EMAIL_PORT` in `src/config/settings/base.py` accordingly.

---

### 5️⃣ Setup Redis

Redis is required for caching and Celery task queue.

#### 🐧 Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify Redis is running
redis-cli ping
# Expected output: PONG
```

#### 🍎 macOS

```bash
# Using Homebrew
brew install redis
brew services start redis

# Verify Redis is running
redis-cli ping
# Expected output: PONG
```

#### 🪟 Windows

Redis doesn't officially support Windows. Use **Memurai** instead:

1. Download Memurai from [memurai.com](https://www.memurai.com/get-memurai)
2. Install and run Memurai
3. Memurai runs on `127.0.0.1:6379` by default (same as Redis)

**Verify Memurai**:
```cmd
memurai-cli ping
# Expected output: PONG
```

#### Update Redis Configuration (if needed)

If your Redis/Memurai is running on a different host/port, update `src/config/settings/base.py`:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",  # Update this if needed
        ...
    }
}

CELERY_BROKER_URL = "redis://127.0.0.1:6379"  # Update this if needed
```

---

### 6️⃣ Run Database Migrations

Apply database migrations to create all necessary tables:

```bash
python src/manage.py migrate
```

**Expected Output**: You should see messages like:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

### 7️⃣ Create Superuser

Create an admin account to access the Django admin panel:

```bash
python src/manage.py createsuperuser
```

You'll be prompted to enter:
- **Username**: Choose a username (e.g., `admin`)
- **Email**: Your email address
- **Password**: A strong password (you'll need to type it twice)

> **Note**: The password won't be visible as you type for security reasons.

---

### 8️⃣ Collect Static Files (Optional)

For development, this step is usually not required. However, if you encounter static file issues:

```bash
python src/manage.py collectstatic --noinput
```

---

### 9️⃣ Run the Development Server

Start the Django development server:

```bash
python src/manage.py runserver
```

**Expected Output**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 29, 2026 - 00:42:00
Django version 6.0, using settings 'config.settings.development'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

🎉 **Success!** Open your browser and navigate to:
- **Main Site**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Log in to the admin panel using the superuser credentials you created.

---

### 🔟 Setup Celery Workers (Optional)

Celery is used for asynchronous tasks like sending emails. To enable Celery:

#### 🐧 Linux / macOS

Open a **new terminal window**, activate your virtual environment, and run:

```bash
celery -A config worker -l info
```

#### 🪟 Windows

Celery doesn't natively support Windows. Use `eventlet` or `threads`:

```cmd
celery -A config worker -l info -P eventlet
```

Or:

```cmd
celery -A config worker -l info -P threads
```

**Keep these terminals running** while using the application for full functionality.

---

## ✅ Installation Complete!

You're all set! Happy coding! 🚀

For more information, see the main [README.md](README.md).

---

<div align="center">
Made with ❤️ and Django
</div>
