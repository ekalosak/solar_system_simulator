import pdb
import time

G = 6.67408 * 10**-11

class Planet(object):

    def __init__(self, location, velocity, mass):
        self.location = [float(a) for a in location]
        self.velocity = [float(b) for b in velocity]
        self.mass = float(mass)
        self.validate()

    def __str__(self):
        s = "Planet of mass {} at loc {} w vel {}".format(
                self.mass, self.location, self.velocity)
        return s

    def validate(self):
        assert len(self.location) == 3
        assert len(self.velocity) == 3
        assert self.mass > 0

    def move(self, howfar):
        self.location = [a + b for a, b in zip(self.location, self.velocity)]

    def getVelocity(self):
        return self.velocity

class Space(object):

    def __init__(self, planets = []):
        self.planets = planets
        self.time = 0
        self.validate()

    def validate(self):
        for p in self.planets:
            assert type(p) == Planet

    def dist(self, p, q):
        a = [abs(b - c) for b, c in zip(p.location, q.location)]
        d = sum([e**2 for e in a])
        return (d)**(0.5)

    def next_time(self):
        # For each object,
        #   move obj based on its velocity
        #   then change velocities based on gravity acceleration
        self.time += 1
        for p in self.planets:
            p.move(p.getVelocity())

        for p in self.planets:
            for q in self.planets:
                if q == p:
                    continue
                else:
                    # force = G * p.mass * q.mass / self.dist(p, q)**2
                    # accel = force / p.mass
                    accel = G * q.mass / self.dist(p, q)**2
                    # TODO make the acceleration a vector
                    p.velocity = [v + a for v, a in zip(p.velocity, accel)]

if __name__ == "__main__":
    masses = [5, 7, 10]
    locations = [(1,1,1), (2,2,2), (5,5,5)]
    velocities = [(0,0,0)]*3
    pts = []
    # pdb.set_trace()
    for a in range(len(masses)):
        mass = masses[a]
        loc = locations[a]
        vel = velocities[a]
        p = Planet(loc, vel, mass)
        pts.append(p)
    spc = Space(planets = pts)
    while 1:
        for p in spc.planets:
            print p
        time.sleep(1)
        spc.next_time()

