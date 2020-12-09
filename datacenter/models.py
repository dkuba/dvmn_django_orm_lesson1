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

    def get_visit_info(self, max_seconds=3600):
        return {"who_entered": self.passcard.owner_name, "entered_at": self.entered_at,
                "duration": self.get_visit_duration(), "is_strange": self.is_visit_too_long(max_seconds)}

    def get_visit_duration(self):
        if not self.leaved_at:
            leaved_time = django.utils.timezone.localtime()
        else:
            leaved_time = self.leaved_at

        time_delta = leaved_time - self.entered_at

        return time_delta

    def is_visit_too_long(self, max_seconds):
        return self.get_visit_duration().total_seconds() > max_seconds

