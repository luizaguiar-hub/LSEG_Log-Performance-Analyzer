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
