import os
import hashlib
import json

class FileIntegrityMonitor:
    def __init__(self, directory, hash_file):
        self.directory = directory
        self.hash_file = hash_file
        self.file_hashes = {}

    def calculate_hash(self, file_path):
        """Calculate the SHA256 hash of a file."""
        hash_func = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def load_hashes(self):
        """Load existing hashes from the hash file."""
        if os.path.exists(self.hash_file):
            try:
                with open(self.hash_file, 'r') as f:
                    self.file_hashes = json.load(f)
            except Exception as e:
                print(f"Error loading hash file {self.hash_file}: {e}")

    def save_hashes(self):
        """Save the current hashes to the hash file."""
        try:
            with open(self.hash_file, 'w') as f:
                json.dump(self.file_hashes, f, indent=4)
        except Exception as e:
            print(f"Error saving hash file {self.hash_file}: {e}")

    def scan_files(self):
    
        """Scan all files in the directory and check for changes."""
        new_hashes = {}
        for root, _, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.calculate_hash(file_path)
                if file_hash:
                    new_hashes[file_path] = file_hash

        self.compare_hashes(new_hashes)
        self.file_hashes = new_hashes
        self.save_hashes()

    def compare_hashes(self, new_hashes):
        """Compare new hashes with the previous ones and report changes."""
        for file_path, new_hash in new_hashes.items():
            old_hash = self.file_hashes.get(file_path)
            if old_hash:
                if old_hash != new_hash:
                    print(f"File modified: {file_path}")
            else:
                print(f"New file detected: {file_path}")

        for file_path in set(self.file_hashes) - set(new_hashes):
            print(f"File deleted: {file_path}")

if __name__ == "__main__":
    directory_to_monitor = input("Enter the directory to monitor: ")
    hash_storage_file = "file_hashes.json"

    monitor = FileIntegrityMonitor(directory_to_monitor, hash_storage_file)
    monitor.load_hashes()
    monitor.scan_files()
