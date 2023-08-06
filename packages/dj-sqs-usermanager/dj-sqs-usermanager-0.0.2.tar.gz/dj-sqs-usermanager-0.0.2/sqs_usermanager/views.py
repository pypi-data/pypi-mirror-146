from django.http import JsonResponse

from .api import process_messages_queue


def notification_about_queue(request):

    process_messages_queue()

    return JsonResponse({})
