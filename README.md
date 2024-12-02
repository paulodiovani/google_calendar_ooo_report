# Google Calendar Out of Office Report

Script to generate an OOO (out of office) monthly report for a list of users.

## Usage

```bash
# Copy and fill settings.yml
cp settings.yml.sample settings.yml

# Create and activate virtual env
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
./bin/google_calendar_ooo_report.py
```
