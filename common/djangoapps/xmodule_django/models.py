from django.db import models
from xmodule.modulestore.locations import SlashSeparatedCourseKey, Location
from types import NoneType


class CourseKeyField(models.CharField):
    description = "A SlashSeparatedCourseKey object, saved to the DB in the form of a string"

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(CourseKeyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        assert isinstance(value, (NoneType, basestring, SlashSeparatedCourseKey))
        if not value:
            # handle empty string for models being created w/o fields populated
            return None
        if isinstance(value, basestring):
            return SlashSeparatedCourseKey.from_deprecated_string(value)
        else:
            return value

    def get_prep_value(self, value):
        assert isinstance(value, (NoneType, SlashSeparatedCourseKey))
        return value.to_deprecated_string() if value else ''

class LocationKeyField(models.CharField):
    description = "A Location object, saved to the DB in the form of a string"

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(LocationKeyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        assert isinstance(value, (NoneType, basestring, Location))
        if not value:
            return None
        if isinstance(value, basestring):
            return Location.from_deprecated_string(value)
        else:
            return value

    def get_prep_value(self, value):
        assert isinstance(value, Location)
        return value.to_deprecated_string() if value else ''
