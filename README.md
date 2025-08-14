# LSEG_Log-Performance-Analyzer
This is a Python script that analyzes log files to assess job performance. It parses log data, calculates job durations, and generates a report that groups jobs into categories based on their runtime, making it easy to identify slow or failed tasks.

Description
This is a Python script that analyzes log files to assess job performance. It parses log data, calculates job durations, and generates a report that groups jobs into categories based on their runtime, making it easy to identify slow or failed tasks.

Usage
To use the script, you'll need a log file in the following format, with each line containing a timestamp, job description, action, and process ID (PID):

11:35:23,scheduled task 032, START,37980
11:35:56,scheduled task 032, END,37980

Save the Script: Save the provided log_monitor.py script in the same directory as your log file.

Name the Log File: Ensure your log file is named logs_9.log. If it has a different name, you will need to update the log_file_path variable in the if __name__ == '__main__': block of the script.

Run the Script: Execute the script from your terminal:

python log_monitor.py

The script will print a performance report to your console and save a copy as log_report.txt in the same directory.

New Upgrades
This version of the script includes several key enhancements to provide more detailed and useful analysis:

Detailed Performance Report: The script now generates a comprehensive report that categorizes jobs based on their duration.

Performance Categories: Jobs are automatically sorted into the following groups:

Less than 1 minute

Longer than 3 minutes

Longer than 5 minutes

Longer than 10 minutes

Failed Job Tracking: The report now includes a dedicated section for any jobs that started but did not have a corresponding END entry, helping to quickly identify failed or incomplete processes.

Output to File: In addition to printing the report to the console, the script now saves the full output to a file named log_report.txt for easy reference and sharing.

# Log Monitoring Application

This is a Python application for monitoring a log file, calculating the duration of jobs and tasks, and generating a report with warnings and errors based on time thresholds.

## Features

- Parses a CSV-formatted log file.
- Tracks the start and end times of each job using its process ID (PID).
- Calculates the total duration for each completed job.
- Flags jobs taking longer than 5 minutes as a **WARNING**.
- Flags jobs taking longer than 10 minutes as an **ERROR**.

## Setup and Usage

### Prerequisites

- Python 3.13.1 or later.
- A text editor or IDE.

### Installation

No special libraries are needed; all dependencies are part of the standard Python library. Simply clone this repository to your local machine.

### Change, Logs and Fixes

1. Initial Bug Fix: Correcting the Test Assertion
Original Issue: The unit test test_full_log_file_processing in test_log_monitor.py failed with an AssertionError. It was incorrectly asserting that the number of reports was 2, when the log file contained 43 completed jobs.

Fix: The assertion was corrected to self.assertEqual(len(reports), 43).

Upgrade: The unit test was enhanced with additional assertions to verify the status (OK, WARNING, ERROR) and calculated durations of specific jobs within the log file.

2. New Feature: Categorized Reporting
Request: The user wanted the script to generate a report that groups jobs by their duration.

Upgrade: The calculate_duration function was refactored to return a dictionary of categorized jobs, including less_than_1min, longer_than_3min, longer_than_5min, longer_than_10min, and failed. A new function, generate_report, was created to format and produce a human-readable report string.

Output: The if __name__ == '__main__': block was updated to print the report to the console and save it to a new file named log_report.txt.

3. Critical Fix: Resolving ImportError
Original Issue: A new ImportError occurred: cannot import name 'parse_log' from 'log_monitor'. This was a circular dependency where the script was trying to import its own functions from itself.

Fix: The line from log_monitor import parse_log, calculate_duration was completely removed from the script. Since the functions were defined in the same file, this import was redundant and caused the error.

4. Repository Documentation
Request: A name, description, and README.md file were requested to document the project.

Upgrade:

Repository Name: Log-Performance-Analyzer

Description: A Python script that monitors and analyzes log files to assess job performance.

README.md: A comprehensive README.md file was created, detailing the project's purpose, usage instructions, and a summary of the new upgrades (categorized reporting, failed job tracking, and file output).

5. New Feature: Email Alerts
Request: The final request was to upgrade the code to send an email alert when a job takes longer than 5 minutes or fails.

Upgrade:

New Function: A new function, send_email_report, was added using Python's smtplib and EmailMessage modules to handle sending emails via an SMTP server.

Alert Logic: The if __name__ == '__main__': block was modified to check the new report categories. If longer_than_5min, longer_than_10min, or failed jobs exist, an email is composed with a detailed body listing these specific jobs and is then sent using the new function.

Configuration: The script now includes placeholders for email configuration (sender_email, sender_password, recipient_email), which the user needs to fill in to use the feature.
