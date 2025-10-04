import os
import whois
import smtplib
from email.mime.text import MIMEText
import requests

# Configs (use GitHub secrets for these)
DOMAINS = ["trupabranding.com", "trupahost.com, adwumawura.com"]
EMAIL_USER = os.getenv("SMTP_USER")
EMAIL_PASS = os.getenv("SMTP_PASS")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_email(domain, status):
    msg = MIMEText(f"Domain '{domain}' is now {status.upper()}.")
    msg["Subject"] = f"Domain Status Alert: {domain}"
    msg["From"] = SMTP_USER
    msg["To"] = SMTP_USER

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
    print(f"✅ Email sent for {domain}")

def send_telegram(domain, status):
    message = f"🔔 Domain '{domain}' is now *{status.upper()}*"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=payload)
    print(f"✅ Telegram alert sent for {domain}")

def check_domain(domain):
    try:
        w = whois.whois(domain)
        if not w.domain_name:
            status = "available"
        else:
            status = "taken"
    except:
        status = "available"
    return status

def main():
    for domain in DOMAINS:
        status = check_domain(domain)
        print(f"{domain}: {status}")
        if status == "available":
            send_email(domain, status)
            send_telegram(domain, status)

if __name__ == "__main__":
    main()
