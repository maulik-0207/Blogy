# 📝 Blogy

A feature-rich blogging platform built with Django to showcase intermediate-level Django development skills. This project demonstrates proficiency in Django's core features, including authentication, ORM relationships, signals, caching, async task processing, and admin customization.

![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> [!NOTE]
> **Project Focus**: This project was created to demonstrate Django backend development skills. UI/UX design was not a priority, and the project was built entirely without the assistance of AI coding tools like Cursor or GitHub Copilot.

---

## 🎥 Demo Video

**[📺 Watch Demo on YouTube](YOUR_YOUTUBE_LINK_HERE)**

---

## ✨ Features

### 👤 User Management
- **User Authentication**: Complete registration, login, and logout functionality
- **Custom User Model**: Extended Django's AbstractUser with additional fields
- **User Profiles**: Profile images, bio, verification status, and ban management
- **Follow System**: Users can follow/unfollow each other with follower counts
- **Password Security**: Argon2 and BCrypt password hashing

### 📰 Blog Posts
- **Rich Text Editor**: TinyMCE integration for creating formatted content
- **Post Management**: Create, edit, delete, and publish/draft posts
- **Slug-based URLs**: SEO-friendly URLs for all posts
- **Post Images**: Upload and manage multiple images within posts
- **Thumbnails**: Custom thumbnail support for post previews
- **Table of Contents**: Auto-generated TOC from post headings (h1-h4)
- **Tagging System**: Add up to 5 tags per post for categorization
- **Read Time Calculation**: Automatic reading time estimation
- **Post Privacy**: Public/private post visibility control
- **View Tracking**: Track post views with IP and user agent logging

### 💬 Comments & Engagement
- **Nested Comments**: Reply to comments with parent-child relationships
- **Comment Likes**: Like system for comments
- **Post Likes**: Like/unlike posts with real-time count updates
- **Comment Management**: Edit and delete functionality

### 📚 Post Lists
- **Collections**: Users can create curated lists of posts
- **List Management**: Add/remove posts from lists with custom ordering
- **List Likes**: Like system for post lists

### 🔔 Notifications
- **Real-time Notifications**: Get notified about:
  - New comments on your posts
  - Replies to your comments
  - Likes on posts and comments
  - New followers
  - Follow-backs
- **Notification Service**: Centralized notification creation system
- **Read/Unread Status**: Track notification read status

### 🚨 Reporting System
- **Content Moderation**: Report inappropriate content
  - User reports
  - Post reports
  - Comment reports
- **Admin Review**: Track review status and actions taken

### ⚙️ Technical Features
- **Celery Integration**: Asynchronous task processing
- **Redis Caching**: Message broker for celery
- **Jazzmin Admin**: Beautiful, customizable Django admin interface
- **Sitemaps**: Auto-generated XML sitemaps for SEO
- **Robots.txt**: Search engine crawling configuration
- **Custom Error Pages**: 400, 403, 404, and 500 error handlers
- **Logging System**: Comprehensive logging (debug, info, warning, error, critical)
- **Django Signals**: Post-save/delete hooks for automated actions & deletes unused images

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 6.0
- **Language**: Python 3.10+
- **Database**: SQLite (development) - easily switchable to PostgreSQL/MySQL
- **Caching**: Redis 7.1.0 with django-redis
- **Task Queue**: Celery 5.6.1 with Redis broker
- **Password Hashing**: Argon2-cffi, BCrypt

### Frontend
- **Templates**: Django Template Language
- **Styling**: Tailwind CSS (via django-tailwind)
- **Rich Text**: TinyMCE (integrated via static files)

### Admin & Tools
- **Admin Interface**: Jazzmin 3.0.1
- **Image Processing**: Pillow 12.0.0
- **HTML Parsing**: BeautifulSoup4 14.3
- **Reading Time**: readtime 3.0.0
- **Environment Management**: django-environ 0.12.0

### Development Tools
- **Async Support**: eventlet 0.40.4 (for Celery on Windows)
- **Task Results**: django-celery-results 2.6.0

---

## 🚀 Quick Start

For detailed installation instructions, see **[INSTALLATION.md](INSTALLATION.md)**.

---

## 📁 Project Structure

For a detailed breakdown of the architecture, see [docs/ARCHITECTURE.md](ARCHITECTURE.md).

---

## 🗄️ Database Schema

The project includes 8 main Django apps with the following models:

- **accounts**: User, UserFollow
- **posts**: Post, Tag, PostTag, PostLike, PostView, PostImage
- **comments**: Comment, CommentLike
- **post_lists**: PostList, PostListItem, PostListLike
- **notifications**: Notification
- **reports**: UserReport, PostReport, CommentReport

See [docs/Blogy_DB_Schema.svg](Blogy_DB_Schema.svg) for the complete database schema.

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in `src/config/` with the following variables:

```env
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True

# Email Configuration (for password reset, notifications)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Redis Setup

Redis is required for caching and Celery. On Windows, use [Memurai](https://www.memurai.com/) as a Redis alternative.

### Celery Workers

Run Celery workers for asynchronous task processing:

```bash
# Windows
celery -A config worker -l info -P eventlet

# Linux/Mac
celery -A config worker -l info
```

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## ⚠️ Disclaimer

> [!WARNING]
> This project was created as a learning exercise and portfolio piece to demonstrate Django development skills. It is **not production-ready** and should not be used in a live environment without significant security hardening, testing, and optimization.

**Key Points**:
- Built for educational and demonstration purposes
- UI/UX was not a primary focus
- No AI coding assistants were used in development
- Future updates and maintenance are not guaranteed
- Use at your own risk


---

## 📧 Contact

**Maulik** - [@maulik-0207](https://github.com/maulik-0207)

**Project Link**: [https://github.com/maulik-0207/Blogy](https://github.com/maulik-0207/Blogy)

---

<div align="center">
Made with ❤️ and Django
</div>
