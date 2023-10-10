import email
import imaplib
import re
from email.header import decode_header

# IMAP server settings for Outlook.com/Hotmail
imap_server = 'outlook.office365.com'
imap_port = 993  # IMAPS (secure) port
username = 'marumgaymonc@hotmail.com'
password = 'W3zSQ792'


def get_code_from_mail(username: str, password: str, pattern: str):
    # Connect to the IMAP server
    github_mail = 'noreply@github.com'
    result = ''
    try:
        mail_server = imaplib.IMAP4_SSL(imap_server, imap_port)
    except Exception as e:
        print(f"Error connecting to the IMAP server: {e}")
        exit()

    # Login to the server
    try:
        mail_server.login(username, password)
    except Exception as e:
        print(f"Login failed: {e}")
        mail_server.logout()
        exit()

    # Select the mailbox (e.g., 'INBOX')
    mailbox = 'INBOX'
    mail_server.select(mailbox)
    # Now you can perform various operations on the mailbox, such as fetching emails, marking them as read, etc.

    # Search for all emails (unseen and seen)
    # search_criteria = f'SEEN FROM "{github_mail}"'
    search_criteria = f'UNSEEN FROM "{github_mail}"'

    status, email_ids = mail_server.search(None, search_criteria)

    # Get a list of email IDs
    email_id_list = email_ids[0].split()

    # Loop through the email IDs and fetch the content of each email
    for email_id in email_id_list:
        status, email_data = mail_server.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]

        # Parse the email content
        msg = email.message_from_bytes(raw_email)

        # Get email subject and decode it
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')

        # Get sender's email address
        sender_email = msg.get('From')

        # Extract and print the email body
        email_body = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', 'ignore')
                print(f"Subject: {subject}")
                print(f"From: {sender_email}")
                print("------------")
                print(email_body)
                print("------------")

                # Use the re.search() function to search for the pattern in the email.
                match = re.search(pattern, email_body)

                # If the pattern is found, extract the 6 digits after it.
                if match:
                    result = match.group(1)

    # Logout from the IMAP server
    mail_server.logout()
    return result


if __name__ == '__main__':
    print('code: ' + get_code_from_mail(username, password, r'(\d{6})'))
