import argparse
import os
import shutil
import logging

def sync_folders(source_path, replica_path):
    
    ### First we check if the replica dir exists, if not, we create it
    if not os.path.exists(replica_path):
        print(f"Replica directory doesn't exist at: {replica_path} so we are creating it")
        os.makedirs(replica_path)

    ### Adding missing elements to the replica folder
    for root, dirs, files in os.walk(source_path):
        # Relative path of the current root to the source directory
        source_relative_path = os.path.relpath(root, source_path)
        print(f"Currently at: {source_relative_path}")

        # Add the current 'root' directory if it's missing
        replica_dir = os.path.join(replica_path, source_relative_path)
        if not os.path.exists(replica_dir):
            print(f"-- DIR: {root} copied to replica folder - {replica_dir}")
            os.makedirs(replica_dir)

        # Syncing files
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_dir, file)
            # Only updating if a file is missing or modified
            if not os.path.exists(replica_file) or os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                shutil.copy2(src=source_file, dst=replica_file)
                print(f"-- FILE: {source_file} copied as {replica_file}")


    ### Removing extra files and folders from the replica
    for root, dirs, files in os.walk(replica_path):
        replica_relative_path = os.path.relpath(root, replica_path)
        source_dir = os.path.join(source_path, replica_relative_path)

        # Removing directories that are not present in source
        for dir in dirs:
            replica_subdir = os.path.join(root, dir)
            source_subdir = os.path.join(source_dir, dir)
            
            if not os.path.exists(source_subdir):
                shutil.rmtree(replica_subdir)
                print(f"** Deleted extra directory: {replica_subdir}")
                
        # Removing files that are not present in source
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_dir, file)
            
            if not os.path.exists(source_file):
                os.remove(replica_file)
                print(f"** Deleted extra file: {replica_file}")






if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("--source_path", type=str, help="Path to the source folder")
    parser.add_argument("--replica_path", type=str, help="Path to the replica folder")
    parser.add_argument("--interval", type=int, default=300, help="Sync interval in seconds (default: 300)")
    parser.add_argument("--log_file", type=str, default="./logs/sync_logging", help="Path to the log file")

    args = parser.parse_args()

    source_path = args.source_path
    replica_path = args.replica_path
    sync_folders(source_path, replica_path)