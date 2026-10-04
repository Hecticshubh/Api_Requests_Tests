# 🛒 E-Commerce API

> A lightweight REST API built with **Python, FastAPI and SQLite**, with automated testing using **Pytest** and reporting through **Allure**.

**📱 Target Environment:** Android + Termux

---

## ✨ Features

- ⚡ FastAPI REST API
- 🔐 Token-based authentication
- 🗄️ SQLite database
- 🧪 Automated testing with Pytest
- 📊 Allure test reporting
- 📱 Android + Termux support
- ⚙️ Environment-based configuration

---

## 🔄 Workflow

```text
API Request
    ↓
Authentication
    ↓
FastAPI
    ↓
Request Processing
    ↓
SQLite Database
    ↓
API Response
    ↓
Pytest
    ↓
Allure Report
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| 🐍 Language | Python |
| ⚡ Framework | FastAPI |
| 🚀 Server | Uvicorn |
| 🗄️ Database | SQLite |
| ✅ Validation | Pydantic |
| ⚙️ Configuration | python-dotenv |
| 🧪 Testing | Pytest |
| 🌐 HTTP Client | Requests |
| 📊 Reporting | Allure |
| 📱 Platform | Android + Termux |

---

## 📁 Project Structure

```text
Api_Requests_Test/
│
├── README.md
├── .gitignore
├── requirements.txt
├── pytest.ini
│
├── api/
│   ├── __init__.py
│   ├── database.py
│   └── main.py
│
└── api_test/
    ├── conftest.py
    ├── test_order_auth_request.py
    ├── test_order_request.py
    └── test_order_response.py
```

---

## 📚 Project Components

### `api/main.py`

Main FastAPI application containing API routes, authentication and request processing.

### `api/database.py`

Handles SQLite database functionality.

### `api/__init__.py`

Defines the `api` directory as a Python package.

### `api_test/conftest.py`

Contains shared Pytest configuration and fixtures.

### `api_test/test_order_auth_request.py`

Authentication-related order request tests.

### `api_test/test_order_request.py`

Order request handling tests.

### `api_test/test_order_response.py`

Order API response tests.

### `requirements.txt`

Contains all required Python dependencies.

### `pytest.ini`

Contains project-level Pytest configuration.

### Environment Configuration

The application uses environment variables for token-based authentication.

For local setup, create a `.env` file in the project root directory and add the following configuration:

```env
AUTH_TOKEN=test-token-123
```

This is a demo token for local testing only. The `.env` file must not be included in the GitHub repository. Use `.env.example` as a template and create your own local `.env` file.

---

# 📱 Android + Termux Setup

## 1. Install and Update Termux

Install Termux from the official F-Droid page:

https://f-droid.org/packages/com.termux/

Update package lists and installed packages:

```bash
termux-change-repo
:When you click Change Repo, select the following option:
Mirror group — Rotate between several mirrors (reco)
Recommended option. It automatically rotates between several mirrors.
All mirrors — All in the entire world
Select this option if you want to use all available mirrors worldwide.
```

If package mirror errors occur, choose a working mirror and retry:

```bash
pkg update
pkg upgrade
```

---

## 2. Install Required Packages

```bash
pkg install python git openjdk-21 rust clang nodejs-lts
```

Check installation:

```bash
python --version
git --version
java -version
node --version
npm --version
```

### Optional: Check Android API Level

```bash
getprop ro.build.version.sdk
```

If a package build specifically requires `ANDROID_API_LEVEL`, set it to the detected SDK version:

```bash
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
echo "$ANDROID_API_LEVEL"
```

This environment variable is optional for normal project execution.

---

## 3. Clone the Repository

```bash
git clone https://github.com/Hecticshubh/Api_Requests_Test.git
cd Api_Requests_Test
```

Replace the repository URL if your GitHub username or repository name is different. If the project is already on your phone, open its existing directory instead of cloning it again.

---

## 4. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 5. Install Dependencies

### Recommended: Install from `requirements.txt`

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Alternative: Install Each Python Package Manually

If you prefer to install the dependencies one by one, run these commands inside the activated virtual environment:

```bash
python -m pip install fastapi
python -m pip install uvicorn
python -m pip install pydantic
python -m pip install python-dotenv
python -m pip install pytest
python -m pip install requests
python -m pip install allure-pytest
```

Install Node.js separately if it was not installed in Step 2:

```bash
pkg install nodejs-lts
```

Install the Allure command-line tool after Node.js/npm is available:

```bash
npm install -g allure-commandline
```

Create a `.env` file in the project root and configure the `AUTH_TOKEN` variable as described in the Configuration section below.

---

# 🔐 Configuration

The API uses Bearer token authentication to protect authorized endpoints.

For local testing, configure the `AUTH_TOKEN` environment variable in your `.env` file:

```env
AUTH_TOKEN=test-token-123
```

Include the token in the `Authorization` header when sending requests:

```http
Authorization: Bearer test-token-123
```

**Note:** This is a demo token for local testing only. Do not use it in production.

---

# ▶️ Run the API

Start the server (keep this Termux session running):

```bash
python -m uvicorn api.main:app
```

To explicitly bind the server to the local device and port 8000, use:

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Open a second Termux session to run the tests. Navigate to the project directory and activate the virtual environment there before testing.

The API will run locally on:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🧪 Run Tests

Run all tests:

```bash
python -m pytest
```

Run with detailed output:

```bash
python -m pytest -v
```

### Test Coverage

- 🔐 Authentication requests
- 📦 Order requests
- 📤 Order responses

---

# 📊 Allure Reports

### Generate Test Results

```bash
pytest --alluredir=allure-results
```

You can also use `python -m pytest --alluredir=allure-results`.

### Install Allure

Make sure Node.js and npm are installed, then run:

```bash
npm install -g allure-commandline
```

### Generate Report

Run this as one complete command (keep `--clean` on the same line):

```bash
allure generate allure-results -o allure-report --clean
```

### Open Report

```bash
allure open allure-report
```

---

# 🧹 Generated Files

```text
.venv/
__pycache__/
.pytest_cache/
*.db
*.sqlite
*.sqlite3
allure-results/
allure-report/
logs/
.env
```

These should normally be excluded through `.gitignore`.

The `.env` file may contain local configuration or secrets. Never upload it; only `.env.example` should be shared as a template.

---

# ✅ Project Status

| Component | Status |
|---|---|
| FastAPI | ✅ Implemented |
| SQLite | ✅ Implemented |
| Authentication | ✅ Included |
| Order Tests | ✅ Included |
| Pytest | ✅ Configured |
| Allure | ✅ Supported |
| Android + Termux | ✅ Supported |
| Documentation | 🚧 Improving |

---

# 🤝 Contributing

Contributions and improvements are welcome.

Before submitting changes:

```bash
python -m pytest -v
```

Make sure the API works correctly and no real credentials are included.

---

# 📄 License

No license has been selected yet.

Add an appropriate license before distributing the project as open source.

---

## 🚀 E-Commerce API

**Build → Test → Report → Improve**

Made with 🐍 Python · ⚡ FastAPI · 🗄️ SQLite · 🧪 Pytest