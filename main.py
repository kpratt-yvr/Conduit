import os
from dotenv import load_dotenv
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceMalformedRequest

import helper as hp

def build_nested_payload(flat_record):
    """Converts dot-notation keys into nested dictionaries for external IDs."""
    nested_output = {}
    for field_path, field_val in flat_record.items():
        keys = field_path.split('.')
        node = nested_output
        
        # Traverse and build nested dicts for all but the last key
        for key in keys[:-1]:
            node = node.setdefault(key, {})
            
        # Assign the value to the final key
        node[keys[-1]] = field_val
        
    return nested_output


def generate_report_files(bulk_results):
    """Processes and writes the success/error logs."""
    if not bulk_results:
        return

    successful, failed = hp.prepare_success_error_keys(bulk_results)
    hp.prepare_success_error_files(bulk_results, successful, failed)


def process_target_directory(target_dir, sf_client):
    """Recursively processes CSV and JSON files in the given directory."""
    if not os.path.isdir(target_dir):
        print("Error: Target path does not exist or is not a directory.")
        return

    os.chdir(target_dir)

    records_to_process = []
    job_config = {}
    has_csv_data = False

    # Scan the current directory
    for item in os.listdir():
        if item == '__results__':
            continue
            
        if os.path.isdir(item):
            # Recursively process subdirectories
            next_dir = os.path.join(target_dir, item)
            process_target_directory(next_dir, sf_client)
            os.chdir(target_dir)  # Return to current dir after recursion
            
        else:
            _, ext = os.path.splitext(item)
            if ext.lower() == ".csv":
                records_to_process = hp.read_data_from_csv(item)
                has_csv_data = True
            elif ext.lower() == ".json":
                job_config = hp.read_data_from_json(item)

    # Abort if we don't have all necessary components
    if not (has_csv_data and job_config and records_to_process):
        return

    obj_name = job_config.get("objectApiName")
    action_type = job_config.get("operationName")

    try:
        # Format the data for Salesforce bulk submission
        formatted_payload = [build_nested_payload(rec) for rec in records_to_process]

        # Submit DML operation
        outcome = sf_client.bulk.submit_dml(
            object_name=obj_name, 
            dml=action_type,
            data=formatted_payload, 
            include_detailed_results=True,
            batch_size="auto"
        )
        
        # Handle results folder creation and file writing
        if not os.path.exists('__results__'):
            os.mkdir('__results__')
            
        os.chdir('__results__')
        generate_report_files(outcome)
        
        # Revert back to the parent target directory
        os.chdir(target_dir)
        
    except (SalesforceMalformedRequest, ValueError) as err:
        print(f"Salesforce Operation Error: {err}")


def main():
    """Main execution block."""
    load_dotenv()
    
    sf_user = os.getenv("SF_USERNAME")
    sf_pass = os.getenv("SF_PASSWORD")
    sf_token = os.getenv("SF_SECURITY_TOKEN")

    # Initialize Salesforce connection
    sf_instance = Salesforce(
        username=sf_user, 
        password=sf_pass, 
        security_token=sf_token
    )

    # Prompt user and kick off processing
    root_location = input('Enter location of files: ')
    process_target_directory(root_location, sf_instance)


if __name__ == '__main__':
    main()