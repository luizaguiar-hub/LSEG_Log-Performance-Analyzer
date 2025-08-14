# log_monitor.py

import datetime

def parse_log(log_data):
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
    # Initializes lists to store the different categories of job reports.
    reports = {
        'less_than_1min': [],
        'longer_than_3min': [],
        'longer_than_5min': [],
        'longer_than_10min': [],
        'failed': []
    }

    # Iterates through all processes in the dictionary.
    for pid, data in processes.items():
        # Check if both start and end times exist. If not, the job is considered incomplete.
        if data['start'] and data['end']:
            # Combines the date and time for duration calculation.
            # A common dummy date is used to make the subtraction possible.
            dummy_date = datetime.date(1, 1, 1)
            start_datetime = datetime.datetime.combine(dummy_date, data['start'])
            end_datetime = datetime.datetime.combine(dummy_date, data['end'])

            # Calculates the duration in seconds.
            duration_seconds = (end_datetime - start_datetime).total_seconds()
            
            # Appends the report to the appropriate category based on the duration.
            report = {
                'pid': pid,
                'description': data['description'],
                'duration': duration_seconds
            }

            if duration_seconds < 60:
                reports['less_than_1min'].append(report)
            elif duration_seconds > 600: # 10 minutes
                reports['longer_than_10min'].append(report)
            elif duration_seconds > 300: # 5 minutes
                reports['longer_than_5min'].append(report)
            elif duration_seconds > 180: # 3 minutes
                reports['longer_than_3min'].append(report)
        else:
            # If a job has a start time but no end time, it is considered failed/incomplete.
            if data['start']:
                reports['failed'].append({
                    'pid': pid,
                    'description': data['description']
                })
    return reports

def generate_report(reports):
    # Creates a formatted string for the final report.
    report_lines = []
    report_lines.append("### Log Monitor Report ###\n")
    
    # Function to format job details for the report.
    def format_job(job):
        duration_formatted = ""
        if 'duration' in job:
            duration_formatted = f" (Duration: {job['duration']:.2f}s)"
        return f"- PID: {job['pid']}, Description: {job['description']}{duration_formatted}"

    # Adds the jobs from each category to the report string.
    report_lines.append("Jobs that took less than 1 minute:")
    if reports['less_than_1min']:
        for job in reports['less_than_1min']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No jobs in this category.")
    
    report_lines.append("\nJobs that took longer than 3 minutes:")
    if reports['longer_than_3min']:
        for job in reports['longer_than_3min']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No jobs in this category.")
        
    report_lines.append("\nJobs that took longer than 5 minutes:")
    if reports['longer_than_5min']:
        for job in reports['longer_than_5min']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No jobs in this category.")
        
    report_lines.append("\nJobs that took longer than 10 minutes:")
    if reports['longer_than_10min']:
        for job in reports['longer_than_10min']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No jobs in this category.")

    report_lines.append("\nFailed/Incomplete Jobs:")
    if reports['failed']:
        for job in reports['failed']:
            report_lines.append(format_job(job))
    else:
        report_lines.append("- No failed or incomplete jobs.")

    return "\n".join(report_lines)

if __name__ == '__main__':
    # Defines the path to the log file.
    log_file_path = 'logs_9.log'
    
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
        
    except FileNotFoundError:
        # Handles the case where the log file is not found.
        print(f"Error: The file '{log_file_path}' was not found.")
    except Exception as e:
        # Catches any other unexpected errors.
        print(f"An error occurred: {e}")
