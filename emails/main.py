from flask import abort


def get_bearer_token(request):
    bearer_token = request.headers.get('Authorization', None)
    if not bearer_token:
        abort(401)
    parts = bearer_token.split()
    if parts[0].lower() != "bearer":
        # authorization header must start with 'Bearer'
        abort(401)
    elif len(parts) == 1:
        # token was not found
        abort(401)
    elif len(parts) > 2:
        # authorization header must be of the form 'Bearer token'
        abort(401)
    bearer_token = parts[1]
    return bearer_token


def send_mail(request):
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    if request.method != 'POST':
        abort(405)
    bearer_token = get_bearer_token(request)
    secret_key = os.environ.get('ACCESS_TOKEN')
    if bearer_token != secret_key:
        abort(401)
    request_json = request.get_json(silent=True)
    parameters = ('sender', 'receiver', 'subject', 'message')
    sender, receiver, subject, message = '', '', '', ''
    if request_json and all(k in request_json for k in parameters):
        sender = request_json['sender']
        receiver = request_json['receiver']
        subject = request_json['subject']
        message = request_json['message']
    else:
        abort(400)
    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        html_content=message
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
        return 'OK', 200, headers
    except Exception as e:
        return e, 400, headers
