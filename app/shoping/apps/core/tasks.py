from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models import Sum
from shoping.apps.sendgrid_template.models import Sendgrid
from shoping.apps.ticket.models import Ticket

@shared_task
def add(x, y):
    return x+y

@shared_task
def task_sendgrid_mail(
        template_name=None, user_pk=None,
        ticket_pk=None, next_url=None):

    user = User.objects.get(pk=user_pk)
    ticket = ticket_pk and Ticket.objects.get(pk=ticket_pk)

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

    substitutions = {
        ':username': user.username,
        ':email': user.email,
        ':first_name': user.first_name,
        ':last_name': user.last_name,
        ':next': next_url or ''
    }


    if ticket:
        items = ticket.items.all().aggregate(Sum('quantity'))['quantity__sum']
        substitutions.update({
            ':total': '{:.2f}'.format(ticket.total),
            ':items': '{}'.format(items)
        })

    msg.substitutions = substitutions

    msg.content_subtype = 'html'
    msg.send()
    context = {
        'user': user.pk,
        'template': template.pk,
        'category': template.category,
        'substitutions': msg.substitutions,
        'ticket': ticket and ticket.pk
    }
