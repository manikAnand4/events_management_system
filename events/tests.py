import pytest

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from events import (
    constants as events_constants,
    models as events_models
)


@pytest.mark.django_db
class TestEventViewSet:

    def setup_method(self):
        self.client = APIClient()

    def test_create_event_success(self):
        url = reverse('event-list')
        payload = {
            'name': 'Tech Talk',
            'start_time': '2025-07-21T10:00:00Z',
            'end_time': '2025-07-21T12:00:00Z',
            'location': 'Auditorium',
            'max_capacity': 100
        }

        response = self.client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert events_models.Events.objects.count() == 1

    def test_create_event_invalid_time_range(self):
        url = reverse('event-list')
        payload = {
            'name': 'Tech Talk',
            'start_time': '2025-07-21T15:00:00Z',
            'end_time': '2025-07-21T12:00:00Z',
            'location': 'Auditorium',
            'max_capacity': 100
        }

        response = self.client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert events_constants.INVALID_TIME_RANGE_MESSAGE == response.data.get('non_field_errors', [])[0]


    def test_list_events(self):
        events_models.Events.objects.create(
            name='Test Event',
            start_time='2025-07-21T10:00:00Z',
            end_time='2025-07-21T12:00:00Z',
            location='Test Hall',
            max_capacity=50
        )
        url = reverse('event-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1


@pytest.mark.django_db
class TestEventAttendeeAPIView:

    def setup_method(self):
        self.client = APIClient()

    def test_list_attendees(self):
        event = events_models.Events.objects.create(
            name='Hackathon',
            start_time='2025-07-21T10:00:00Z',
            end_time='2025-07-21T12:00:00Z',
            location='Lab',
            max_capacity=10
        )

        events_models.EventRegistration.objects.create(
            name='Manik', email='manik@example.com', event=event
        )

        url = reverse('event-attendees-list', kwargs={'event_id': event.id}) 
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['email'] == 'manik@example.com'


@pytest.mark.django_db
class TestEventRegistrationAPIView:

    def setup_method(self):
        self.client = APIClient()

    def test_register_user_success(self):
        event = events_models.Events.objects.create(
            name='Workshop',
            start_time='2025-07-21T10:00:00Z',
            end_time='2025-07-21T12:00:00Z',
            location='Room 1',
            max_capacity=2
        )

        url = reverse('participant-registration', kwargs={'event_id': event.id})
        payload = {
            'name': 'Bob',
            'email': 'bob@example.com'
        }

        response = self.client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert events_models.EventRegistration.objects.filter(event=event).count() == 1

    def test_register_duplicate_email(self):
        event = events_models.Events.objects.create(
            name='Seminar',
            start_time='2025-07-21T10:00:00Z',
            end_time='2025-07-21T12:00:00Z',
            location='Hall A',
            max_capacity=5
        )

        events_models.EventRegistration.objects.create(
            name='Tom',
            email='tom@example.com',
            event=event
        )

        url = reverse('participant-registration', kwargs={'event_id': event.id})
        payload = {
            'name': 'Tom Again',
            'email': 'tom@example.com'
        }

        response = self.client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert events_constants.ALREADY_REGISTERED_MESSAGE == response.data.get('email', [])[0]

    def test_register_capacity_exceeded(self):
        event = events_models.Events.objects.create(
            name='Limited Workshop',
            start_time='2025-07-21T10:00:00Z',
            end_time='2025-07-21T12:00:00Z',
            location='Room B',
            max_capacity=1
        )

        events_models.EventRegistration.objects.create(
            name='Jane', email='jane@example.com', event=event
        )

        url = reverse('participant-registration', kwargs={'event_id': event.id})
        payload = {
            'name': 'Jake',
            'email': 'jake@example.com'
        }

        response = self.client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert events_constants.MAX_CAPACITY_REACHED_MESSAGE == response.data.get('non_field_errors', [])[0]
