from Models.models import SatelliteDatasets
from Models.pydantic_models import FilePath, SatelliteDatasetIn_Pydantic
from pathlib import Path
from geopandas import read_file
from time import time

def get_raw_satellite_datasets(satellite_dataset: SatelliteDatasetIn_Pydantic):
    parent_path = Path(__file__).resolve().parents[2]
    new_dir = parent_path/'processed_data'
    
    if not new_dir.exists():
        new_dir.mkdir()

    new_dir = new_dir/f'{satellite_dataset.satellite_name}_{satellite_dataset.dataset_type}'

    if not new_dir.exists():
        new_dir.mkdir()

    log = dict()

    for path in parent_path.rglob(f'*/*_{satellite_dataset.satellite_name}_*'):
        if path.suffix in ['.shp', '.csv']:
            log_read_geo_file = read_geo_file(path, new_dir, satellite_dataset)
            log.update(log_read_geo_file)
    return log

def read_geo_file(file_path: FilePath, new_dir: FilePath, satellite_dataset: SatelliteDatasetIn_Pydantic):
    start_time = time()
    gdf = read_file(rf'{file_path}')
    reading_file_time = (time() - start_time) / 60
    print('reading_file_time:', reading_file_time)
    start_time = time()
    gdf.columns= [x.lower() for x in gdf.columns]
    unique_values = gdf[satellite_dataset.dataset_type].unique()
    print(unique_values)
    path_dict = dict()
    
    for unique_value in unique_values:
        new_gdf = gdf[gdf[satellite_dataset.dataset_type]==unique_value]
        unique_value = unique_value.replace('-', '_')
        new_file_name = new_dir/f'{unique_value}.shp'
        new_gdf.to_file(new_file_name)
        path_dict.update({'unique_value': unique_value, 'path': new_file_name})
        print(path_dict)
        # await SatelliteDatasets.create(**satellite_dataset.dict(), dataset_path=str(new_dir/f'{unique_value}.shp'), user_id=current_user.id)
    del gdf, new_gdf

    writing_file_time=(time() - start_time)/60
    print('writing_file_time:', writing_file_time)
    return {'new_dir':new_dir, 'reading_file':reading_file_time, 'writing_file':writing_file_time, 'path_dict': path_dict}