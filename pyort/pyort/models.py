from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from .managers import UserProfileManager, ShortenedUrlManager


class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=False, null=False)
    description = models.CharField(max_length=160, blank=True, null=True, default=None)
    avatar = models.ImageField(null=True, default=None)

    objects = UserProfileManager()

    def __unicode__(self):
        return u'{}'.format(self.user.username)


class ShortenedUrl(models.Model):
    user = models.ForeignKey(User)
    short_key = models.CharField(max_length=5, unique=True)
    target_url = models.URLField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    objects = ShortenedUrlManager()

    def __unicode__(self):
        return u'{} - {}'.format(self.user.username, self.short_key)

    def get_absolute_url(self):
        """
            TODO:
                Make this portable as recommended in the docs
                See: https://docs.djangoproject.com/en/dev/ref/models/instances/#get-absolute-url
        """
        return self.short_key

    def get_absolute_short_url(self):
        try:
            return 'http://{}/{}'.format(
                Site.objects.get_current().domain,
                self.get_absolute_url()
            )
        except:
            return None


#### SIGNALS SECTION (KEEP AT BOTTOM)
import signals
#### END SIGNALS SECTION
