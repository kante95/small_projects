from itertools import combinations
from disk import Disk
import pylab
import os
import numpy as np
import operator

output_dir = "event_disks_box_movie"


pylab.subplots_adjust(left=0.10, right=0.90, top=0.90, bottom=0.10)
pylab.gcf().set_size_inches(6, 6)
img = 0
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def setproblem():
    all_disk = [Disk([1., 1.], [1., 1.], 0.1), Disk([-1., -1.], [1., 1.], 0.1)]
    return all_disk


def snapshot(all_disks, box, arrow_scale=.2):
    global img
    pylab.cla()
    pylab.axis(np.ravel(box))
    pylab.setp(pylab.gca(), xticks=[0, 1], yticks=[0, 1])
    for disk in all_disks:
        print disk
        dx = arrow_scale * disk.v_x
        dy = arrow_scale * disk.v_y
        circle = pylab.Circle(tuple(disk.position), radius=disk.radius, fc='b')
        pylab.gca().add_patch(circle)
        pylab.arrow(disk.x, disk.y, dx, dy, fc="k", ec="k",
                    head_width=0.05, head_length=0.05)
    pylab.text(.5, 1.03, 't = %.2f' % 0, ha='center')
    pylab.savefig(os.path.join(output_dir, '%04i.png' % img))
    img += 1


def compute_next_event(all_disks, couples, box):
    pair_times = [all_disks[i].pair_time(all_disks[j]) for i, j in couples]
    wall_times = [disk.wall_time(box) for disk in all_disks]
    print pair_times
    return min_and_arg(pair_times + wall_times)


def min_and_arg(values):
    return min(enumerate(values), key=operator.itemgetter(1))




x = setproblem()
box = np.array([[-10, 10], [-10, 10]])
snapshot(x, box)
couples = [couple for couple in combinations(range(2), 2)]
print couples
print compute_next_event(x, couples, box)
