# 🔐 Secure File Encryption & Sharing System

A secure web-based file management system that allows users to **upload, encrypt, store, share, and download files securely**. The system uses **Fernet symmetric encryption** to protect file contents and **SHA-256 hashing** to verify file integrity.

## 📌 Overview

The **Secure File Encryption & Sharing System** is a cybersecurity-focused application designed to protect sensitive files from unauthorized access.

When a user uploads a file, the application encrypts it before storing it on the server. Authorized users can download shared files, which are decrypted only when accessed through the application.

The project demonstrates practical concepts such as **file encryption, authentication, access control, secure file handling, and data integrity verification**.

## ✨ Features

* 🔑 User registration and login
* 🔒 Secure file encryption using **Fernet**
* 📁 Secure file upload and storage
* 📥 File download and automatic decryption
* 👥 File sharing between authorized users
* 🛡️ Access control for shared files
* 🔍 SHA-256 based file integrity verification
* 🗄️ SQLite database for user and file information
* 📊 Basic activity/file management
* 🌐 Web-based user interface
* 🚫 Unauthorized users cannot access protected files

## 🛠️ Technologies Used

| Technology                | Purpose                        |
| ------------------------- | ------------------------------ |
| **Python**                | Backend development            |
| **Flask**                 | Web application framework      |
| **SQLite**                | Database                       |
| **Cryptography (Fernet)** | File encryption and decryption |
| **SHA-256**               | File integrity verification    |
| **HTML/CSS**              | Frontend                       |
| **Jinja2**                | Dynamic HTML templates         |
| **Git & GitHub**          | Version control                |

## 🔐 How It Works

```text
              ┌─────────────────┐
              │      User       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Login / Auth   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   File Upload   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Generate SHA-256│
              │    Hash         │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Fernet Encrypt  │
              │      File       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Encrypted File  │
              │    Storage      │
              └─────────────────┘


For authorized download:

Encrypted File
      │
      ▼
Fernet Decryption
      │
      ▼
Integrity Verification
      │
      ▼
Original File
      │
      ▼
     User
```

## 🔒 Encryption

The project uses **Fernet symmetric encryption** from the Python `cryptography` library.

Fernet provides authenticated symmetric encryption, meaning the same secret key is used for encryption and decryption while also helping detect unauthorized modification of encrypted data.

The original file is never stored directly in the file storage directory.

### Encryption Flow

```text
Original File
     ↓
Read File Data
     ↓
Fernet Encryption
     ↓
Encrypted File
     ↓
Store Securely
```

### Decryption Flow

```text
Encrypted File
     ↓
Retrieve File
     ↓
Fernet Decryption
     ↓
Integrity Verification
     ↓
Original File
```

## 🧩 File Sharing

The application provides controlled file sharing between registered users.

When a file owner shares a file with another user, the system records the sharing permission in the database.

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
Create Sharing Permission
    │
    ▼
Authorized User
    │
    ▼
Download File
```

Only users who have the required permission can access the shared file.

## 🔍 File Integrity

The system can use **SHA-256** to generate a unique hash of the original file.

Example:

```text
File
 ↓
SHA-256
 ↓
Hash Value
```

The generated hash can be used to verify whether the file contents have changed.

If the calculated hash does not match the stored/reference hash, the file can be treated as potentially modified or corrupted.

> **Note:** SHA-256 is used for integrity verification, not for encrypting the file.

## 🗃️ Database

The application uses **SQLite** to store application metadata such as:

* User accounts
* File information
* File ownership
* File sharing permissions
* File hashes
* Relevant timestamps

The actual file contents are stored separately in encrypted form.

## 📂 Project Structure

```text
secure-file-sharing/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── Procfile
├── vercel.json
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
│
├── static/
│   ├── css/
│   └── js/
│
├── uploads/
│   └── encrypted files
│
└── database/
    └── database.db
```

> The exact structure may vary depending on the final implementation.

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/secure-file-sharing.git
```

### 2. Navigate to the Project

```bash
cd secure-file-sharing
```

### 3. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Encryption Key

The encryption key should **not be hard-coded or uploaded to GitHub**.

Set the required secret/encryption key using an environment variable.

Example:

```text
FERNET_KEY=your-secret-key
```

Make sure sensitive configuration files are included in `.gitignore`.

### 6. Run the Application

```bash
python app.py
```

The application will start on the configured local Flask server.

Open the displayed local URL in your browser.

## 🔑 Security Considerations

The project follows several basic security practices:

* Files are encrypted before storage.
* Authentication is required to access user-specific functionality.
* File-sharing permissions are checked before allowing access.
* SHA-256 can be used for integrity verification.
* Encryption keys should be stored separately from source code.
* Sensitive configuration files should not be committed to GitHub.
* Unauthorized users are prevented from accessing protected files.

## ⚠️ Limitations

This project is primarily intended as an **educational cybersecurity project** and should not be considered a production-grade enterprise file-sharing platform.

Potential improvements include:

* Stronger production-grade authentication
* Multi-factor authentication (MFA)
* Role-based access control
* Secure cloud object storage
* Key rotation and dedicated key management
* HTTPS enforcement
* Rate limiting
* Malware/file scanning
* Improved audit logging
* Secure password hashing and account recovery
* Database encryption
* Containerization and production deployment

## 🚀 Future Enhancements

Possible future improvements include:

1. ☁️ Cloud storage integration
2. 🔐 Multi-factor authentication
3. 🔑 Automated encryption-key rotation
4. 👤 Role-based access control
5. 📧 Secure sharing through expiring links
6. ⏳ Automatic file expiration
7. 📱 Responsive mobile interface
8. 📋 Detailed security audit logs
9. 🦠 Malware scanning before encryption
10. 🔒 End-to-end encryption improvements

## 🎯 Learning Outcomes

Through this project, the following concepts are demonstrated:

* Symmetric cryptography
* File encryption and decryption
* Hashing and integrity verification
* Authentication
* Authorization and access control
* Secure file handling
* Database management
* Flask web development
* Cybersecurity principles
* Git and GitHub workflow

## 👨‍💻 Author

**Pranav Prakasam Nair**

Computer Engineering Student
Interested in **Cybersecurity, Cloud Computing, AI, and Software Development**

---

## 📜 License

This project is developed for **educational and academic purposes**.

