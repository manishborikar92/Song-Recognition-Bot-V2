from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate and create a PyDrive client
def authenticate_pydrive():
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile("utils/mycreds.txt")

    # If the credentials don't exist, perform the authentication flow
    if not gauth.credentials:
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    elif gauth.access_token_expired:
        gauth.Refresh()  # Refreshes the expired token
    else:
        gauth.Authorize()

    # Save the credentials for the next run
    gauth.SaveCredentialsFile("utils/mycreds.txt")
    
    # Create GoogleDrive instance with authenticated GoogleAuth instance
    drive = GoogleDrive(gauth)
    return drive

# Create a folder on Google Drive  
def create_folder(drive, folder_name, parent_folder_id=None):  
    folder_metadata = {  
        'title': folder_name,  
        'mimeType': 'application/vnd.google-apps.folder'  
    }  

    if parent_folder_id:  
        folder_metadata['parents'] = [{'id': parent_folder_id}]  
    
    folder = drive.CreateFile(folder_metadata)  
    folder.Upload()  
    print(f"Folder '{folder_name}' created with ID: {folder['id']}")  
    return folder['id']  

# Find or create a folder hierarchy  
def get_or_create_folder(drive, folder_path):  
    folder_ids = {}  
    
    # Split the folder path into components  
    folders = folder_path.split('/')  
    
    # Start searching from the root folder  
    parent_id = None  

    for folder in folders:  
        # Check if the folder already exists  
        folder_list = drive.ListFile({  
            'q': f"title = '{folder}' and mimeType = 'application/vnd.google-apps.folder'" +   
                  (f" and '{parent_id}' in parents" if parent_id else "")  
        }).GetList()  

        if folder_list:  
            # Get the existing folder ID  
            folder_id = folder_list[0]['id']  
            print(f"Folder '{folder}' found with ID: {folder_id}")  
        else:  
            # Create the folder if it doesn't exist  
            folder_id = create_folder(drive, folder, parent_folder_id=parent_id)  

        # Update the parent ID for the next iteration  
        parent_id = folder_id  
        folder_ids[folder] = folder_id  

    return parent_id  # Return the ID of the last created folder  

# Search for a file in a specific folder (Google Drive)
def search_file(drive, folder_name, file_name):
    # Find the folder first
    folder_list = drive.ListFile({'q': f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"}).GetList()

    if folder_list:
        folder_id = folder_list[0]['id']  # Get the folder ID
        print(f"Folder '{folder_name}' found with ID: {folder_id}")

        # Now search for the file inside the folder
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and title = '{file_name}'"}).GetList()
        
        if file_list:
            file = file_list[0]
            print(f"File '{file_name}' found in Drive with ID: {file['id']}")
            return file  # Return file metadata
        else:
            print(f"File '{file_name}' not found in folder '{folder_name}' on Google Drive.")
            return None
    else:
        print(f"Folder '{folder_name}' not found on Google Drive.")
        return None

# Upload a file to a specific folder on Google Drive  
def upload_file_to_folder(drive, local_file_path, folder_path):  
    # Get or create the folder hierarchy  
    folder_id = get_or_create_folder(drive, folder_path)  

    # Create the file object in the folder  
    file_drive = drive.CreateFile({  
        'title': os.path.basename(local_file_path),   
        'parents': [{'id': folder_id}]  
    })  
    file_drive.SetContentFile(local_file_path)  
    file_drive.Upload()  

    print(f"File '{local_file_path}' uploaded to Google Drive folder '{folder_path}'")  

# Example usage
def main():
    drive = authenticate_pydrive()

    # Upload a file to the 'data/videos' folder on Google Drive
    upload_file_to_folder(drive, 'data/videos/DDwxNkCzf8u.mp4', 'data/videos')

    # Search for a file in the 'data/videos' folder
    file = search_file(drive, 'data/videos', 'DDwxNkCzf8u.mp4')
    
    if file:
        # Do something with the file (e.g., return file ID or URL)
        print(f"File ID: {file['id']}")
        print(f"Download URL: {file['alternateLink']}")

if __name__ == "__main__":
    main()