import ssl
from email.message import EmailMessage

from outlook.contacts import Contacts
from outlook.emailconstants import SEND_PASS, SEND_ADDRESS, PORT, HOST, LAST
import smtplib


class EmailFunc:
    def __init__(self, subject, message, attachment_path=None):
        """
        Method that creates email message
        :param subject:
        :param message:
        :param attachment_path:
        """
        # Create EmailMessage object
        self.email_msg = self.create_msg(subject, message)
        self.attach_attachment(attachment_path)
        self.contacts = Contacts.extract_contacts()

    def send_emails(self):
        """
        Method that receives email sends email accordingly
        """
        # generate contacts address list
        self.contacts.extract_contacts()
        receiver_addresses = self.contacts.__getattribute__("email_addresses")

        # Create SSL context
        context = ssl.create_default_context()

        try:
            # Connect to SMTP server and send email
            with smtplib.SMTP_SSL(HOST, PORT, context=context) as smtp:
                smtp.login(SEND_ADDRESS, SEND_PASS)
                try:
                    for receiver_address in receiver_addresses:
                        self.email_msg['To'] = receiver_address
                        # smtp.send_message(self.email_msg)
                except Exception as error:
                    print(f'Unable to send email: \n{str(error)}')
        except Exception as e:
            print(f'Error: {str(e)}')

    @staticmethod
    def create_msg(subject, message):
        """
        method that creates and returns message
        :param subject:
        :param message:
        :return:
        """
        # Create EmailMessage object
        email_msg = EmailMessage()
        email_msg['From'] = SEND_ADDRESS
        email_msg['Subject'] = subject
        email_msg.set_content(message)

        return email_msg

    def attach_attachment(self, attachment_path):
        """
        Method that adds attachment to email
        :param attachment_path:
        :return:
        """
        # Add attachment if provided
        if attachment_path:
            with open(attachment_path, 'rb') as attachment_file:
                attachment_data = attachment_file.read()
                filename = attachment_path.split('/')[LAST]  # Extract the filename from the path
                self.email_msg.add_attachment(attachment_data, maintype='application', subtype='octet-stream',
                                              filename=filename)
