import os
import zipfile
from datetime import datetime

def create_submission():
    # List of files to include in the submission
    files_to_include = [
        'Robot.py',
        'sample_path.py',
        'calculated_path.npy',
        'ground_truth_path.npy',
        'sample_path_plot.png'  # Assuming the student saved their plot with this name
    ]

    # Create a timestamp for the zip file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"ex_01_submission_{timestamp}.zip"

    # Create a zip file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to the submission zip.")
            else:
                print(f"Warning: {file} not found and not included in the submission.")

    print(f"\nSubmission zip created: {zip_filename}")
    print("Please upload this file to Gradescope.")

if __name__ == "__main__":
    create_submission()