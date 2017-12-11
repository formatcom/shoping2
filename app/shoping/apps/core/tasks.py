from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from shoping.apps.sendgrid_template.models import Sendgrid

@shared_task
def add(x, y):
    return x+y

@shared_task
def task_sendgrid_mail(
        template_name=None, user_pk=None,
        ticket_pk=None ):

    user = User.objects.get(pk=pk)

    template = Sendgrid.objects.filter(name=template_name).first()

    msg = EmailMessage(
        subject='Register',
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    if template:
        msg.template_id = template.template_id

        if template.category and template.category != '':
            msg.categories = [template.category]

    else:
        raise ValueError('no found template name: {}'.format(template_name))

    msg.substitutions = {
        ':username': user.username,
        ':email': user.email,
        ':first_name': user.first_name,
        ':last_name': user.last_name
    }

    msg.send()
    return {
        'user': user.pk,
        'template': template.pk,
        'category': template.category,
        'substitutions': msg.substitutions
    }
