from Models.pydantic_models import SatelliteDataset_Pydantic, SatelliteDatasetIn_Pydantic, User_Pydantic, UserIn_Pydantic, Status
from Models.models import SatelliteDatasets

from services.users_services import get_current_user
from services.datasets_services import get_raw_satellite_datasets
from fastapi import APIRouter, Security, HTTPException
from typing import List

router = APIRouter()

@router.get('/datasets/', response_model=List[SatelliteDataset_Pydantic], tags=['datasets'])
async def get_all_dataset():
    return await SatelliteDataset_Pydantic.from_queryset(SatelliteDatasets.all())

@router.post('/datasets/', tags=["datasets"])
async def create_datasets(satellite_dataset: SatelliteDatasetIn_Pydantic):
    return get_raw_satellite_datasets(satellite_dataset, current_user)