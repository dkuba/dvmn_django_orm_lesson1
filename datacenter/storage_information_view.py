import django

from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    non_closed_visits = []
    for visit in Visit.objects.filter(leaved_at=None):
        non_closed_visits.append({})
        non_closed_visits[-1]["who_entered"] = visit.passcard.owner_name
        non_closed_visits[-1]["entered_at"] = django.utils.timezone.localtime(visit.entered_at)
        time_delta = django.utils.timezone.localtime() - visit.entered_at
        non_closed_visits[-1]["duration"] = django.utils.timezone.localtime() - visit.entered_at
        if time_delta.total_seconds() > 3600:
            non_closed_visits[-1]["is_strange"] = True
        else:
            non_closed_visits[-1]["is_strange"] = False

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
