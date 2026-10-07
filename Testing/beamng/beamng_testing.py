import time
import beamngpy
import beamngpy.sensors as bns


def main() -> None:
    bng: beamngpy.BeamNGpy = beamngpy.BeamNGpy(
        host="localhost",
        port=64256,
        home="E:\\SteamLibrary\\steamapps\\common\\BeamNG.drive\\",
        user="C:\\Git\\DashAR\\Build\\DAS\\BeamNGUser\\",
    )

    bng.open()

    scenario: beamngpy.Scenario = beamngpy.Scenario("west_coast_usa", "Test")
    vehicle: beamngpy.Vehicle = beamngpy.Vehicle(
        vid="ego_vehicle", model="etk800", license="DashAR"
    )

    vehicle.sensors.attach("electrics", bns.Electrics())

    scenario.add_vehicle(
        vehicle=vehicle, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795)
    )

    scenario.make(bng=bng)

    bng.scenario.load(scenario=scenario)
    bng.scenario.start()

    while True:
        vehicle.sensors.poll("electrics")

        speed_mps: float = vehicle.sensors["electrics"]["wheelspeed"]
        speed_mph: float = speed_mps * 2.236936

        print(f"Speed: {speed_mph:.1f} mph")
        time.sleep(0.1)


if __name__ == "__main__":
    main()
