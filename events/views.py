from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
from .models import Event
from .forms import EventForm
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_datetime
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed:index')  # перенаправление на главную
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})
def events_list(request):
    """Список подій (HTML) і віджет календаря"""
    events = Event.objects.order_by("-start")[:20]
    return render(request, "events/events_list.html", {"events": events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.creator = request.user
            ev.save()
            return redirect("events:event_detail", event_id=ev.id)
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form, "action": "create"})

@login_required
def event_edit(request, event_id):
    ev = get_object_or_404(Event, id=event_id)
    if ev.creator != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Нема доступу")
    if request.method == "POST":
        form = EventForm(request.POST, instance=ev)
        if form.is_valid():
            form.save()
            return redirect("events:event_detail", event_id=ev.id)
    else:
        form = EventForm(instance=ev)
    return render(request, "events/event_form.html", {"form": form, "action": "edit", "event": ev})

@login_required
def event_delete(request, event_id):
    ev = get_object_or_404(Event, id=event_id)
    if ev.creator != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Нема доступу")
    if request.method == "POST":
        ev.delete()
        return redirect("events:events_list")
    return render(request, "events/event_confirm_delete.html", {"event": ev})

# API для календаря (FullCalendar)
def events_api(request):
    """
    Повертає події у форматі, який розуміє FullCalendar.
    Можна додати фільтр по діапазону через GET-параметри start,end.
    """
    qs = Event.objects.all()
    start = request.GET.get("start")
    end = request.GET.get("end")
    if start:
        # FullCalendar присилає ISO-8601 дати — працює як фільтр
        try:
            s = parse_datetime(start)
            if s:
                qs = qs.filter(end__gte=s) | qs.filter(start__gte=s)
        except:
            pass
    if end:
        try:
            e = parse_datetime(end)
            if e:
                qs = qs.filter(start__lte=e) | qs.filter(end__lte=e)
        except:
            pass

    events = []
    for ev in qs:
        events.append({
            "id": ev.id,
            "title": ev.title,
            "start": ev.start.isoformat(),
            "end": ev.end.isoformat() if ev.end else None,
            "allDay": ev.all_day,
            "url": reverse("events:event_detail", args=[ev.id])
        })
    return JsonResponse(events, safe=False)
