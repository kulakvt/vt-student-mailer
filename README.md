# vt-student-mailer
A simple Python command line tool for automating personalized emails to Virginia Tech student lists

# Overview
As a teacher, I often send email announcements and other class messages to my students. The email platforms I use offer limited bulk emailing options, however. Setting up a listserv or group is clunky and annoying, and copying and pasting email lists takes time and can cause privacy problems. I also don't really want to add an additional email platform to my already irritating email workflow. Enter vt-student-mailer.

vt-student-mailer takes a summary class list CSV file generated by Hokie Spa and sends a templated message to each student on the list from your Gmail account. In addition to sending individual emails to each student, you can add the student's name to the message to make it feel less like a bulk email and more like an individual note.

Does it work? The first time I used it to send an announcement addressed to individual students by name, I saw a roughly 10 percent increase in responses. I haven't done a formal study, but anecdotally this tool may help if your goal is increased engagement via email. I teach online only classes, so this is a primary goal of mine.

Because each message is an individual email, you don't have to worry about accidentally sending out an email that includes every student's email address. You also don't have to manage listservs or groups. Just download a class list from Hokie Spa, and you're good to go. You can adjust individual entries to account for preferred names or nicknames.

# Version Information

This is v. 1.0 of this tool, and it is currently being tested. I offer no warrantee on this software. You can take this and do whatever you want with it. Note that I am an English student, so use this at your own risk.

# Acknowledgement

This tool was based off of a script by [Arjun Krishna Babu](https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f "How to Send Emails Using Python"). See the original Medium post for more information about the script and how Python interacts with email messages and servers.

# System Requirements

This tool was written and tested on an Apple Macbook Pro with OS X El Capitan running Python 2.7.10. It will probably work on other machines running a version of Python 2, but your mileage may vary. Let me know if you run into any issues with compatibility.

# Getting Ready

