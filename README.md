# Folder Synchronization Script

This Python script synchronizes the contents of a source folder with a replica folder by copying new or updated files and removing any extra files in the replica. 
It can be scheduled to run at regular intervals.


## Features
- **Sync Folders**: Copies new/modified files from source to replica.
- **Remove Extras**: Deletes files/folders in replica that are not in source.
- **Logging**: Logs sync activities to a specified log file.
- **Scheduling**: Runs at specified intervals.


## Requirements
- Python 3.x (no external libraries needed)


## Usage
Run the script with:

```
python3 sync_folders.py --source_path <source_folder> --replica_path <replica_folder> --interval <seconds> --log_file <log_file>
```

*  --source_path: Path to the source folder (required)
*  --replica_path: Path to the replica folder (required)
*  --interval: Sync interval in seconds (default: 60)
*  --log_file: Log file path (default: `./logs/sync_logging`)

