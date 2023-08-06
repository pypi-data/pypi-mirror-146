import requests
import json
from Settings.config import LOGIN_FILE, STAFF_OAUTH_LOGIN
from Utilities.File import checkForFile, readFile, writeFile

def generateOAuthTokenFromCredentials() -> str:
  if STAFF_OAUTH_LOGIN:
    if checkForFile(fileName=LOGIN_FILE):
      login = json.loads(readFile(LOGIN_FILE))
    else:
      print("Please enter your MyCP username")
      username = input().strip()
      print("Please enter your MyCP password")
      password = input().strip()
      login = {'Username': username, 'Password': password}
      print("Would you like to store these credentials for later use? (y/n)")
      storeLogin = input().strip().lower()
      if storeLogin == 'y' or storeLogin == 'yes':
        writeFile(fileName=LOGIN_FILE, data=json.dumps(login))

    requestURL = "https://my.chili-publish.com/api/v1/auth/login"

    requestHeaders = {
        "Content-Type":"application/json",
        "accept": "*/*"
    }

    response = requests.post(url=requestURL, headers=requestHeaders, json=login)

    if response.status_code != 200:
        return f"There was an error generating an OAuth Bearer Token. Status Code: {response.status_code}. Text: {response.text}"
    else:
        return response.json()['token']
  return "This method uses Azure AD OAuth login and is reserved for CHILI Staff"

def generateLoginTokenForURL(backofficeURL: str) -> str:
  if STAFF_OAUTH_LOGIN:
    requestURL = "https://my.chili-publish.com/api/v1/backoffice/generate"

    requestHeaders = {
        "Content-Type":"application/json",
        "accept": "application/json",
        "Authorization": "Bearer " + generateOAuthTokenFromCredentials()
    }

    requestJSON = {
        "Url":backofficeURL
    }

    response = requests.post(url=requestURL, headers=requestHeaders, json=requestJSON)

    if response.status_code != 200:
        return f"There was an error generating an login token. Status Code: {response.status_code}. Text: {response.text}"
    else:
        return response.json()['token']
  return "This method uses Azure AD OAuth login and is reserved for CHILI Staff"

