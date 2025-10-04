import os
import whois
import smtplib
from email.mime.text import MIMEText
import requests

# --- Config ---
EMAIL_USER = os.getenv("SMTP_USER")
EMAIL_PASS = os.getenv("SMTP_PASS")
EMAIL_1 = os.getenv("EMAIL_1")
EMAIL_2 = os.getenv("EMAIL_2")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def load_domains():
    """Read domain names from domains.txt"""
    with open("domains.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def send_email(subject, body):
    """Send email notification to all configured recipients"""
    recipients = [e for e in [EMAIL_USER, EMAIL_1, EMAIL_2] if e]
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(EMAIL_USER, EMAIL_PASS)
            s.sendmail(EMAIL_USER, recipients, msg.as_string())
        print(f"📨 Email sent: {subject}")
    except Exception as e:
        print(f"⚠️ Email failed: {e}")
        send_telegram(f"⚠️ Email failed: {e}")

def send_telegram(message):
    """Send Telegram alert"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
        print(f"📨 Telegram alert sent: {message}")
    except Exception as e:
        print(f"⚠️ Telegram failed: {e}")

def check_domain(domain):
    """Check if a domain is available or taken"""
    try:
        w = whois.whois(domain)
        if not w.domain_name:
            return "available"
        return "taken"
    except Exception:
        return "available"

def main():
    domains = load_domains()
    for domain in domains:
        status = check_domain(domain)
        print(f"{domain}: {status}")
        subject = f"Domain Status Update: {domain}"
        body = f"Domain '{domain}' is currently {status.upper()}."
        send_email(subject, body)
        send_telegram(f"🔔 Domain '{domain}' is now *{status.upper()}*")

if __name__ == "__main__":
    main()
