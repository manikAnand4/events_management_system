from django.urls import path, include
from rest_framework.routers import DefaultRouter

from events import views as event_views

router = DefaultRouter()
router.register('', event_views.EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    path(
        '<int:event_id>/attendees/',
        event_views.EventAttendeeAPIView.as_view(),
        name='event-attendees-list'
    ),
    path(
        '<int:event_id>/register/',
        event_views.EventRegistrationAPIView.as_view(),
        name='participant-registration'
    ),
]
