import os
import whois
import smtplib
from email.mime.text import MIMEText
import requests

# Configs (use GitHub secrets for these)
DOMAINS = ["trupabranding.com", "trupahost.com", "adwumawura.com"]
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_telegram(message):
    """Send a message to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
        print(f"📨 Telegram alert sent: {message}")
    except Exception as e:
        print(f"⚠️ Failed to send Telegram alert: {e}")

def send_email(domain, status):
    """Send an email alert for domain status."""
    msg = MIMEText(f"Domain '{domain}' is now {status.upper()}.")
    msg["Subject"] = f"Domain Status Alert: {domain}"
    msg["From"] = SMTP_USER
    msg["To"] = SMTP_USER

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        print(f"✅ Email sent for {domain}")
    except Exception as e:
        error_msg = f"⚠️ Email failed for {domain}: {e}"
        print(error_msg)
        # Notify you via Telegram too
        send_telegram(error_msg)

def check_domain(domain):
    """Check if a domain is available."""
    try:
        w = whois.whois(domain)
        if not w.domain_name:
            return "available"
        else:
            return "taken"
    except Exception:
        # WHOIS failed → treat as available
        return "available"

def main():
    for domain in DOMAINS:
        status = check_domain(domain)
        print(f"{domain}: {status}")
        if status == "available":
            send_email(domain, status)
            send_telegram(f"🔔 Domain '{domain}' is now *AVAILABLE!*")

if __name__ == "__main__":
    main()
