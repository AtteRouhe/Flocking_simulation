from boid import Boid


# holds the boids and some parameters for the simulation
class World:

    # screen size
    MAX_X = 1000
    MAX_Y = 1000

    def __init__(self):
        # holds all the boid objects
        self.boids = []
        # weights for the 3 rules
        self.sep_w = 0
        self.coh_w = 0
        self.ali_w = 0
        # speeds and range of vision
        self.max_speed = 0
        self.range = 0

    # Adds a new boid to the world at x, y
    def add_boid(self, x, y):
        self.boids.append(Boid(x, y, self))

    # Updates the locations of the boids
    def update_all(self):
        for boid in self.boids:
            boid.update()

    # return all boids
    def get_boids(self):
        return self.boids



