from chilitools.utilities.errors import ErrorHandler

def isValidBackofficeURL(backofficeURL: str) -> bool:
    try:
        backoffice = splitURL(url=backofficeURL)
        if backoffice[-1].lower() != 'interface.aspx':
            return False
        return True
    except:
        return False

def splitURL(url: str) -> dict:
    return url.strip().split('/')

def getBaseURL(backofficeURL: str) -> str:
    if isValidBackofficeURL(backofficeURL=backofficeURL):
        return splitURL(url=backofficeURL)[2]
    return ErrorHandler().getError('INVALIDBACKOFFICEURL')

def getEnviormentName(backofficeURL: str) -> str:
    if isValidBackofficeURL(backofficeURL=backofficeURL):
        if backofficeURLType(backofficeURL=backofficeURL) != 'saas':
            return splitURL(url=backofficeURL)[4]
        else:
            return splitURL(url=backofficeURL)[3]
    return ErrorHandler().getError('INVALIDBACKOFFICEURL')

def getRequestURL(backofficeURL: str) -> str:
    if isValidBackofficeURL(backofficeURL=backofficeURL):
        baseURL = getBaseURL(backofficeURL=backofficeURL)
        urlType = backofficeURLType(backofficeURL=backofficeURL)
        if urlType != 'saas':
            return splitURL(url=backofficeURL)[0] + "//" + baseURL + "/"+ urlType + "//rest-api/v1.1/"
        return "https://" + baseURL + "/rest-api/v1/"
    return ErrorHandler().getError('INVALIDBACKOFFICEURL')

def backofficeURLType(backofficeURL: str) -> str:
    backoffice = splitURL(url=backofficeURL)

    if len(backoffice) == 6:
        return backoffice[3]
    else:
        return 'saas'

def backofficeURLInput(backofficeURL: str = None) -> str:
    if backofficeURL == None:
        backofficeURL = ""

    while isValidBackofficeURL(backofficeURL=backofficeURL) != True:
        print("Please enter the URL for the BackOffice you would like an API key for (it should end with '/interface.aspx'): ")
        backofficeURL = input()

    return backofficeURL