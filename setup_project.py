import os

# Define the project structure
project_name = "financial_modeling_project"
folders = [
    "data",
    "notebooks",
    "scripts"
]

subfolders = {
    "scripts": [
        "data_retrieval",
        "data_transformation",
        "financial_forecast",
        "depreciation_schedule"
    ],
    "data": [
        "raw",  # Store raw datasets or Excel files here
        "processed"  # Store cleaned or processed versions
    ]
}

# Create the main project folder if it doesn't exist
if not os.path.exists(project_name):
    os.mkdir(project_name)

# Create each main folder and subfolders
for folder in folders:
    path = os.path.join(project_name, folder)
    if not os.path.exists(path):
        os.mkdir(path)
    # If the folder has subfolders, create them
    if folder in subfolders:
        for subfolder in subfolders[folder]:
            subfolder_path = os.path.join(path, subfolder)
            if not os.path.exists(subfolder_path):
                os.mkdir(subfolder_path)

# Create additional files
open(os.path.join(project_name, "integrate_to_excel.py"), 'a').close()
open(os.path.join(project_name, "environment_setup.md"), 'a').close()
open(os.path.join(project_name, "requirements.txt"), 'a').close()

print("Project structure created successfully.")
