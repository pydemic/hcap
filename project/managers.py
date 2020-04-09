from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Manager


class CleanManager(Manager):
    def create_clean(self, *args, **kwargs):
        """
        Create object and perform full_clean(). Revert operation if full_clean()
        fails.
        """
        with transaction.atomic():
            obj = self.create(*args, **kwargs)
            try:
                obj.full_clean()
            except ValidationError:
                obj.remove()
                raise
            return obj
