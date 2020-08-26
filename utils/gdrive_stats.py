from __future__ import print_function
from google.oauth2 import service_account

# utils I have written
from utils.gsuite_auth import auth
from utils.gsuite_util import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group',
          'https://www.googleapis.com/auth/admin.directory.user',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

SHEET = '1cdG9c_o_WU-hH8JeJpsiAXwVkw2-1EGyAtlvAy3Zsc8'

def main():
    creds = auth(SCOPES)
    drive_access(creds)
    group_membership(creds)

#================== GOOGLE DRIVE FUNCTIONS ==================#


def group_membership(creds):
    keys = []
    master_list = list_users(creds)
    service = build('admin', 'directory_v1', credentials=creds)
    results = service.groups().list(customer='my_customer', maxResults=200,
                                orderBy='email').execute()

    groups = results.get('groups', [])

    if not groups:
        pass
    else:
        for group in groups:
            master_list[0].append(group['name'])
            keys.append(group['id'])

    for key in keys:
        results = service.members().list(groupKey=key).execute()
        members_list = {}
        if 'members' in results:
            members = results['members']
            for i in members:
                members_list[i['email']] = i['role']
            for i in master_list:
                if i[1] in members_list:
                    i.append(members_list[i[1]])
                else:
                    if i[0] != 'name':
                        i.append('')
        else:
            for i in master_list:
                i.append('')
    archive(master_list=master_list, sheet=SHEET, sheet_range='G Suite Group Membership!A1:AZ', creds=creds)


def drive_access(creds):
    master_list = list_users(creds)
    keys = []

    service = build('drive', 'v3', credentials=creds)

    result = service.drives().list(
        pageSize=100, useDomainAdminAccess=True
    ).execute()
    drives = result['drives']

    if not drives:
        pass
    else:
        for drive in drives:
            master_list[0].append(drive['name'])
            keys.append(drive['id'])
    len0 = len(master_list[0])
    for i in master_list:
        if i[0] == 'name':
            continue
        x = [''] * (len0-1)
        i += x

    for person in master_list:
        if person[0] == 'name':
            continue
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = 'sa.json'

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        delegated_credentials = credentials.with_subject(person[1])

        service = build('drive', 'v3', credentials=delegated_credentials)
        result = service.drives().list(pageSize=100).execute()
        drives = result['drives']

        if not drives:
            pass
        else:
            for drive in drives:
                if drive['name'] in master_list[0]:
                    i = master_list[0].index(drive['name'])
                    person[i] = 'HAS ACCESS'

    archive(master_list=master_list, sheet=SHEET, sheet_range='Drives Access!A1:DZ', creds=creds)

if __name__ == '__main__':
    main()