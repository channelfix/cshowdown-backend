# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest
)
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.forms.models import model_to_dict
from .models import Event, Entry
import datetime
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class CreateEventView(View):
    def post(self, request, **kwargs):
        context = {}
        event_name = request.POST.get('eventName', None)
        description = request.POST.get('eventDescription', None)
        # date_created = timezone.now()
        date_event = parse_datetime(request.POST.get('eventDate', None))
        user = User.objects.get(username=request.POST.get('username', None))
        prize = request.POST.get('prize', None)
        # creator = request.user.id
        event = Event.objects.get(
            creator_id=user.id,
            status__gte=0,
            status__lte=1
        )
        if event is not None:
            return HttpResponseBadRequest(
                "You already have an upcoming or ongoing event right now"
            )

        event = Event(
            event_name=event_name,
            description=description,
            # date_created=date_created,
            date_event=date_event,
            creator=user,
            prize=prize,
        )
        event.save()
        context['status'] = "created"
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class SendEntryView(View):
    def post(self, request, **kwargs):
        context = {}
        event_id = request.POST.get('event_id', None)
        username = request.POST.get('username', None)
        user = User.objects.get(username=username)
        entry, created = Entry.objects.get_or_create(event_id=event_id,
                                                     user_id=user.id,
                                                     entry_status=0)
        if created:
            context['status'] = "Entry sent"
            entry.save()
            return JsonResponse(context)
        else:
            return HttpResponseBadRequest("You have already sent your entry")


@method_decorator(csrf_exempt, name='dispatch')
class AllEntriesView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        entries = list(Entry.objects.filter(event_id=event_id).values())
        for entry in entries:
            entry['username'] = User.objects.get(pk=entry['user_id']).username
        context = {
            'entries': entries
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class UpcomingEventsView(View):
    def get(self, request, **kwargs):
        events = list(Event.objects.filter(status=0).values())
        context = {
            'events': events
        }
        for event in context['events']:
            event['date_event'] = event['date_event'].replace(tzinfo=None)
            user = User.objects.get(pk=event['creator_id'])
            event['creator_name'] = user.username
            if event['contestant1_id'] is not None:
                user = User.objects.get(pk=event['contestant1_id'])
                event['contestant1_name'] = user.username
            else:
                event['contestant1_name'] = ""
            if event['contestant2_id'] is not None:
                user = User.objects.get(pk=event['contestant2_id'])
                event['contestant2_name'] = user.username
            else:
                event['contestant2_name'] = ""
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class OngoingEventsView(View):
    def get(self, request, **kwargs):
        events = list(Event.objects.filter(status=1).values())
        context = {
            'events': events
        }
        for event in context['events']:
            event['date_event'] = event['date_event'].replace(tzinfo=None)
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class FinishedEventsView(View):
    def get(self, request, **kwargs):
        events = list(Event.objects.filter(status=2).values())
        context = {
            'events': events
        }
        for event in context['events']:
            event['date_event'] = event['date_event'].replace(tzinfo=None)
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class ApproveEntryView(View):
    def post(self, request, **kwargs):
        context = {}
        entry_id = request.POST.get('entry_id', None)
        entry = Entry.objects.get(id=entry_id)
        event = Event.objects.get(id=entry.event.id)
        if entry.entry_status != 2:
            if not event.contestant1:
                event.contestant1 = entry.user
                entry.entry_status = 2
                entry.save()
                event.save()
                context['status'] = "Approved"
                return JsonResponse(context)
            elif not event.contestant2:
                event.contestant2 = entry.user
                entry.entry_status = 2
                entry.save()
                event.save()
                context['status'] = "Approved"
                return JsonResponse(context)
            else:
                return HttpResponseNotFound("Cannot approve entry")
        else:
            return HttpResponseNotFound("Entry already approved")


@method_decorator(csrf_exempt, name='dispatch')
class RejectEntryView(View):
    def post(self, request, **kwargs):
        context = {}
        entry_id = request.POST.get('entry_id', None)
        entry = Entry.objects.get(id=entry_id)
        event = Event.objects.get(id=entry.event.id)
        if event.contestant1_id == entry.user_id:
            event.contestant1 = None
        else:
            event.contestant2 = None
        entry.entry_status = 1
        entry.save()
        event.save()
        context['status'] = "Rejected"
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class CreatorEventProfileView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        user = User.objects.get(username=username)
        event = Event.objects.get(
            creator_id=user.id,
            status__lte=1,
            status__gte=0)
        eventdict = model_to_dict(event)
        eventdict['date_event'] = eventdict['date_event'].replace(tzinfo=None)
        eventdict['creator_name'] = event.creator.username
        if eventdict['contestant1'] is not None:
            user = User.objects.get(pk=eventdict['contestant1'])
            eventdict['contestant1_name'] = user.username
        else:
            eventdict['contestant1_name'] = ""
        if eventdict['contestant2'] is not None:
            user = User.objects.get(pk=eventdict['contestant2'])
            eventdict['contestant2_name'] = user.username
        else:
            eventdict['contestant2_name'] = ""
        context = {
            'event': eventdict
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class EventProfileView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = model_to_dict(Event.objects.get(id=event_id))
        context = {
            'event': event
        }
        return JsonResponse(context)
