# log_monitor.py

# This script monitors and analyzes log files to assess job performance,
# categorizing jobs by duration and sending email alerts for critical issues.

import datetime
import smtplib
from email.message import EmailMessage

def parse_log(log_data):
    """
    Parses a list of log lines to extract job information.

    Args:
        log_data (list): A list of strings, where each string is a line from the log file.

    Returns:
        dict: A dictionary where keys are process IDs (PIDs) and values are
              dictionaries containing job descriptions, start times, and end times.
    """
    # Initializes a dictionary to store process information, using a unique ID as the key.
    processes = {}
    
    # Iterate through each line of the log data.
    for line in log_data:
        try:
            # Splits the line into components: timestamp, description, action, and PID.
            parts = line.strip().split(',')
            if len(parts) != 4:
                # Skips lines that do not have the expected format.
                continue

            # Extracts and cleans the data from the line parts.
            timestamp_str, job_desc, action, pid_str = parts
            pid = int(pid_str.strip())
            
            # Parses the timestamp string into a datetime.time object.
            time_obj = datetime.datetime.strptime(timestamp_str.strip(), '%H:%M:%S').time()

            # If the process ID (PID) is not already in the dictionary, create a new entry.
            if pid not in processes:
                processes[pid] = {
                    'description': job_desc.strip(),
                    'start': None,
                    'end': None
                }

            # Updates the start or end time based on the action in the log line.
            if action.strip().upper() == 'START':
                processes[pid]['start'] = time_obj
            elif action.strip().upper() == 'END':
                processes[pid]['end'] = time_obj

        except (ValueError, IndexError):
            # Handles potential errors during parsing, like incorrect time format or missing parts.
            print(f"Warning: Could not parse line: {line.strip()}")
            continue
            
    return processes

def calculate_duration(processes):
    """
    Calculates the duration of completed jobs and assigns a status.

    Args:
        processes (dict): The dictionary of process data from the parse_log function.

    Returns:
        list: A list of dictionaries, where each dictionary is a report for a single job
              and includes its status ('OK', 'WARNING', 'ERROR', or 'CRITICAL_ERROR').
    """
    reports = []
    
    # Iterates through all processes in the dictionary.
    for pid, data in processes.items():
        # A report dictionary to be populated and appended.
        report = {
            'pid': pid,
            'description': data['description']
        }

        # Check if both start and end times exist.
        if data['start'] and data['end']:
            # Combines the date and time for duration calculation.
            # A common dummy date is used to make the subtraction possible.
            dummy_date = datetime.date(1, 1, 1)
            start_datetime = datetime.datetime.combine(dummy_date, data['start'])
            end_datetime = datetime.datetime.combine(dummy_date, data['end'])

            # Calculates the duration in seconds.
            duration_seconds = (end_datetime - start_datetime).total_seconds()
            report['duration'] = duration_seconds
            
            # Assigns a status based on the duration.
            if duration_seconds > 600:  # More than 10 minutes
                report['status'] = 'ERROR'
            elif duration_seconds > 300:  # More than 5 minutes
                report['status'] = 'WARNING'
            else:
                report['status'] = 'OK'
        else:
            # If a job has a start time but no end time, it is considered a failed job.
            if data['start']:
                report['status'] = 'CRITICAL_ERROR'
                report['duration'] = 'N/A'  # No duration for incomplete jobs

        reports.append(report)

    return reports

def generate_report(reports):
    """
    Generates a formatted, multi-line string report from the categorized job data.

    Args:
        reports (list): A list of job report dictionaries.

    Returns:
        str: A formatted string ready to be printed or saved to a file.
    """
    # Group reports by their status for a cleaner output.
    grouped_reports = {'OK': [], 'WARNING': [], 'ERROR': [], 'CRITICAL_ERROR': []}
    for report in reports:
        grouped_reports[report['status']].append(report)

    report_lines = []
    report_lines.append("### Log Monitor Report ###\n")
    
    # Function to format job details for the report.
    def format_job(job):
        duration_formatted = ""
        if 'duration' in job and job['duration'] != 'N/A':
            duration_formatted = f" (Duration: {job['duration']:.2f}s)"
        elif job['duration'] == 'N/A':
            duration_formatted = " (Status: Incomplete/Failed)"
        return f"- PID: {job['pid']}, Description: {job['description']}{duration_formatted}"

    # Adds the jobs from each category to the report string.
    report_lines.append("--- OK Jobs (Less than 5 minutes) ---")
    if grouped_reports['OK']:
        for job in grouped_reports['OK']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No jobs in this category.")
    
    report_lines.append("\n--- WARNING Jobs (5 to 10 minutes) ---")
    if grouped_reports['WARNING']:
        for job in grouped_reports['WARNING']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No jobs in this category.")
        
    report_lines.append("\n--- ERROR Jobs (More than 10 minutes) ---")
    if grouped_reports['ERROR']:
        for job in grouped_reports['ERROR']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No jobs in this category.")

    report_lines.append("\n--- CRITICAL ERROR Jobs (Failed/Incomplete) ---")
    if grouped_reports['CRITICAL_ERROR']:
        for job in grouped_reports['CRITICAL_ERROR']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No jobs in this category.")
        
    return "\n".join(report_lines)

