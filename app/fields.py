from django_postgres_extensions.models.fields import HStoreField
from jsonschema import validate, exceptions as jsonschema_exceptions
from django.core import exceptions
from django.db.models import base

class CustomHStoreField(HStoreField):

    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop('schema', None)
        super().__init__(*args, **kwargs)

    def _validate_schema(self, value):
        if self.model.__module__ == '__fake__':
            return True
        try:
            status = validate(value, self.schema)
        except jsonschema_exceptions.ValidationError as e:
            raise exceptions.ValidationError(e.message, code='invalid')
        return status

    def _split_check_string(self, value):
        try:
            int_list = list(map(str, value.split(":")))
            if not len(int_list) == 2: return False
        except:
            return False
        return True

    def _validate_keys(self, value):
        keys = value.keys() or []
        if not all(self._split_check_string(key) for key in keys):
            message = "key should be in format of 'row:colomn'"
            raise exceptions.ValidationError(message, code='invalid')

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        self._validate_schema(value)
        self._validate_keys(value)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value and not self.null:
            self._validate_schema(value)
            self._validate_keys(value)
        return value