import pytest
import json
import tempfile
import os
from main import read_logs, generate_average_report

def test_read_logs():
    logs = [
        {
            'path': '/api/v1/users', 
            'time': 0.5, 
            'date': '2025-22-06'
         },
        {
            'path': '/api/v1/products', 
            'time': 0.2, 
            'date': '2025-22-06'
        }
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')
        temp_file = f.name

    try:
        result = read_logs([temp_file])
        assert len(result) == 2
        result_with_date = read_logs([temp_file], '2025-22-06')
        assert len(result_with_date) == 2
        result_with_wrong_date = read_logs([temp_file], '2025-23-06')
        assert len(result_with_wrong_date) == 0
    finally:
        os.unlink(temp_file)

def test_generate_average_report():
    logs = [
        {'path': '/api/v1/users', 'time': 0.5},
        {'path': '/api/v1/users', 'time': 0.3},
        {'path': '/api/v1/products', 'time': 0.2}
    ]
    data, headers = generate_average_report(logs)
    assert headers == ['Endpoint', 'Count', 'Average Time']
    data_dict = {row[0]: (row[1], row[2]) for row in data}
    assert data_dict['/api/v1/users'] == (2, 0.4)
    assert data_dict['/api/v1/products'] == (1, 0.2)

def test_generate_average_report_missing_fields():
    logs = [
        {'path': '/api/v1/users', 'time': 0.5},
        {'time': 0.3},
        {'path': '/api/v1/products'}
    ]
    data, headers = generate_average_report(logs)
    assert len(data) == 1
    assert data[0][0] == '/api/v1/users'