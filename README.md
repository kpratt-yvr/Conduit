# Conduit
![Header](https://raw.githubusercontent.com/kpratt-yvr/Conduit/refs/heads/main/images/conduit.jpg) 


## Overview 
Stop clicking through Data Loader. Conduit is a Python script turns Salesforce data loads into a repeatable, config-driven process. Simply point it at a folder, and it handles the rest.

### Why I Created This
Manual data loads work until they don't. For small deployments, clicking through Data Loader is fine and simple to get the right data into the right objects and fields. For go-lives with 10+ objects, dependent lookups, junction objects, and tight release windows, it becomes a liability. Wrong operation selected, mismatched field mappings, results saved in the wrong folder. Conduit eliminates the repetition and the guesswork and aims at supporting better data imports when going live. After 10+ go-lives, one thing is always true: bad data kills adoption. If users open the system on day one and the data is wrong, incomplete, or missing they won't trust it. And once that trust is gone, it's hard to get back.

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
