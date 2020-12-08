import django
from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    @property
    def data_dict(self):
        if not self.leaved_at:
            leaved_time = django.utils.timezone.localtime()
        else:
            leaved_time = self.leaved_at

        time_delta = leaved_time - self.entered_at

        tmp_vitis_data = {
            "who_entered": self.passcard.owner_name,
            "entered_at": self.entered_at,
            "duration": time_delta,
            "is_strange": False}

        if time_delta.total_seconds() > 3600:
            tmp_vitis_data["is_strange"] = True

        return tmp_vitis_data
