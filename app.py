import streamlit as st
import pandas as pd
import smtplib
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

st.set_page_config(
    page_title="Bulk Email Manager",
    layout="wide"
)

st.title("📧 Bulk Email Management System")

# =========================
# HELPER FUNCTIONS
# =========================

def parse_and_validate_emails(email_string):
    """
    Parses comma-separated emails, trims whitespace, removes empties,
    validates format, and removes duplicates while preserving order.
    """
    if not email_string or pd.isna(email_string):
        return []
    
    raw_emails = [e.strip() for e in str(email_string).split(",")]
    valid_emails = []
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    
    for email in raw_emails:
        if not email:
            continue
            
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid email format detected: '{email}'")
            
        valid_emails.append(email)
        
    return list(dict.fromkeys(valid_emails))

# =========================
# SMTP SETTINGS
# =========================

st.sidebar.header("SMTP Settings")

smtp_host = st.sidebar.text_input("SMTP Host", value="smtp.gmail.com")
smtp_port = st.sidebar.number_input("SMTP Port", value=587)
sender_email = st.sidebar.text_input("Sender Email")
app_password = st.sidebar.text_input("App Password", type="password")

cc_emails = st.sidebar.text_input(
    "CC Emails",
    help="Enter multiple email addresses separated by commas."
)

bcc_emails = st.sidebar.text_input(
    "BCC Emails",
    help="Enter multiple email addresses separated by commas."
)

# =========================
# CSV UPLOAD
# =========================

st.header("Upload Recipients")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"{len(df)} recipients loaded")
    st.dataframe(df)

# =========================
# TEMPLATE BUILDER & PREVIEW
# =========================

st.header("Email Template")

subject_template = st.text_input(
    "Subject",
    value="Congratulations - {{Position}} Selection"
)

body_template = st.text_area(
    "Email Body",
    height=300,
    value="""Hello {{Applicant Name}},

You have been selected as the {{Section}} {{Position}}

Congratulations.

Best Regards,
IEEE Team"""
)

st.header("Preview")

preview_subject = subject_template
preview_body = body_template

if df is not None and len(df) > 0:
    preview_row = df.iloc[0]
    for col in df.columns:
        placeholder = "{{" + col + "}}"
        preview_subject = preview_subject.replace(placeholder, str(preview_row[col]))
        preview_body = preview_body.replace(placeholder, str(preview_row[col]))

st.subheader("Subject")
st.code(preview_subject)
st.subheader("Body")
st.text(preview_body)

# =========================
# CORE EMAIL LOGIC
# =========================

def send_email(recipient_email, subject, body, cc_str="", bcc_str=""):
    """Core function used by BOTH Test Send and Bulk Send."""
    to_list = parse_and_validate_emails(recipient_email)
    cc_list = parse_and_validate_emails(cc_str)
    bcc_list = parse_and_validate_emails(bcc_str)
    
    if not to_list:
        raise ValueError("Primary recipient is missing or invalid.")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject
    
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(sender_email, app_password)

    all_recipients = list(dict.fromkeys(to_list + cc_list + bcc_list))

    server.sendmail(sender_email, all_recipients, msg.as_string())
    server.quit()

# =========================
# 1. TEST EMAIL SECTION
# =========================

st.header("Test Email")
test_email = st.text_input("Send Test Email To")

if st.button("Send Test Email"):
    try:
        # Uses the preview text if a CSV is loaded, otherwise uses the raw template
        send_email(
            test_email,
            preview_subject,
            preview_body,
            cc_str=cc_emails,
            bcc_str=bcc_emails
        )
        st.success("Test email sent successfully! CC and BCC recipients were included.")
    except Exception as ex:
        st.error(f"Error: {str(ex)}")

# =========================
# 2. BULK SEND SECTION
# =========================

st.header("Bulk Email Campaign")

if st.button("Send Bulk Emails"):
    if df is None:
        st.error("Upload a CSV first before starting a bulk campaign.")
    else:
        try:
            # Pre-validate CC/BCC formats before looping
            parse_and_validate_emails(cc_emails)
            parse_and_validate_emails(bcc_emails)
        except ValueError as ve:
            st.error(f"Global SMTP Validation Error: {ve}")
            st.stop()

        progress = st.progress(0)
        success_count = 0
        logs = []

        for index, row in df.iterrows():
            try:
                subject = subject_template
                body = body_template

                for col in df.columns:
                    placeholder = "{{" + col + "}}"
                    subject = subject.replace(placeholder, str(row[col]))
                    body = body.replace(placeholder, str(row[col]))

                # Core function called for each row
                send_email(
                    row["Email"],
                    subject,
                    body,
                    cc_str=cc_emails,
                    bcc_str=bcc_emails
                )
                success_count += 1
                logs.append({"Email": row["Email"], "Status": "Sent"})

            except Exception as ex:
                logs.append({"Email": row.get("Email", "Unknown"), "Status": f"Failed: {ex}"})

            progress.progress((index + 1) / len(df))

        st.success(f"Campaign Complete: {success_count}/{len(df)} emails sent.")
        st.subheader("Campaign Logs")
        st.dataframe(pd.DataFrame(logs))