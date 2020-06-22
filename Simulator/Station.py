import random


class Station:
    """Class of device which can be connected to the carrier"""
    def __init__(self, name, signature, place_of_connection, probability): #, simulation):
        self.name = name
        self.signature = signature
        self.place_of_connection = place_of_connection
        self.probability_of_broadcasting = probability
        # number of signals left to broadcast if > 0 then still broadcasting
        self.left_to_broadcast = 0
        self.steps_to_wait = 0  # number of steps to wait
        # counter for how many collisions in a row lets us know from what numbers
        # should station draw when detects a collison
        self.collisions_ina_row = 0
        #self.simulation = simulation

    def send(self, jamming):
        # everytime station sends signal, then decrement number of signals left to broadcast
        self.left_to_broadcast -= 1
        # return 'J' as signature when station should send jamming signal
        if jamming and self.left_to_broadcast > 0:
            return 'J'
        # if broadcasted everything, then reset number of collisions
        if self.left_to_broadcast == 0:
            self.collisions_ina_row = 0
        # return None if shouldnt broadcast anymore
        if self.left_to_broadcast <= 0:
            return None

        return self.signature

    def backoff_randomizer(self):
        i = self.collisions_ina_row
        if i <= 10:
            return list(range(0, 2**i))
        elif 10 < i < 16:
            return list(range(0, 2**10))
        else:
            return None

    def broadcast(self, carrier, signal):
        # don't send jamming signal by deafult
        jamming = False

        # decrease amount of steps to wait through if already waiting
        # station is in waiting state only when detected collision earlier
        # so station has to send jamming signal when detected a collison!
        if self.steps_to_wait > 0:
            jamming = True
            self.steps_to_wait -= 1

        # If there is something else than free field in the carrier
        elif carrier[self.place_of_connection] != ' ':
            # If already sending and detects a collision - !
            if self.steps_to_wait == 0 and carrier[self.place_of_connection] == '!' and self.left_to_broadcast > 0:
                # if collision detected then increment collision in a row
                #self.simulation.increment_collisions(self.collisions_ina_row)
                self.collisions_ina_row += 1
                # randomize how many time gaps to wait (time gap is 2*carrier_len)
                # it is a part of backoff algorithm which allows to avoid conitnuous collisions
                how_many_gaps_to_wait = self.backoff_randomizer()
                # if there was 16 collisions in a row, then return and print that simulation failed:
                if how_many_gaps_to_wait is None:
                    print("ERROR: Too many waiting turns in a row")
                    return
                # when station knows it has been collision, then start to broadcast
                # Jamming signal 'J' and broadcast for 2*carrier_len steps so everyone knows about the collision
                jamming = True
                self.left_to_broadcast = 2 * len(carrier)
                self.steps_to_wait = random.choice(how_many_gaps_to_wait) * 2 * len(carrier)

        p = random.randint(0, 100)

        if self.steps_to_wait == 0 and self.left_to_broadcast <= 0 and p <= self.probability_of_broadcasting:
            if signal is None:
                self.left_to_broadcast = 2 * len(carrier)

        return self.send(jamming)
