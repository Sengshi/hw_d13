from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Retry


@receiver(post_save, sender=Retry)
def notify_author(sender, instance, **kwargs):
    retry = Retry.objects.get(id=instance.id)
    recipient = [retry.post.author.email]
    html_content = render_to_string(
            'retry_created.html',
            {
                'post': retry,
                'author': retry.post.author,
            }
        )
    msg = EmailMultiAlternatives(
            subject=f'{retry.post.author}',
            body=retry.retries,
            from_email='testpysend@mail.ru',
            to=recipient,
        )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

