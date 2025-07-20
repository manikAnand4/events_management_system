from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics

from events import (
    models as events_models,
    paginations as events_pagination,
    serializers as events_serializers
)


class EventViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet for creating and listing events.
    """
    queryset = events_models.Events.objects.all()
    serializer_class = events_serializers.EventCreateListSerializer
    pagination_class = events_pagination.EventPagination


class EventAttendeeAPIView(generics.ListAPIView):
    """
    View for handling student registration for events.
    """
    queryset = events_models.EventRegistration.objects.all()
    serializer_class = events_serializers.EventAttendeeListSerializer
    pagination_class = events_pagination.EventAttendeeListPagination


class EventRegistrationAPIView(generics.CreateAPIView):
    """
    View for handling student registration for events.
    """
    serializer_class = events_serializers.EventRegistrationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['event'] = get_object_or_404(
            events_models.Events.objects.prefetch_related('registrations'),
            id=self.kwargs['event_id']
        )

        return context
