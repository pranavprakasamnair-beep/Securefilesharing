# 🔐 Secure File Encryption & Sharing System

A Flask-based cybersecurity application designed to securely **upload, encrypt, store, share, and download files**. The system uses **Fernet symmetric encryption** to protect file contents, authentication to identify users, database management for file and user information, and controlled access for file sharing.

## 📌 Overview

The **Secure File Encryption & Sharing System** provides a secure way for users to manage and share files without storing the original file contents directly in an accessible form.

When a user uploads a file, the application processes the file through the encryption module before storing it. Authenticated users can manage their files and share them with other users through the application.

The project demonstrates practical cybersecurity concepts including:

* File encryption and decryption
* User authentication
* Access control
* Secure file handling
* Database management
* Environment-based configuration
* Web application development

---

## ✨ Features

* 🔑 User registration and login
* 👤 User authentication
* 📤 Secure file upload
* 🔐 File encryption using Fernet
* 📥 Secure file download and decryption
* 👥 File sharing between users
* 🗄️ Database-backed user and file management
* 📁 Dedicated upload storage
* 🌐 Flask-based web interface
* 🎨 Responsive frontend using HTML and CSS
* ⚡ JavaScript-based frontend functionality
* 🔒 Environment variables for sensitive configuration

---

## 🛠️ Technologies Used

| Technology                 | Purpose                         |
| -------------------------- | ------------------------------- |
| **Python**                 | Core programming language       |
| **Flask**                  | Backend web framework           |
| **Cryptography / Fernet**  | File encryption and decryption  |
| **SQLite**                 | Database management             |
| **HTML**                   | Web page structure              |
| **CSS**                    | User interface styling          |
| **JavaScript**             | Client-side functionality       |
| **Jinja2**                 | Dynamic HTML templating         |
| **python-dotenv / `.env`** | Environment-based configuration |
| **Git**                    | Version control                 |
| **GitHub**                 | Source code hosting             |

---

# 🔐 Security Architecture

The main security workflow of the application can be represented as:

```text
                    USER
                     │
                     ▼
             ┌───────────────┐
             │ Authentication│
             └───────┬───────┘
                     │
                     ▼
               File Upload
                     │
                     ▼
             ┌───────────────┐
             │   Encryption  │
             │    (Fernet)   │
             └───────┬───────┘
                     │
                     ▼
              Encrypted File
                     │
                     ▼
             ┌───────────────┐
             │    Database   │
             │    Metadata   │
             └───────────────┘
                     │
                     ▼
              Authorized Access
                     │
                     ▼
                 Download
                     │
                     ▼
                Decryption
                     │
                     ▼
              Original File
```

---

# 🔒 Encryption

The project uses **Fernet symmetric encryption** through Python's `cryptography` library.

Fernet uses a secret encryption key to encrypt and decrypt file data.

### Encryption

```text
Original File
      │
      ▼
Read File Data
      │
      ▼
Fernet Encryption
      │
      ▼
Encrypted File
      │
      ▼
Secure Storage
```

### Decryption

```text
Encrypted File
      │
      ▼
Retrieve File
      │
      ▼
Fernet Decryption
      │
      ▼
Original File
      │
      ▼
User Download
```

The encryption key is kept outside the source code using environment variables.

> **Important:** The encryption key should never be committed to a public GitHub repository.

---

# 👤 Authentication

The application contains a dedicated authentication module:

```text
Main/
└── utils/
    └── auth.py
```

The authentication functionality is responsible for handling user-related authentication operations.

The general workflow is:

```text
User
 ↓
Register
 ↓
Login
 ↓
Authentication
 ↓
Access Application
```

Authentication ensures that application functionality is available only to authenticated users.

---

# 👥 File Sharing & Access Control

The application allows users to share files through the web interface.

The basic workflow is:

```text
File Owner
    │
    ▼
Select File
    │
    ▼
Select User
    │
    ▼
Share File
    │
    ▼
Authorized User
    │
    ▼
Access / Download
```

This provides controlled access to shared files instead of making all uploaded files publicly accessible.

---

# 🗄️ Database

Database functionality is handled through:

```text
Main/
└── utils/
    └── database.py
```

The database is used to manage application information such as:

* User information
* File information
* File ownership
* File-sharing information
* Other application metadata

SQLite is suitable for this project because it is lightweight and integrates easily with Python applications.

---

# 🧰 Utility Modules

The project separates important functionality into individual modules.

### `auth.py`

Handles authentication-related functionality.

```text
utils/
└── auth.py
```

### `database.py`

Handles database-related operations.

```text
utils/
└── database.py
```

### `encryption.py`

Contains the file encryption and decryption functionality.

```text
utils/
└── encryption.py
```

### `__init__.py`

Makes the `utils` directory usable as a Python package and supports importing the utility modules.

---

# 🌐 Frontend

The frontend is organized into two main sections.

## HTML Templates

Located in:

```text
Main/templates/
```

The project contains:

| File             | Purpose                |
| ---------------- | ---------------------- |
| `base.html`      | Base layout/template   |
| `index.html`     | Main/home page         |
| `login.html`     | Login interface        |
| `register.html`  | Registration interface |
| `dashboard.html` | User dashboard         |
| `upload.html`    | File upload interface  |
| `shared.html`    | Shared file interface  |

The templates use **Jinja2**, allowing Flask to dynamically provide information to the HTML pages.

---

