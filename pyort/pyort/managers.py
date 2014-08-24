from django.db import models

from .utils import short_key_generator


class UserProfileManager(models.Manager):
    pass


class ShortenedUrlManager(models.Manager):

    def create_short_url(self, user, target_url):
        """ Create a new short url record.

            TODO:
                - Improve error handling
                - Improve short_key generation
                - Validate target_url

            Args:
                user (obj) - User model instance
                target_url (str) - Valid url string

            Returns:
                Created ShortendUrl instance or raise exception on failure

        """
        short_key = short_key_generator()
        while True:
            try:
                self.get(short_key=short_key)
                short_key = short_key_generator()
                continue
            except self.model.DoesNotExist:
                break

        try:
            obj = self.create(
                user=user,
                short_key=short_key,
                target_url=target_url
            )
        except Exception as e:
            raise e
        else:
            return obj
