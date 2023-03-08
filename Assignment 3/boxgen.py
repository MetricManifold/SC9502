# setup for doing assignment questions

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

random.seed()

PARTICLE_RADIUS = 1.0 / 2.0     # radius of each particle that is inserted
BOX_DIMENSIONS = (11.0, 11.0)   # dimensions of the system to place the particles
MAX_ATTEMPTS = 1000             # maximum number of attempts to randomly place a particle

BOX_AREA = BOX_DIMENSIONS[0] * BOX_DIMENSIONS[1]
PARTICLE_AREA = 2 * np.pi * PARTICLE_RADIUS

def check_overlap(check_particle, particle_list):
    cx, cy = check_particle
    
    for x, y in particle_list:
        dx = cx - x
        dy = cy - y
        
        if dx * dx + dy * dy < 4 * PARTICLE_RADIUS * PARTICLE_RADIUS:
            return True
    
    return False

# randomly inserts a particle inside the box
def insert_particle(particle_list, x=None, y=None, wall=True):
    x0 = PARTICLE_RADIUS if wall else 0
    y0 = x0
    x1 = BOX_DIMENSIONS[0] - x0 if wall else BOX_DIMENSIONS[0]
    y1 = BOX_DIMENSIONS[1] - y0 if wall else BOX_DIMENSIONS[1]

    # if coordinates were provided, check if it can be placed there
    if x is not None and y is not None:
        particle = (x, y)
        
        # if the given particle position is outside the box or overlaps
        # the walls, then attempts will be set to 1
        if x >= x0 and x <= x1 and y >= y0 and y <= y1:
            attempts = 1 if check_overlap(particle, particle_list) else 0
        else:
            attempts = 1
        inserted = (attempts == 0)
    
    # if coordinates were not provided, find a random position
    else:
        inserted = False
        attempts = -1
        
        while not inserted and attempts <= MAX_ATTEMPTS:
            attempts += 1
            particle = (random.uniform(x0, x1), random.uniform(y0, y1))
            inserted = not check_overlap(particle, particle_list)
    
    # if the particle was inserted, then add it tot he list     
    if inserted:
        particle_list.append(particle)
    
    # returns the number of times it attempted to place the parcticle
    # if coordinates were provided, and placement was successful, the number
    # of attempts will be 0. Otherwise, random attempts will try up to MAX_ATTEMPTS
    # times.
    return attempts



ROWS = 2 # number of rows of the lattice
LATTICE_SEP = (BOX_DIMENSIONS[0] / ROWS) / 2.
FIRST_POS = LATTICE_SEP / 2.
EPS = 1e-4

# generate a lattice arrangement
def generate_lattice(wall=True):
    
    particle_list = []
    inserted = True

    x = FIRST_POS
    y = FIRST_POS
    while inserted:
        inserted = True if insert_particle(particle_list, x, y, wall) == 0 else False
        
        shift = FIRST_POS * (-1 if (y // LATTICE_SEP) % 2 == 0 else 1)
        x += LATTICE_SEP
        
        if x > BOX_DIMENSIONS[0]:
            x -= EPS
            
        y += int(x / BOX_DIMENSIONS[0]) * LATTICE_SEP
        x -= int(x / BOX_DIMENSIONS[0]) * (BOX_DIMENSIONS[0] + shift)

    if not particle_list:
        print("too many rows: particles would overlap")
        
    return particle_list


def plot_lattice(*particle_lists):
    
    i = 0
    for particle_list in particle_lists:
        xs, ys = zip(*particle_list)
        plt.plot(xs, ys, 'o', label="{}".format(i))
        i += 1
        
    plt.xlim(0, BOX_DIMENSIONS[0])
    plt.ylim(0, BOX_DIMENSIONS[1])
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.legend()
    plt.title("Positions of particles in a box {}Å x {}Å".format(*BOX_DIMENSIONS))
    plt.show()

        

def animate_lattice(positions):
    
    fig, ax = plt.subplots()
    frames = []
    for i in range(0, len(positions)):
        xs, ys = zip(*positions[i])
        frame = ax.plot(xs, ys, 'o', animated=True)
        if i == 0:
            ax.plot(xs, ys, 'o')
            
        frames.append([frame])


    plt.xlim(0, BOX_DIMENSIONS[0])
    plt.ylim(0, BOX_DIMENSIONS[1])
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.legend()
    plt.title("Positions of particles in a box {}Å x {}Å".format(*BOX_DIMENSIONS))
    
    ani = animation.ArtistAnimation(fig, frames, interval=50, repeat_delay=1000, blit=True)
    plt.show()
    return ani