# 🎨 CSS

The stylesheet is located at:

```text
Main/static/css/style.css
```

It controls the visual appearance and layout of the application.

---

# ⚡ JavaScript

The JavaScript file is located at:

```text
Main/static/js/main.js
```

It provides client-side functionality and interaction for the web interface.

---

# 📁 Upload Storage

The application contains a dedicated upload directory:

```text
Main/static/uploads/
```

This directory is used for file storage during application operation.

Files should be handled carefully because uploaded files can contain sensitive information.

---

# ⚙️ Configuration

The project contains configuration files:

```text
config.py
```

and:

```text
Main/config.py
```

Environment-specific and sensitive values are stored using:

```text
.env
```

Using environment variables helps prevent sensitive configuration such as secret keys from being hard-coded into the application.

### Example

```text
SECRET_KEY=your_secret_key
FERNET_KEY=your_encryption_key
```

> Never commit real secret keys or `.env` files to GitHub.

---

# 📂 Project Structure

The current project structure is organized as follows:

```text
Securefilesharing/
│
├── __pycache__/
│   └── config.cpython-314.pyc
│
├── .vscode/
│   └── launch.json
│
├── Main/
│   ├── .env
│   ├── config.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   │
│   │   ├── js/
│   │   │   └── main.js
│   │   │
│   │   └── uploads/
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── shared.html
│   │   └── upload.html
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   └── encryption.py
│   │
│   └── venv/
│
├── .env
├── .gitignore
├── app.py
├── config.py
└── requirements.txt
```

### Important

The following directories/files are **development or environment-specific** and should generally not be uploaded to GitHub:

```text
venv/
__pycache__/
.env
```

Your `.gitignore` should make sure sensitive and unnecessary files are excluded.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/secure-file-sharing.git
```

Replace the URL with your actual GitHub repository URL.

## 2. Navigate to the Project

```bash
cd Securefilesharing
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create/configure your `.env` file with the required secret values.

For example:

```text
SECRET_KEY=your_secret_key
FERNET_KEY=your_fernet_key
```

Use the variable names required by your actual `config.py`.

**Do not upload your real `.env` file to GitHub.**

## 6. Run the Application

From the project root:

```bash
python app.py
```

Then open the local Flask URL displayed in the terminal.

---

# 🔄 Application Workflow

### 1. Registration

A new user creates an account through:

```text
/register
```

### 2. Login

The user authenticates through:

```text
/login
```

### 3. Dashboard

After authentication, the user can access the dashboard.

```text
Login
 ↓
Dashboard
```

### 4. Upload

The user selects a file and uploads it.

```text
User
 ↓
Upload File
 ↓
Encryption
 ↓
Encrypted Storage
```

### 5. Sharing

The owner can share a file with another registered user.

```text
Owner
 ↓
Select File
 ↓
Select User
 ↓
Share
```

### 6. Download

An authorized user can access the file through the application.

```text
Authorized User
 ↓
Request File
 ↓
Access Check
 ↓
Decrypt
 ↓
Download
```

---

# 🛡️ Security Concepts Demonstrated

This project demonstrates several important cybersecurity concepts:

### 1. Symmetric Encryption

Fernet is used to encrypt and decrypt file data using a secret key.

### 2. Authentication

Users must authenticate before accessing protected application functionality.

### 3. Authorization

Access to shared files is controlled based on the user's permissions.

### 4. Secure Configuration

Sensitive values are managed through environment variables rather than being directly embedded in source code.

### 5. Secure File Handling

Files are processed through the application's encryption workflow before being stored.

---

# 🧪 Testing

The application can be tested by performing the following operations:

```text
✓ Register a new user
✓ Login with valid credentials
✓ Test invalid login credentials
✓ Upload a file
✓ Verify encrypted file storage
✓ Download an uploaded file
✓ Verify downloaded file contents
✓ Share a file with another user
✓ Verify authorized access
✓ Test unauthorized access
✓ Test multiple file uploads
```

---

# ⚠️ Limitations

This project is developed primarily as an **educational cybersecurity project**.

For production deployment, additional security measures would be recommended, including:

* Multi-factor authentication
* Stronger account security controls
* Rate limiting
* HTTPS enforcement
* Malware scanning for uploaded files
* Dedicated secure key management
* Key rotation
* Improved audit logging
* Secure cloud storage
* Production-grade database configuration
* Additional input validation and security hardening

---

# 🚀 Future Enhancements

Potential improvements include:

* 🔐 Multi-factor authentication
* ☁️ Cloud-based encrypted storage
* 🔗 Expiring file-sharing links
* ⏳ Automatic file expiration
* 🔑 Encryption key rotation
* 📋 Detailed security audit logs
* 🦠 Malware scanning
* 👤 Role-based access control
* 📧 Secure email-based file sharing
* 📱 Improved responsive interface

---

# 🎯 Learning Outcomes

This project provides practical experience with:

* Python
* Flask
* Symmetric cryptography
* Fernet encryption
* Authentication
* Authorization
* Secure file handling
* Database management
* HTML/CSS/JavaScript
* Jinja2 templating
* Environment variables
* Git and GitHub
* Basic web application security

---

# 👨‍💻 Author

**Pranav Prakasam Nair**

Computer Engineering Student

Interested in:

**Cybersecurity • Cloud Computing • Artificial Intelligence • Software Development**

---

# 📜 License

This project was developed for **educational and academic purposes**.
