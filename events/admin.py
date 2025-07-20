from django.contrib import admin

from events import models as events_models


admin.site.register(events_models.Events)
admin.site.register(events_models.EventRegistration)
