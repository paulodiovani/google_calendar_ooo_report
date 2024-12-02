#!/usr/bin/env python

from datetime import UTC, datetime
from functools import lru_cache
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

    for calendar_id in settings()["calendar_id"]:
      # Call the Calendar API
      now = datetime.now(UTC).isoformat()
      # print("Getting the upcoming 10 events")
      events_result = (
          service.events()
          .list(
              # calendarId="primary",
              calendarId=calendar_id,
              timeMin=now,
              maxResults=10,
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
        if event["eventType"] == "outOfOffice"
        or any(keyword.lower() in event["summary"].lower() for keyword in settings()["keywords"])
      ]

    print_report(ooo_events)
    # Prints the start and name of the next 10 events
    # for calendar, events in ooo_events:
    #   for event in events:
    #     start = event["start"].get("dateTime", event["start"].get("date"))
    #     print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")


@lru_cache(maxsize=None)
def settings():
  with open("settings.yml") as file:
    config = yaml.safe_load(file)
  return config["settings"]


def print_report(calendars):
  print(calendars)


if __name__ == "__main__":
  main()
