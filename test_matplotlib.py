import time
from matplotlib import pyplot as plt
import numpy as np


def live_update_demo(blit = False):
    x = np.linspace(0,50., num=100)
    fig = plt.figure()
    ax2 = fig.add_subplot(2, 1, 2)

    line, = ax2.plot([], lw=3)

    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim([-1.1, 1.1])

    fig.canvas.draw()


    ax2background = fig.canvas.copy_from_bbox(ax2.bbox)

    plt.show(block=False)


    t_start = time.time()
    k=0.

    for i in np.arange(10000):

        line.set_data(x, np.sin(x/3.+k))

        #print tx
        k+=0.11

        fig.canvas.restore_region(ax2background)
        ax2.draw_artist(line)
        fig.canvas.blit(ax2.bbox)
        fig.canvas.flush_events()



live_update_demo(True)   # 175 fps