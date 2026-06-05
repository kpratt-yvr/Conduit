# Conduit
![Header](https://raw.githubusercontent.com/kpratt-yvr/Conduit/refs/heads/main/images/conduit.jpg) 


## Overview 
Stop clicking through Data Loader. Conduit is a Python script turns Salesforce data loads into a repeatable, config-driven process. Simply point it at a folder, and it handles the rest.

### Why I Created This
Manual data loads work until they don't. For small deployments, clicking through Data Loader is fine and simple to get the right data into the right objects and fields. For go-lives with 10+ objects, dependent lookups, junction objects, and tight release windows, it becomes a liability. Wrong operation selected, mismatched field mappings, results saved in the wrong folder. Conduit eliminates the repetition and the guesswork and aims at supporting better data imports when going live. One thing is always true and that is bad data kills adoption. If users open the system on day one and the data is wrong, incomplete, or missing they won't trust it. And once that trust is gone, it's hard to get back.

Some issues I have found during related large volume data loads: 
1. Error-prone due to incorrect load order
2. Time consuming to reproduce across environments
3. Manual and time consuming

Conduit aims to remove manual effort by automating data load from folders directly via Data Loader.




### How It Works
Each data load operation lives in its own folder containing two files:

1. A CSV with the data
2. A JSON with the instructions (object API name, DML operation, load config)

Point the script at a parent directory. It scans recursively, finds every valid operation folder, and executes each load automatically via the Salesforce Bulk API. No SDL files. No UI clicks. No manual repetition.
Results land in a `__results__ folder` which has timestamped success and error CSVs, every run

### Folder Structure 

```
parent-directory/
├── 01_accounts/
│   ├── data.csv
│   └── config.json
├── 02_contacts/
│   ├── data.csv
│   └── config.json
└── __results__/
    ├── success2026-01-31 10.00.00.csv
    └── error2026-01-31 10.00.00.csv
```
### Support.py Function
`support.py` is a utility module and it handles all the file I/O so `main.py` stays clean. It has four functions:
1. Reads a CSV into a pandas DataFrame, replaces any blank cells with empty strings (so the Bulk API doesn't choke on NaN values), then returns it as a list of dictionaries — one dict per row.
2. Opens a JSON config file and returns it as a Python object. This is where the DML operation and object API name get read from.
3. Looks at the keys returned in the Bulk API result and splits them into two lists: 1) for success records, and 2) for errors by removing the columns that don't belong in each file (e.g. removes errors from success keys, removes success and created from error keys).
4. Takes the full result set, splits it into successes and errors, and writes each to a timestamped CSV in the current directory. Uses the key lists from the function above to control which columns appear in each file.

### Setup
#### Step 1: Clone the Repo
```
git clone https://github.com/kpratt-yvr/Conduit
cd Conduit
```

#### Step 2: Create a `.env` File
```
SF_USERNAME=your_username
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
```

#### Step 3: Install Dependencies 
```
pip install -prodorgreqs.txt
```

#### Step 4: Run
```
python main.py
```
When prompted, enter the path to the parent directory and Conduit handles everything else. 

### Limitations
1. CSV headers must match SF field API names exactly, as JSON based field mapping is not supported
2. Single record files are skipped (as a result of the bulk API requirement)

### Stack
- Python 3.9 (and higher) 
- [simple-salesforce](https://simple-salesforce.readthedocs.io/en/latest/) 
- Salesforce Bulk API 

### Notes
This is not a replacement for Data Loader, rather it's a wrapper around the parts that shouldn't require human attention.

![footer](https://raw.githubusercontent.com/kpratt-yvr/Conduit/refs/heads/main/images/updated%20footer.jpeg)
