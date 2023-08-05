

from flask import render_template, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

# from app import myapp, logger #mail, logger 
from . import bp
# from ..celery.celeryrun import celeryJob


# def send_async_email(app, msg):
#     with app.app_context():
		
class Emailer():
	####################################################
	def __init__(self, logger=None, config=None):
		self.logger = logging
		self.config  = config

	# @celeryJob.task(name="cjob.send_email")
	def send_email(subject, sender, recipients, text_body, html_body):
		if not self.config['TESTING']:
			msg = Message(subject, sender=sender, recipients=recipients)
			msg.body = text_body
			msg.html = html_body
			myapp.mail.send(msg)  
			self.log_debug( "Sent async message - subject[{}]".format(subject) )
		else:
			self.log_debug( 'Skipping sending due to testing')


	####################################################
	def generate_confirmation_token(email):
		serializer = URLSafeTimedSerializer(self.config['SECRET_KEY'])
		return serializer.dumps(email, salt=self.config['SECURITY_PASSWORD_SALT'])

	####################################################
	def confirm_token(token, expiration=3600):
		serializer = URLSafeTimedSerializer(self.config['SECRET_KEY'])
		try:
			email = serializer.loads(
				token,
				salt=self.config['SECURITY_PASSWORD_SALT'],
				max_age=expiration
			)
		except:
			return False
		return email

	####################################################
	# @celeryJob.task(name="cjob.send_email")
	def send_register_email_confirmation(user):
		token = generate_confirmation_token(user.email)
		send_email.apply_async( args={ 'subject':' Confrim Your email',
					'sender':self.config['MAIL_USERNAME'],
					'recipients': [user.email],
					'text_body':  render_template('zemail/confirm_email.txt',
											user=user, token=token),
					'html_body': render_template('zemail/confirm_email.html',
											user=user, token=token) } )   


	####################################################
	def log_debug(self, message):
		if(self.logger): self.logger.debug(message)
	
	####################################################
	def log_error(self, message):
		if(self.logger): self.logger.error(message)
	
	
