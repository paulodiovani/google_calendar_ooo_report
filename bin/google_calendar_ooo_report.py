#!/usr/bin/env python

from datetime import UTC, datetime, timedelta
from functools import lru_cache
import calendar
import os.path
import yaml

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("store/token.json"):
    creds = Credentials.from_authorized_user_file("store/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "store/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("store/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    ooo_events = {}
    service = build("calendar", "v3", credentials=creds)

    start_date = get_start_date().isoformat() + "Z"
    end_date = get_end_date().isoformat() + "Z"

    for calendar_id in settings()["calendar_id"]:
      # Call the Calendar API
      events_result = (
          service.events()
          .list(
              calendarId=calendar_id,
              timeMin=start_date,
              timeMax=end_date,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      events = events_result.get("items", [])

      if not events:
        # no upcoming events for calendar
        continue

      ooo_events[calendar_id] = [
        event for event in events
        if (
          event["eventType"] == "outOfOffice"
          or any(keyword.lower() in event["summary"].lower() for keyword in settings()["keywords"])
        )
        and not any(keyword.lower() in event["summary"].lower() for keyword in settings()["exclude_keywords"])
      ]

    print_report(ooo_events)

  except HttpError as error:
    print(f"An error occurred: {error}")


@lru_cache(maxsize=None)
def settings():
  with open("settings.yml") as file:
    config = yaml.safe_load(file)
  return config["settings"]


@lru_cache(maxsize=None)
def get_start_date():
  today = datetime.today()
  match settings()["period"]:
    case "DAY":
      return today.replace(hour=0, minute=0, second=0, microsecond=0)
    case "WEEK":
      start_of_week = today - timedelta(days=today.weekday())
      return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    case "MONTH":
      return today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    case "YEAR":
      return today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    case _:
      raise ValueError("Invalid period specified in settings")


def get_end_date():
  start_date = get_start_date()
  match settings()["period"]:
    case "DAY":
      return start_date.replace(hour=23, minute=59, second=59, microsecond=999)
    case "WEEK":
      end_of_week = start_date + timedelta(days=6)
      return end_of_week.replace(hour=23, minute=59, second=59, microsecond=999)
    case "MONTH":
      last_day_of_month = calendar.monthrange(start_date.year, start_date.month)[1]
      return start_date.replace(day=last_day_of_month, hour=23, minute=59, second=59, microsecond=999)
    case "YEAR":
      return start_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999)
    case _:
      raise ValueError("Invalid period specified in settings")


def print_report(calendars):
  for calendar_id, events in calendars.items():
      print(calendar_id)
      for event in events:
          summary = event.get("summary", "No summary")
          print(f"  * {summary}: {event["start"]["dateTime"]} - {event["end"]["dateTime"]}")


if __name__ == "__main__":
  main()
