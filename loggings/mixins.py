from .constants import ACTION_CREATE, ACTION_DELETE, ACTION_UPDATE
from .logger import Logger


class LogModelObject(object):
    """ Generic base object for CBV mixins. """
    action = None
    log_extras = None


class LogCreateObjectMixin(LogModelObject):
    """
    Mixin to be used on Django's CreateView class-based view.
    Automatic logging of instance creation.
    """
    action = ACTION_CREATE

    def form_valid(self, form):
        """
        Call the super so the object is created in the database.
        Log the object then return the response.
        """
        response = super(LogCreateObjectMixin, self).form_valid(form)

        Logger(self.action, self.object, user=self.request.user,
            extras=self.log_extras).create()

        return response


class LogUpdateObjectMixin(LogModelObject):
    """
    Mixin to be used on Django's UpdateView class-based view.
    Automatic logging of instance updates.
    """
    action = ACTION_UPDATE

    def form_valid(self, form):
        """
        Get the unchanged object from the database.
        Call super to save changes to the object.
        Log the old and current objects.
        """
        old_object = self.model.objects.get(pk=self.object.pk)

        response = super(LogUpdateObjectMixin, self).form_valid(form)

        Logger(self.action, self.object, old_object, user=self.request.user,
            extras=self.log_extras).create()

        return response


class LogDeleteObjectMixin(LogModelObject):
    """
    Mixin to be used on Django's DeleteView class-based view.
    Automatic logging of instance deletions.
    """
    action = ACTION_DELETE

    def delete(self, request, *args, **kwargs):
        """
        Get the object before it is deleted.
        Log it and return the super.
        """
        self.object = self.get_object()

        Logger(self.action, self.object, user=request.user,
            extras=self.log_extras).create()

        return super(LogDeleteObjectMixin, self).delete(request, *args,
            **kwargs)