def send_email_report(subject, body, sender_email, recipient_email, password):
    """
    Sends an email notification.

    Args:
        subject (str): The subject line of the email.
        body (str): The content of the email.
        sender_email (str): The email address of the sender.
        recipient_email (str): The email address of the recipient.
        password (str): The password for the sender's email account.
    """
    # Creates the email message object.
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Connects to the SMTP server (using a common one as an example).
        # You may need to change 'smtp.gmail.com' and the port for your provider.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Logs in to the email account.
            smtp.login(sender_email, password)
            # Sends the email.
            smtp.send_message(msg)
        print("\nEmail sent successfully!")
    except Exception as e:
        # Handles any errors during the email sending process.
        print(f"\nFailed to send email. An error occurred: {e}")

if __name__ == '__main__':
    # Defines the path to the log file.
    log_file_path = 'logs 9.log'
    
    # --- EMAIL CONFIGURATION ---
    # !!! IMPORTANT: Fill in your email details here. !!!
    # This example uses Gmail with SSL. You may need to enable "less secure apps" or
    # use an app-specific password if you have 2FA enabled.
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    recipient_email = "your_recipient@example.com"
    
    try:
        # Opens and reads the log file.
        with open(log_file_path, 'r') as f:
            log_data = f.readlines()
        
        # Calls the functions to process the log data and generate the report.
        processes = parse_log(log_data)
        reports = calculate_duration(processes)
        final_report = generate_report(reports)
        
        # Prints the report to the console.
        print(final_report)
        
        # Saves the report to a new file.
        with open('log_report.txt', 'w') as f:
            f.write(final_report)
            
        print("\nReport saved to 'log_report.txt'")
        
        # --- EMAIL ALERT LOGIC ---
        # Checks if there are any jobs that need an alert.
        critical_error_jobs = [r for r in reports if r['status'] == 'CRITICAL_ERROR']
        warning_jobs = [r for r in reports if r['status'] == 'WARNING']
        error_jobs = [r for r in reports if r['status'] == 'ERROR']
        
        if critical_error_jobs or warning_jobs or error_jobs:
            alert_body = "The following jobs require attention:\n\n"
            email_subject = "Log Monitor Alert"
            
            if critical_error_jobs:
                alert_body += "--- CRITICAL ERROR Jobs (Failed/Incomplete) ---\n"
                for job in critical_error_jobs:
                    alert_body += f"- PID: {job['pid']}, Description: {job['description']} (Failed/Incomplete)\n"
                alert_body += "\n"
                email_subject = "CRITICAL ERROR DETECTED"
            
            if warning_jobs:
                alert_body += "--- WARNING Jobs (5 to 10 minutes) ---\n"
                for job in warning_jobs:
                    alert_body += f"- PID: {job['pid']}, Description: {job['description']}, Duration: {job['duration']:.2f}s\n"
                alert_body += "\n"
            
            if error_jobs:
                alert_body += "--- ERROR Jobs (More than 10 minutes) ---\n"
                for job in error_jobs:
                    alert_body += f"- PID: {job['pid']}, Description: {job['description']}, Duration: {job['duration']:.2f}s\n"
                alert_body += "\n"

            send_email_report(
                subject=email_subject,
                body=alert_body,
                sender_email=sender_email,
                recipient_email=recipient_email,
                password=sender_password
            )
        else:
            print("\nNo alerts to send. All monitored jobs are within acceptable limits.")

    except FileNotFoundError:
        # Handles the case where the log file is not found.
        print(f"Error: The file '{log_file_path}' was not found.")
    except Exception as e:
        # Catches any other unexpected errors.
        print(f"An error occurred: {e}")
