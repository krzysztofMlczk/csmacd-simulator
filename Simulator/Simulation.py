import os
import time

from Signal import Signal, Directions


class Simulation:
    def __init__(self, carrier_len):
        self.carrier = [' ' for _ in range(carrier_len)]
        self.connected_stations = []
        self.inserted_signals = []
        self.collisions = 0

    def connect_station(self, station):
        self.connected_stations.append(station)

    def simulate(self, refresh_after, steps_to_perform):
        time1 = time.time()
        poc_info = {}
        step = 0

        for station in self.connected_stations:
            poc_info[station.place_of_connection] = station

        while step < steps_to_perform:
            # we want to execute code below after "refresh_after" seconds
            if time.time() - time1 >= refresh_after:
                self.cls()
                step += 1

                print('[' + ''.join(self.carrier) + ']')

                # poprawic wyswietlanie
                print('|' + ''.join([str(poc_info[i].name) if i in poc_info.keys()
                                     else ' ' for i in range(len(self.carrier))]) + '|')
                print('|' + ''.join(['w' if i in poc_info.keys() and poc_info[i].steps_to_wait != 0
                                     else ' ' for i in range(len(self.carrier))]) + '|')
                # print number of performed steps
                print('Step =', step, '/', steps_to_perform)
                self.step()
                time1 = time.time()

    def propagate(self):
        """perform specific steps for signals to propagate (change signals positions)"""
        to_remove = []

        for signal in self.inserted_signals:
            # shift signal to the specified direction in carrier
            signal.perform_step()
            # if signal out of carrier, then delete it
            if signal.position < 0 or signal.position >= len(self.carrier):
                to_remove.append(signal)
            # create new list of signals without these to remove
        self.inserted_signals = [s for s in self.inserted_signals if s not in to_remove]

    def update_carrier(self):
        """Apply changes to the carrier"""

        # clear the carrier
        for i in range(len(self.carrier)):
            self.carrier[i] = ' '

        for signal in self.inserted_signals:
            # J - indicates Jamming Signal
            if signal.signature == 'J':
                self.carrier[signal.position] = 'J'
                continue
            # If field is empty, place station signature
            if self.carrier[signal.position] == ' ':
                self.carrier[signal.position] = signal.signature
            # Don't change if its signal from the same station
            elif signal.signature == self.carrier[signal.position]:
                pass
            elif signal.signature != self.carrier[signal.position] and self.carrier[signal.position] != 'J':
                self.carrier[signal.position] = '!'

    def step(self):
        """method to perform one step - propagate signals and update carrier state"""
        self.propagate()

        for station in self.connected_stations:
            signature = station.broadcast(self.carrier, self.get_signal(station.place_of_connection))
            if signature is not None:
                signal_to_the_right = Signal(
                    starting_pos=station.place_of_connection,
                    signature=signature,
                    direction=Directions.RIGHT)
                signal_to_the_left = Signal(
                    starting_pos=station.place_of_connection,
                    signature=signature,
                    direction=Directions.LEFT)
                self.inserted_signals.append(signal_to_the_right)
                self.inserted_signals.append(signal_to_the_left)
        # apply changes to the carrier
        self.update_carrier()

    def get_signal(self, pos):
        for s in self.inserted_signals:
            if s.position == pos:
                return s
        return None

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def increment_collisions(self, amount):
        self.collisions += 1

    def display_collisions(self):
        print("Total collisions amount: " + str(self.collisions / len(self.connected_stations)))

    def get_instance(self):
        return self
