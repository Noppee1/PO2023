import unittest


# from time import sleep

from charging_station import *
from uuid import uuid4

# from errors import *

# we're all gonna die


class ChargingServiceTests(unittest.TestCase):

    def setUp(self):
        self.station = ChargingService()

    def test_add_charger(self):
        self.station.add_charger("charger1", 50)
        self.assertEqual(len(self.station.chargers), 1)
        self.assertEqual(self.station.chargers[0]["charger_name"], "charger1")
        self.assertEqual(self.station.chargers[0]["max_current"], 50)

    def test_add_client_account(self):
        name = "Test name"
        funds = 1000.0
        initial_clients_count = len(self.station.clients)

        self.station.addClientAccount(name, funds)
        self.assertEqual(len(self.station.clients), 1)
        self.assertEqual(self.station.clients[0]["name"], name)
        self.assertEqual(self.station.clients[0]["funds"], funds)
        self.assertIsNotNone(self.station.clients[0]["id"])

    def test_add_car(self):
        client_id = uuid4()
        vin = "123abc"
        total_charged_kwh = 100
        max_current_kw = 50
        self.station.add_car(client_id, vin, total_charged_kwh, max_current_kw)
        self.assertEqual(len(self.station.cars), 1)
        self.assertEqual(self.station.cars[0]["client_id"], client_id)
        self.assertEqual(self.station.cars[0]["vin"], vin)
        self.assertEqual(self.station.cars[0]["total_charged_kwh"], total_charged_kwh)
        self.assertEqual(self.station.cars[0]["max_current_kw"], max_current_kw)
        self.assertEqual(self.station.cars[0]["status"], ChargingStatus.FREE)

    def test_start_charging(self):
        self.station.addClientAccount("Test name", 100)
        self.station.add_car(uuid4(), "123abc", 0, 50)
        self.station.add_charger("charger1", 50)

        initial_funds = self.station.clients[0]["funds"]
        initial_status = self.station.cars[0]["status"]

        self.station.start_charging("Test name", "123abc", 10, 50, "charger1")

        self.assertEqual(self.station.clients[0]["funds"], initial_funds - 10)
        self.assertEqual(self.station.cars[0]["status"], ChargingStatus.CHARGING)
        self.assertEqual(self.station.chargers[0]["status"], ChargingStatus.CHARGING)

    def test_stop_charging(self):
        self.station.addClientAccount("Test name", 100)
        self.station.add_car(uuid4(), "123abc", 0, 50)
        self.station.add_charger("charger1", 50)
        self.station.start_charging("Test name", "123abc", 10, 50, "charger1")

        self.station.stop_charging("Test name", "123abc")

        self.assertEqual(self.station.clients[0]["status"], ChargingStatus.FREE)
        self.assertEqual(self.station.cars[0]["status"], ChargingStatus.FREE)
        self.assertEqual(self.station.chargers[0]["status"], ChargingStatus.FREE)

    def test_start_charging(self):
        self.station.addClientAccount("Test name", 100)
        self.station.add_car(uuid4(), "123abc", 0, 50)
        self.station.add_charger("charger1", 50)

        initial_funds = self.station.clients[0]["funds"]
        initial_status = self.station.cars[0]["status"]

        self.station.start_charging("Test name", "123abc", 10, 50, "charger1")

        self.assertEqual(self.station.clients[0]["funds"], initial_funds - 10)
        self.assertEqual(self.station.cars[0]["status"], ChargingStatus.CHARGING)
        self.assertEqual(self.station.chargers[0]["status"], ChargingStatus.CHARGING)

    def test_stop_charging(self):
        self.station.addClientAccount("Test name", 100)
        self.station.add_car(uuid4(), "123abc", 0, 50)
        self.station.add_charger("charger1", 50)
        self.station.start_charging("Test name", "123abc", 10, 50, "charger1")

        self.station.stop_charging("Test name", "123abc")

        self.assertEqual(self.station.clients[0]["status"], ChargingStatus.FREE)
        self.assertEqual(self.station.cars[0]["status"], ChargingStatus.FREE)
        self.assertEqual(self.station.chargers[0]["status"], ChargingStatus.FREE)

    def test_attach_charger(self):
        self.station.add_car(uuid4(), "123abc", 0, 50)
        self.station.add_charger("charger1", 50)

        self.station.attach_charger("charger1", "123abc")

        self.assertEqual(self.station.chargers[0]["status"], ChargingStatus.OCCUPIED)
        self.assertEqual(self.station.chargers[0]["attached_vin"], "123abc")

    def test_disable_charger(self):
        self.station.add_charger("charger1", 50)

        self.station.disable_charger("charger1")

        self.assertEqual(self.station.chargers[0]["status"], ChargingStatus.ERROR)

    def test_enable_charger(self):
        self.station.add_charger("charger1", 50)
        self.station.disable_charger("charger1")

        self.station.enable_charger("charger1")

        self.assertEqual(self.station.chargers[0]["status"], ChargingStatus.FREE)

    def test_remove_charger(self):
        self.station.add_charger("charger1", 50)
        self.station.attach_charger("charger1", "ABC123")

        self.station.remove_charger("charger1")

        self.assertEqual(self.station.chargers[0]["status"], ChargingStatus.FREE)
        self.assertEqual(self.station.chargers[0]["attached_vin"], "")
