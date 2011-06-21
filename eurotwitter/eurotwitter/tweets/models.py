import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete

from eurotwitter.tweets.timelines import Timeline

class Tweet(models.Model):
    author  = models.ForeignKey(User)
    message = models.CharField(max_length=140)
    date    = models.DateTimeField(default=datetime.datetime.now)
    parent  = models.ForeignKey('self', null=True)

    @classmethod
    def post_save(cls, instance, **kwargs):
        PublicTimeline.add(instance)
        ProfileTimeline.add(instance, user_id=instance.author_id)
        
    @classmethod
    def post_delete(cls, instance, **kwargs):
        PublicTimeline.remove(instance)
        ProfileTimeline.remove(instance, user_id=instance.author_id)

class Relationship(models.Model):
    from_user = models.ForeignKey(User)
    to_user   = models.ForeignKey(User)

# Application triggers to keep timelines updated
post_save.connect(Tweet.post_save)
post_delete.connect(Tweet.post_delete)

# stores all tweets
PublicTimeline = Timeline(Tweet, 'public')

# stores tweets keyed by user_id
ProfileTimeline = Timeline(Tweet, 'profile')
