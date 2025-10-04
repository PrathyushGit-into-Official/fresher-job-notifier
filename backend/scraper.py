import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def load_old_jobs():
    if os.path.exists("jobs.json"):
        with open("jobs.json", "r") as f:
            return json.load(f)
    return []

def save_jobs(jobs):
    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)

def send_email(job):
    message = Mail(
        from_email=os.getenv("SENDGRID_FROM"),
        to_emails=os.getenv("SENDGRID_TO"),
        subject=f"New Job Alert: {job['company']} - {job['role']}",
        html_content=f"<p>Company: {job['company']}<br>Role: {job['role']}<br>Location: {job['location']}<br><a href='{job['apply_link']}'>Apply Here</a></p>"
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
        print(f"Email sent for {job['company']}")
    except Exception as e:
        print(f"Email error: {e}")

def send_sms(job):
    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        msg = f"New Job Alert: {job['company']} - {job['role']} ({job['location']}). Apply: {job['apply_link']}"
        client.messages.create(
            body=msg,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=os.getenv("TWILIO_TO")
        )
        print(f"SMS sent for {job['company']}")
    except Exception as e:
        print(f"SMS error: {e}")

# Scraper functions for fresher/entry-level jobs
def scrape_google_jobs():
    return [{"company": "Google", "role": "Software Engineer", "location": "Bangalore", "apply_link": "https://careers.google.com/jobs"}]

def scrape_amazon_jobs():
    return [{"company": "Amazon", "role": "Junior Developer", "location": "Hyderabad", "apply_link": "https://amazon.jobs/en"}]

def scrape_bank_jobs():
    return [{"company": "Federal Bank", "role": "IT Trainee", "location": "Nandyal", "apply_link": "https://www.federalbank.co.in/careers"}]

def scrape_all_jobs():
    old_jobs = load_old_jobs()
    all_jobs = []
    all_jobs.extend(scrape_google_jobs())
    all_jobs.extend(scrape_amazon_jobs())
    all_jobs.extend(scrape_bank_jobs())

    # Identify new jobs
    new_jobs = [job for job in all_jobs if job not in old_jobs]

    # Send notifications for new jobs
    for job in new_jobs:
        send_email(job)
        send_sms(job)

    save_jobs(all_jobs)
    print(f"{len(all_jobs)} jobs scraped. {len(new_jobs)} new jobs notified.")
