from __future__ import print_function
from google.oauth2 import service_account

# utils I have written
from utils.gsuite_auth import auth
from utils.gsuite_util import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group',
          'https://www.googleapis.com/auth/admin.directory.user',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/gmail.labels']

SHEET = '1KzrNHxw75FwLiXJTblG9QuYbutERDcNvn0xcGEJsISE'

def main():
    creds = auth(SCOPES)
    master_list = list_users(creds)
    result_list = []

    for person in master_list:
        person = person + messagesTotal(userId=person[1])
        person.append(labels(userId=person[1]))
        person.append(autoForwarding(userId=person[1]))
        result_list.append(person)
        print(person)

    archive(result_list, SHEET, 'mailbox!A1:AZ', creds)


# ====================== GMAIL API FUNCTIONS ======================#

def messagesTotal(userId):
    if userId == 'Email':
        return ['primarySMTPAddress', 'messagesTotal']
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    SERVICE_ACCOUNT_FILE = '../sa.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    delegated_credentials = credentials.with_subject(userId)

    service = build('gmail', 'v1', credentials=delegated_credentials)
    # Call the Gmail API
    results = service.users().getProfile(userId='me').execute()
    return [results['emailAddress'], results['messagesTotal']]

def labels(userId):
    if userId == 'Email':
        return 'labels'
    SCOPES = ['https://www.googleapis.com/auth/gmail.labels']
    SERVICE_ACCOUNT_FILE = '../sa.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    delegated_credentials = credentials.with_subject(userId)

    service = build('gmail', 'v1', credentials=delegated_credentials)
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()

    return len(results.get('labels', []))



def autoForwarding(userId):

    if userId == 'Email':
        return 'autoForwardingEnabled'
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    SERVICE_ACCOUNT_FILE = '../sa.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    delegated_credentials = credentials.with_subject(userId)

    service = build('gmail', 'v1', credentials=delegated_credentials)
    # Call the Gmail API
    results = service.users().settings().getAutoForwarding(userId='me').execute()

    return results['enabled']



if __name__ == '__main__':
    main()