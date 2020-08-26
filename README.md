#### About

This repo contains python scripts that have helped with some assorted G Suite tasks. 

The utils/gsuite_auth.py file contains one of two auth functions provided by google. This uses the credentials.json 
file that is not provided in this repo. This file can be made in the [Google Developers Console](https://console.developers.google.com/).
For some the admin tasks, domain wide delegation is needed. To get this permission, go to the credentials
tab in the console, click create credentials, oauth client id. You may have to set up an OAuth consent screen. 
This part was annoying and I don't think you ever use it for these cli scripts. Once you have that set up, 
continue creating the OAuth client ID and select Desktop app for the application type. Give it a name and copy the 
Client ID it provides. Find it in the credentials tab of the console and click the download icon. Rename the file 
to credentials.json and put it in the root of this dir. 

This is the part that I always forget to do: You need to create a service account and enable domain wide 
delegation. In the Developers Console credentials tab, create a service account, give it a name and leave everything
else blank. Once it has been created, click on it in the credentials tab. Expand the Show Domain-wide Delegation
expander and check the allow checkbox. Click add key, create key, JSON, and move the downloaded file to the root 
of this dir and rename it sa.json. Go into the [G Suite Admin Console](https://admin.google.com/) and click 
security. Scroll down to Advanced Setting, click that, then click Manage domain wide delegation. Click Add new, 
paste in the Unique ID from the service account and enter all the scopes. The scopes needed are found in each file. 
These are not exactly the scopes at the topof the file, rather the scopes found in the functions that use
delegated credentials. Maybe I should move these to a central place.



more info is on the way