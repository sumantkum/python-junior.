
Log File Processing Script
A Python script for processing JSON log files to generate reports on endpoint usage and performance metrics.

Features
Processes multiple log files in JSON format

Generates average response time reports by endpoint

Filters log entries by specific dates

Displays results in easy-to-read tabular format

Extensible architecture for adding new report types

Comprehensive test coverage

Requirements
Python 3.6 or higher

Required Python packages:

tabulate

pytest (for testing)

Installation
Clone or download the project files

Create a virtual environment (recommended):

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install tabulate pytest pytest-cov
Usage
Basic Command
bash
python main.py --file <logfile> --report average
Process Multiple Files
bash
python main.py --file log1.log log2.log --report average
Filter by Date
bash
python main.py --file access.log --report average --date 2025-22-06
Example Output
text
+-----------------+---------+----------------+
| Endpoint        |   Count |   Average Time |
+=================+=========+================+
| /api/v1/users   |       2 |           0.4  |
+-----------------+---------+----------------+
| /api/v1/products|       1 |           0.2  |
+-----------------+---------+----------------+
Log File Format
The script expects log files with JSON objects on each line. Each entry should include:

path: The endpoint path (required)

time: Response time in seconds (required)

date: Date in YYYY-DD-MM format (optional, for filtering)

Example log entry:

json
{"path": "/api/v1/users", "time": 0.5, "date": "2025-22-06"}
Testing
Run the test suite with:

bash
pytest
Generate a coverage report with:

bash
pytest --cov=.
Project Structure
text
log-processor/
├── main.py          # Main script
├── test_main.py     # Test cases
└── README.md        # This file
Error Handling
The script handles:

Missing files with informative error messages

Invalid JSON with line number reporting

Missing required fields in log entries

Invalid date formats

Extensibility
The code is designed to easily accommodate new report types. To add a new report:

Create a new report generation function following the pattern of generate_average_report

Add the report type to the argument parser choices

Add a conditional branch in the main function to handle the new report type
