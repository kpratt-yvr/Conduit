import csv
import json
from datetime import datetime
import pandas as pd

def read_data_from_csv(filepath):
    """Loads a CSV into a list of dictionaries, replacing nulls with empty strings."""
    dataframe = pd.read_csv(filepath)
    # Using inplace=True avoids reassigning the variable
    dataframe.fillna('', inplace=True)
    return dataframe.to_dict(orient='records')


def read_data_from_json(filepath):
    """Reads and parses a JSON file."""
    # Added encoding='utf-8' for safer cross-platform reading
    with open(filepath, 'r', encoding='utf-8') as file_pointer:
        # json.load() is cleaner than json.loads(file.read())
        return json.load(file_pointer)


def prepare_success_error_files(json_data, success_keys, error_keys):
    """Splits the result data into success and error CSV logs."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    
    success_filename = f"success{timestamp}.csv"
    error_filename = f"error{timestamp}.csv"

    # Separate records using list comprehensions instead of lambda/filter
    successful_records = [record for record in json_data if 'success' in record]
    failed_records = [record for record in json_data if 'errors' in record]

    # Write success log
    with open(success_filename, 'w', newline='', encoding='utf-8') as success_out:
        success_writer = csv.DictWriter(success_out, fieldnames=success_keys, extrasaction='ignore')
        success_writer.writeheader()
        success_writer.writerows(successful_records)

    # Write error log (added newline='' to prevent blank rows on Windows)
    with open(error_filename, 'w', newline='', encoding='utf-8') as error_out:
        error_writer = csv.DictWriter(error_out, fieldnames=error_keys, extrasaction='ignore')
        error_writer.writeheader()
        error_writer.writerows(failed_records)

    # Maintaining the original script's return behavior exactly
    return success_out, error_out


def prepare_success_error_keys(result_data):
    """Determines the appropriate CSV headers for success and error logs."""
    all_keys = list(result_data.keys())

    # Use list comprehensions to filter out unwanted headers instead of .remove()
    success_headers = [key for key in all_keys if key != 'errors']
    error_headers = [key for key in all_keys if key not in ['success', 'created']]

    return success_headers, error_headers


if __name__ == '__main__':
    print('Helper module initialized.')