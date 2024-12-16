# Google Calendar Out of Office Report

Script to generate an OOO (out of office) monthly report for a list of users.

## Preliminary setup

1. Follow the **Set up your environment** Instructions from the [Python Quickstart page](https://developers.google.com/calendar/api/quickstart/python)
    - Enable the API (select or create a project)
    - Configure the OAuth consent screen
    - Authorize credentials for a desktop application

    You can ignore the remaining instructions from that page.
2. Save the client secret file to `store/credentials.json`
3. Ask to "See all events details" on the calendars to read (listed in `settings.yml`)

## Setup and usage

```bash
# Copy and fill settings.yml
cp settings.yml.sample settings.yml

# Create and activate virtual env
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
./bin/google_calendar_ooo_report
```

### Help

```
Usage: google_calendar_ooo_report [OPTIONS]

  Fetch user calendars and print a report of OOO (Out of Office) events.
  Configuration is defined in settings.yml file.

  Some options can be overridden with arguments.

Options:
  -d, --date TEXT               Date to report (default to today).
  -p, --period TEXT             Period to report: DAY, WEEK, MONTH, YEAR.
                                Start at beginning of.
  -f, --format [csv|json|text]  Output format (default to text).
  -w, --weekend / --no-weekend  Include weekends in report (default to False)
  --help                        Show this message and exit.
```

### Sample output

```
$ ./bin/google_calendar_ooo_report --date 2024-12-01 --period MONTH
harry.potter@example.com
  2024-12-23 - 2024-12-24 - Harry Potter OOO (2 days, 0:00:00)
frodo.baggins@example.com
  2024-12-23 - 2024-12-31 - Codeminer's Collective Vacation (9 days, 0:00:00)
luke.skywalker@example.com
  2024-12-23 - 2024-12-31 - Vacations! (9 days, 0:00:00)
sherlock.holmes@example.com
  2024-12-20              - Out of office: Medical Appointment (1:00:00)
  2024-12-23 - 2024-12-31 - Out of office: Codeminer42 collective vacation (9 days, 0:00:00)
hermione.granger@example.com
  2024-12-23 - 2024-12-31 - Out of Office (9 days, 0:00:00)
```
