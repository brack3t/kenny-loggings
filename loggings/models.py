from django.db import models


class Log(models.Model):
    """ Log model """
    action = models.SmallIntegerField()
    app_name = models.CharField(blank=True, db_index=True, default='',
        max_length=255)
    model_name = models.CharField(blank=True, db_index=True, default='',
        max_length=255)
    model_instance_pk = models.CharField(blank=True, db_index=True, default='',
        max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    previous_json_blob = models.TextField(blank=True, default='')
    current_json_blob = models.TextField(blank=True, default='')
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        rep = ''

        if self.app_name:
            rep = u"%s | " % self.app_name

        if self.model_name:
            rep = u"%s%s | " % (rep, self.model_name)

        return u"%s%s" % (rep, self.timestamp)


class LogExtra(models.Model):
    """
    Log Extra model which is used for attaching extra filterable
    data to log objects.
    """
    log = models.ForeignKey(Log, related_name="extras")
    field_name = models.CharField(db_index=True, max_length=255)
    field_value = models.CharField(db_index=True, max_length=255)

    class Meta:
        ordering = ["-log__timestamp"]

    def __unicode__(self):
        return self.log.__unicode__()
