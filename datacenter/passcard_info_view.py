import django

from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    # Программируем здесь
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        if not visit.leaved_at:
            leaved_time = django.utils.timezone.localtime()
        else:
            leaved_time = visit.leaved_at

        time_delta = leaved_time - visit.entered_at

        tmp_vitis_data = {
            "entered_at": visit.entered_at,
            "duration": time_delta,
            "is_strange": False}

        if time_delta.total_seconds() > 3600:
            tmp_vitis_data["is_strange"] = True

        this_passcard_visits.append(tmp_vitis_data)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }

    return render(request, 'passcard_info.html', context)
