import os

import config

import boto3


class Cognito(object):
    def __init__(self):
        self.client = boto3.client('cognito-idp')
        self.pool_id = os.getenv('pool_id')
