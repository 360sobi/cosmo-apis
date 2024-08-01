from django.urls import path
from .views import zoom_authorize_view, zoom_callback_view, CreateMeeting

urlpatterns = [
    path('authorize/', zoom_authorize_view, name='zoom_authorize'),
    path('callback/', zoom_callback_view, name='zoom_callback'),
    path('create-meeting/', CreateMeeting.as_view(), name='create_meeting'),
]