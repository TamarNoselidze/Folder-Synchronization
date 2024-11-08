import argparse
import os
import shutil
import sched
import time
import hashlib


def file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f: # opening the file in binary read mode
        buf = f.read() # reading the entire file into memory
        hasher.update(buf)
    return hasher.hexdigest()


def sync_folders(source_path, replica_path, log):
    try: 
        message = f"{'-'*30} Starting synchronization {'-'*30}"
        print(message)
        log.write(message+"\n")
        log.flush()  # Ensure real-time logging

        ### First we check if the replica dir exists, if not, we create it
        if not os.path.exists(replica_path):
            os.makedirs(replica_path)
            message = f"Replica directory doesn't exist at: {replica_path} so we are creating it."
            print(message)
            log.write(message+"\n")
            log.flush()

        ### Adding missing elements to the replica folder
        for root, dirs, files in os.walk(source_path):
            # Relative path of the current root to the source directory
            source_relative_path = os.path.relpath(root, source_path)


            # Add the current 'root' directory if it's missing
            replica_dir = os.path.join(replica_path, source_relative_path)
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)
                message = f"{root} copied to replica folder: {replica_dir}"
                print(message)
                log.write(message+ "\n")
                log.flush()

            # Syncing files
            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_dir, file)
                # Only updating if a file is missing or modified
                if not os.path.exists(replica_file) or file_hash(source_file) != file_hash(replica_file):
                    message = f"{source_file} copied to: {replica_file}"
                    shutil.copy2(src=source_file, dst=replica_file)
                    print(message)
                    log.write(message+"\n")
                    log.flush()

        
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
                    message = f"Deleted extra directory: {replica_subdir}"
                    print(message)
                    log.write(message+"\n")
                    log.flush()

                    
            # Removing files that are not present in source
            for file in files:
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_dir, file)
                
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    message = f"Deleted extra file: {replica_file}"
                    print(message)
                    log.write(message+"\n")
                    log.flush()

        message = f"{'-'*31} Ending synchronization {'-'*31}\n\n"
        print(message)
        log.write(message+"\n")
        log.flush()
        
    except Exception as e:
        print(f"Error during synchronization: {e}")


def schedule_sync(sc, source_path, replica_path, log_file, interval):
    sync_folders(source_path, replica_path, log_file)
    # Reschedule synchronization every interval seconds
    sc.enter(interval, 1, schedule_sync, (sc, source_path, replica_path, log_file, interval))



if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("--source_path", type=str, help="Path to the source folder")
    parser.add_argument("--replica_path", type=str, help="Path to the replica folder")
    parser.add_argument("--interval", type=int, default=10, help="Sync interval in seconds (default: 10)")
    parser.add_argument("--log_file", type=str, default="./logs/sync_logging", help="Path to the log file")

    args = parser.parse_args()

    source_path = args.source_path
    if os.path.exists(source_path):

        replica_path = args.replica_path
        interval = args.interval
        log_file_path = args.log_file
        with open(log_file_path, "w") as log_file:
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(interval, 1, schedule_sync, (scheduler, source_path, replica_path, log_file, interval))
            scheduler.run()
            # sync_folders(source_path, replica_path, log_file_path)
    else:
        print(f'Source folder "{source_path}" does not exist. Please, provide a valid path.')
 

