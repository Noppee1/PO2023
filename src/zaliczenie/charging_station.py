from model import *
from uuid import uuid4


class ChargingStatus(Enum):
    FREE = "FREE"
    CHARGING = "CHARGING"
    OCCUPIED = "OCCUPIED"
    FINISHED = "FINISHED"


class Chargerstatus(Enum):
    FREE = "FREE"
    CHARGING = "CHARGING"
    ERROR = "ERROR"
    FINISHED = "FINISHED"


class ChargingService:
    def __init__(self):
        self.chargers = []
        self.cars = []
        self.clients = []
        self.time_modifier = 1.0

    def add_charger(
        self, name: str, max_current_kw: int, max_current=None, charger_name=None
    ):
        charger = {
            "charger_name": name,
            "max_current": max_current_kw,
            "attached_vin": "",
        }
        self.chargers.append(charger)

    def add_car(self, client_id, vin: str, total_charged_kwh: int, max_current_kw: int):
        car = {
            "client_id": client_id,
            "vin": vin,
            "total_charged_kwh": total_charged_kwh,
            "max_current_kw": max_current_kw,
            "status": ChargingStatus.FREE,
        }
        self.cars.append(car)

    def addClientAccount(self, name: str, funds: float):
        client = {
            "id": uuid4(),
            "name": name,
            "funds": funds,
            "status": ChargingStatus.FREE,
        }
        self.clients.append(client)

    def start_charging(
        self, client_id, vin, kwh, desired_current_kw, charger_name: int
    ):
        if (
            client_id in self.clients
            and vin in self.cars
            and charger_name in self.chargers
        ):
            for charger in self.chargers:
                if not charger["status"] == Chargerstatus.ERROR:

                    for client in self.clients:
                        if client["name"] == client_id:
                            client["funds"] = client["funds"] - 10

                    for car in self.cars:
                        if (
                            car["vin"] == vin
                            and car["max_current_kw"] < desired_current_kw
                        ):
                            car["status"] = ChargingStatus.CHARGING
                            car.total_charged_kwh += kwh

                    for charger in self.chargers:
                        if charger["name"] == charger_name:
                            charger.status = Chargerstatus.CHARGING
                else:
                    return TypeError("Charger disabled")

    def stop_charging(self, client_id, vin):

        for client in self.clients:
            if client["name"] == client_id:
                client.status = ChargingStatus.FINISHED

        for car in self.cars:
            if car["vin"] == vin:
                car.status = ChargingStatus.FINISHED

    def attach_charger(self, charger_name, vin):
        for charger in self.chargers:
            if charger["charger_name"] == charger_name:
                charger["status"] = ChargingStatus.OCCUPIED
                charger["attached_vin"] = vin

    def disable_charger(self, charger_name):
        for charger in self.chargers:
            if charger["charger_name"] == charger_name:
                charger["status"] = ChargingStatus.ERROR

    def enable_charger(self, charger_name):
        for charger in self.chargers:
            if charger["charger_name"] == charger_name:
                charger["status"] = ChargingStatus.FREE

    def remove_charger(self, charger_name):
        for charger in self.chargers:
            if charger["charger_name"] == charger_name:
                charger["status"] = ChargingStatus.FREE
                charger["attached_vin"] = ""
