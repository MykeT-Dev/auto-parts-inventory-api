import os
import shutil
import kagglehub
from dotenv import load_dotenv

load_dotenv()

def get_and_organize_data():
    # 1. Download from Kaggle
    download_path = kagglehub.dataset_download("qubdidata/auto-parts-dataset")
    
    # 2. Define our local 'data_raw' folder
    local_data_folder = "data_raw"
    
    # 3. Create the folder if it doesn't exist
    if not os.path.exists(local_data_folder):
        os.makedirs(local_data_folder)
        print(f"Created folder: {local_data_folder}")

    # 4. Copy files from the cache to our project folder
    for filename in os.listdir(download_path):
        source = os.path.join(download_path, filename)
        destination = os.path.join(local_data_folder, filename)
        
        # Only copy files (not subfolders)
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print(f"Copied: {filename}")

    print(f"\n✅ All set! Files are now in your project folder: /{local_data_folder}")

if __name__ == "__main__":
    get_and_organize_data()