import argparse
import json
from collections import defaultdict
from tabulate import tabulate

def read_logs(files, date_filter=None):
    logs = []
    for file_path in files:
        try:
            with open(file_path, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        log_entry = json.loads(line.strip())
                        if date_filter and log_entry.get('date') != date_filter:
                            continue
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {file_path} at line {line_num}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
    return logs

def generate_average_report(log_entries):
    endpoint_stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
    for entry in log_entries:
        path = entry.get('path')
        time = entry.get('time')
        if path is None or time is None:
            continue
        try:
            time_val = float(time)
        except ValueError:
            continue
        endpoint_stats[path]['count'] += 1
        endpoint_stats[path]['total_time'] += time_val
    
    report_data = []
    for endpoint, stats in endpoint_stats.items():
        avg_time = stats['total_time'] / stats['count']
        report_data.append([endpoint, stats['count'], round(avg_time, 2)])
    return report_data, ['Endpoint', 'Count', 'Average Time']

def main():
    parser = argparse.ArgumentParser(description='Process log files and generate reports.')
    parser.add_argument('--file', nargs='+', required=True, help='Path to the log file(s)')
    parser.add_argument('--report', required=True, choices=['average'], help='Type of report to generate')
    parser.add_argument('--date', help='Filter logs by date (format: YYYY-DD-MM)')
    
    args = parser.parse_args()
    
    logs = read_logs(args.file, args.date)
    
    if args.report == 'average':
        data, headers = generate_average_report(logs)
        print(tabulate(data, headers=headers, tablefmt='grid'))

if __name__ == '__main__':
    main()