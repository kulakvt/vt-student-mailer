#!/usr/bin/env python

# vt-student-mailer v1.0 by Andrew Kulak
# Revised August 2017
# Currently in testing phase...
# akulak@vt.edu

import smtplib
import getpass
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import optparse
import os


def create_template():
    """
    Creates template file in the current working directory
    Takes no arguments
    Returns file that demonstrates how to use placeholders
    """

    try:
        cwd = os.getcwd()
        with open(os.path.join(cwd, 'example-email.txt'), 'wb') as my_file:
            my_file.write('Dear ${FULL_NAME},\n\nThis is an example message. '
                          'The placeholders would be replaced with names from the class list provided. '
                          '\n\nYou can run vt-student-mailer in test mode for a demonstration! '
                          'Use the -x flag with -m example-email.txt and -s followed by the name of '
                          'a CSV file with student information from Hokie Spa. A sample email substituting the '
                          'placeholders with student infromation from the first line of the CSV file will be printed. '
                          'Use -h or --help for more usage information.'
                          '\n\nThanks for reading, ${FIRST_NAME}!\n\n'
                          'All the best,\n\n'
                          '-Foo')

    except Exception, e:
        print '[-] Error: Could not create file in current directory. Please retry. Trace:'
        print str(e)
        print '[-] -h or --help for usage information'
        exit(1)


def get_contacts_directory(directory):
    """
    reads student list csvs from a directory linked from current working directory
    Takes one string argument representing the location of the student names files
    Returns student names and emails from all of the files.
    """

    lists_dir = os.path.join(os.getcwd(), directory)
    student_list_files = []
    first_names = []
    full_names = []
    emails = []

    try:
        for afile in os.listdir(lists_dir):
            if afile.endswith(".csv"):
                student_list_files.append(os.path.join(lists_dir, afile))

        if student_list_files:
            for afile in student_list_files:
                file_first_names, file_full_names, file_emails = get_contacts(afile)
                first_names.extend(file_first_names)
                full_names.extend(file_full_names)
                emails.extend(file_emails)
            return first_names, full_names, emails
        else:
            print '[-] Error: No CSV files found in provided directory. Please retry.'
            print '[-] -h or --help for usage information'
            exit(0)

    except Exception, e:
        print '[-] Error: Could not open or parse contacts directory. Please retry. Trace:'
        print str(e)
        print '[-] -h or --help for usage information'
        exit(1)


def get_contacts(filename):
    """
    reads a student list csv
    Takes one string argument representing the name of the student list file
    Returns student names and emails from the file.
    """

    first_names = []
    full_names = []
    emails = []

    try:
        with open(filename, mode='r') as contacts_file:
            for a_contact in contacts_file:
                last_names = a_contact.split(',')[3].replace('"', '')
                first_middle_names = a_contact.split(',')[4].replace('"', '')
                first_name, sep, tail = first_middle_names.partition(' ')
                first_names.append(first_name.strip())
                full_names.append(first_middle_names + ' ' + last_names)
                emails.append(a_contact.split(',')[8].replace('"', '').strip())
        return first_names, full_names, emails

    except Exception, e:
        print '[-] Error: Could not open or parse contacts file. Please retry. Trace:'
        print str(e)
        print '[-] -h or --help for usage information'
        exit(1)


