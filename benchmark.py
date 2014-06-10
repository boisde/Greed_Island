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



def test_visualize():
    particles = [Particle(0.1, 0.5, +1),
            Particle(0.0, -0.5, -1),
            Particle(-0.1, -0.4, +3)]
    print('hallo alice')


if __name__ == '__main__':
    test_visualize()
