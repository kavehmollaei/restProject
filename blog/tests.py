import time

def delete_folder_contents(folder_path):
    try:
        # Delete all files and subdirectories in the folder
        import os
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        
        # Create the folder again
        os.makedirs(folder_path)
        
        print("Folder contents deleted successfully.")
    except Exception as e:
        print("Error deleting folder contents:", str(e))

# Replace 'folder_path' with the path to your folder
folder_path = '/home/kaveh/Downloads'

# Schedule the deletion to run every 24 hours
while True:
    delete_folder_contents(folder_path)
    time.sleep(24 * 60 * 60)  # Sleep for 24 hours