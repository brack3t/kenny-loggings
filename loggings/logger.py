from django.core import serializers
from django.db.models import Model

from . import ACTION_CREATE, ACTION_DELETE, ACTION_UPDATE
from .models import Log, LogExtra


class Logger(object):
    actions = (ACTION_CREATE, ACTION_UPDATE, ACTION_DELETE)
    extras = None
    previous_obj = None
    user = None

    def __init__(self, action, current_obj, previous_obj=None, user=None,
        extras=None):

        try:
            action = int(action)
        except ValueError:
            raise ValueError("Action must be an integer.")

        if action not in self.actions:
            raise Exception("Action must be an integer in %s" %
                str(self.actions))
        self.action = action

        if not isinstance(current_obj, Model):
            raise TypeError("current_obj must be a Django model instance.")
        self.current_obj = current_obj

        if previous_obj:
            if not isinstance(previous_obj, Model):
                raise TypeError(
                    "previous_obj must be a Django model instance.")

            if (previous_obj._meta.app_label !=
                self.current_obj._meta.app_label):

                raise Exception("current_obj and previous_obj must be from "
                    "the same Django app.")

            if (previous_obj._meta.object_name !=
                self.current_obj._meta.object_name):

                raise Exception("current_obj and previous_obj must be "
                    "instances of the same Django model.")

            self.previous_obj = previous_obj

        if user:
            self.user = user

        if extras:
            if not isinstance(extras, list):
                raise TypeError("extras must be a list.")

            for extra in extras:
                if len(extra.split("__")) > 1:
                    steps = extra.split("__")[:-1]
                    obj = self.current_obj

                    for step in steps:
                        if not hasattr(obj, step):
                            raise Exception(
                                "'%s' in %s is not a valid attribute." % (
                                    step, extra))

                        if not isinstance(getattr(obj, step), Model):
                            raise Exception("'%s' in %s is not a subclass of "
                                "django.db.models.Model." % (step, extra))

                        obj = getattr(obj, step)
                else:
                    if not hasattr(self.current_obj, extra):
                        raise Exception("The attribute '%s' does not "
                            "exist on the current instance." % extra)

            self.extras = extras

    def _create_extra_logs(self, log):
        for field in self.extras:
            obj = self.current_obj

            if len(field.split("__")) > 1:
                steps = field.split("__")
                field_name = steps.pop(-1)

                for step in steps:
                    obj = getattr(obj, step)
            else:
                field_name = field

            LogExtra.objects.create(
                log=log,
                field_name=field_name,
                field_value=getattr(obj, field_name)
            )

    def create(self):
        log = Log(
            action=self.action,
            app_name=self.current_obj._meta.app_label,
            model_name=self.current_obj._meta.object_name,
            model_instance_pk=self.current_obj.pk,
            current_json_blob=serializers.serialize(
                "json", [self.current_obj])
        )

        if self.previous_obj:
            log.previous_json_blob = serializers.serialize(
                "json", [self.previous_obj])

        if self.user:
            log.user_id = self.user.pk

        log.save()

        if self.extras:
            self._create_extra_logs(log)
