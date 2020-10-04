from tortoise.fields import IntField, CharField, TextField, DatetimeField, ForeignKeyField, FloatField, ForeignKeyRelation, ReverseRelation
from tortoise.models import Model

class Users(Model):

    id = IntField(pk=True)
    name = CharField(max_length=100)
    email = CharField(max_length=50, unique=True)
    password = CharField(max_length=255)

    satellite_dataset: ReverseRelation["SatelliteDatasets"]

class SatelliteDatasets(Model):

    id = IntField(pk=True)
    satellite_name = CharField(max_length=50)
    dataset_path = TextField()
    dataset_type = CharField(max_length=50)

    # class PydanticMeta:
    #     exclude = ['dataset_path']

    # user: ForeignKeyRelation[Users] = ForeignKeyField('models.Users', related_name='satellite_dataset')
    data_visualization: ReverseRelation['DataVisualization']

class DataVisualization(Model):

    id = IntField(pk=True)
    image_name = CharField(max_length=100)

    satellite_dataset: ForeignKeyRelation[SatelliteDatasets] = ForeignKeyField('models.SatelliteDatasets', related_name='data_visualization')
