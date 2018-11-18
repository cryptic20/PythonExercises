class Aircraft:
    def __init__(self, number_of_passenger, model):
        self._number_of_passenger = number_of_passenger
        self._name = model

    def get_number_of_passengers(self):
        return self._number_of_passenger

    def get_name(self):
        return self._name


class IntercontinentalAircraft(Aircraft):
    def __init__(self, number_of_passenger, model, cargo_hold):
        Aircraft.__init__(self, number_of_passenger, model)
        self.__cargo_hold = cargo_hold

    def calculate_amount_of_fuel(self, km):
        return (.25 * km * self.get_number_of_passengers()) + (2 * km * self.__cargo_hold)

    @property
    def manifest(self):
        return 'Intercontinental flight {0}: passenger count {1}, cargo load {2}'\
            .format(self.get_name(), self.get_number_of_passengers(), self.__cargo_hold)


class ShortHaulAircraft(Aircraft):
    serial_number = -1

    def __init__(self, number_of_passenger, model):
        Aircraft.__init__(self, number_of_passenger, model)
        ShortHaulAircraft.serial_number += 1
        self.__serial_number = ShortHaulAircraft.serial_number

    def get_serial_number(self):
        return self.__serial_number

    def calculate_amount_of_fuel(self, km):
        return .1 * km * self.get_number_of_passengers()

    @property
    def manifest(self):
        return 'Short haul flight serial number {0}, name {1}: passenger count {2}'\
            .format(self.get_serial_number(), self.get_name(), self.get_number_of_passengers())


class ControlTower:
    def __init__(self):
        self.aircraft_hangar = []

    def add_aircraft(self, plane):
        self.aircraft_hangar.append(plane)

    def get_manifests(self):
        return [ac.manifest for ac in self.aircraft_hangar]


if __name__ == '__main__':
    intercontinental_flight = IntercontinentalAircraft(500, "Boeing-747", 100)
    short_haul_flight = ShortHaulAircraft(110, "Airbus-A220")
    short_haul_flight2 = ShortHaulAircraft(85, "Airbus-A220")

    print(short_haul_flight.get_serial_number())

    assert short_haul_flight.get_serial_number() == 0
    assert short_haul_flight2.get_serial_number() == 1

    assert short_haul_flight.get_number_of_passengers() == 110
    assert short_haul_flight.get_name() == "Airbus-A220"

    assert intercontinental_flight.get_number_of_passengers() == 500
    assert intercontinental_flight.get_name() == "Boeing-747"

    assert intercontinental_flight.calculate_amount_of_fuel(10000) == 3250000.
    assert short_haul_flight.calculate_amount_of_fuel(250) == 2750.

    assert intercontinental_flight.manifest == "Intercontinental flight Boeing-747: passenger count 500, cargo load 100"
    assert short_haul_flight2.manifest == "Short haul flight serial number 1, name Airbus-A220: passenger count 85"

    tower = ControlTower()
    tower.add_aircraft(intercontinental_flight)
    tower.add_aircraft(short_haul_flight)
    tower.add_aircraft(short_haul_flight2)

    air_traffic_report = tower.get_manifests()
    for aircraft in air_traffic_report:
        print(aircraft)

    # prints:
    # Intercontinental flight Boeing-747: passenger count 500, cargo load 100
    # Short haul flight serial number 0, name Airbus-A220: passenger count 110
    # Short haul flight serial number 1, name Airbus-A220: passenger count 85