To use this app, you will need an app password for your Gmail account. This is a fairly simple process. Google has [provided documentation](https://support.google.com/accounts/answer/185833?hl=en "App Password Documentation"). Be sure to safely store or remember your app password, as it will not be saved anywhere in the tool.

Be sure to secure your app password like you would any other password because it could be used to access your Gmail account. You can manage app passwords, and I recommend regularly resetting your app password just like you would any other password.

# Command Line Flags

This tool was designed to have a simple Unix-y interface. It requires at least a classlist file and an email template file. Optional flags allow you to send the same message to a directory of multiple classlist files and to specify HTML input if you want to include things like links and in-line formatting in your email.

## Required Parameters

- -s *classlist.csv*: S stands for single list. Use this flag to specify a single file from which to read addresses and student names. File should be a standard class list CSV from Hokie Spa. A file name must follow the -s flag.

- -m *email.txt*: M stands for message. Use this to specify the email template to send. A file name must follow the -s flag.

## Optional Parameters

- -d */path/to/lists/*: D stands for directory of lists. Use this flag to send a message to a directory containing multiple class lists. The directory should only contain class lists. Use this flag instead of -s.

- --html: Use this flag to indicate that your *email.txt* file uses HTML formatting. The default is plaintext. You will need to use this flag if your message contains links or any other HTML elements. Be sure that all paragraphs are wrapped in paragraph tags, or paragraphs will not render correctly.

- -q: Q stands for Quiet. By default, the program is verbose when sending messages. It will write one line for each email message sent. Use the -q flag to suppress this output. Errors will still print to the terminal.

## Support Options

- -t: T stands for template. Use this tag on its own. This will generate a plaintext template.txt file with an example message illustrating the use of placeholders for student names.

- -h: H stands for help. Use this tag on its own. This will print usage information and exit gracefully. Any non-supported flag should also return usage information.

- -x: X stands for eXperiment. This flag is for a testing mode, which allows you to check that your template message and your class list CSV are playing nice. It will print one email message based on your template to the terminal screen. It will use the student information from the first line in the CSV file.

# Personalizing Messages

In your *email.txt* document, you can add student names to give each message a personal touch. Currently the tool supports the following options to add student names to emails:

- ${FIRST_NAME}

Anywhere this appears in your document, the student's first given name will be substituted.

Ex: Dear ${FIRST_NAME}, -> Dear Andrew,

If more than one given name is listed, only the first name is returned. If only one name is given, then that name is returned. You can replace the first name field in the CSV with a student's preferred name. Spaces are assumed to be a delimiter.

- ${FULL_NAME}

Anywhere this appears in your document, the student's full name will be substituted.

Ex: Dear ${FULL_NAME}, -> Dear Andrew Michael Kulak,

**Note:** the dollar sign ($) is used to indicate the start of a template placeholder variable. If you need to use an actual dollar sign in your message, indicate that using two dollar signs.

Ex: $$20 -> $20

Failing to do this when using dollar signs will return an error.

# Sending your Messages

When you execute the program, you will be prompted for some additional information before your messages can be sent. You will have the opportunity to double check information and re-enter if needed. You will be asked for:

1. Your Gmail address, including the @gmaildomain.com part of the address
2. Your Gmail app password
3. A subject line for your email message

Once you provide this information, the software will start sending messages provided the email address and password information was correct and input files were properly formatted. Output will let you know as messages are being sent. They will appear in your Gmail outbox, and replies will go to your address.

# Use Cases

- vt-student-mailer.py -h

Prints usage options.

- vt-student-mailer.py -s *classlist.csv* -m *email.txt*

Sends the email in *email.txt* to everyone on *classlist.csv*. Assumes the input email message is plaintext. HTML tags will be taken literally and will not render as HTML elements.

- vt-student-mailer.py -d */path/to/lists* -m *email.txt*

Sends the email in *email.txt* to everyone on each *classlist.csv* in the specified directory. Assumes all files in the directory are properly formatted class list CSV documents.

- vt-student-mailer.py -s *classlist.csv* -m *email.txt* --html

Sends the email in *email.txt* to everyone on *classlist.csv*. Assumes the input email message is HTML and will render HTML elements like links.

- vt-student-mailer.py -t

Generates a file named example-email.txt in the current working directory demonstrating how student names can be incorporated into messages.

- vt-student-mailer.py -x -s *classlist.csv* -m *email.txt*

The -x flag indicates test mode. This will print a formatted email to your terminal to test that templating variables are entered correctly and that input files are being read accurately. No messages will be sent in test mode. The first line of the class list provided will be used for the test.

# Security

- This program does not store any information about your credentials between sessions.

- This program does not store any student information.

- Program uses getpass Python library to get Gmail app password. Password will not be displayed in your terminal, which prevents password from appearing in shell logs.

- Program uses TLS session to send email information. Provided certificates are authentic, communication with server will be encrypted.

- Program only accesses your account to send messages while you are using the program. It does not access any other information about your account.

- Let me know about any possible security issues

# Notes

- To test your message, you can generate a student list then delete all of the entries and add your own information to the first line. I recommend testing your initial messages until you get used to how everything works.

- The templating engine assumes that the dollar sign symbol ($) indicates a variable to substitute. If you need to enter a dollar sign, use a second dollar sign to escape. In other words, '$$20' in your email message file will become '$20' in the sent email message.

- This application does not access your full Gmail account. It will not fetch your signature or other personalized settings. Therefore you will either need to include your signature manually if you would like to use one. You can use HTML to adjust style settings.

# Troubleshooting

- If you are getting an error related to your Google account password, ensure that you have generated an app password for this program and are using that app password when prompted. This app password is not the same as your usual Gmail password.

- If you are getting an error related to reading your class list input file, check to see if you are using a CSV file from Hokie Spa. The number of columns or their location should not be modified, though you can add additional entries or change individual name fields as needed. You can rename the file but it must be in CSV format and end with ".csv".

- If you are getting an error related to reading your email message input file, check to see if you are using dollar signs anywhere in your message. Replace them with two dollar signs as discussed in the sections above. File must be plaintext to be read correctly. Use --html flag if you are using any HTML formatting.

- Misspelling any of the template variables will cause an error. Check to make sure that variable strings are written into your template message exactly as they appear.

# Planned Future Features

- Support for custom fields allowing you to store and reference fields like assigned group names or numbers, preferred names/nicknames, or individual assignment comments in messages

- Support for both Hokie Spa and Canvas generated class lists

- Validation features to ensure lists and messages are properly formatted

- Logging for messages that did not send allowing for quickly resending

- Other ideas? Let me know!
