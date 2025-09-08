from typing import List
from pydantic import BaseModel, field_validator, ConfigDict


class Coordinate(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("coordinates", mode="after")
    @classmethod
    def validate_coordinate(cls, coordinates: List[float]) -> List[float]:
        if len(coordinates) != 2:
            raise ValueError(
                "coordinates must be in format [longitude, latitude]",
            )

        longitude, latitude = coordinates
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")

        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")

        return coordinates
