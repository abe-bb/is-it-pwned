#!/usr/bin/env python3

import urllib.request
import argparse



def parseArgs():
    parser = argparse.ArgumentParser(description="A program to securely check an email address, password, or sha1 sum "
                                                 "againsta database of known data leaks and available passwords from"
                                                 "around the web. When called with no optional arguments, defaults"
                                                 "to checking email addresses.")
    parser.add_argument("stringToCheck", help="The input, whether password, sha1 sum, or email. Default: email")
    parser.add_argument("-s", "--sha1", help="Treat given input as sha1 sum and check accordingly",
                        action="store_true")
    parser.add_argument("-p", "--password", help="")
    args = parser.parse_args()
    return args




def hashPassword():
    pass


def main():
    args = parseArgs()

main()