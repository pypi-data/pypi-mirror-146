from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from knox import crypto
from knox.settings import CONSTANTS, knox_settings

User = settings.AUTH_USER_MODEL


class AuthTokenManager(models.Manager):
    def create(self, user, token_type, expiry=knox_settings.WEB_TOKEN_TTL):
        token = crypto.create_token_string()
        digest = crypto.hash_token(token)

        if expiry is not None:
            expiry = timezone.now() + expiry

        instance = super(AuthTokenManager, self).create(
            token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH], digest=digest,
            user=user, expiry=expiry, token_type=token_type)
        return instance, token


class AuthToken(models.Model):

    TOKEN_TYPE_WEB = "web"
    TOKEN_TYPE_MOBILE = "mobile"
    TOKEN_TYPE_CHOICES = (
        (TOKEN_TYPE_WEB, _(TOKEN_TYPE_WEB)),
        (TOKEN_TYPE_MOBILE, _(TOKEN_TYPE_MOBILE))
    )

    objects = AuthTokenManager()
    digest = models.CharField(
        max_length=CONSTANTS.DIGEST_LENGTH, primary_key=True)
    token_key = models.CharField(
        max_length=CONSTANTS.TOKEN_KEY_LENGTH, db_index=True)
    token_type = models.CharField(max_length=32, choices=TOKEN_TYPE_CHOICES, default=TOKEN_TYPE_WEB)
    user = models.ForeignKey(User, null=False, blank=False,
                             related_name='auth_token_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s : %s' % (self.digest, self.user)
