# 📧 Bulk Email Manager

A simple and efficient Streamlit-based Bulk Email Management System that allows users to upload recipient lists through CSV files, create personalized email templates using dynamic placeholders, preview emails, send test emails, and execute bulk email campaigns through SMTP providers such as Gmail.

---

## Features

### 📤 CSV Recipient Upload

Upload recipient data using CSV files.

Supported format:

```csv
Applicant Name,Email,Section,Position
John Doe,john@gmail.com,IEEE CS SYP,Media Lead
Jane Smith,jane@gmail.com,IEEE WIE,Chairperson
```

Features:

* CSV file upload
* Recipient preview
* Dynamic placeholder mapping
* Supports unlimited recipients (subject to SMTP limits)

---

### ✉️ Email Template Builder

Create reusable email templates with dynamic placeholders.

Supported placeholders:

```text
{{Applicant Name}}
{{Email}}
{{Section}}
{{Position}}
```

Example Subject:

```text
Congratulations - {{Position}} Selection
```

Example Body:

```text
Hello {{Applicant Name}},

You have been selected as the {{Section}} {{Position}}.

Congratulations.

Best Regards,
IEEE Team
```

---

### 👀 Email Preview

Preview the generated email before sending.

Displays:

* Rendered subject
* Rendered email body

The preview automatically uses the first recipient in the uploaded CSV file.

---

### 🧪 Test Email Sending

Send a test email before launching a bulk campaign.

Features:

* Verify SMTP settings
* Verify template rendering
* Verify CC recipients
* Verify BCC recipients

---

### 📬 Bulk Email Campaigns

Send personalized emails to all recipients in the uploaded CSV.

Features:

* Dynamic placeholder replacement
* Individual email generation
* Progress tracking
* Delivery logs
* Success count reporting

---

### 📋 CC & BCC Support

Send copies to multiple recipients.

Example:

```text
cc1@example.com,cc2@example.com
```

```text
bcc1@example.com,bcc2@example.com
```

Features:

* Multiple recipients
* Email validation
* Duplicate removal

---

### ✅ Email Validation

The system automatically validates:

* Email format
* Empty email addresses
* Duplicate email addresses

Invalid emails are rejected before sending.

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python 3.x
* Pandas
* SMTP (smtplib)

### Email Components

* email.mime.multipart
* email.mime.text

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/bulk-email-manager.git

cd bulk-email-manager
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Requirements

Create a `requirements.txt` file with:

```text
streamlit
pandas
```

Install:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## SMTP Configuration

### Gmail

To use Gmail SMTP:

```text
SMTP Host: smtp.gmail.com
SMTP Port: 587
```

Requirements:

1. Enable Two-Factor Authentication on your Google Account.
2. Generate a Google App Password.
3. Use the App Password instead of your Gmail password.

---

### Outlook

```text
SMTP Host: smtp.office365.com
SMTP Port: 587
```

---

## How to Use

### Step 1

Configure SMTP settings from the sidebar.

Enter:

* SMTP Host
* SMTP Port
* Sender Email
* App Password

---

### Step 2

Upload a CSV file containing recipient information.

---

### Step 3

Create your email subject and body using placeholders.

---

### Step 4

Review the email preview.

---

### Step 5

Send a test email.

---

### Step 6

Click **Send Bulk Emails** to start the campaign.

---

## Example CSV

```csv
Applicant Name,Email,Section,Position
John Doe,john@gmail.com,IEEE CS SYP,Media Lead
Jane Smith,jane@gmail.com,IEEE WIE,Chairperson
Alice Brown,alice@gmail.com,IEEE PES,Secretary
```

---

## Example Email Output

Subject:

```text
Congratulations - Media Lead Selection
```

Body:

```text
Hello John Doe,

You have been selected as the IEEE CS SYP Media Lead.

Congratulations.

Best Regards,
IEEE Team
```

---

## Current Limitations

* No database integration
* No campaign history
* No email scheduling
* No attachment support
* No authentication system
* No analytics dashboard
* No HTML email editor

---

## Future Improvements

* SQLite/PostgreSQL integration
* Campaign management
* Email templates storage
* Attachment support
* Rich HTML email editor
* Analytics dashboard
* Email scheduling
* SMTP profile management
* Real-time campaign tracking

---

## License

This project is released under the MIT License.

---

## Author

Developed by Kavindu Ranasinghe
