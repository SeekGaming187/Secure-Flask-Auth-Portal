# 🔐 Secure Flask Authentication Portal with Hash Chain-Based OTP

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Security](https://img.shields.io/badge/Security-2FA-red?style=for-the-badge&logo=security&logoColor=white)
![RSA](https://img.shields.io/badge/RSA-Encryption-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Flask web authentication portal with two-factor authentication using 100-iteration SHA-256 hash chain-based OTP and RSA-encrypted database storage**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security-architecture) • [Documentation](#-technical-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Security Architecture](#-security-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Technical Documentation](#-technical-documentation)
  - [Hash Chain OTP](#hash-chain-based-otp)
  - [Client Implementation](#client-implementation)
  - [Server Implementation](#server-implementation)
- [Database Structure](#-database-structure)
- [Academic Context](#-academic-context)
- [Security Considerations](#-security-considerations)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🎯 Overview

This project implements a **modern web authentication system** with **two-factor authentication (2FA)** using a unique hash chain-based One-Time Password (OTP) mechanism. It combines traditional password authentication with cryptographic OTP verification for enhanced security.

### What is Hash Chain-Based OTP?

Unlike traditional TOTP (Time-based OTP) or HOTP (HMAC-based OTP), this system uses a **hash chain** approach:

```
Password → SHA-256 → SHA-256 → ... (100 times) → OTP Chain
S₀ → S₁ → S₂ → ... → S₉₉ → S₁₀₀

Usage: S₁₀₀, S₉₉, S₉₈, ... (reverse order)
Verification: SHA-256(Sₙ₋₁) = Sₙ
```

**Advantages:**
- ✅ **Offline Capable** - No time synchronization needed
- ✅ **Replay Attack Resistant** - Each OTP used exactly once
- ✅ **Lightweight** - No additional hardware/apps required
- ✅ **Cryptographically Secure** - SHA-256 hash chain

---

## ✨ Features

### 🔒 Authentication & Security

- ✅ **Two-Factor Authentication (2FA)** - Password + OTP verification
- ✅ **Hash Chain-Based OTP** - 100-iteration SHA-256 chain
- ✅ **RSA Encrypted Database** - PKCS1_OAEP encryption for data at rest
- ✅ **SHA-256 Password Hashing** - Secure credential storage
- ✅ **Automatic OTP Chain Renewal** - Seamless chain regeneration
- ✅ **Session Management** - Flask secure sessions

### 💻 Web Application

- ✅ **Flask Framework** - Modern Python web framework
- ✅ **Responsive UI** - HTML/CSS templates
- ✅ **User Registration** - Secure account creation
- ✅ **User Login** - Multi-step authentication
- ✅ **Welcome Page** - Post-authentication dashboard
- ✅ **Input Validation** - Username/password requirements
- ✅ **Flash Messages** - User feedback and error handling

### 🛡️ Security Features

- ✅ **Encrypted Storage** - RSA encryption for database
- ✅ **OTP Counter Tracking** - Prevents OTP reuse
- ✅ **Chain Exhaustion Handling** - Automatic renewal at 100 logins
- ✅ **Server-Side Validation** - All security logic on backend
- ✅ **Password Complexity Requirements** - Minimum 6 characters
- ✅ **Username Restrictions** - Alphanumeric only

---

## 🔐 Security Architecture

### System Overview

```
┌────────────────────────────────────────────────────────────┐
│           Flask Authentication Portal Architecture          │
└────────────────────────────────────────────────────────────┘

CLIENT (Flask Frontend)                    SERVER (Backend Logic)
┌─────────────────────┐                   ┌──────────────────────┐
│  Registration Form  │                   │  User Database       │
│  - Username         │──────────────────▶│  (RSA Encrypted)     │
│  - Password         │   Hash Password   │  username;hash;OTP   │
└─────────────────────┘   Generate OTP    └──────────────────────┘
         │                                          │
         │                                          │
         ▼                                          ▼
┌─────────────────────┐                   ┌──────────────────────┐
│  Login Form         │                   │  Verification Logic  │
│  - Username         │──────────────────▶│  1. Check Password   │
│  - Password         │   Send Hashed     │  2. Verify OTP       │
│                     │   Password + OTP  │  3. Update Counter   │
└─────────────────────┘                   └──────────────────────┘
         │                                          │
         │                    ✓ Valid               │
         ▼                                          ▼
┌─────────────────────┐                   ┌──────────────────────┐
│  Welcome Page       │◀──────────────────│  Session Created     │
│  "Welcome, user!"   │   Redirect        │  Login Successful    │
└─────────────────────┘                   └──────────────────────┘
```

### Authentication Flow

#### Registration Process

```python
1. User Input:
   - Username (letters only)
   - Password (>6 chars)

2. Client-Side:
   - Validate username format: ^[A-Za-z]+$
   - Validate password length: >6
   - Hash password: SHA-256(password)
   - Generate OTP chain: hash_otp(password, 100)
   - Send: username, hashed_password, OTP[0] (S₁₀₀)

3. Server-Side:
   - Check username uniqueness
   - Encrypt database entry with RSA
   - Store: username;hash;S₁₀₀;0
   - Save encrypted to database.txt

4. Result:
   - Redirect to login page
   - Flash: "User registered successfully"
```

#### Login Process

```python
1. User Input:
   - Username
   - Password

2. Client-Side (Password Verification):
   - Hash password: SHA-256(password)
   - Send: username, hashed_password

3. Server-Side (Password Check):
   - Decrypt database
   - Verify: username exists AND hash matches
   - Return: True/False

4. Client-Side (OTP Generation):
   - Generate OTP chain: hash_otp(password, 100)
   - Get current index: counter % 100
   - Send: OTP[counter] (Sₙ₋₁)

5. Server-Side (OTP Verification):
   - Load stored OTP: Sₙ
   - Hash received OTP: SHA-256(Sₙ₋₁)
   - Verify: SHA-256(Sₙ₋₁) == Sₙ
   - Update: store Sₙ₋₁, increment counter
   - Re-encrypt database

6. Result:
   - If valid: Redirect to /welcome
   - If invalid: Show error message
```

---

## 🚀 Installation

### Prerequisites

```bash
Python 3.8 or higher
pip (Python package manager)
```

### Clone Repository

```bash
git clone https://github.com/memo-13-byte/secure-flask-auth-portal.git
cd secure-flask-auth-portal
```

### Install Dependencies

```bash
pip install Flask pycryptodome
```

**Required Libraries:**
- `Flask` - Web framework
- `pycryptodome` - Cryptographic operations

### Generate RSA Keys

```python
# generate_keys.py
from Crypto.PublicKey import RSA

# Generate 2048-bit RSA key pair
key = RSA.generate(2048)

# Save private key
with open('private.pem', 'wb') as f:
    f.write(key.export_key())

# Save public key
with open('public.pem', 'wb') as f:
    f.write(key.publickey().export_key())

print("Keys generated successfully!")
```

```bash
python generate_keys.py
```

---

## 💡 Quick Start

### 1. Project Structure

Ensure your project has this structure:

```
secure-flask-auth-portal/
├── Client.py              # Flask application (frontend)
├── Server.py              # Backend logic
├── templates/
│   ├── register.html      # Registration form
│   ├── login.html         # Login form
│   └── welcome.html       # Welcome page
├── public.pem             # RSA public key
├── private.pem            # RSA private key
├── database.txt           # Encrypted user database (auto-generated)
├── requirements.txt       # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

### 2. Run Application

```bash
python Client.py
```

### 3. Access Portal

Open your browser and navigate to:

```
http://localhost:5000
```

### 4. Register a User

1. Click "**Register**" or go to `http://localhost:5000/register`
2. Enter username (letters only): `alice`
3. Enter password (>6 chars): `mysecurepassword`
4. Click "**Register**"
5. You'll be redirected to login page

### 5. Login

1. Enter username: `alice`
2. Enter password: `mysecurepassword`
3. Click "**Submit**"
4. OTP is automatically verified
5. You'll see: "**Welcome, alice!**"

---

## 📚 Technical Documentation

### Hash Chain-Based OTP

#### Generation Process

```python
def hash_otp(seed: str, n: int = 100) -> list:
    """
    Generate hash chain OTP
    
    Process:
    1. Start with password as seed
    2. Hash 100 times using SHA-256
    3. Return chain in reverse order
    
    Example:
    S₀ = "password"
    S₁ = SHA-256(S₀)
    S₂ = SHA-256(S₁)
    ...
    S₁₀₀ = SHA-256(S₉₉)
    
    Return: [S₁₀₀, S₉₉, S₉₈, ..., S₁]
    """
    chain = []
    current_hash = bytes(seed, 'utf-8')
    
    for i in range(n):
        hash_obj = SHA256.new(current_hash)
        current_hash = hash_obj.digest()
        chain.append(current_hash.hex())
    
    return chain[::-1]  # Reverse for usage
```

#### Verification Process

```python
Server stores: Sₙ
Client sends: Sₙ₋₁

Server verification:
1. Hash client OTP: SHA-256(Sₙ₋₁)
2. Compare: SHA-256(Sₙ₋₁) == Sₙ
3. If match:
   - Update stored OTP: Sₙ ← Sₙ₋₁
   - Increment counter: counter += 1
   - Save encrypted database
4. Return: True/False
```

#### Chain Renewal

```python
When counter reaches 100:
1. Client generates new chain
2. Reset counter to 0
3. Store new S₁₀₀
4. Continue authentication
```

### Client Implementation

#### `Client.py` - Flask Application

**Routes:**

| Route | Methods | Description |
|-------|---------|-------------|
| `/` | GET | Redirects to `/login` |
| `/register` | GET, POST | User registration form |
| `/login` | GET, POST | User login with OTP |
| `/welcome` | GET | Post-authentication page |

**Key Functions:**

```python
# Password hashing
hash_password(password, algorithm="SHA256")
→ Returns: Hex digest of hashed password

# OTP chain generation
hash_otp(seed, n=100)
→ Returns: List of 100 OTP values in reverse order

# Registration handler
@app.route('/register', methods=['GET', 'POST'])
→ Validates input → Generates OTP → Registers user

# Login handler
@app.route('/login', methods=['GET', 'POST'])
→ Verifies password → Generates OTP → Validates OTP → Redirects
```

### Server Implementation

#### `Server.py` - Backend Logic

**Class: `Server`**

**Attributes:**
```python
database_path: str = "database.txt"
public_key: RSA.RsaKey
private_key: RSA.RsaKey
index: int = 0
register_otp: str = "000000"
otp_mod: int = 99  # 100 - 1
```

**Methods:**

| Method | Purpose | Input | Output |
|--------|---------|-------|--------|
| `encrypt_line()` | Encrypt data with RSA | plaintext | ciphertext |
| `decrypt_line()` | Decrypt data with RSA | ciphertext | plaintext |
| `load_database()` | Load encrypted database | - | List of users |
| `save_database()` | Save encrypted database | user list | - |
| `register_user()` | Register new user | username, hash, OTP | True/False |
| `verify_login()` | Verify credentials | username, hash | True/False |
| `validate_otp()` | Verify OTP | username, OTP | True/False |
| `hash_one_time_otp()` | Hash single OTP | OTP | hashed OTP |

**Database Encryption:**

```python
RSA PKCS1_OAEP Encryption Flow:

Write:
1. Format: "username;hash;OTP;counter"
2. Encrypt with public key
3. Store: [4 bytes size] + [encrypted data]

Read:
1. Read 4-byte size
2. Read encrypted data
3. Decrypt with private key
4. Parse: split by ";"
```

---

## 🗄️ Database Structure

### File Format

**Filename:** `database.txt` (RSA encrypted)

**Decrypted Format:**
```
username1;hashed_password;OTP_token;counter
username2;hashed_password;OTP_token;counter
```

**Field Descriptions:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `username` | str | Letters only | `alice` |
| `hashed_password` | hex | SHA-256 hash | `5e884898da...` |
| `OTP_token` | hex | Current OTP (Sₙ) | `a3f2b8c1...` |
| `counter` | int | OTP usage count | `0-99` |

**Example Entry (Decrypted):**
```
alice;5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8;a3f2b8c1d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6;5
```

### Encryption Details

```python
Storage Process:
1. Format line: "user;hash;otp;counter"
2. Encrypt with RSA public key (PKCS1_OAEP)
3. Get encrypted bytes
4. Write: [len(encrypted).to_bytes(4, 'big')] + [encrypted]

Retrieval Process:
1. Read 4 bytes → get encrypted data length
2. Read N bytes → get encrypted data
3. Decrypt with RSA private key
4. Parse decrypted string by ";"
```

---

## 🎓 Academic Context

**Course:** BBM 465 - Information Security Laboratory  
**Institution:** Hacettepe University, Computer Engineering Department  
**Semester:** Fall 2024  
**Group:** 28  
**Team Members:**
- Mehmet Yiğit (b2210356159)
- Mehmet Oğuz Kocadere (b2210356021)

**Topics Covered:**
- Multi-factor authentication (MFA/2FA)
- Hash chain-based OTP systems
- RSA public key encryption
- SHA-256 cryptographic hashing
- Flask web application security
- Secure password storage
- Session management
- Database encryption

**Assignment Objectives:**
1. Implement secure user authentication
2. Design hash chain OTP mechanism
3. Encrypt sensitive data with RSA
4. Build Flask web application
5. Understand 2FA principles
6. Practice secure coding

---

## ⚠️ Security Considerations

### Strengths ✅

1. **Two-Factor Authentication**
   - Password + OTP verification
   - Each factor independently secure

2. **Hash Chain Security**
   - SHA-256 cryptographic strength
   - One-time use prevents replay attacks
   - Offline capable (no time sync)

3. **Database Encryption**
   - RSA PKCS1_OAEP encryption
   - Data encrypted at rest
   - Private key required for access

4. **Password Protection**
   - SHA-256 hashing
   - Never stored in plaintext
   - Server-side verification only

5. **OTP Counter Tracking**
   - Prevents OTP reuse
   - Automatic chain renewal
   - State management

### Limitations ⚠️

1. **Password Hashing (Educational)**
   - **Issue:** Basic SHA-256 without salt
   - **Production Fix:** Use bcrypt, Argon2, or PBKDF2
   - **Example:**
   ```python
   # Instead of:
   SHA256(password)
   
   # Use:
   bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
   ```

2. **RSA Key Management**
   - **Issue:** Keys stored in plaintext files
   - **Production Fix:** Use HSM or key vault
   - **Example:** AWS KMS, Azure Key Vault

3. **Session Management**
   - **Issue:** Basic Flask sessions
   - **Production Fix:** Use secure session storage
   - **Example:** Redis, database-backed sessions

4. **No Rate Limiting**
   - **Issue:** Vulnerable to brute force
   - **Production Fix:** Implement rate limiting
   - **Example:** Flask-Limiter

5. **Global Index Variable**
   - **Issue:** Not thread-safe
   - **Production Fix:** Use database-stored counter
   - **Example:** Store counter per-user in database

### Production Recommendations

```python
# 1. Password Hashing
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))

# 2. Rate Limiting
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["5 per minute"])

# 3. HTTPS Only
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# 4. CSRF Protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# 5. Environment Variables for Keys
import os
private_key_path = os.environ.get('PRIVATE_KEY_PATH')

# 6. Logging
import logging
logging.basicConfig(level=logging.INFO)

# 7. Input Sanitization
from bleach import clean
username = clean(username, tags=[])
```

---

## 📡 API Reference

### Client Endpoints

#### `POST /register`

Register a new user account.

**Request Body (Form):**
```
username: str (letters only)
password: str (>6 chars)
```

**Process:**
1. Validate username/password
2. Hash password (SHA-256)
3. Generate OTP chain (100 iterations)
4. Send to server: username, hash, OTP[0]

**Response:**
- **Success:** Redirect to `/login` + flash message
- **Failure:** Error message displayed

---

#### `POST /login`

Authenticate user with password + OTP.

**Request Body (Form):**
```
username: str
password: str
```

**Process:**
1. Hash password
2. Verify credentials with server
3. Generate OTP chain
4. Send OTP[counter] to server
5. Verify OTP

**Response:**
- **Success:** Redirect to `/welcome`
- **Failure:** Error message displayed

---

#### `GET /welcome`

Display welcome page after successful login.

**Response:**
```html
<h1>Welcome, {username}!</h1>
```

---

### Server Methods

#### `register_user(username, hashed_password, otp_token)`

**Input:**
- `username` (str): Unique username
- `hashed_password` (str): SHA-256 hash
- `otp_token` (str): Initial OTP (S₁₀₀)

**Output:**
- `True`: Registration successful
- `False`: Username exists

---

#### `verify_login(username, hashed_password)`

**Input:**
- `username` (str): Username to verify
- `hashed_password` (str): SHA-256 hash

**Output:**
- `True`: Valid credentials
- `False`: Invalid credentials

---

#### `validate_otp(username, client_otp)`

**Input:**
- `username` (str): Username
- `client_otp` (str): OTP from client (Sₙ₋₁)

**Process:**
1. Load stored OTP (Sₙ)
2. Hash client OTP: SHA-256(Sₙ₋₁)
3. Compare: SHA-256(Sₙ₋₁) == Sₙ
4. Update: store Sₙ₋₁, counter++

**Output:**
- `True`: Valid OTP
- `False`: Invalid OTP

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Add bcrypt password hashing**
2. **Implement rate limiting**
3. **Add CSRF protection**
4. **Create user profile pages**
5. **Add password reset functionality**
6. **Implement email verification**
7. **Add logging and monitoring**
8. **Create admin dashboard**

### How to Contribute

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👤 Author

**Mehmet Oğuz Kocadere**

- 🎓 Computer Engineering Student @ Hacettepe University
- 🔒 Focus: Web Security, Authentication, Cryptography
- 💼 [LinkedIn](https://linkedin.com/in/mehmet-oguz-kocadere)
- 📧 Email: canmehmetoguz@gmail.com
- 🌐 GitHub: [@memo-13-byte](https://github.com/memo-13-byte)

### 🔗 Related Security Projects

- [Classical Cryptography Toolkit](https://github.com/memo-13-byte/classical-cryptography-toolkit) - Cipher implementation & cryptanalysis
- [File Integrity Checker](https://github.com/memo-13-byte/file-integrity-checker) - RSA digital signatures & PKI
- [Hybrid Kerberos System](https://github.com/memo-13-byte/hybrid-kerberos-system) - Enterprise authentication

---

## 🙏 Acknowledgments

- **Hacettepe University** - Computer Engineering Department
- **BBM 465 Course** - Information Security Laboratory
- **Flask Documentation** - Web framework guide
- **PyCryptoDome** - Cryptographic library

---

## 📊 Statistics

![Python](https://img.shields.io/badge/Python-100%25-blue?style=flat-square)
![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-400+-green?style=flat-square)
![Security](https://img.shields.io/badge/Security-2FA-red?style=flat-square)

---

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Hash Chain OTP RFC](https://datatracker.ietf.org/doc/html/rfc2289)

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

**Made with ❤️ for modern web security education**

</div>