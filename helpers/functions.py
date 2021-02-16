import os

import boto3
import logging

from config import email_sender, requester_response_template

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ses = boto3.client('ses')


def email(name: str, email_address: str, subject: str, message: str):

    send_requester_response = send_response_email(email_address, requester_response_template)
    send_personal_response = send_personal_email(
        name=name,
        email_address=email_address,
        subject=subject,
        message=message
    )

    logger.info(f'Requester response sent: {send_requester_response}')
    logger.info(f'Personal response sent: {send_personal_response}')


def send_response_email(email_address: str, template_content: str):
    try:
        send_email = ses.send_email(
            Source=email_sender,
            Destination={
                'ToAddresses': [email_address]
            },
            Message={
                'Subject': {
                    'Data': 'Thanks for reaching out!',
                    'Charset': 'utf-8'
                },
                'Body': {
                    'Text': {
                        'Data': template_content,
                        'Charset': 'utf-8'
                    },
                    'Html': {
                        'Data': template_content,
                        'Charset': 'utf-8'
                    }
                }
            }
        )
        return True if 'MessageId' in send_email else False
    except Exception as e:
        logger.error(str(e))
        return False


def send_personal_email(name: str, email_address: str, subject: str, message: str):
    try:
        email_body = str(
            f'Sender: {name}\n'
            f'Sender email: {email_address}\n'
            f'Subject: {subject}\n'
            f'Message: {message}'
        )

        logger.info(f'Email data:\n{email_body}')

        send_email = ses.send_email(
            Source=email_sender,
            Destination={
                'ToAddresses': [os.getenv('personal_address')]
            },
            Message={
                'Subject': {
                    'Data': f'Personal website email from {email_address}',
                    'Charset': 'utf-8'
                },
                'Body': {
                    'Text': {
                        'Data': email_body.replace('\n', '<br>'),
                        'Charset': 'utf-8'
                    },
                    'Html': {
                        'Data': email_body.replace('\n', '<br>'),
                        'Charset': 'utf-8'
                    }
                }
            }
        )
        return True if 'MessageId' in send_email else False

    except Exception as e:
        logger.error(str(e))
        return False


def build_logout() -> str:
    return str(
        f'{os.getenv("logout_uri")}?'
        f'client_id={os.getenv("client_id")}&'
        f'logout_uri={os.getenv("logout_redirect_uri")}'
    )
