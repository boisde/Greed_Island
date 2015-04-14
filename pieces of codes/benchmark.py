class Particle:
    def __init__(self, x, y, ang_speed):
        self.x = x
        self.y = y
        self.ang_speed = ang_speed


class ParticleSimulator:
    def __init__(self, particles):
        self.particles = particles

    def evolve(self, dt):
        time_step = 0.00001
        n_steps = int(dt/time_step)

        for i in range(n_steps):
            for p in self.particles:
                # 1. calculate the direction
                norm = (p.x**2+p.y**2)**0.5
                v_x = (-p.y)/norm
                v_y = p.x/norm
                # 2. calculate the displacement
                d_x = time_step * p.ang_speed * v_x
                d_y = time_step * p.ang_speed * v_y
                p.x += d_x
                p.y += d_y
                # 3. repeat for all the time_step


from matplotlib import pyplot as plt
from matplotlib import animation

def visualize(simulator):
    xs = [p.x for p in simulator.particles]
    ys = [p.y for p in simulator.particles]
    
    fig = plt.figure()
    ax = plt.subplot(111, aspect='equal')
    line, = ax.plot(xs, ys, 'ro')
# Axis limits
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
# It will be run when the animation starts
    def init():
        line.set_data([],[])
        return line,

    def animate(i):
        simulator.evolve(0.01)
        x = [p.x for p in simulator.particles]
        y = [p.y for p in simulator.particles]
        line.set_data(x, y)
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True, interval=10)
    plt.show()


def test_visualize():
    particles = [Particle(0.1, 0.5, +1),
            Particle(0.0, -0.5, -1),
            Particle(-0.1, -0.4, +3)]
    simulator = ParticleSimulator(particles)
    visualize(simulator)
    print('hallo alice')


from random import uniform

def benchmark():
    particles = [Particle(uniform(-1.0, +1.0),uniform(-1.0, +1.0),uniform(-1.0,+1.0)) for i in range(1000)]
    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)


if __name__ == '__main__':
    benchmark()
