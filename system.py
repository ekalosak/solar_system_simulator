import sys

import pdb
import time
import pygame as pg
import numpy as np

import utils

G = 6.67408 * 10**-5
DIMENSION = 2
SCREEN_SIZE = 450, 450
REFRESH_RATE = 60
RED, GREEN, BLUE = (255,0,0), (0,255,0), (0,0,255)
BLACK = (0,0,0)

class Planet(object):

    def __init__(self,
            location = (50,50),
            velocity = (0,0),
            mass = 100,
            color = GREEN,
            size = 20,
            sound = None,
            channel = 0):
        self.location = np.array([float(l) for l in location])
        self.velocity = np.array([float(v) for v in velocity])
        self.mass = float(mass)
        self.color = color
        self.size = size
        self.validate()
        self.sound = sound
        self.maxspeed = np.linalg.norm(self.velocity)

        self.sound.play()

    def __repr__(self):
        s = "Planet of mass {} at loc {} w vel {}".format(
                self.mass, self.location, self.velocity)
        return s

    def __eq__(self, other):
        assert type(other) == Planet
        eq_relations = [all(self.location == other.location),
                all(self.velocity == other.velocity),
                self.mass == other.mass]
        return all(eq_relations)

    def validate(self):
        assert len(self.location) == DIMENSION
        assert len(self.velocity) == DIMENSION
        assert self.mass > 0
        assert type(self.location) == np.ndarray
        assert type(self.velocity) == np.ndarray
        # assert type(self.sound) == pg.mixer.Sound

    def move(self, howfar):
        assert type(howfar) == np.ndarray
        self.location = self.location + howfar

    def get_velocity(self):
        return self.velocity

    def draw(self, screen):
        pg.draw.circle(screen,
                self.color,
                [int(x) for x in self.location[::-1]],
                int(self.size))

    def change_volume(self):
        # This is an art function - determine volume based on velocity
        if self.maxspeed == 0.0:
            self.maxspeed = 0.01
        vol = np.linalg.norm(self.velocity) / self.maxspeed
        if np.linalg.norm(self.velocity) > self.maxspeed:
            self.maxspeed = np.linalg.norm(self.velocity)
        self.sound.set_volume(vol)

class Space(object):

    def __init__(self, planets = []):
        self.planets = planets
        self.time = 0
        self.validate()

    def validate(self):
        for p in self.planets:
            assert type(p) == Planet

    def dist(self, p, q):
        assert type(p) == Planet
        assert type(q) == Planet
        diff = p.location - q.location
        return np.linalg.norm(diff)

    def next_time(self):
        # Move time forward
        dt = 1
        self.time += dt

        # Move planets according to their velocity
        for p in self.planets:
            p.move(p.velocity * dt)

        # Calculate velocity for each planet
        for p in self.planets:
            dv = np.zeros(len(p.velocity), dtype=float)
            for q in self.planets:
                if q == p:
                    continue
                else:
                    magnitude = G * q.mass * p.mass / self.dist(p, q)**2
                    direction = q.location - p.location
                    direction = direction / np.linalg.norm(direction)
                    dv = dv + direction + magnitude
            p.velocity = p.velocity + dv
            # log.debug("planet <{}> velocity is <{}>".format(p, dv))

    def draw(self, screen):
        for p in self.planets:
            p.draw(screen)

    def set_volumes(self):
        for p in self.planets:
            p.change_volume()

def test(log):
    pass

def main(log):

    log.debug("initializing app")
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.init()

    # load sounds
    sounds = []
    for fn in ['./sounds/ambient.wav']*3:
            # './sounds/water-tarp.wav',
            # './sounds/water-tarp.wav']:
        # pdb.set_trace()
        sounds.append(pg.mixer.Sound(fn))

    # Define planet statuses
    masses = [1,20,10]
    locations = [(100,100), (200,400), (300,50)]
    velocities = [(0.1,0.1)]*3
    colors = RED, GREEN, BLUE, BLACK
    sizes = [4*mass for mass in masses]
    pts = []

    # Create planets
    for a in range(len(masses)):
        mass = masses[a]
        loc = locations[a]
        vel = velocities[a]
        color = colors[a]
        size = sizes[a]
        sound = sounds[a % len(sounds)]
        p = Planet(location=loc,
                velocity=vel,
                mass=mass,
                color=color,
                size=size,
                sound=sound)
        pts.append(p)

    # Setup the space
    spc = Space(planets = pts)

    # load the pygame tools
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()

    # Enter mainloop
    log.debug("starting main loop")
    while 1:
        clock.tick(REFRESH_RATE)

        # Handle keyboard input
        for event in pg.event.get():

            if event.type == pg.QUIT:
                log.debug("quitting")
                sys.exit()

            keypress = pg.key.get_pressed()
            if sum(keypress) > 0:
                key_name = pg.key.name(keypress.index(1))
                log.debug("key pressed: <{}>".format(key_name))

            # Pause, play
            if keypress[pg.K_SPACE]:
                pdb.set_trace()

            # Quit
            elif keypress[pg.K_ESCAPE]:
                log.debug("quitting")
                sys.exit(1)

        # Move time forward
        spc.next_time()

        # Draw images
        screen.fill(BLACK)
        spc.draw(screen)
        pg.display.flip()

        # Play sounds
        spc.set_volumes()

if __name__ == "__main__":
    log = utils.make_logger('solar-system')
    test(log)
    main(log)

