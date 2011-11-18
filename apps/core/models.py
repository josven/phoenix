import datetime
from django.db import models
from django.db.models import get_model
from django.contrib.auth.models import User, Group
from django.core.exceptions import ImproperlyConfigured, ValidationError
from utils import find_request

class Profile(models.Model):
    """
    A user profile

    """

    pass


class Entry(models.Model):
    group = models.ForeignKey(Group, related_name="%(class)s_entries", blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_%(class)s_entries", blank=True, null=True)
    last_changed_by = models.ForeignKey(User, related_name="changed_%(class)s_entries", blank=True, null=True)
    deleted_by = models.ForeignKey(User, related_name="deleted_%(class)s_entries", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_changed = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_deleted = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta():
        abstract = True

    def save(self, *args, **kwargs):
        """
        Custom save for Entry. 
        
        Sets created_by or last_changed_by depending on if the object is being 
        created or modified. If the field in question has not been specified in 
        the method call the user will be extracted from the request.
        
        When modifying rather than creating, checks if there is a corresponding 
        History model and saves the old version of the object there. History
        will not be saved if:
        There is no History model.
        None of the fields that the History model tracks has been changed.
        The change was made by the same user as the last change, and within 5
        min of the last change. 
        
        """
        if not self.id:
            # This is a new item, set created_by
            if not self.created_by:
                # created_by not in args, find the request to get the user
                request = find_request()
                if request and request.user.is_authenticated():
                    self.created_by = request.user
        else:
            # Modyfing object, set last_changed_by
            if not self.last_changed_by:
                # last_changed_by not in args, find the request to get the user
                request = find_request()
                if request and request.user.is_authenticated():
                    self.last_changed_by = request.user

            # Check if there is a history model, and if so handle history
            history_name = self.__class__.__name__ + "History"
            history_model = get_model(self._meta.app_label, history_name)
            if history_model:
                # Validate that the origin field exists
                if "origin" not in history_model._meta.get_all_field_names():
                    error = """
All History models must contain a ForeignKey named "origin", pointing to the
model that it tracks history for."
                            """
                    raise ImproperlyConfigured(error)

                # We have a history model, check time and user
                needs_history = False
                current_object = self.__class__.objects.get(pk=self.pk)

                last_changer = current_object.last_changed_by
                if not last_changer:
                    # Not changed, or changed by anonymous. Use created_by
                    last_changer = current_object.created_by

                if not last_changer or last_changer != self.last_changed_by:
                    # Not edited by the same user as before, save history
                    needs_history = True
                else:
                    # Changed by the same user, check timestamps
                    last_changed = current_object.date_last_changed
                    if not last_changed:
                        # Has not been changed before, use date_created instead
                        last_changed = current_object.date_created

                    time_d = datetime.timedelta(minutes=5)
                    if last_changed < datetime.datetime.now() - time_d:
                        needs_history = True

                # Check if fields have changed
                if needs_history:
                    changed = False
                    history_fields = {}

                    for field_n in history_model._meta.get_all_field_names():
                        # Skip id, created_by, date_created, origin
                        s_f = ["id", "created_by", "date_created", "origin"]
                        if field_n in s_f:
                            continue

                        # Check all other fields
                        field = getattr(current_object, field_n)
                        if field != getattr(self, field_n):
                            changed = True
                        history_fields[field_n] = getattr(self, field_n)

                    if changed:
                        # All requirements for history has been checked,
                        # save the history item
                        history_fields['created_by'] = self.last_changed_by
                        history_fields['origin'] = self
                        try:
                            history_model.objects.create(**history_fields)
                        except TypeError:
                            error = """
TypeError encountered on field when creating history. History can only be used 
on "simple" fields, advanced fields like ManyToManyField cannot be tracked.
                                    """
                            raise ImproperlyConfigured(error)

        # Call the real save() method.
        # Setting hierarchy calls save twice as it needs the pk to set the
        # hierarchy. If the save originated from a objects.create force_insert 
        # will be on. If we see this, foce_update instead
        if self.pk:
            kwargs['force_insert'] = False
            kwargs['force_update'] = True
            super(Entry, self).save(*args, **kwargs)
        else:
            super(Entry, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Custom delete for Entry. 
        
        Sets date_deleted and deleted_by instead of a hard delete.
        Extracts user for deleted_by from request, unless given an argument.
        
        """

        self.date_deleted = datetime.datetime.now()
        if not self.deleted_by:
            request = find_request()
            if request and request.user.is_authenticated():
                self.deleted_by = request.user

        # Call the real save() method, NOT the delete()
        super(Entry, self).save(*args, **kwargs)

    def get_history(self):
        history_name = self.__class__.__name__ + "History"
        history_model = get_model(self._meta.app_label, history_name)

        if history_model:
            return history_model.objects.filter(origin=self)
        else:
            error = "History not enabled: No model named %s" % history_name
            raise ImproperlyConfigured(error)


class EntryHistory(models.Model):
    created_by = models.ForeignKey(User, related_name="created_%(class)s_history", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta():
        abstract = True


class ThreadedEntry(Entry):
    """
    Abstract model for Entries containing threading logic. Used for
    forum-posts, comments and other items needing threading. Subclasses Entry.
    
    ThreadedEntry models must have a ForeignKey named "collection" pointing
    to the parent object for the thread.
    
    Example:
    The forum has Thread:s that contains ForumPost:s. The ForumPost model is 
    threaded and uses ThreadedEntry, as such it must have a ForeignKey, named 
    collection, to the Thread model.
        
    """
    hierarchy = models.CharField(max_length="1024")
    hierarchy_level = models.PositiveIntegerField(blank=True, null=True)
    sub_thread = models.CharField(max_length="1024")
    parent = models.ForeignKey('self', blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Custom save for threaded entry. Will handle hierarchy.
        Will also run custom save from Entry, handling history.
        
        Takes one additional argument (only used on create): parent
        parent is the ThreadedEntry that this is is a reply to and is used to
        caluculate hierarchy. parent can be None, but should only be so for the
        first ThreadedEntry in this group (such as the first message in a
        form thread).

        Hierarchy - Rules
        Objects in the root thread have a hierarchy equal to their pk. Ex: 24
         
        Objects in a sub-thread have a hierarchy equal to the hierarchy of 
        the parent of the sub-thread dot their pk. Ex: 24.28
         
        If multiple sub-threads exist, newer ones gets their pk prepended with
        an increasing number of zeroes. Ex: 24.28, 24.034, 24.0067

        An objects indentation is called its hierarchy level, and can be counted
        by the number of "." in the hierarchy. 24 has hierarchy level 0, 24.28
        has hierarchy level 1, etc.
        """

        # Check that we are not using a normal history with a threaded entry
        history_name = self.__class__.__name__ + "History"
        history_model = get_model(self._meta.app_label, history_name)
        if history_model:
            if not "hierarchy" in history_model._meta.get_all_field_names():
                error = """
Mismatch: ThreadedEntry cannot use a subclass of EntryHistory for tracking. Use
ThreadedEntryHistory instead.
                        """
                raise ImproperlyConfigured(error)

        #=======================================================================
        # HIERARCHY
        #=======================================================================
        # Check if we have an id, if we don't we must save first
        if not self.id:
            super(Entry, self).save(*args, **kwargs)

        # Caluclate hierarchy if it does not already exist
        if not self.hierarchy:
            chie = None
            self.sub_thread = ""

            # If parent is none, just set hierarchy as the pk
            if not self.parent_id:
                chie = str(self.id)
            else:
                # We are unfortunatly going to need the parent object now
                parent = self.__class__.objects.get(pk=self.parent_id)

            if not chie:
                # Check if parent is latest in the sub-thread. If it is, this answer
                # should appear just under it on the same hierarchy level.
                if parent.is_latest_in_thread():
                    self.sub_thread = parent.sub_thread

                    # Remove last part of parents hierarchy and add the new pk to it
                    first_dot = parent.hierarchy.rfind(".")
                    if first_dot == -1:
                        # This was at hierarchy level one, just set hierarchy as pk
                        chie = str(self.id)
                    else:
                        chie = parent.hierarchy[0:first_dot] + "." + parent.get_sub_thread() + str(self.id)
                else:
                    # Parent was not latest in thread, check if there are any subs
                    newest_sub = parent.get_newest_sub_thread()
                    if newest_sub:
                        if newest_sub == "EMPTY":
                            newest_sub = ""
                        # There are sub-threads. Create a new one by prepending 0
                        chie = parent.hierarchy + ".0" + newest_sub + str(self.id)
                        self.sub_thread = "0" + newest_sub
                    else:
                        # No sub threads, just add the id to the end
                        chie = parent.hierarchy + "." + str(self.id)

            # Get the hierarchy level
            self.hierarchy = chie
            self.hierarchy_level = chie.count(".")

            # Call the Entry save() method.
            super(ThreadedEntry, self).save(*args, **kwargs)

    def is_latest_in_thread(self):
        if self.__class__.objects.filter(
            collection=self.collection,
            hierarchy_level=self.hierarchy_level,
            sub_thread=self.sub_thread,
            pk__gt=self.pk
            ):
            return False
        else:
            return True

    def get_newest_sub_thread(self):
        children = self.__class__.objects.filter(
            collection=self.collection,
            hierarchy_level=self.hierarchy_level + 1,
            hierarchy__startswith=self.hierarchy
        ).order_by("-sub_thread")

        if not children:
            return None
        else:
            if children[0].sub_thread:
                return children[0].sub_thread
            else:
                # We want to differentiate between no children and no sub_thread
                return "EMPTY"

    def get_sub_thread(self):
        hierarchy_id = self.hierarchy[(self.hierarchy.rfind(".") + 1):]
        sub_index = hierarchy_id.find(str(self.id))
        return hierarchy_id[0:sub_index]

    class Meta():
        abstract = True
        ordering = ['hierarchy']

class ThreadedEntryHistory(EntryHistory):
    """
    Abstract model for ThreadedEntry history. ThreadedEntry will not accept
    a history based on just EntryHistory.
    
    """
    hierarchy = models.CharField(max_length="1024")

    class Meta():
        abstract = True


class NewsEntry(Entry):
    """
    A news entry, visible on the start page

    """

    pass
