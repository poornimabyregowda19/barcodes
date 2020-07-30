from django.db import models

# Create your models here.
from app.fields import CustomHStoreField
from app.json_schema import serial_number_validation
from common.models import BaseModel
from django_postgres_extensions.models.fields import HStoreField

class Feature(BaseModel):
    name = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Barcode(BaseModel):

    feature = models.OneToOneField('Feature', on_delete=models.CASCADE)
    serial_number = CustomHStoreField(schema = serial_number_validation)
    num_modules_horizontal = models.IntegerField(default=0)
    num_modules_vertical = models.IntegerField(default=0)

    def validate_row(self):
        if not self.num_modules_horizontal:
            raise ValueError("required value", code = "invalid")

    def validate_column(self):
        if not self.num_modules_vertical:
            raise ValueError("required value", code = "invalid")

    def validate_serialnumbers(self):
        keys = getattr(self, 'serial_number').keys()
        for row,column in [key.split(":") for key in keys]:
            if int(row) > self.num_modules_horizontal:
                raise ValueError("module has row number greater than actual row" , code = "invalid")
            if int(column) > self.num_modules_vertical:
                raise ValueError("module has column number greater than actual column" , code = "invalid")

    def clean(self):
        self.get_uid()



