# File: todo-main/reminder_service/reminder_service.py
import os
import time
import requests
import boto3
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

CHECK_INTERVAL = 60  # seconds

TODO_API_URL = os.getenv("TODO_API_URL", "http://localhost:5000/api/due_soon")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
GOOGLE_CREDS_JSON_PATH = os.getenv("GOOGLE_CREDENTIALS_JSON", "")

def send_email_sns(subject, message):
    """
    Publishes a message to the given SNS topic ARN to send an email notification.
    Make sure your SNS topic is set up to email subscribers.
    """
    if not SNS_TOPIC_ARN:
        print("No SNS_TOPIC_ARN provided. Skipping email.")
        return

    sns = boto3.client("sns", region_name=AWS_REGION)
    sns.publish(TopicArn=SNS_TOPIC_ARN, Subject=subject, Message=message)

def add_event_to_google_calendar(title, due_date, due_time):
    """
    Adds an event to Google Calendar if credentials are provided.
    This is a minimal example using a service account JSON key.
    """
    if not GOOGLE_CREDS_JSON_PATH or not os.path.exists(GOOGLE_CREDS_JSON_PATH):
        print("No valid Google credentials found. Skipping calendar integration.")
        return

    # Build credentials object (Service Account)
    creds = Credentials.from_service_account_file(GOOGLE_CREDS_JSON_PATH, scopes=["https://www.googleapis.com/auth/calendar"])
    service = build("calendar", "v3", credentials=creds)

    # Combine date/time into an RFC3339 datetime string
    # Example: '2025-01-31T14:30:00'
    try:
        dt_str = f"{due_date} {due_time}"
        dt = datetime.strptime(dt_str, "%m/%d/%Y %H:%M")
        dt_iso = dt.isoformat()

        event = {
            "summary": f"TODO Reminder: {title}",
            "start": {"dateTime": dt_iso, "timeZone": "UTC"},
            "end": {"dateTime": dt_iso, "timeZone": "UTC"},
        }

        # Insert into the primary calendar
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Added event to Google Calendar: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"Error adding event to Google Calendar: {e}")

def check_reminders():
    """
    Calls the TODO service for tasks due soon, sends emails via SNS,
    and optionally adds them to Google Calendar.
    """
    try:
        resp = requests.get(TODO_API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        tasks = data.get("due_soon", [])

        if not tasks:
            print(f"[{datetime.now()}] No tasks due soon.")
            return

        for task in tasks:
            title = task["title"]
            date = task["due_date"]
            ttime = task["due_time"]
            msg = f"Task '{title}' is due at {date} {ttime}.\nNotes: {task.get('notes','')}"

            # 1) Send an email via SNS
            send_email_sns(subject=f"Reminder: {title}", message=msg)

            # 2) Add to Google Calendar
            add_event_to_google_calendar(title, date, ttime)

            print(f"[{datetime.now()}] Processed reminder for task {task['id']}: {title}")

    except Exception as e:
        print(f"[{datetime.now()}] Error in check_reminders: {e}")

def main():
    print("Starting Reminder Service...")
    while True:
        check_reminders()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
