from celery import shared_task
from django.core.mail import send_mail
from decouple import config

# Send an email notification to the user when a snippet is created.
# The email contains the snippet's name and description.
@shared_task
def sendEmailInSnippetCreation(snippet_name, snippet_description, user_mail):
    print('enviando mail' + user_mail)
    subject = 'Snippet "' + snippet_name + '" created successfully'
    body = (
        'The snippet "' + snippet_name + '" was created with the following description: \n'
        + snippet_description
    )
    # Only send the email if the user has registered an email address
    if user_mail:
        
        send_mail(
            subject,
            body,
            config("EMAIL_HOST_USER"),
            [user_mail],
            fail_silently=False,
        )