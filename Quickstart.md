# Quickstart
No idea where to begin? This is a good place to start. This document will walk you through the most basic functionality of the program: Sending an email message to a single class list.

# Getting Ready

To begin, you will need the following items:

1. A class list file from Hokie Spa in CSV format. Do not alter the formatting of this document. You can add entries or alter existing entries, but do not change the order of columns. You can rename the file, but it must end in ".csv".

2. An email message you want to send to all of your students. Edit this in your favorite plaintext editor. You can send your message as a plaintext message or using HTML formatting.

3. A Google app password for your Gmail account. This is easy enough to generate, and it provides some additional security over using your regular Gmail password. Google provides [documentation for getting an app password](https://support.google.com/accounts/answer/185833?hl=en "App Password Documentation"). This program will not store your credentials, so please remember or keep track of your app password.

# Editing Your Email

Edit your email as you would any plaintext document. Anywhere in the message that you want the student's first name to appear, use the placeholder ${FIRST_NAME}. Use the placeholder ${FULL_NAME} for the full name instead.

You can add basic HTML markup to your message to accommodate links or other inline formatting. Remember to wrap all paragraphs in paragraph tags or else paragraphs will not appear. Use the --html flag at the command line to specify that the message contains HTML markup.

Once you are happy with your message, you can use the program to send it to the whole class. See the following walkthrough, but only use the commands if you are ready to send. See the README file if you would like to test a message first.

# Running the Program

This is a Python program. You can check if you have Python by pulling up a terminal window and typing:

```
$ python --version
```

Don't type the dollar sign ($)—that's just a conventional way of indicating that this should be typed into a terminal. If you have Python 2.x, this program should work. If you do not have Python, you will need to download it first.

You can download the program code from Github, or you can copy and paste the code into a text file and save it with a ".py" extension. The documentation assumes you are running the software as "vt-student-email.py".

You have several options for running this program:

- Using the python interpreter (easiest)

Pull up a terminal. Make sure you are in the same directory as the program. Type the following to send an email to a list:

```
$ python vt-student-email.py -s your-class-list.csv -m your-email.txt
```

- Making the script executable (pretty easy)

Pull up a terminal. Make sure you are in the same directory as the program. Type the following:

```
$ chmod +x vt-student-email.py
```
Now the script is executable without having to specify the Python interpreter. You can run it like this:

```
$ ./vt-student-email.py -s your-class-list.csv -m your-email.txt
```

- Adding the program to your class path (advanced)

There are several options for adding this to your terminal's class path, which will allow you to execute the software from whichever directory you are in. This saves you from having to keep a copy of the script in each directory you are using or constantly referencing back to wherever it is stored. You will need to find the best way to do this for your operating system and version.

# What to Expect

When the program starts, it will provide some version information. If there are issues with input files or command syntax, an error will be displayed. If everything is entered correctly, it will begin the process to send your message.

The program will prompt you for your email address. This should be your Gmail email address with the domain information included.

Ex. akulak@vt.edu

The program will then prompt you for your app password (discussed above). You can copy and paste this or enter it manually. Note that the password will not display as you type it. This is to provide security by keeping the app password from being stored in your terminal log.

Finally, the program will ask you for a subject for your message.

The program will check that you provided input for each line (all three are required). You will have an opportunity to re-enter information if it was not provided or if it isn't correct. If you entered your password incorrectly, you will get an error and need to restart the program.

If everything works, the program will start sending emails! By default, you will receive a notification for each message sent. Use the -q flag to silence this feedback. The program will exit once all messages have been sent. An error will be returned if there was an issue with any individual addresses.

# Checking on Your Messages

All sent messages will appear in your Gmail sent messages folder, so you can check for your messages there. Responses will go to your account. All this program does is handle the formatting and transmission of bulk messages—it is not a standalone email client. We all have enough of those.
