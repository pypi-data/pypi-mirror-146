from pydantic import BaseModel
from pyrsona import BaseStructure


class SlowdataFileStructure(BaseStructure):
    pass


class _9357a6f3(SlowdataFileStructure):

    structure = "system_time,sample_count,left_tyre_temperature,left_road_temperature,right_tyre_temperature,right_road_temperature,air_temperature,passing_truck,other_flag\n"

    class row_model(BaseModel):
        system_time: str
        sample_count: int
        left_tyre_temperature: float
        left_road_temperature: float
        right_tyre_temperature: float
        right_road_temperature: float
        air_temperature: float
        passing_truck: bool
        other_flag: bool
