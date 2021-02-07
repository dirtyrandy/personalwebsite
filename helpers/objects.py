from flask_restx.reqparse import RequestParser


email_parser = RequestParser()
email_parser.add_argument('name', required=True, location='form')
email_parser.add_argument('subject', required=True, location='form')
email_parser.add_argument('message', required=True, location='form')
email_parser.add_argument('email_address', required=True, location='form')
