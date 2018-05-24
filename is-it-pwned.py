#!/usr/bin/env python3

import urllib.request
import argparse
import getpass



def parseArgs():
    parser = argparse.ArgumentParser(description="A program to securely check an email address, password, or sha1 sum "
                                                 "against database of known data leaks and available passwords from"
                                                 "around the web. When called with no optional arguments, defaults"
                                                 "to checking email addresses. Uses the haveibeenpwned.com database"
                                                 "and uses the range API request for security.")
    parser.add_argument("stringToCheck", help="The input, whether password, sha1 sum, or email. Default: email")
    parser.add_argument("-s", "--sha1", help="Treat given input as sha1 sum and check accordingly",
                        action="store_true")
    parser.add_argument("-p", "--password", help="Prompt for password, hash it, and securely check if it has been aquired"
                                                 "in any known attacks", action="store_true")
    args = parser.parse_args()
    return args



# Prompts user for password and returns the SHA1 sum of it
def hashPassword():
    password = getpass.getpass()
    print(password)

def buildAPICall():
    pass


def main():
    args = parseArgs()
    if args.password:
        passHash = hashPassword()

main()