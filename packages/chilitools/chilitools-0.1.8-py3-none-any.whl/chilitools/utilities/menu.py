import re
import pyperclip as pc
from chilitools.utilities.backoffice import backofficeURLInput
from chilitools.api.connector import ChiliConnector
from chilitools.api.mycp import generateLoginTokenForURL, generateOAuthTokenFromCredentials

def getChili():
    url = backofficeURLInput()
    return ChiliConnector(backofficeURL=url)

def run():
  while (True):

    print("CHILI Publish Testing Tools")
    print("--------------------------\n\n")
    print("1) Generate Login Token for BackOffice URL")
    print("2) Get API Key for BackOffice URL")
    print("3) Generate Login Token for ft-nostress")
    print("4) Generate Login Token for ft-nostress-sandbox")
    print("5) Generate Chili-Publish OAuth Bearer Token")


    option = input()

    if re.search("[0-6]", option):
      option = int(option)

      match option:
        case 1:
          chili = getChili()
          token = generateLoginTokenForURL(backofficeURL=chili.backofficeURL)
          pc.copy(token)
          print(token)
        case 2:
          chili = getChili()
          key = chili.getAPIKey()
          pc.copy(key)
          print(key)
        case 3:
          chili = ChiliConnector(backofficeURL='https://ft-nostress.chili-publish.online/ft-nostress/interface.aspx')
          token = generateLoginTokenForURL(backofficeURL=chili.backofficeURL)
          pc.copy(token)
          print(token)
        case 4:
          chili = ChiliConnector(backofficeURL='https://ft-nostress.chili-publish-sandbox.online/ft-nostress/interface.aspx')
          token = generateLoginTokenForURL(backofficeURL=chili.backofficeURL)
          pc.copy(token)
          print(token)
        case 5:
          print(generateOAuthTokenFromCredentials())

    else:
      print("That is not a valid option, please try again")

