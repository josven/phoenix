from django.db import models


class Profile(models.Model):
    """
    A user profile

    """

    pass


class Entry(models.Model):
    """
    A generic threading entry

    """

    pass


class NewsEntry(Entry):
    """
    A news entry, visible on the start page

    """

    pass
