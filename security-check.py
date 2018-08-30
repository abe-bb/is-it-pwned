#!/usr/bin/env python3

import urllib.request
import argparse
import getpass
import hashlib
import json
import urllib.error
import re

# parse arguments and perform argument error checking. Returns clean arguments
def parseArgs():
    parser = argparse.ArgumentParser(description="A program to securely check an email address, password, or sha1 sum "
                                                 "against database of known data leaks and available passwords from"
                                                 "around the web. When called with no optional arguments, defaults"
                                                 "to checking email addresses. Uses the haveibeenpwned.com database"
                                                 "and uses the range API request for security.")
    parser.add_argument("emailOrHash", nargs='?', help="The input, either sha1 sum, or email. Default: email")
    parser.add_argument("-s", "--sha1", help="Treat given input as sha1 sum and check accordingly",
                        action="store_true")
    parser.add_argument("-p", "--password", help="Prompt for password, hash it, and securely check if it has been aquired"
                                                 " in any known attacks", action="store_true")
    args = parser.parse_args()

    # Sha1 error Checking
    if args.sha1 and not args.emailOrHash is None:
        invalidCharacters = re.compile('[g-zG-Z]')
        if invalidCharacters.match(args.emailOrHash):
            print("Not a valid sha1 hash.")
            print("Is it in hexadecimal?")
            exit(1)
        elif len(args.emailOrHash) != 40:
            print("Not a valid sha1 hash")
            exit(1)

    # Basic email address error checking
    elif not args.password:
        if args.emailOrHash is None:
            print("No input given\n Nothing to do...")
            exit(1)
        elif not ("@" in args.emailOrHash):
            print("Invalid email address")
            exit(1)
    return args


# Prompts user for password and returns the SHA1 sum of it
def hashPassword():
    password = getpass.getpass().encode("utf-8")
    rePassword = getpass.getpass(prompt="Enter password again: ").encode("utf-8")
    if password != rePassword:
        print("Passwords do not match...")
        exit(1)
    toHash = hashlib.sha1()
    toHash.update(password)
    passwordHash = toHash.hexdigest()
    return passwordHash.lower()

#     Takes a string, calls the haveibeenpwned hash range search, interprets it, and returns a list of lines to be
# printed
def makeHashAPICall(hash):
    linesToPrint = []
    found = 0
    request = urllib.request.Request("https://api.pwnedpasswords.com/range/" + hash[:5], data=None,
                                     headers={"User-Agent": "Python-Pwnage_check-for-friends-and-fami https://github.com/abramjc/is-it-pwned"})
    response = urllib.request.urlopen(request)
    bodytext = response.read().decode()
    listOfLines = bodytext.split('\r\n')
    # tuples contain two elements ('returned sha1', 'number of times seen')
    listOfTuples = [tuple(x.lower().split(':')) for x in listOfLines]
    for i in listOfTuples:
        if i[0] == hash[5:]:
            found = int(i[1])
            break

    if found > 0:
        if found == 1:
            linesToPrint = ["\nWARNING", "THIS PASSWORD HAS BEEN EXPOSED IN A SECURITY BREACH.",
                            "It probably shouldn't be used"]
        else:
            linesToPrint = ["\nWARNING", "THIS PASSWORD HAS BEEN SEEN IN " + str(found) + " SECURITY BREACHES",
                            "It probably shouldn't be used"]
    else:
        linesToPrint = ["\nNo breaches found :)", "Always be smart with your passwords"]

    return linesToPrint

#     Takes a string, calls the haveibeenpwned api, interprets it and returns a list of lines to printed
def makeEmailAPICall(userInput):
    linesToPrint = []
    request = urllib.request.Request("https://haveibeenpwned.com/api/v2/breachedaccount/" + userInput + "?truncateResponse=true&includeUnverified=true", data=None,
                                     headers={"User-Agent": "Python-Pwnage_check-for-friends-and-fam https://github.com/abramjc/is-it-pwned"})
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            linesToPrint.append("Too many requests too fast. Please wait a few seconds and try again.")
            exit(1)
        elif e.code == 404:
            linesToPrint.append("\nCongratulations!!")
            linesToPrint.append("No security breaches associated with your email address were found  :):)")
            return linesToPrint
        else:
            raise e
    bodytext = json.loads(response.read().decode('utf-8'))

    # This try/except block makes the validEmail api call and interprets the response
    if len(bodytext) == 1:
        linesToPrint.append("\nWARNING")
        linesToPrint.append("There is one known security breach associated with this email address.")
        linesToPrint.append("If this is news to you, you should probably change and check your passwords\n")
        linesToPrint.append("Your account is associated with the following breached site:")
        linesToPrint.append(bodytext[0]["Name"])
    else:
        linesToPrint.append("\nWARNING")
        linesToPrint.append("There are " + str(len(bodytext)) + " known security breaches associated with this email address.")
        linesToPrint.append("If this is news to you, you should probably change and check your passwords\n")
        linesToPrint.append("Your account is associated with the following breached sites:")
        for i in bodytext:
            linesToPrint.append(i["Name"])


    return linesToPrint



def main():
    args = parseArgs()
    # this if group assigns either passHash or valid email as needed.
    if args.password:
        passHash = hashPassword()
    elif args.sha1:
        passHash = args.emailOrHash
    else:
        validEmail = args.emailOrHash

    if args.password or args.sha1:
        linesToPrint = makeHashAPICall(passHash)
    else:
        linesToPrint = makeEmailAPICall(validEmail)

    for i in linesToPrint:
        print(i)



main()

exit(0)
