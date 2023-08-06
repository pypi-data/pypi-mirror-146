from pyjjasim import *

import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("TkAgg")

"""
Dynamic example 5: Giant shapiro steps

With a biassed AC current, the DC voltage has plateaus. This effect is called shapiro steps for single junctions,
and giant shapiro steps for arrays as the step height is proportional to the array size. 

Of course after the array voltage is normalized, the steps are not so 
giant, and the step heights will be Ifreq.
"""

if __name__ == "__main__":

    # define array
    N = 20
    sq_array = SquareArray(N, N)

    # define problem
    T = 0.01
    dt = 0.05
    Nt = 10000
    ts = [Nt//3, Nt - 1]

    IAmp = 1.0
    Ifreq = 0.25
    IDC = np.linspace(0, 2, 101)
    Is = lambda i: sq_array.current_base(angle=0)[:, None] * (IDC + IAmp * np.sin(Ifreq * i * dt))
    prob = TimeEvolutionProblem(sq_array, time_step=dt, time_step_count=Nt,
                                current_sources=Is, temperature=T, store_time_steps=ts,
                                store_current=False, store_voltage=False)

    # do time simulation
    out = prob.compute()

    # compute array voltage
    th = out.get_theta()[np.isclose(sq_array.current_base(angle=0), 1.0), :, :]
    V = np.mean((th[:, :, 1] - th[:, :, 0]) / (dt * (ts[1] - ts[0])), axis=0)

    # plot array voltage
    plt.plot(IDC, V, label='f=0')
    plt.xlabel("DC current")
    plt.ylabel("mean array voltage")
    plt.title("giant shapiro steps in square array")
    plt.legend()
    plt.show()
