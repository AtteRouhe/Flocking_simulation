import numpy as np
import random


class Boid:

    def __init__(self, x, y, world):
        # the world in which the boid is created in
        self.world = world
        # vector for boids position
        self.position = np.array([x, y])
        # vector for velocity, init at random dir
        self.velocity = np.array([random.randint(-10, 10), random.randint(-10, 10)])

    def update(self):
        nearby = []  # boids in the range of a single boid
        acceleration = np.array([0, 0])  # calculate acceleration to a numpy vector

        # find all the boids within the given range
        for b in self.world.get_boids():
            # distance between two boids
            distance = np.linalg.norm(b.position - self.position)
            # check that boid is in range and not the boid we are calculating the movement for
            if self.world.range > distance > 0 and self.world.range > distance > 0:
                # add to list if in range
                nearby.append(b)

        # no need for extra calculations if no boids nearby
        if len(nearby) != 0:

            # calculate a velocity vector from the nearby boids for each of the flocking rules and add weights
            sep = self.separate(nearby)
            coh = self.cohesion(nearby)
            ali = self.align(nearby)

            # add weights to the vectors
            sep = sep * self.world.sep_w
            coh = coh * self.world.coh_w
            ali = ali * self.world.ali_w

            # add the three vectors to the acceleration vector
            acceleration += sep.astype(int)
            acceleration += coh.astype(int)
            acceleration += ali.astype(int)

            # add acceleration to velocity and limit to max speed
            self.velocity = self.velocity + acceleration
            if np.linalg.norm(self.velocity) > self.world.max_speed:
                self.velocity = ((self.velocity / np.linalg.norm(self.velocity)) * self.world.max_speed).astype(int)

        # add velocity to position
        self.position += self.velocity

        # check if boid is off frame and move accordingly
        if self.position[0] > self.world.MAX_X:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.world.MAX_X
        # same for y coord
        if self.position[1] > self.world.MAX_Y:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.world.MAX_Y

    # steer away from other boids that are too close
    def separate(self, nearby):
        ret = np.array([0, 0])
        limit = 40   # range for boids that are too close
        # track the amount of boids in range
        count = 0
        # sum up vectors facing away fom boids too near, weighed by distance inverted
        for b in nearby:
            # distance to
            distance = np.linalg.norm(b.position - self.position)
            # if distance is smaller than limit
            if distance < limit:
                # calculate a vector pointing away from the boid
                x = self.position - b.position
                # the closer boids should be avoided more
                x = x / distance
                # add up
                ret = ret + x
                # increment
                count += 1
        # if none were found just return 0 vector
        if count > 0:
            # calculate avg
            ret = ret / count
            # set to max speed
            if np.linalg.norm(ret) > 0:
                ret = (ret / np.linalg.norm(ret)) * self.world.max_speed
            # steering
            ret = ret - self.velocity
            return ret
        else:
            # no boids within limit
            return np.array([0, 0])

    # steer towards the average position of nearby boids
    def cohesion(self, nearby):
        ret = np.array([0, 0])
        count = 0
        # count average position of boids in range
        for b in nearby:
            # add up all positions
            ret = ret + b.position
            count += 1
        if count > 0:
            # average
            ret = ret / count
            ret = ret - self.position
            if np.linalg.norm(ret) > 0:
                # set to max speed
                ret = (ret / np.linalg.norm(ret)) * self.world.max_speed
            # steering
            ret = ret - self.velocity
            return ret
        else:
            # no boids nearby
            return np.array([0, 0])

    # align towards flocks heading
    def align(self, nearby):
        ret = np.array([0, 0])
        count = 0
        # calculate average velocity of the boids
        for b in nearby:
            ret = ret + b.velocity
            count += 1
        # avg and limit to max speed
        if count > 0:
            ret = ret / count
            if np.linalg.norm(ret) > 0:
                ret = (ret / np.linalg.norm(ret) * self.world.max_speed)
            return ret - self.velocity
        else:
            # no boids nearby
            return np.array([0, 0])


