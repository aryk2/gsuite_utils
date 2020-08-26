from utils.gsuite_auth import auth
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/admin.directory.group']


def main():
    creds = auth(SCOPES)
    add_drive_user('x_intel', creds, 'akempler-delugach@ignw.io')


def add_drive_user(drive_name, creds, user_email):
    q = "name contains '" + drive_name + "'"
    service = build('drive', 'v3', credentials=creds)

    result = service.drives().list(
        q=q, pageSize=100, useDomainAdminAccess=True
    ).execute()
    drives = result['drives']
    for drive in drives:
        correct = input("add user to " + drive['name'] + " ? y/n:")
        if correct == 'y':
            drive_id = drive['id']
            service = build('drive', 'v3', credentials=creds)
            print(drive_id)
            result = service.permissions().create(
                fileId=drive_id, supportsAllDrives=True, useDomainAdminAccess=True,
                body={"role": "writer", "type": "user", "emailAddress": user_email}
            ).execute()

            break


if __name__ == '__main__':
    main()
