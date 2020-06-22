from Station import Station
from Simulation import Simulation


simulation = Simulation(carrier_len=100)
station_a = Station(name='A', signature='a', place_of_connection=1, probability=50)
station_b = Station(name='B', signature='b', place_of_connection=50, probability=10)
station_c = Station(name='C', signature='c', place_of_connection=99, probability=50)

simulation.connect_station(station=station_a)
simulation.connect_station(station=station_b)
simulation.connect_station(station=station_c)

simulation.simulate(refresh_after=0.3, steps_to_perform=2000)











#simulation.display_collisions()
#print("Total collisions amount: ", 29)
















#simulation.connect_station(station_b)
#simulation.connect_station(station_c)


#station_b = Station(name='B', signature='b', place_of_connection=50, probability=100)
#station_c = Station(name='C', signature='c', place_of_connection=99, probability=10)