from django.db import models


class BetaReg(models.Model):
    """
    A user signed up for the preliminary beta registration.

    """

    email = models.EmailField(max_length=75)
    ip = models.IPAddressField()

    def __unicode__(self):
        return '%s: %s' % (self.email, self.ip)
