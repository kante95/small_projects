import numpy as np


class Disk():
    def __init__(self, position, velocity, radius, mass=1):
        self.position = np.array(position)
        self.x = position[0]
        self.y = position[1]
        self.velocity = np.array(velocity)
        self.v_x = velocity[0]
        self.v_y = velocity[1]
        self.radius = radius
        self.mass = mass

    def collide_with(self, other):
        versor = (self.position - other.position) / \
            np.linalg.norm(self.position - other.position)
        del_v = self.velocity - other.velocity
        self.velocity = self.velocity - versor * (np.dot(del_v, versor))
        other.velocity = other.velocity + versor * (np.dot(del_v, versor))

    def wall_time(self, box):
        de_t = []
        for velocity, position, wall in zip(self.velocity, self.position, box):
            if velocity > 0.0:
                de_t.append((wall[0] - self.radius - position) / velocity)
            elif velocity < 0.0:
                de_t.append((position - wall[1] - self.radius) / abs(velocity))
        return min(de_t)

    def pair_time(self, other):
        delta_position = np.sum((other.position - self.position) ** 2)
        delta_velocity = np.sum((other.velocity - self.velocity) ** 2)
        scal = np.sum((other.position - self.position) *
                      (other.velocity - self.velocity))
        Upsilon = scal ** 2 - delta_velocity * \
            (delta_position - (self.radius + other.radius) ** 2)
        if Upsilon > 0.0 and scal < 0.0:
            delta_t = -(scal + np.sqrt(Upsilon)) / delta_velocity
        else:
            delta_t = np.inf
        return delta_t


def test_collide():
    # TEST 1
    disk_1 = Disk([1, 0], [-1, 0], 1)
    disk_2 = Disk([-1, 0], [0, 1], 1)
    disk_1.collide_with(disk_2)
    print disk_1.velocity == np.array([0., 0.])
    disk_1.velocity


def test_wall_time():
    disk_x = Disk([0., 0.], [3., 4.], 1)
    print disk_x.wall_time([[10., 10.], [5., 4.]])


def test_pair_time(N):
    def pair_time(pos_a, vel_a, pos_b, vel_b, R_a, R_b):
        del_x = [pos_b[0] - pos_a[0], pos_b[1] - pos_a[1]]
        del_x_sq = del_x[0] ** 2 + del_x[1] ** 2
        del_v = [vel_b[0] - vel_a[0], vel_b[1] - vel_a[1]]
        del_v_sq = del_v[0] ** 2 + del_v[1] ** 2
        scal = del_v[0] * del_x[0] + del_v[1] * del_x[1]
        Upsilon = scal ** 2 - del_v_sq * (del_x_sq - (R_a + R_b) ** 2)
        if Upsilon > 0.0 and scal < 0.0:
            del_t = - (scal + np.sqrt(Upsilon)) / del_v_sq
        else:
            del_t = float('inf')
        return del_t

    for i in range(N):
        pos_a = np.random.rand(2) * 2
        vel_a = np.random.rand(2)
        pos_b = np.random.rand(2) * 2
        vel_b = np.random.rand(2)
        R_a = np.random.rand(1)[0]
        R_b = np.random.rand(1)[0]
        disk_1 = Disk(pos_a, vel_a, R_a)
        disk_2 = Disk(pos_b, vel_b, R_b)
        print disk_1.pair_time(disk_2), pair_time(pos_a, vel_a, pos_b, vel_b, R_a, R_b)

