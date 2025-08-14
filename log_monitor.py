# log_monitor.py
import datetime

def parse_log(log_data):
    """
    Parses log data to identify start and end times for each process ID.
    Args:
        log_data (list): A list of log lines.
    Returns:
        dict: A dictionary with process IDs as keys and a dictionary of start and end times as values.
    """
    # Dictionary to store the start and end times for each process ID.
    processes = {}
    for line in log_data:
        try:
            # Split the line by comma to get the individual components.
            parts = line.strip().split(',')
            # Ensure the line has the expected number of parts and format.
            if len(parts) != 4:
                continue

            timestamp_str, job_desc, status, pid = parts
            pid = int(pid)
            timestamp = datetime.datetime.strptime(timestamp_str, '%H:%M:%S').time()

            # Store the start and end times for each process.
            if pid not in processes:
                processes[pid] = {'start': None, 'end': None}
            
            if status.strip().upper() == 'START':
                processes[pid]['start'] = timestamp
            elif status.strip().upper() == 'END':
                processes[pid]['end'] = timestamp
        except (ValueError, IndexError):
            # Skip lines that can't be parsed correctly.
            continue
    return processes

def calculate_duration(processes):
    """
    Calculates the duration for each process and flags based on thresholds.
    Args:
        processes (dict): A dictionary of processes with start and end times.
    Returns:
        list: A list of reports for each process.
    """
    reports = []
    for pid, times in processes.items():
        start_time = times.get('start')
        end_time = times.get('end')

        # Only process jobs that have both a start and end time.
        if start_time and end_time:
            # Convert time objects to datetime objects for calculation.
            start_datetime = datetime.datetime.combine(datetime.date.min, start_time)
            end_datetime = datetime.datetime.combine(datetime.date.min, end_time)
            duration = (end_datetime - start_datetime).total_seconds()

            # Define time thresholds in seconds.
            warning_threshold = 5 * 60  # 5 minutes
            error_threshold = 10 * 60  # 10 minutes

            # Create a report for each process.
            report = {
                'pid': pid,
                'duration': duration,
                'status': 'OK',
                'message': f'Job {pid} completed in {duration:.2f} seconds.'
            }

            # Check against thresholds.
            if duration > error_threshold:
                report['status'] = 'ERROR'
                report['message'] = f'ERROR: Job {pid} took longer than 10 minutes. Duration: {duration:.2f} seconds.'
            elif duration > warning_threshold:
                report['status'] = 'WARNING'
                report['message'] = f'WARNING: Job {pid} took longer than 5 minutes. Duration: {duration:.2f} seconds.'
            
            reports.append(report)
    return reports

def generate_report(file_path):
    """
    Main function to read a log file, process it, and print a report.
    Args:
        file_path (str): The path to the log file.
    """
    try:
        with open(file_path, 'r') as f:
            log_data = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    processes = parse_log(log_data)
    reports = calculate_duration(processes)
    
    # Print the final report.
    print("--- Log Monitoring Report ---")
    for report in reports:
        print(report['message'])

if __name__ == '__main__':
    # You can change the file path here.
    log_file = 'logs_9.log' 
    generate_report(log_file)