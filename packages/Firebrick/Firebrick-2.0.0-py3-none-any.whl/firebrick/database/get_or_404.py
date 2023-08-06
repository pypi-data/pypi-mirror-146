from django.db.models.manager import Manager
from django.http import Http404


def get_object_or_404(self, error_text='Page is can not be found', **kwargs):
    try:
        return self.get(**kwargs)
    except self.model.DoesNotExist:
        raise Http404(error_text)


# Adding the `get_object_or_404` method the `Manager` class so it can be used like
# Model.objects.get_object_or_404 (the models objects is a instance of `Manager`)
Manager.get_object_or_404 = get_object_or_404