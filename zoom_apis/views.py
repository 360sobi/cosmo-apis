from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import get_zoom_authorization_url, fetch_zoom_token, get_zoom_oauth_session
import datetime


def zoom_authorize_view(request):
    authorization_url, state = get_zoom_authorization_url()
    request.session['oauth_state'] = state
    return redirect(authorization_url)


def zoom_callback_view(request):
    state = request.session.get('oauth_state')
    zoom = get_zoom_oauth_session(state=state)
    token = fetch_zoom_token(request.GET.get('code'))
    request.session['oauth_token'] = token
    return redirect('create_meeting')


class CreateMeeting(APIView):
    def post(self, request, *args, **kwargs):
        topic = request.POST.get('topic')
        start_time = request.POST.get('start_time')
        duration = request.POST.get('duration')
        password = request.POST.get('password', None)

        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

        token = request.session.get('oauth_token')
        zoom = get_zoom_oauth_session(token=token)
        url = "https://api.zoom.us/v2/users/me/meetings"
        payload = {
            "topic": topic,
            "type": 2,
            "start_time": start_time.isoformat(),
            "duration": duration,
            "password": password
        }
        response = zoom.post(url, json=payload)
        return Response(response.json(), status=status.HTTP_200_OK)
