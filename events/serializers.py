from rest_framework import serializers

from events import (
    constants as events_constants,
    models as events_models
)


class EventCreateListSerializer(serializers.ModelSerializer):
    """
    Serializer used for event creation and listing.
    """

    def validate(self, attrs):
        # validate if date range is valid
        if attrs.get('start_time') and attrs.get('end_time'):
            if attrs['start_time'] >= attrs['end_time']:
                raise serializers.ValidationError(events_constants.INVALID_TIME_RANGE_MESSAGE)
        
        return super().validate(attrs)

    class Meta:
        model = events_models.Events
        fields = (
            'id', 'name', 'start_time', 'end_time', 'location', 'max_capacity',
        )
        read_only_fields = ('id',)


class EventAttendeeListSerializer(serializers.ModelSerializer):
    """
    Serializer used for event attendee list.
    """

    class Meta:
        model = events_models.EventRegistration
        fields = ('id', 'name', 'email')


class EventRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer used for event registration.
    """
    class Meta:
        model = events_models.EventRegistration
        fields = ('name', 'email', 'id')
        read_only_fields = ('id',)

    def validate_email(self, value):
        if events_models.EventRegistration.objects.filter(
            email=value, event_id=self.context['event'].id
        ).exists():
            raise serializers.ValidationError(events_constants.ALREADY_REGISTERED_MESSAGE)

        return value
    
    def validate(self, attrs):
        max_capacity = self.context['event'].max_capacity
        # Check if the event has a maximum capacity and if it has been reached
        if max_capacity and self.context['event'].registrations.count() >= max_capacity:
            raise serializers.ValidationError(events_constants.MAX_CAPACITY_REACHED_MESSAGE)

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['event_id'] = self.context['event'].id
    
        return super().create(validated_data)

