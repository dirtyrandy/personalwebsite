import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
import requests
from flask import request
from jinja2 import Template
import logging

from .objects import email_parser
from config import email_template_directory, email_sender, requester_response_template, personal_address

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ses = boto3.client('ses')


def email():
    parsed_args = email_parser.parse_args(request)

    send_requester_response = send_response_email(parsed_args, requester_response_template)
    send_personal_response = send_personal_email(parsed_args)

    logger.info(f'Requester response sent: {send_requester_response}')
    logger.info(f'Personal response sent: {send_personal_response}')
    logger.info(f'Email args: {parsed_args}')


def send_response_email(email_args: dict, template: str) -> bool:
    template_file = next(
        file for file in email_template_directory.iterdir() if template == file.name.lower()
    )
    template_content = Template(template_file.read_text()).render(email_args)

    message = MIMEMultipart('mixed')
    msg_body = MIMEMultipart('alternative')
    msg_body.attach(MIMEText(template_content.encode('utf-8'), 'plain', 'utf-8'))
    msg_body.attach(MIMEText(template_content.encode('utf-8'), 'html', 'utf-8'))
    message.attach(msg_body)

    message['From'] = email_sender
    message['To'] = [email_args['email_address']]
    message['Subject'] = 'Thanks for reaching out!'

    try:
        ses.send_raw_email(
            RawMessage={
                'Data': message.as_string()
            }
        )
        return True
    except Exception as e:
        logger.error(str(e))
        return False


def send_personal_email(email_args: dict) -> bool:
    email_body = str(
        f'Sender: {email_args["name"]}\n'
        f'Sender email: {email_args["email_address"]}\n'
        f'Subject: {email_args["subject"]}\n'
        f'Message: {email_args["message"]}'
    )

    message = MIMEMultipart('mixed')
    msg_body = MIMEMultipart('alternative')
    msg_body.attach(MIMEText(email_body, 'plain', 'utf-8'))
    msg_body.attach(MIMEText(email_body, 'html', 'utf-8'))
    message.attach(msg_body)

    message['From'] = email_sender
    message['To'] = [personal_address]
    message['Subject'] = f'Website message from {email_args["name"]}'

    try:
        ses.send_raw_email(
            RawMessage={
                'Data': message.as_string()
            }
        )
        return True
    except Exception as e:
        logger.error(str(e))
        return False


def logout():
    logout_request = requests.get(
        f'https://auth.seecook.info/logout?'
        f'client_id=1fu24611953cnn87ee907quqlf&'
        f'logout_uri={os.getenv("logout_redirect_uri")}'
    )

    logger.info(f'logout response: {logout_request.text}')
