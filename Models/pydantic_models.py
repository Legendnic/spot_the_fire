from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from typing import List, Optional
from Models import models
from pathlib import WindowsPath
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    scopes: List[str] = []

class Status(BaseModel):
    message: str

class FilePath(BaseModel):
    file_path: WindowsPath
User_Pydantic = pydantic_model_creator(models.Users, name='User')
UserIn_Pydantic = pydantic_model_creator(models.Users, name='UserIn', exclude_readonly=True)

SatelliteDataset_Pydantic = pydantic_model_creator(models.SatelliteDatasets, name="SatelliteDataset")
SatelliteDatasetIn_Pydantic = pydantic_model_creator(models.SatelliteDatasets, name="SatelliteDatasetIn", exclude_readonly=True, exclude=['dataset_path'])

DataVisualization_Pydantic = pydantic_model_creator(models.DataVisualization, name='DataVisualization')
DataVisualizationIn_Pydantic = pydantic_model_creator(models.DataVisualization, name='DataVisualizationIn', exclude_readonly=True)