def read_template(filename):
    """
    reads a message template
    Takes one string argument representing the name of the template file
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    try:
        with open(filename, 'r') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    except Exception, e:
        print '[-] Error: Could not open template file. Please retry. Trace:'
        print str(e)
        print '[-] -h or --help for usage information'
        exit(1)


def smtp_connect(address, password):
    """
    sets up the SMTP server
    Takes two string arguments representing email address and password
    Returns an SMTP connection over TLS
    """

    try:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(address, password)
        return s

    except Exception, e:
        print '[-] Error: Could not connect to Gmail SMTP server. Please check internet settings and Gmail ' \
              'credentials then retry. Trace:'
        print str(e)
        print '[-] -h or --help for usage information'
        exit(1)


def send_messages(first_names, full_names, emails, template, is_quiet, is_html):
    """
    where the magic happens
    Takes three main arguments, a list of first names, a list of full names, a list of emails, and a template string
    Also takes two booleans defining mode settings
    Sends emails in specified format with the specified stout messages
    void function
    """

    while True:
        my_address = raw_input('[*] Please enter your Gmail address including domain:\n')
        password = getpass.getpass('[*] Please enter your Gmail app password (will not be displayed):\n')
        subject = raw_input('[*] Please enter a subject for your email:\n')
        print '\n[+] You have provided the following information:'
        print '[+] Your email: ' + my_address
        print '[+] Your Gmail app password: [hidden]'
        print '[+] Email subject: ' + subject
        if not my_address or not password or not subject:
            print '[-] Input for all fields required!'
            continue
        else:
            correct = raw_input('[*] Is all this information correct? [Y/y]es to begin sending messages: ')
            if correct.lower() == 'yes':
                print '\n'
                break

    server = smtp_connect(my_address, password)
    print '[+] Connected to server, beginning to send messages...'

    for first_name, full_name, email in zip(first_names, full_names, emails):
        msg = MIMEMultipart()  # create a message

        # adds in types of names where specified in the template file
        try:
            message = template.substitute(FIRST_NAME=first_name.title(), FULL_NAME=full_name.title())
        except Exception, e:
            print '[-] Error: Could not complete template parsing.'
            print '[-] Please check message file and try again.'
            print '[-] Remember that \'$\' is a reserved character. See README.'
            print str(e)
            print '[-] -h or --help for usage information'
            exit(1)

        # Prints out message info if not quiet
        if not is_quiet:
            print ('[+] Sending message to ' + full_name.title() + ' at ' + email)

        # setup the parameters of the message
        msg['From'] = my_address
        msg['To'] = email
        msg['Subject'] = subject

        # add in the message body based on format specified by user
        if is_html:
            msg.attach(MIMEText(message, 'html'))
        else:
            msg.attach(MIMEText(message, 'plain'))
        # send the message via the server set up earlier.
        try:
            server.sendmail(my_address, email, msg.as_string())
            del msg
        except Exception, e:
            print '[-] Error: Problem sending message to ' + full_name.title() + ' at ' + email
            print '[-] See trace for more information:'
            print str(e)
            pass
    # Terminate the SMTP session and close the connection
    server.quit()


def message_test(first_names, full_names, emails, template, is_html):
    """
    Generates a test email message
    Takes list of first names, full names, and emails and email template to test
    Also takes one boolean specifying mode
    Returns test email with substitutions from first line in contacts file.
    """

    first_name = first_names[0]
    full_name = full_names[0]
    email = emails[0]

    try:
        msg = MIMEMultipart()  # create a message

        # adds in names where specified in the template file
        message = template.substitute(FIRST_NAME=first_name.title(), FULL_NAME=full_name.title())

        # setup the parameters of the message
        msg['From'] = 'test@domain.com'
        msg['To'] = email
        msg['Subject'] = "TESTING"

        # add in the message body based on format specified by user
        if is_html:
            msg.attach(MIMEText(message, 'html'))
        else:
            msg.attach(MIMEText(message, 'plain'))

        return msg.as_string()

    except Exception, e:
        print '[-] Error: Problem generating test message'
        print '[-] See trace for more information:'
        print '[-] -h or --help for usage information'
        print str(e)
        exit(1)


def main():
    """
    The main function
    Handles input parsing and function calls
    Returns errors if there are any issues with input
    Contains version and usage information
    """

    # Begin command line argument parsing
    usage = '%prog -s classlist.csv -m message.txt [options]\n\nvt-student-mailer v1.0 by Andrew Kulak\n' \
            'Sends bulk personalized emails to all of your students\nSend feedback or spam to akulak@vt.edu'
    parser = optparse.OptionParser(usage=usage, version="%prog 1.0")  # Parses Unix-y command line arguments
    parser.add_option('-t', '--template',
                      action='store_true', dest='print_template', default=False,
                      help='generate example email in working directory and exit')
    parser.add_option('-s', '--singlelist', dest='listfile',
                      help='read student information from LIST.csv', metavar='LIST.csv')
    parser.add_option('-d', '--directory', dest='listdir',
                      help='read student information from all files in PATH/WITH/LISTS', metavar='PATH/WITH/LISTS')
    parser.add_option('-m', '--message', dest='template',
                      help='read email template from MESSAGE.txt', metavar='MESSAGE.txt')
    parser.add_option('-q', '--quiet',
                      action='store_true', dest='is_quiet', default=False,
                      help='don\'t print status messages for each email sent, default is to print status')
    parser.add_option('--html',
                      action='store_true', dest='is_html', default=False,
                      help='treats email message text as HTML, default is plaintext')
    parser.add_option('-x', '--test', action='store_true', dest='test_mode', default=False,
                      help='print test email with -s LIST.csv and -m MESSAGE.txt')
    (options, args) = parser.parse_args()

    # Print program info
    print parser.get_version() + ' by Andrew Kulak'
    print 'Send feedback or spam to akulak@vt.edu\n'

    # Checks for mode overide settings
    if options.print_template:
        print '[+] Creating template file...'
        create_template()
        print '[+] Example-email.txt created in ' + os.getcwd()
        exit(0)

    elif options.test_mode:
        if options.listfile and options.template:
            print '[+] Generating test email with first entry from names list provided'
            first_names, full_names, emails = get_contacts(options.listfile)  # read contacts
            message_template = read_template(options.template)
            test_msg = message_test(first_names, full_names, emails, message_template, options.is_html)
            print '[+] Example with first line of data from student file provided:'
            print test_msg
            print '\n[+] Exiting...'
        else:
            print '[-] Error: Must specify both list of students and message template to test'
            print '[-] -h or --help for usage information'
        exit(0)

    # If sending messages, checks arguments and begins selected process
    else:
        if not options.listfile and not options.listdir:  # won't work without a single file or directory
            print '[-] Error: Must specify either a single student list or directory containing at least one list'
            print '[-] -h or --help for usage information'
            exit(0)

        elif options.listfile and options.listdir:  # won't work with both a single file and a directory
            print '[-] Error: Must specify either single list or list directory, not both'
            print '[-] -h or --help for usage information'
            exit(0)

        elif not options.template:  # won't work without a template
            print '[-] Error: Must provide a template file'
            print '[-] -h or --help for usage information'
            exit(0)

        else:
            if options.listfile:
                first_names, full_names, emails = get_contacts(options.listfile)  # read contacts
                message_template = read_template(options.template)
                send_messages(first_names, full_names, emails, message_template, options.is_quiet, options.is_html)
                print '[+] Completed iteration through student list provided'
                exit(0)

            elif options.listdir:
                first_names, full_names, emails = get_contacts_directory(options.listdir)  # read contacts
                message_template = read_template(options.template)
                send_messages(first_names, full_names, emails, message_template, options.is_quiet, options.is_html)
                print '[+] Completed iteration through all student lists in directory'
                exit(0)


if __name__ == '__main__':
    main()
