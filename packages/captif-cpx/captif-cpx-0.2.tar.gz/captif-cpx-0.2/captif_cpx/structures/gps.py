from pydantic import BaseModel
from pyrsona import BaseStructure


class GpsFileStructure(BaseStructure):
    pass


class _e201ae2b(GpsFileStructure):

    structure = (
        "system_time,sample_count,gps_time,latitude_nmea,longitude_nmea,speed_kph\n"
    )

    class row_model(BaseModel):
        system_time: str
        sample_count: int
        gps_time: str
        latitude_nmea: float
        longitude_nmea: float
        speed_kph: float
