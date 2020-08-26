from googleapiclient.discovery import build

#====================== HELPER FUNCTIONS ======================#


def list_users(creds):
    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    user_results = service.users().list(customer='my_customer', maxResults=200,
                                        orderBy='email').execute()

    users = user_results.get('users', [])

    master_list = [['name', 'Email']]

    if not users:
        pass
    else:
        for user in users:
            master_list.append([user['name']['fullName'], user['primaryEmail']])
    return master_list


def archive(master_list, sheet, sheet_range, creds):
    service = build('sheets', 'v4', credentials=creds)

    body = {
        'values': master_list
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=sheet, range=sheet_range,
        valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

