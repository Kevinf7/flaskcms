from flask import current_app

def log(message, user=None):
    if not user:
        current_app.logger.info(message)
    else:
        current_app.logger.info(message + user.first_name + ' '
            + user.last_name + ' - ' + user.email)