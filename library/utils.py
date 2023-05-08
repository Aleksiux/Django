# import smtplib
#
# from django.core.mail import EmailMessage
#
#
# def send_reset_email(user):
#     sender = 'email@gmail.com'
#     token = user.get_reset_token()
#     msg = f'''If you want to reset password press on the link:
#     {url_for('reset_password', token=token, _external=True)}
#     If you did not pressed reset password just ignore this letter and password won't be changed.
#     '''
#
#     {{protocol}}: // {{domain}}
#     { % url 'password_reset_confirm'
#     uidb64 = uid
#     token = token %}
#     email_sender = EmailMessage()
#     email_sender['from_email'] = sender
#     email_sender['to'] = user.email
#     email_sender['subject'] = 'Password recovery'
#     email_sender['body'] = msg
#
#     smtp = smtplib.SMTP_SSL("smtp.gmail.com")
#     smtp.login(sender, 'passkey')
#     smtp.sendmail(sender, user.email, email_sender.as_string())
#     smtp.quit()
#
