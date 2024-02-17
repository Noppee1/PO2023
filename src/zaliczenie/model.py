from dataclasses import dataclass
from enum import Enum
from uuid import UUID


@dataclass
class ClientAccount:
    id: UUID
    name: str
    funds: float


@dataclass
class Car:
    vin: str
    total_charged_kwh: int
    max_current_kw: int


@dataclass
class ChargingSession:
    csid: int
    status: str
    current_kw: int
    total_kwh: int


@dataclass
class ChargingStatus(Enum):
    OPEN = "OPEN"
    ERROR = "ERROR"
    FINISHED = "FINISHED"


@dataclass
class Chargerstatus(Enum):
    FREE = "FREE"
    CHARGING = "CHARGING"
    ERROR = "ERROR"


@dataclass
class ChargingService:
    chargers: list["Charger"]
    time_modifier: float


@dataclass
class Charger:
    max_current_kw: int
    total_charged_kwh: int
    attached_car_vin: str
    status: ChargingStatus
