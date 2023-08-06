
from pyjjasim import *

import matplotlib.pyplot as plt

# import matplotlib
# matplotlib.use("TkAgg")

"""
Dynamic example 3: Moving a vortex with current pulse. Used in rapid-single-flux-quanum (RSFQ) technology.
"""

from scipy.stats import norm

if __name__ == "__main__":
    # define array
    N = 20
    sq_array = SquareArray(N, N)

    # define problem
    dt = 0.05
    Nt = 600
    ts = np.arange(0, Nt, 3)
    Ih = sq_array.current_base(angle=0)
    amp = 2
    Is = amp * Ih[:, None, None] * norm(loc=12, scale=1.0).pdf(np.arange(Nt) * dt)

    # define initial condition with vortex in centre
    n = np.zeros(sq_array.face_count(), dtype=int)
    n[sq_array.locate_faces((N - 1) / 2, (N - 1) / 2)] = 1

    init, status, info = StaticProblem(sq_array, vortex_configuration=n).compute()
    init_th = init.get_theta()[:, None]


    problem = TimeEvolutionProblem(sq_array, time_step=dt, time_step_count=Nt, current_sources=Is,
                                   store_time_steps=ts, config_at_minus_1=init_th)

    # do time simulation
    out = problem.compute()

    # animate result
    handles = out.animate(figsize=(8, 8), title="Move vortex with current pulse ")
    plt.show()
