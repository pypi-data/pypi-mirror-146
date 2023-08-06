[Documentation](https://jameskabbes.github.io/user_profile)

# user_profile
Provides the framework for storing a unique profile for individuals and Python environments. Each user profile has a unique set of attributes and methods, much like a Python class instance.

# Project Description
When importing your profile from a unique location on your computer, you have access to unique attributes and methods to this profile. This allows us to call

```
user_profile.profile.name
user_profile.profile.say_hi()
```

# How does it work?
Let's take the following code block:
```
import user_profile
profile = user_profile.profile
```
The first two lines of code import the user's unique profile. It is stored on the user's local laptop, SageMaker instance, or wherever else their code is stored. It utilizes the "USER" environment variable on your machine.
Specifically, it is found at the path ./user_profile/Users/"USER".py. This Python script is imported as a module and stored in the variable "profile"

```
print (profile.first_name)
print (profile.last_name)
user_profile.say_hi()
```
These next lines access attributes and methods of the imported Python Class, `profile`. The first two lines print off the attributes `first_name` and `last_name` stored in the given user's profile module.
The last line runs a module method `say_hi()`.

These attributes and methods can be different for every single user. This opens the door for several cool applications from a team development perspective.

# Why does this exist?
This repository allows for multiple users to run the same code while achieving different results.

Imagine you need to access a Database using an encrypted password.
```
encryped_password = 'ASDF1234'
database.access( encryped_password )
```

Each person that runs this Python script has a different value for their unique encrypted password. Not everyone's password is going to be `ASDF1234`. Instead of typing out one password that will only work for you, utilize the following:
```
# My Profile

first_name = 'James'
last_name = 'Kabbes'
encryped_password_path = 'C:/Users/e150445/Documents/Passwords/encrypted_password.txt'
```
```
# My Co-worker's Profile

first_name = 'Michael'
last_name = 'Scott'
encryped_password_path = 'C:/Users/e94586/Documents/Passwords/mikes_password.txt'
```
```
encrypted_password = read_text_file( profile.encryped_password_path )
database.access( encrypted_password )
```

This block instead reads information from a text file stored in a path on your computer. Each user running this script will have a different value for `encrypted_password_path`. Using the user profile to store your unique `encrypted_password_path` allows each team member to run this same block of code without any issues.


# Author(s)
James Kabbes - Data Scientist: Ameren Innovation Center
