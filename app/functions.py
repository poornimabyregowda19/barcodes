from django.db.models.expressions import Func, Expression
from django.db.models.sql.constants import GET_ITERATOR_CHUNK_SIZE
from django.utils import six
from django_postgres_extensions.models.expressions import F, Value as V


class CustomFunc(Func):
    def __init__(self, *values, **extra):
        values = list(values)
        for i, value in enumerate(values):
            if not isinstance(value, Expression):
                values[i] = V(value)
        super(CustomFunc, self).__init__(*values, **extra)


class HStoreAdd(CustomFunc):
    function = 'HSTORE'
    template = '"serial_number"  || %(function)s(%(expressions)s)'

