# security-check

A python script for interacting with the https://haveibeenpwned.com API.
Run it with an email address as an argument and it will 
check for known breaches involving that email address.

Specify -p and it will prompt you to enter a password. 
The password is never saved, but securely checked against 
a database of known passwords. 

This script is pretty much just a front end to the 
https://haveibeenpwned.com api. All the heavy lifting 
was already done over there, so check them out.


## Running it

Just download the script, make it executable and run it. 


## Security

Passwords are hashed, then the first 5 digits of the 
hash are sent to the haveibeenpwned api, which will 
return all hashes that start with those 5 digits in their 
known exposed passwords database. The returned list is then 
locally searched to see if the remaining 35 characters match 
any known exposed passwords. The password is never sent over 
the internet. Only the first five digits of the hash are 
sent over the internet, make it impossible to recover the 
password by intercepting the api requests. Neither the 
password, nor the password hash are saved locally. 


## Arguments

Specify email address as first argument to check for 
security breaches associated with accounts tied to that email address.

-h prints a help summary.

Specifying -p or --password will prompt for a password.

Use -s or --sha1 when you want to hash the password yourself. Just make sure a valid sha1 hash is passed to the program.

