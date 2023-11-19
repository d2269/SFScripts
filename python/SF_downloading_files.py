import os
import logging
import requests
from simple_salesforce import Salesforce

logging.basicConfig(filename='file_download_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

file_path = '' # Specify the file path; the file contains the record parameters "<SF_ACCOUNT_ID>:<ContentVersion ID>". For downloading, "<ContentVersion ID>" will be used.
base_save_path = '' # Please specify the directory where to save the files.
def ar_from_file(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line:
                lines.append(line.strip().split(':'))
    return lines

my_instance_url = ''
my_session_id = '' # session id -- Access Token

sf = Salesforce(instance_url=my_instance_url, session_id=my_session_id)

file_info_list = ar_from_file(file_path)
for i, (dir_name, file_id) in enumerate(file_info_list, start=1):
    try:
        print(f"{i} from {len(file_info_list)}: {file_id} START")

        specific_save_path = os.path.join(base_save_path, f"{dir_name}-{file_id}")
        if not os.path.exists(specific_save_path):
            os.makedirs(specific_save_path)

        # get info about the file
        file_info = sf.ContentVersion.get(file_id)
        download_url = file_info['VersionDataUrl']
        
        # download file
        file_content = requests.get(download_url, headers=sf.headers).content

        # save file
        file_name = file_info['Title'].replace('/', '_')
        #file_save_path = os.path.join(specific_save_path, file_info['PathOnClient']) # for PathOnClient
        file_save_path = os.path.join(specific_save_path, file_info['Title']) # for Title
        with open(file_save_path, 'wb') as file:
            file.write(file_content)

        print(f"File {file_info['Title']} saved to {file_save_path}.")
        print(f"{i} from {len(file_info_list)}: {file_id} -- DONE")
    except Exception as e:
        print(f"Error with file {file_id}: {e}")
        logging.error(f"Error with file {file_id}: {e}")

