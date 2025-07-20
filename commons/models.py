from datetime import datetime
from django.db import models

class DatesModel(models.Model):
    """
    Abstract model for dates that can be used in all your models to track creation and update times of objects in db.
    """

    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta(object):
        abstract = True

    def save(self, force_insert=None, force_update=None, using=None, update_fields=None, *args, **kwargs):
        """
        Overriden save method to ensure that the `updated_at` field is always updated
        """
        if update_fields is not None:
            update_fields = list(set(update_fields).union({'updated_at'}))

        super(DatesModel, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
            *args,
            **kwargs
        )
