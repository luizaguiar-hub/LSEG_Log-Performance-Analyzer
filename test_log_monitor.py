# test_log_monitor.py
import unittest
import datetime
from log_monitor import parse_log, calculate_duration

class TestLogMonitor(unittest.TestCase):
    
    def test_parse_log_valid_data(self):
        #Test parsing of valid log lines.
        log_data = [
            "11:35:23,scheduled task 032, START,37980",
            "11:35:56,scheduled task 032, END,37980"
        ]
        processes = parse_log(log_data)
        self.assertIn(37980, processes)
        self.assertEqual(processes[37980]['start'], datetime.time(11, 35, 23))
        self.assertEqual(processes[37980]['end'], datetime.time(11, 35, 56))

    def test_parse_log_incomplete_data(self):
        #Test parsing of log lines with missing end times.
        log_data = [
            "11:36:11,scheduled task 796, START,57672"
        ]
        processes = parse_log(log_data)
        self.assertIn(57672, processes)
        self.assertIsNone(processes[57672]['end'])

    def test_calculate_duration_ok(self):
        #Test duration calculation for a job under the threshold.
        processes = {
            12345: {
                'start': datetime.time(10, 0, 0),
                'end': datetime.time(10, 1, 0)
            }
        }
        reports = calculate_duration(processes)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]['status'], 'OK')
        self.assertAlmostEqual(reports[0]['duration'], 60.0)

    def test_calculate_duration_warning(self):
        #Test duration calculation for a job over the 5-minute warning threshold.
        processes = {
            54321: {
                'start': datetime.time(10, 0, 0),
                'end': datetime.time(10, 5, 1)
            }
        }
        reports = calculate_duration(processes)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]['status'], 'WARNING')
        self.assertAlmostEqual(reports[0]['duration'], 301.0)
    
    def test_calculate_duration_error(self):
        #Test duration calculation for a job over the 10-minute error threshold.
        processes = {
            98765: {
                'start': datetime.time(10, 0, 0),
                'end': datetime.time(10, 10, 1)
            }
        }
        reports = calculate_duration(processes)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]['status'], 'ERROR')
        self.assertAlmostEqual(reports[0]['duration'], 601.0)

    def test_full_log_file_processing(self):
        #Test the end-to-end processing of the provided logs.log file.
        log_file_path = 'logs_9.log'
        try:
            with open(log_file_path, 'r') as f:
                log_data = f.readlines()
        except FileNotFoundError:
            self.fail(f"Test failed: The file '{log_file_path}' was not found.")

        processes = parse_log(log_data)
        reports = calculate_duration(processes)
        
        # There are 43 completed jobs in the provided log file.
        self.assertEqual(len(reports), 43)
        
        # Verify a job that should pass with an OK status (33 seconds)
        report_37980 = next((r for r in reports if r['pid'] == 37980), None)
        self.assertIsNotNone(report_37980)
        self.assertEqual(report_37980['status'], 'OK')
        self.assertAlmostEqual(report_37980['duration'], 33.0)

        # Verify a job that should trigger a WARNING (9m 28s = 568 seconds)
        report_87228 = next((r for r in reports if r['pid'] == 87228), None)
        self.assertIsNotNone(report_87228)
        self.assertEqual(report_87228['status'], 'WARNING')
        self.assertAlmostEqual(report_87228['duration'], 568.0)

        # Verify a job that should trigger an ERROR (14m 46s = 886 seconds)
        report_81258 = next((r for r in reports if r['pid'] == 81258), None)
        self.assertIsNotNone(report_81258)
        self.assertEqual(report_81258['status'], 'ERROR')
        self.assertAlmostEqual(report_81258['duration'], 886.0)

if __name__ == '__main__':
    unittest.main()