"""
Renders messages based on
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import logging, datetime
from biostar.apps.util import html

from biostar.apps.notes.models import Message, MessageBody

NEW_POST_CREATED_TEMPLATE = "notes/post.created.html"

def post_create_subscriptions(sender, instance, created, *args, **kwargs):
    "The actions to undertake when creating a new post"
    from biostar.apps.posts.models import Subscription

    if created:
        # Create a subscription by the user
        Subscription.create(post=instance, user=instance.author)

def post_create_messages(sender, instance, created, *args, **kwargs):
    "The actions to undertake when creating a new post"
    from biostar.apps.posts.models import Subscription

    if created:
        # The user sending the notifications.
        sender = instance.author

        # Get all subscriptions for the post.
        subs = Subscription.objects.get_subs(instance).exclude(user=sender)

        # Generate the message from the template.
        page = html.render(name=NEW_POST_CREATED_TEMPLATE, post=instance)

        # Create the message body.
        body = MessageBody(sender=instance.author, subject=instance.title, text=page)
        body.save()

        # Insert a message for everyone involved.
        for sub in subs:
            Message.objects.create(user=sub.user, body=body)