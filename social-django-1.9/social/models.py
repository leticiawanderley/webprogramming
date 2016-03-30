import collections
from django.db import models

class Profile(models.Model):
    text = models.CharField(max_length=4096)

class Member(models.Model):
    username = models.CharField(max_length=16,primary_key=True)
    password = models.CharField(max_length=16)
    profile = models.OneToOneField(Profile, null=True)
    friends = models.ManyToManyField("self", symmetrical=True)
    friendship_request = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.username

    """ Creates a list of Members recommended to the user
    A Member is recommended if it is friend of another friend of the user
    and there isn't any friendship request pending or relationship between it and the user
    The recommendations are ordered by the number of common relationships between the user and the Member
    """
    def get_recommendations(self):
        recommendations = []
        for friend in self.friends.all():
            for f in friend.friends.all():
                if f != self and f not in self.friends.all() and f not in self.friendship_request.all() and self not in f.friendship_request.all():
                    recommendations.append(f)
        recommendations = collections.Counter(recommendations)
        return [member for member, count in recommendations.most_common()]


class Message(models.Model):
    user = models.ForeignKey(Member, related_name='%(class)s_user')
    recip = models.ForeignKey(Member, related_name='%(class)s_recip')
    pm = models.BooleanField(default=True)
    time = models.DateTimeField()
    text = models.CharField(max_length=4096)
