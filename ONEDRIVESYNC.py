import requests
import msal
import io
import pandas as pd

# Azure app details (replace with your actual details)
client_id = 'd3158ba8-831f-45da-a9fc-c135d4b5645c'
client_secret = 'AKu8Q~AiFIQu_cqGHb33DjXRqMDf1j0TbRydMdiC'
tenant_id = '2aaedeef-ef86-4ec4-a0b5-f2821c5448b6'

# Authentication URL and scope
scopes = ['https://graph.microsoft.com/.default']
auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

# MSAL - Microsoft Authentication Library
app = msal.ConfidentialClientApplication(client_id, authority=f"https://login.microsoftonline.com/{tenant_id}", client_credential=client_secret)

# Get the access token
result = app.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    access_token = result["access_token"]
    print("Access Token obtained")
else:
    print("Error getting access token:", result.get("error_description"))
    exit()

# Function to get the Excel file content from OneDrive
def get_file_content(file_id, access_token):
    url = f'https//graph.microsoft.com/v1.0/users/arthurfprodc@outlook.com/items/{file_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return io.BytesIO(response.content)  # Return the content as a byte stream
    else:
        print(f"Error fetching file: {response.text}")
        return None

# Function to upload the Excel file content to OneDrive
def upload_file_content(file_id, access_token, file_content):
    url = f'https//graph.microsoft.com/v1.0/users/arthurfprodc@outlook.com/items/{file_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    response = requests.put(url, headers=headers, data=file_content)
    
    if response.status_code == 200:
        print("File uploaded successfully!")
    else:
        print(f"Error uploading file: {response.text}")

# Function to sync data from one file to another
def sync_sheets(source_file_id, dest_file_id, access_token):
    # Step 1: Download the source file content from OneDrive
    source_file_content = get_file_content(source_file_id, access_token)
    
    if source_file_content:
        # Step 2: Read the source Excel file into a DataFrame
        source_df = pd.read_excel(source_file_content)
        print("Source DataFrame:\n", source_df)

        # Step 3: Download the destination file content
        dest_file_content = get_file_content(dest_file_id, access_token)
        
        if dest_file_content:
            # Step 4: Read the destination Excel file into a DataFrame
            dest_df = pd.read_excel(dest_file_content)
            print("Destination DataFrame before sync:\n", dest_df)

            # Step 5: Append data from the source file to the destination file
            updated_df = pd.concat([dest_df, source_df], ignore_index=True)
            print("Updated DataFrame:\n", updated_df)

            # Step 6: Save the updated DataFrame to a byte stream
            updated_file_stream = io.BytesIO()
            updated_df.to_excel(updated_file_stream, index=False, sheet_name='Sheet1')
            updated_file_stream.seek(0)  # Reset the pointer to the start of the stream

            # Step 7: Upload the updated file back to OneDrive
            upload_file_content(dest_file_id, access_token, updated_file_stream)

# Sample file IDs for Source and Destination Excel Files (Replace with your actual file IDs)
source_file_id = '29b69af1-c96b-4629-8bc5-bbf802084e83'  # The ID of the source file (the one you're copying data from)
dest_file_id = '4f702869-5b97-4456-bb83-abf3600f4b94'  # The ID of the destination file (the one you're copying data to)

# Sync the source sheet to the destination sheet
sync_sheets(source_file_id, dest_file_id,access_token)
