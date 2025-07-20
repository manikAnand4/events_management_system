from django.db import models

from commons import (
    constants as commons_constants,
    models as commons_models
)


class Events(commons_models.DatesModel):
    """
    Model to represent an event. 
    """

    name = models.CharField(max_length=commons_constants.CHAR_FIELD_MAX_LENGTH)
    location = models.CharField(max_length=commons_constants.CHAR_FIELD_MAX_LENGTH, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    max_capacity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['created_at']


class EventRegistration(commons_models.DatesModel):
    """
    Model to represent a registration for an event.
    NOTE:
    Not using django's auth user model as user can register for different events with the
    different emails, and we are not tracking user accounts and providing signup/login functionality for now.
    For further scalability, we can consider using a custom user model in future.
    """

    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='registrations')
    email = models.EmailField(max_length=commons_constants.EMAIL_FIELD_MAX_LENGTH)
    name = models.CharField(max_length=commons_constants.CHAR_FIELD_MAX_LENGTH)

    def __str__(self):
        return f"{self.email} - {self.event.name}"

    class Meta:
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"
        ordering = ['created_at']
        unique_together = ('event', 'email') # Ensure a user can register only once for an event
