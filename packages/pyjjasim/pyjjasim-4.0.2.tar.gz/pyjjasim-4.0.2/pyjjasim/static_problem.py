from __future__ import annotations

import time
from typing import List

import numpy as np
import scipy
import scipy.sparse.linalg
import scipy.optimize

from pyjjasim.embedded_graph import EmbeddedGraph
from pyjjasim.josephson_circuit import Circuit

__all__ = ["CurrentPhaseRelation", "DefaultCPR", "StaticProblem",
           "StaticConfiguration", "compute_maximal_parameter",
           "node_to_junction_current", "DEF_TOL", "DEF_NEWTON_MAXITER",
           "DEF_MAX_PAR_TOL", "DEF_MAX_PAR_REDUCE_FACT",
           "NewtonIterInfo", "ParameterOptimizeInfo"]


"""
Static Problem Module
"""

DEF_TOL = 1E-10

DEF_NEWTON_MAXITER = 30

DEF_MAX_PAR_TOL = 1E-4
DEF_MAX_PAR_REDUCE_FACT = 0.42
DEF_MAX_PAR_MAXITER = 100


class CurrentPhaseRelation:

    """

    Current-Phase relation Icp(Ic, theta). The default value is Icp = Ic * sin(theta).

    Parameters
    ----------
    func : func(Ic, theta)
        Current-phase relation.
    d_func : func(Ic, theta)
        Derivative of current-phase relation to theta.
    i_func : func(Ic, theta)
        Integral of current-phase relation over theta (starting at 0).

    Notes
    -----
     - func, d_func and i_func must be numpy ufunc, so their output must be broadcast
       of input Ic and theta.
    """
    def __init__(self, func, d_func, i_func):
        self.func = func
        self.d_func = d_func
        self.i_func = i_func

    def eval(self, Ic, theta):
        """
        Evaluate current phase relation; returns func(Ic, theta).
        """
        return self.func(Ic, theta)

    def d_eval(self, Ic, theta):
        """
        Evaluate derivative of current phase relation; returns d_func(Ic, theta).
        """
        return self.d_func(Ic, theta)

    def i_eval(self, Ic, theta):
        """
        Evaluate integral of current phase relation; returns i_func(Ic, theta).
        """
        return self.i_func(Ic, theta)

class DefaultCPR(CurrentPhaseRelation):

    """
    Default current-phase relation Icp = Ic * sin(theta).
    """
    def __init__(self):
        super().__init__(lambda Ic, th: Ic * np.sin(th),
                         lambda Ic, th: Ic * np.cos(th),
                         lambda Ic, th: Ic * (1.0 - np.cos(th)))


class NewtonIterInfo:

    """
    Information about the newton iteration used to find static configurations.
    Use print(newton_iter_info) to display the information.
    """
    def __init__(self, tol, maxiter):
        self.start_time = time.perf_counter()
        self.tol = tol
        self.maxiter = maxiter
        self.iteration = 0
        self.error = np.zeros(self.maxiter + 1, dtype=np.double)
        self.has_converged = False
        self.is_target_n = np.zeros(self.maxiter + 1, dtype=int)
        self.runtime = 0.0

    def get_max_iter(self):
        """
        Returns number of iterations after which iteration is aborted.
        """
        return self.maxiter

    def get_tol(self):
        """
        Returns tolerance.
        """
        return self.tol

    def get_status(self):
        """
        Returns status of newton iteration result; returns value:
         * 0: converged. residual < tolerance
         * 1: diverged before reaching maxiter.
         * 2: reached max_iter without converging or diverging.
        """
        return int(not self.found_target_solution()) + 2 * int(self.iteration >= self.maxiter)

    def has_converged(self):
        """
        Returns if iteration has converged.
        """
        return self.has_converged

    def get_is_target_vortex_configuration(self):
        """
        Returns (nr_of_iters,) bool array if vortex configuration at iter
        agrees with vortex configuration specified in problem.
        """
        return self.is_target_n[:(self.get_number_of_iterations()+1)]

    def found_target_solution(self):
        """
        Returns True if has_converged() and final iter obeys target vortex config.
        """
        return self.has_converged and self.is_target_n[self._get_iteration()]

    def get_number_of_iterations(self):
        """
        Returns number of newton iterations done.
        """
        return self._get_iteration()

    def get_residual(self):
        """
        Returns (nr_of_iters,) array containing residual at each iteration.
        """
        return self.error[:(self.get_number_of_iterations()+1)]

    def get_runtime(self):
        """
        Returns runtime in seconds.
        """
        return self.runtime

    def plot_residuals(self):
        """
        Plots residual vs iteration number.
        """
        import matplotlib.pyplot as plt
        n = self.get_is_target_vortex_configuration().astype(bool)
        y = self.get_residual()
        x = np.arange(len(y))
        plt.semilogy(x[n], y[n], color=[0, 0, 0], label="n is target_n", linestyle="None", marker="o")
        plt.semilogy(x[~n], y[~n], color=[1, 0, 0], label="n is not target_n", linestyle="None", marker="o")
        plt.xlabel("Newton iteration number")
        plt.ylabel("residual")
        plt.title("Evolution of residual for newton iteration.")
        plt.legend()

    def __str__(self):
        out = f"newton iteration info: (tol={ self.get_tol()}, maxiter={self.get_max_iter()})\n\t"
        out += f"status: {self.get_status()}"
        if self.get_status() == 0:
            out += f" (converged)\n\t"
        if self.get_status() == 1:
            out += f" (diverged)\n\t"
        if self.get_status() == 2:
            out += f" (indeterminate; reached max_iter without converging or diverging)\n\t"
        out += f"number of iterations: {self.get_number_of_iterations()}\n\t"
        out += f"residual: {self.get_residual()}\n\t"
        out += f"runtime (in sec): {self.get_runtime()}"
        return out

    def _set(self, error, is_target_n_v):
        self.has_converged = error < self.tol
        self.is_target_n[self.iteration] = is_target_n_v
        self.error[self.iteration] = error
        self.runtime += time.perf_counter() - self.start_time
        self.start_time = time.perf_counter()
        self.iteration += 1
        return self

    def _get_iteration(self):
        return max(0, self.iteration - 1)


class ParameterOptimizeInfo:

    """
    Information about the parameter optimization process.
    Use print(parameter_optimize_info) to display a summary of
    the information.
    """
    def __init__(self, problem_func, lambda_tol, require_stability, require_target_n, maxiter):
        self.problem_func = problem_func
        self.lambda_tol = lambda_tol
        self.require_target_n = require_target_n
        self.require_stability = require_stability
        self.maxiter = maxiter
        self.has_solution_at_zero = False
        self.lambda_history = np.zeros(self.maxiter, dtype=np.double)
        self.solutions = []
        self.stepsize_history = np.zeros(self.maxiter, dtype=np.double)
        self.solution_history = np.zeros(self.maxiter, dtype=np.bool)
        self.stable_history = np.zeros(self.maxiter, dtype=np.int)
        self.target_n_history = np.zeros(self.maxiter, dtype=np.int)
        self.newton_iter_infos = []
        self._step = 0
        self._time = time.perf_counter()
        self.last_step_status = None
        self.last_step_stable_status = None

    def get_has_solution_at_zero(self):
        """
        Returns if a stable target solution is found at lambda=0.
        """
        return self.has_solution_at_zero

    def get_lambda(self):
        """
        Returns (nr_of_steps,) array with lambda at each step.
        """
        return self.lambda_history[:self._step]

    def get_lambda_error(self):
        """
        Returns (nr_of_steps,) array with error in lambda.
        """
        return self._get_lambda_stepsize() / self.get_lambda()

    def get_lambda_lower_bound(self):
        """
        Returns lower bound for lambda.
        """
        if not self.get_has_solution_at_zero():
            return np.nan
        s = self.get_lambda()[self.get_found_solution()]
        return s[-1] if s.size > 0 else 0

    def get_lambda_upper_bound(self):
        """
        Returns upper bound for lambda.
        """
        s = self.get_lambda()[~self.get_found_solution()]
        return s[-1] if s.size > 0 else np.inf

    def get_found_solution(self):
        """
        Returns (nr_of_steps,) array if a stable target solution is found at step.
        """
        return self.solution_history[:self._step]

    def get_is_stable(self):
        """
        Returns (nr_of_steps,) array if a stable target solution is found at step.
        """
        return self.stable_history[:self._step]

    def get_is_target_vortex_configuration(self):
        """
        Returns (nr_of_steps,) array if a solution has target vortex configuration.
        """
        return self.target_n_history[:self._step]

    def get_newton_iter_all_info(self):
        """
        Returns (nr_of_steps,) list containing newton_iter_infos.
        """
        return self.newton_iter_infos

    def get_newton_steps(self):
        """
        Returns (nr_of_steps,) array with nr of newton iterations at step.
        """
        return np.array([info.get_number_of_iterations() for info in self.newton_iter_infos], dtype=int)

    def get_runtime(self):
        """
        Returns runtime in seconds.
        """
        return self._time

    def plot_residuals(self):
        """
        Plots residual vs iteration number.
        """
        import matplotlib.pyplot as plt
        for i, n_info in enumerate(self.get_newton_iter_all_info()):
            n = n_info.get_is_target_vortex_configuration().astype(bool)
            y = n_info.get_residual()
            x = np.arange(len(y))
            plt.semilogy(x[n], y[n], color=[0, 0, 0], linestyle="None", marker="o")
            plt.semilogy(x[~n], y[~n], color=[1, 0, 0], linestyle="None", marker="o")
            plt.text(x[-1], y[-1], str(i), color=[0.3, 0.3, 0.3])
            plt.semilogy(x, y, color=[0, 0, 0])
        plt.xlabel("Newton iteration number")
        plt.ylabel("residual")
        plt.title("Newton residuals in parameter optimization.")
        plt.legend(["n is target_n", "n is not target_n"])

    def animate_solutions(self):
        import matplotlib.animation as anim
        fig, ax = self.solutions[0].plot()
        lambdas = self.get_lambda()[self.get_found_solution()]
        stable = self.get_is_stable()[self.get_found_solution()]
        def _animate(i):
            p_fig, p_ax = self.solutions[i].plot(fig=fig)
            p_ax.set_title(f"lambda={np.round(lambdas[i], 5)}, is stable: {stable[i]}")
            return [p_ax]
        ani = anim.FuncAnimation(fig, _animate, frames=range(len(self.solutions)),
                                 interval=1000, blit=False)
        return ani

    def __str__(self):
        np.set_printoptions(linewidth=100000)
        out = "Parameter optimize info:\n\t"
        if not self.get_has_solution_at_zero():
            out += "Optimization failed because not solution was found at lambda=0."
        else:
            def int_digit_count(x):
                return np.ceil(np.log(np.max(x)) / np.log(10)).astype(int)
            n = max(5, 3 + int_digit_count(1/self.lambda_tol), int_digit_count(self.get_newton_steps()))
            out += f"Found lambda between {self.get_lambda_lower_bound()} and {self.get_lambda_upper_bound()}.\n\t"
            if self.last_step_stable_status == 2:
                out += f"Stopped because stability could not be determined.\n\t"
            elif self.last_step_status == 2:
                out += f"Stopped because newton iteration was indeterminate. Consider increasing newton_maxiter.)\n\t"
            elif self._step == self.maxiter:
                out += f"Optimization reached maxiter {self.maxiter} before reaching desired tolerance. (resid={self.get_lambda_error()[-1]})\n\t"
            else:
                out += f" at desired tolerance (resid={self.get_lambda_error()[-1]}) \n\t"
            out += f"runtime: {np.round(self.get_runtime(), 7)} sec\n\t"
            np.set_printoptions(formatter={'float': lambda x: ("{0:0." + str(n - 2) + "f}").format(x)})
            out += f"lambda:              {self.get_lambda()}\n\t"
            np.set_printoptions(formatter={'bool': lambda x: ("{:>" + str(n) + "}").format(x)})
            out += f"found solution:      {self.get_found_solution().astype(bool)}\n\t"
            if self.require_target_n:
                out += f"if so; has target n: {self.get_is_target_vortex_configuration().astype(bool)}\n\t"
            if self.require_stability:
                out += f"is so; is stable:    {self.get_is_stable().astype(bool)}\n\t"
            np.set_printoptions(formatter={'int': lambda x: ("{:>" + str(n) + "}").format(x)})
            out += f"newton step count:   {self.get_newton_steps()}\n\t"
        return out

    def _preset(self, has_solution_at_zero):
        self.has_solution_at_zero = has_solution_at_zero
        return self

    def _set(self, lambda_value, solution, lambda_stepsize, found_solution, newton_iter_info, is_target_n, is_stable=1):
        self.lambda_history[self._step] = lambda_value
        self.stepsize_history[self._step] = lambda_stepsize
        self.solution_history[self._step] = found_solution
        self.stable_history[self._step] = is_stable
        self.newton_iter_infos += [newton_iter_info]
        if solution is not None:
            self.solutions += [solution]
        if is_target_n is not None:
            self.target_n_history[self._step] = is_target_n
        self._step += 1
        return self

    def _finish(self, last_step_status, last_step_stable_status):
        self.last_step_status = last_step_status
        self.last_step_stable_status = last_step_stable_status
        self._time = time.perf_counter() - self._time
        return self

    def _get_lambda_stepsize(self):
        return self.stepsize_history[:self._step]


class StaticProblem:
    """
    Define a static josephson junction array problem.

    Parameters
    ----------
    circuit : Circuit
         Circuit on which the problem is based.
    current_sources=0.0 : (Nj,) ndarray or scalar
         Current sources at each junction in circuit (abbreviated Is). If scalar the same
         value is used for all junctions.

    external_flux=0.0 : (Nf,) ndarray or scalar
         external_flux, or normalized external magnetic flux, through each face in circuit
         (abbreviated f). If scalar the same value is used for all faces.
    vortex_configuration=0 : (Nf,) ndarray or scalar
         Target vorticity at each face in circuit (abbreviated n).  If scalar the same value is
         used for all faces.
    current_phase_relation=DefaultCPR() : CurrentPhaseRelation
        Current-phase relation used to do computations on problem.

     Notes
     -----
     - All physical quantities are dimensionless. See the UserManual (on github)
       for how all quantities are normalized.
     - It is assumed each junction has a current source, see user manual
       (on github) for diagram of junction. To omit the sources in particular
       junctions set the respective values to zero.
     - To use a node-based souce current (represented as an (Nn,) array Is_node
       with current in/e-jected at each node), convert it to a junction-based
       source with Is = node_to_junction_current(circuit, Is_node) and
       us Is as input for a static problem.

    """

    def __init__(self, circuit: Circuit, current_sources=0.0, external_flux=0.0,
                 vortex_configuration=0, current_phase_relation=DefaultCPR()):
        self.circuit = circuit
        self.current_sources = np.atleast_1d(current_sources)
        self.external_flux = np.atleast_1d(external_flux)
        self.vortex_configuration = np.atleast_1d(vortex_configuration)
        self.current_phase_relation = current_phase_relation
        self.current_sources_norm = None

    def save(self, filename):
        """
        Store problem in .npy file. Note that the current-phase-relation is not stored!
        """
        with open(filename, "wb") as ffile:
            x, y = self.circuit.graph.coo()
            n1, n2 = self.circuit.graph.get_edges()
            np.save(ffile, x)
            np.save(ffile, y)
            np.save(ffile, n1)
            np.save(ffile, n2)
            np.save(ffile, self.circuit.critical_current)
            np.save(ffile, self.circuit.resistance)
            np.save(ffile, self.circuit.capacitance)
            L_is_sparse = scipy.sparse.issparse(self.circuit.inductance)
            np.save(ffile, L_is_sparse)
            if L_is_sparse:
                np.save(ffile, self.circuit.inductance.indptr)
                np.save(ffile, self.circuit.inductance.indices)
                np.save(ffile, self.circuit.inductance.data)
            else:
                np.save(ffile, self.circuit.inductance)
            np.save(ffile, self.current_sources)
            np.save(ffile, self.external_flux)
            np.save(ffile, self.vortex_configuration)

    @staticmethod
    def load(filename) -> StaticProblem:
        """
        Load problems created with the .save(filename) method. Returns StaticProblem.
        Note that the loaded problem will always have the default current-phase-relation.
        """
        with open(filename, "rb") as ffile:
            x = np.load(ffile)
            y = np.load(ffile)
            node1 = np.load(ffile)
            node2 = np.load(ffile)
            g = EmbeddedGraph(x, y, node1, node2)
            Ic = np.load(ffile)
            R = np.load(ffile)
            C = np.load(ffile)
            L_is_sparse = np.load(ffile)
            if L_is_sparse:
                indptr = np.load(ffile)
                indices = np.load(ffile)
                data = np.load(ffile)
                Nj = len(node1)
                L = scipy.sparse.csc_matrix((data, indices, indptr), shape=(Nj, Nj))
            else:
                L = np.load(ffile)
            circuit = Circuit(g, critical_current=Ic, resistance=R,
                              capacitance=C, inductance=L)
            Is = np.load(ffile)
            f = np.load(ffile)
            n = np.load(ffile)
            return StaticProblem(circuit, current_sources=Is, external_flux=f, vortex_configuration=n)

    def get_circuit(self) -> Circuit:
        """
        Returns the circuit.
        """
        return self.circuit

    def get_current_sources(self):
        """
        Returns the current sources (abbreviated Is).
        """
        return self.current_sources

    def get_external_flux(self):
        """
        Returns the external_flux (abbreviated f).
        """
        return self.external_flux

    def get_vortex_configuration(self):
        """
        Returns the vortex configuration.
        """
        return self.vortex_configuration

    def get_current_phase_relation(self):
        """
        Returns the current-phase relation.
        """
        return self.current_phase_relation

    def new_problem(self, current_sources=None, external_flux=None,
                    vortex_configuration=None, current_phase_relation=None) -> StaticProblem:
        """
        Makes copy of self with specified modifications.
        """
        return StaticProblem(self.circuit, current_sources=self.current_sources if current_sources is None else current_sources,
                             external_flux=self.external_flux if external_flux is None else external_flux,
                             vortex_configuration=self.vortex_configuration if vortex_configuration is None else vortex_configuration,
                             current_phase_relation=self.current_phase_relation if current_phase_relation is None else current_phase_relation)

    def get_phase_zone(self):
        """
        Returns the phase zone (In all of pyJJAsim phase_zone=0).
        """
        return 0

    def get_net_sourced_current(self):
        """
        Gets the sum of all (positive) current injected at nodes to create Is.
        """
        M = self.get_circuit().get_cut_matrix()
        return 0.5 * np.sum(np.abs((M @ self._Is())), axis=0)

    def get_node_current_sources(self):
        """
        Returns (Nn,) array of currents injected at nodes to create Is.
        """
        M = self.get_circuit().get_cut_matrix()
        return M @ self.current_sources

    def approximate(self) -> StaticConfiguration:
        """
        Computes approximate solution.
        """

        theta = london_approximation(self.circuit, self._f(), self._nt(), self._Is())
        theta = change_phase_zone(self.get_circuit(), theta, self._nt(), 0)
        return StaticConfiguration(self, theta)

    def compute(self, initial_guess = None, tol=DEF_TOL, maxiter=DEF_NEWTON_MAXITER,
                stop_as_residual_increases=True, stop_if_not_target_n=False) -> tuple[StaticConfiguration,
                                                                                 int, NewtonIterInfo]:

        """
        Compute solution to static_problem using Newton iteration.

        Parameters
        ----------
        initial_guess=None : (Nj,) array, StaticConfiguration or None
            Guess for initial state. If None; uses approximation. If input
            is array; it must contain values of theta to represent state.

        tol=DEF_TOL : scalar
            Tolerance; is solution if |residual| < tol.
        maxiter=DEF_NEWTON_MAXITER : int
            Maximum number of newton iterations.
        stop_if_not_target_n=False : bool
            Iteration stops  if n(iter) != n (diverged)
        stop_as_residual_increases=True : bool
            Iteration stops if error(iter) > error(iter - 3) (diverged).

        Returns
        -------
        config : StaticConfiguration
            Object containing solution.
        status : int
            * 0: converged
            * 1: diverged if error(iter)>0.5 or above reasons.
            * 2: max_iter reached without converging or diverging.
        iter_info :  NewtonIterInfo
            Handle containing information about newton iteration.
        """
        if initial_guess is None:
            initial_guess = self.approximate()

        if isinstance(initial_guess, StaticConfiguration):
            initial_guess = initial_guess._th()

        initial_guess = np.array(initial_guess, dtype=np.double)

        theta, status, iter_info = static_compute(self.get_circuit(), initial_guess, Is=self._Is(),
                                                  f=self._f(), n=self._nt(), z=0,
                                                  cp=self.current_phase_relation, tol=tol,
                                                  maxiter=maxiter,
                                                  stop_as_residual_increases=stop_as_residual_increases,
                                                  stop_if_not_target_n=stop_if_not_target_n)
        config = StaticConfiguration(self, theta)
        return config, status, iter_info

    def compute_external_flux_bounds(self, initial_guess = None,
                                   middle_of_range_guess=None, lambda_tol=DEF_MAX_PAR_TOL,
                                   maxiter=DEF_MAX_PAR_MAXITER, require_stability=True,
                                   require_vortex_configuration_equals_target=True,
                                   compute_parameters=None) -> tuple[tuple[float, float],
             tuple[StaticConfiguration, StaticConfiguration], tuple[ParameterOptimizeInfo, ParameterOptimizeInfo]]:

        """

        Finds extremum values of x such that this problem with f = x * self.external_flux
        has a valid solution.

        Parameters
        ----------
        middle_of_range_guess=None : scalar  or None.
            Value of x somewhere in the middle of range. If None; this is
            estimated based on vortex configuration.
        initial_guess=None : valid initial_guess input for StaticProblem.compute()
            Initial guess for the algorithm to start at
            external_flux=middle_of_range_guess * self.external_flux.

        Returns
        -------
        (smallest_x, largest_x) : (float, float)
            Resulting external_flux range.
        (smallest_f_config, largest_f_config) : (StaticConfiguration, StaticConfiguration)
            StaticConfigurations at bounds of range.
        (smallest_f_info, largest_f_info) : (ParameterOptimizeInfo, ParameterOptimizeInfo)
             ParameterOptimizeInfo objects containing information about the iterations.
        """

        options = {"lambda_tol": lambda_tol, "maxiter": maxiter, "compute_parameters": compute_parameters,
                   "require_stability": require_stability,
                   "require_vortex_configuration_equals_target": require_vortex_configuration_equals_target}
        if np.allclose(self._f(), 0):
            raise ValueError("Problem must contain nonzero external_flux.")
        if middle_of_range_guess is None:
            if np.all(self._nt() == 0):
                middle_of_range_guess = 0
            else:
                a = self._f() / self.circuit.get_face_areas() ** 0.5
                b = self._nt().astype(np.double) / self.circuit.get_face_areas() ** 0.5
                middle_of_range_guess = np.sum(a * b) / np.sum(a ** 2)
        external_flux_initial_stepsize = 1.0
        problem_small_func = lambda x: self.new_problem(external_flux=(middle_of_range_guess - x) * self._f())
        problem_large_func = lambda x: self.new_problem(external_flux=(middle_of_range_guess + x) * self._f())
        out = compute_maximal_parameter(problem_small_func, initial_guess=initial_guess,
                                        estimated_upper_bound=external_flux_initial_stepsize, **options)
        smallest_factor, _, smallest_f_config, smallest_f_info = out
        smallest_x = middle_of_range_guess - smallest_factor if smallest_factor is not None else None
        out = compute_maximal_parameter(problem_large_func, initial_guess=initial_guess,
                                        estimated_upper_bound=external_flux_initial_stepsize, **options)

        largest_factor, _, largest_f_config, largest_f_info = out
        largest_x = middle_of_range_guess + largest_factor if largest_factor is not None else None
        return (smallest_x, largest_x), (smallest_f_config, largest_f_config), (smallest_f_info, largest_f_info)

    def compute_maximal_current(self, initial_guess=None, lambda_tol=DEF_MAX_PAR_TOL,
                                maxiter=DEF_MAX_PAR_MAXITER, require_stability=True,
                                require_vortex_configuration_equals_target=True,
                                compute_parameters=None)-> tuple[float,
             StaticConfiguration, ParameterOptimizeInfo]:


        """
        Computes largest source current for which a stable solution exists at the
        specified target vortex configuration and external_flux, where the  source
        current is assumed to be max_current_factor * self.get_current_sources().

        For parameters see documentation of compute_maximal_parameter()

        Returns
        -------
        max_current_factor : float
            Maximal current factor for which a problem with max_current_factor * Is
            has a (stable) solution.
        out_config : StaticConfiguration
            StaticConfiguration of state with maximal current.
        info : ParameterOptimizeInfo
            ParameterOptimizeInfo objects containing information about the iterations.

        """
        M, Nj = self.get_circuit()._Mr(), self.get_circuit()._Nj()
        if np.all(self._Is() == 0):
            raise ValueError("Problem must contain nonzero current sources.")
        Is_per_node = np.abs(M @ self._Is())
        max_super_I_per_node = np.abs(M) @ self.get_circuit()._Ic()
        current_factor_initial_stepsize = 1.0 / np.max(Is_per_node / max_super_I_per_node)
        problem_func = lambda x: self.new_problem(current_sources=x * self._Is())
        out = compute_maximal_parameter(problem_func, initial_guess=initial_guess,
                                        lambda_tol=lambda_tol, maxiter=maxiter,
                                        estimated_upper_bound=current_factor_initial_stepsize,
                                        compute_parameters=compute_parameters,
                                        require_stability=require_stability,
                                        require_vortex_configuration_equals_target=
                                        require_vortex_configuration_equals_target)
        max_current_factor, upper_bound, out_config, info = out
        return max_current_factor, out_config, info

    def compute_stable_region(self, angles=np.linspace(0, 2*np.pi, 61), f_middle_of_range_guess=None,
                              start_initial_guess=None, lambda_tol=DEF_MAX_PAR_TOL,
                              maxiter=DEF_MAX_PAR_MAXITER, require_stability=True,
                              require_vortex_configuration_equals_target=True,
                              compute_parameters=None) -> tuple[np.ndarray, np.ndarray,
                                                                List[StaticConfiguration],
                                                                List[ParameterOptimizeInfo]]:

        """
        Finds edge of stable region in (f, Is) space for vortex configuration n.

        More precisely, returns xf(angle) and xI(angle) such that (xf(angle) * self.f, xI(angle)*self.Is)
        lies on the boundary of the stable region in  (f, Is) space for all specified angles.

        For unlisted parameters see documentation of compute_maximal_parameter()

        Parameters
        ----------
        angles=np.linspace(0, 2*np.pi, 61) : array
            Angles at which an extremum in (f, Is) space is searched for.
        f_middle_of_range_guess=None : scalar  or None.
            Value of xf somewhere in the middle of range. If None; this is
            estimated based on vortex configuration.

        Returns
        -------
        external_flux : (num_angles,) array
            Extermum external_flux factor at each angle.
        current : (num_angles,) array
            Extremum sourced current factor at each angle.
        all_configs : list containing StaticConfiguration
            Configurations at extreme value for each angle.
        all_infos : list containing ParameterOptimizeInfo
            Objects containing information about the iterations at each angle.

        """
        num_angles = len(angles)
        options = {"lambda_tol": lambda_tol, "maxiter": maxiter, "compute_parameters": compute_parameters,
                   "require_stability": require_stability,
                   "require_vortex_configuration_equals_target": require_vortex_configuration_equals_target}

        frust_bnd_prb = self.new_problem(current_sources=0)
        out = frust_bnd_prb.compute_external_flux_bounds(initial_guess=start_initial_guess,
                                                       middle_of_range_guess=f_middle_of_range_guess,
                                                       **options)

        (smallest_x, largest_x), _, _ = out
        if smallest_x is None:
            return None, None, None, None
        dome_center_x = 0.5 * (smallest_x + largest_x)
        dome_center_f = dome_center_x * self._f()
        dome_center_problem = self.new_problem(external_flux=dome_center_f)
        out = dome_center_problem.compute_maximal_current(initial_guess=start_initial_guess, **options)
        max_current_factor, _, info = out
        if max_current_factor is None:
            return None, None, None, None

        external_flux = np.zeros(num_angles, dtype=np.double)
        current = np.zeros(num_angles, dtype=np.double)
        all_configs, all_infos = [], []
        for angle_nr in range(num_angles):
            angle = angles[angle_nr]
            Is_func = lambda x: x * self._Is() * np.sin(angle) * max_current_factor
            x_func = lambda x: (dome_center_x + x * np.cos(angle) * (0.5 * (largest_x - smallest_x)))
            f_func = lambda x: x_func(x) * self._f()
            problem_func = lambda x: self.new_problem(external_flux=f_func(x), current_sources=Is_func(x))
            out = compute_maximal_parameter(problem_func, initial_guess=start_initial_guess, **options)
            lower_bound, upper_bound, out_config, info = out
            current[angle_nr] = lower_bound * np.sin(angle) * max_current_factor if lower_bound is not None else np.nan
            external_flux[angle_nr] = x_func(lower_bound) if lower_bound is not None else np.nan
            all_configs += [out_config]
            all_infos += [info]

        return external_flux, current, all_configs, all_infos

    def __str__(self):
        return "static problem: " + \
               "\n\tcurrent sources: " + self.get_current_sources().__str__() + \
               "\n\texternal_flux: " + self.get_external_flux().__str__() + \
               "\n\tvortex configuration: " + self.get_vortex_configuration().__str__() + \
               "\n\tphase zone: " + self.get_phase_zone().__str__() + \
               "\n\tcurrent-phase relation: " + self.current_phase_relation.__str__()

    def _Is(self):
        return self.current_sources

    def _f(self):
        return self.external_flux

    def _nt(self):
        return self.vortex_configuration

    def _cp(self, Ic, theta):
        return self.current_phase_relation.eval(Ic, theta)

    def _dcp(self, Ic, theta):
        return self.current_phase_relation.d_eval(Ic, theta)

    def _icp(self, Ic, theta):
        return self.current_phase_relation.i_eval(Ic, theta)

    def _Is_norm(self):
        if self.current_sources_norm is None:
            self.current_sources_norm = scipy.linalg.norm(np.broadcast_to(self.current_sources, (self.circuit._Nj(),)))
        return self.current_sources_norm


class StaticConfiguration:
    """
    Approximation or solution to static problem.

    It is defined by a StaticProblem and theta. Here theta must be a
    numpy array of shape (Nj,).

    Provides methods to compute all physical quantities associated with the state.
    The quantities are dimensionless, see the user manual (on github) for a list
    of definitions.

    Furthermore provides a .plot() method to visualize the quantities superimposed
    on the circuit.

    Parameters
    ----------
    problem : StaticProblem
        Static problem object for which this is an approximation or solution.
    theta : (Nj,) array
        Gauge invariant phase differences at each junction, which fully encodes
        the state.
    """

    def __init__(self, problem: StaticProblem, theta: np.ndarray):
        self.problem = problem
        self.theta = np.array(theta)
        if not self.theta.shape == (self.problem.get_circuit()._Nj(),):
            raise ValueError("theta must be of shape (Nj,)")

    def get_circuit(self) -> Circuit:
        """
        Returns circuit (stored in problem).
        """
        return self.problem.get_circuit()

    def get_problem(self) -> StaticProblem:
        """
        Returns the static problem this configuration is associated with.
        """
        return self.problem

    def get_phase(self) -> np.ndarray:
        """
        Returns (Nn,) array containing phases at each node
        """
        # by default the last node (node with highest index number) is grounded.
        M = self.get_circuit().get_cut_matrix()
        return self.get_circuit().Msq_solve(M @ self._th())

    def get_theta(self) -> np.ndarray:
        """
        Returns (Nj,) array containing gauge invariant phase difference at each junction.
        """
        return self.theta

    def get_vortex_configuration(self) -> np.ndarray:
        """
        Returns (Nf,) int array containing vorticity at each face.
        """
        A, tpr = self.get_circuit().get_cycle_matrix(), 1.0 / (2.0 * np.pi)
        return - (A @ np.round(self._th() / (2.0 * np.pi))).astype(int)

    def get_current(self) -> np.ndarray:
        """
        Returns (Nj,) array containing current through each junction.
        """
        return self.problem._cp(self.get_circuit()._Ic(), self._th())

    def get_cycle_current(self) -> np.ndarray:
        """
        Returns (Nf,) array containing path current around each face.
        Defined as I = A.T @ J + I_source.
        """
        A = self.get_circuit().get_cycle_matrix()
        return self.get_circuit().Asq_solve(A @ (self.get_current() - self.problem.current_sources))

    def get_flux(self) -> np.ndarray:
        """
        Returns (Nf,) array containing magnetic flux at each face.
        Defined as f + (A @ L @ I) / (2 * pi).
        """
        A = self.get_circuit().get_cycle_matrix()
        L = self.get_circuit()._L()
        return self.problem.external_flux + A @ L @ self.get_current() / (2 * np.pi)

    def get_magnetic_energy(self) -> np.ndarray:
        """
        Returns (Nj,) array containing magnetic energy at each junction.
        """
        return 0.5 * self.get_circuit()._L() @ (self.get_current() ** 2)

    def get_josephson_energy(self) -> np.ndarray:
        """
        Returns (Nj,) array containing Josephson energy at each junction.
        """
        return self.problem._icp(self.get_circuit()._Ic(), self._th())

    def get_energy(self) -> np.ndarray:
        """
        Returns get_EM() + get_EJ().
        """
        return self.get_josephson_energy() + self.get_magnetic_energy()

    def satisfies_kirchhoff_rules(self, tol=DEF_TOL):
        """
        Returns if configuration satisfies Kirchhoff's current law.

        """
        return self.get_error_kirchhoff_rules() < tol

    def satisfies_winding_rules(self, tol=DEF_TOL):
        """
        Returns if configuration satisfies the winding rules.

        """
        return self.get_error_winding_rules() < tol

    def satisfies_target_vortices(self):
        """
        Returns if vortex configuration equals that of problem.
        """
        return np.all(self.get_vortex_configuration() == self.problem.get_vortex_configuration())

    def is_stable(self) -> int:
        """
        Determines if a configuration is dynamically stable.

        The criterion for stability is that the Jacobian matrix of the time-evolution at the
        stationairy point is negative definite.

        Returns
        -------
        status : int
            0: stable, 1: unstable or 2: indeterminate
        """
        cp = self.get_problem().get_current_phase_relation()
        status = compute_stability(self.get_circuit(), self._th(), cp)
        return status

    def is_solution(self, tol=DEF_TOL):
        """
        Returns if configuration is a solution meaning it must satisfy both Kirchhoff
        current law and winding rules.
        """
        return self.satisfies_kirchhoff_rules(tol) & self.satisfies_winding_rules(tol)

    def is_target_solution(self, tol=DEF_TOL):
        """
        Returns if configuration is a solution and its vortex_configuration equals
        the one specified in problem.
        """
        return self.is_solution(tol=tol) & self.satisfies_target_vortices()

    def is_stable_target_solution(self, tol=DEF_TOL):
        """
        Returns if configuration is a solution, is stable and its vortex_configuration equals
        the one specified in problem.
        """
        return self.is_target_solution(tol=tol) & (self.is_stable() == 0)

    def get_error_kirchhoff_rules(self) -> np.ndarray:
        """
        Returns normalized residual of kirchhoff's rules (normalized so cannot exceed 1).
        """
        return get_kirchhoff_error(self.get_circuit(), self.get_current(), self.get_problem()._Is(),
                                   precomputed_Is_norm=self.problem._Is_norm())

    def get_error_winding_rules(self) -> np.ndarray:
        """
        Returns normalized residual of the winding rules (normalized so cannot exceed 1).
        """
        circuit, problem = self.get_circuit(), self.get_problem()
        f, L = problem._f(), circuit._L()
        return get_winding_error(circuit, self._th(), self.get_current(), 2 * np.pi * f)

    def get_error(self):
        """
        Returns get_error_kirchhoff_rules(), get_error_winding_rules().
        """
        return self.get_error_kirchhoff_rules(), self.get_error_winding_rules()

    def plot(self, fig=None, node_quantity=None, junction_quantity="I", face_quantity=None,
             vortex_quantity="n", show_grid=True, show_nodes=True, return_plot_handle=False,
             **kwargs):
        """
        Visualize static configuration on circuit.

        See :py:attr:`circuit_visualize.CircuitPlot` for documentation.

        Attributes
        ----------
        return_plot_handle=False : bool
            If True this method returns the ConfigPlot object used to create the plot.

        Returns
        -------
        fig : matplotlib figure handle
            Returns figure handle
        ax : matplotlib axis handle
            Returns axis handle
        plot_handle : ConfigPlot (optional)
            Object used to create the plot

        """
        from pyjjasim.circuit_visualize import ConfigPlot

        self.plot_handle = ConfigPlot(self, vortex_quantity=vortex_quantity, show_grid=show_grid,
                                      junction_quantity=junction_quantity,  show_nodes=show_nodes,
                                      node_quantity=node_quantity, face_quantity=face_quantity,
                                      fig=fig, **kwargs)
        if return_plot_handle:
            return *self.plot_handle.make(), self.plot_handle
        return self.plot_handle.make()

    def report(self):
        print("Kirchhoff rules error:    ", self.get_error_kirchhoff_rules())
        print("Path rules error:         ", self.get_error_winding_rules())
        print("is stable:                ", self.is_stable() == 0)
        print("is target vortex solution:", self.satisfies_target_vortices())


    def save(self, filename):
        """
        Store configuration in .npy file. Note that the current-phase-relation is not stored!
        """
        with open(filename, "wb") as ffile:
            x, y = self.problem.circuit.graph.coo()
            n1, n2 = self.problem.circuit.graph.get_edges()
            np.save(ffile, x)
            np.save(ffile, y)
            np.save(ffile, n1)
            np.save(ffile, n2)
            np.save(ffile, self.problem.circgiduit.critical_current)
            np.save(ffile, self.problem.circuit.resistance)
            np.save(ffile, self.problem.circuit.capacitance)
            L_is_sparse = scipy.sparse.issparse(self.problem.circuit.inductance)
            np.save(ffile, L_is_sparse)
            if L_is_sparse:
                np.save(ffile, self.problem.circuit.inductance.indptr)
                np.save(ffile, self.problem.circuit.inductance.indices)
                np.save(ffile, self.problem.circuit.inductance.data)
            else:
                np.save(ffile, self.problem.circuit.inductance)
            np.save(ffile, self.problem.current_sources)
            np.save(ffile, self.problem.external_flux)
            np.save(ffile, self.problem.vortex_configuration)
            np.save(ffile, self.theta)

    @staticmethod
    def load(filename) -> StaticConfiguration:
        """
        Load configuration created with the .save(filename) method. Returns StaticConfiguration.
        Note that the loaded problem will always have the default current-phase-relation.
        """

        with open(filename, "rb") as ffile:
            x = np.load(ffile)
            y = np.load(ffile)
            node1 = np.load(ffile)
            node2 = np.load(ffile)
            g = EmbeddedGraph(x, y, node1, node2)
            Ic = np.load(ffile)
            R = np.load(ffile)
            C = np.load(ffile)
            L_is_sparse = np.load(ffile)
            if L_is_sparse:
                indptr = np.load(ffile)
                indices = np.load(ffile)
                data = np.load(ffile)
                Nj = len(node1)
                L = scipy.sparse.csc_matrix((data, indices, indptr), shape=(Nj, Nj))
            else:
                L = np.load(ffile)
            circuit = Circuit(g, critical_current=Ic, resistance=R,
                              capacitance=C, inductance=L)
            Is = np.load(ffile)
            f = np.load(ffile)
            n = np.load(ffile)
            prob = StaticProblem(circuit, current_sources=Is, external_flux=f, vortex_configuration=n)
            th = np.load(ffile)
            return StaticConfiguration(problem=prob, theta=th)

    def _th(self):
        return self.theta

    def __str__(self):
        return f"Static configuration with theta={self.theta}"


"""
UTILITY ALGORITHMS
"""

def get_kirchhoff_error(circuit: Circuit, I, Is, precomputed_Is_norm=None):
    """
    Residual of kirchhoffs current law: M @ (I - Is) = 0. Normalized; so between 0 and 1.
    """
    if precomputed_Is_norm is None:
        precomputed_Is_norm = scipy.linalg.norm(Is)
    b = circuit.get_cut_matrix() @ (I - Is)
    M_norm = circuit._get_M_norm()
    normalizer = M_norm * (precomputed_Is_norm + scipy.linalg.norm(I))
    return np.finfo(float).eps if np.abs(normalizer) < 1E-20 else scipy.linalg.norm(b) / normalizer

def get_winding_error(circuit: Circuit, th, I, df):
    """
    Residual of winding rule: A @ (thp - g) = 0. Normalized; so between 0 and 1.
    (where thp = th + L @ I)
    """
    def norm(x):
        return scipy.linalg.norm(x) / np.sqrt(len(x))
    A = circuit.get_cycle_matrix()
    L = circuit.get_inductance()
    A_norm = circuit._get_A_norm()
    normalizer = A_norm * (norm(th) + norm(L @ I)) + norm(df)
    return np.finfo(float).eps if np.abs(normalizer) < 1E-20 else norm(df + A @ (th + L @ I)) / normalizer

def principle_value(theta):
    """
    Principle value of angle quantity defined as its value in range [-pi, pi)
    """
    return theta - 2 * np.pi * np.round(theta / (2 * np.pi))

def get_g(circuit: Circuit, f=0, z=0):
    """
    g vector obeying A @ g = 2 * pi * (z - f)
    """
    A, Nf = circuit.get_cycle_matrix(), circuit._Nf()
    return 2 * np.pi * A.T @ circuit.Asq_solve(np.broadcast_to(z - f, (Nf,)))

def change_phase_zone(circuit: Circuit, theta, z_old, z_new):
    """
    Converts solution theta in old phase zone z_old to the equivalent
    state theta_out in new phase zone z_new.

    More precisely: adds multiples of 2*pi to theta such that it obeys
    A @ (th_new + L @ I) = 2 * pi * (z_new - f)
    (assuming it already satisfied A @ (th_old + L @ I) = 2 * pi * (z_old- f))

    Parameters
    ----------
    circuit : Circuit
        Circuit.
    theta : (Nj,) array
        Theta in old phase zone.
    z_old : (Nf,) int array
        Old phase zone.
    z_new : (Nf,) int array
        New phase zone.

    Returns
    -------
    theta_new : (Nj,) array
        Theta expressed in new phase zone.
    """
    if np.all(z_new == z_old):
        return theta
    return theta + circuit._A_solve(np.broadcast_to(z_new - z_old, (circuit._Nf(),)).copy()) * 2.0 * np.pi

def node_to_junction_current(circuit: Circuit, node_current):
    """
    Conversion from node_current to junction_current.

    Parameters
    ----------
    node_current : (Nn,) array
        At each node how much current is injected or ejected  (+ if injected)

    Returns
    -------
    junction_current: (Nj,) array
        Returns a configuration of currents at each junction such that at any node
        the net injected current through all its neighbouring edges matches the specified
        node_current.
    """
    # Mr = circuit._Mr()
    # return -Mr.T @ scipy.sparse.linalg.spsolve(Mr @ Mr.T, node_current[:-1])
    return - circuit.get_cut_matrix().T @ circuit.Msq_solve(node_current)

"""
PARAMETER MAXIMIZATION ALGORITHMS
"""


def compute_maximal_parameter(problem_function, initial_guess=None, lambda_tol=DEF_MAX_PAR_TOL,
                              estimated_upper_bound=1.0, maxiter=DEF_MAX_PAR_MAXITER,
                              stepsize_reduction_factor=DEF_MAX_PAR_REDUCE_FACT, require_stability=True,
                              require_vortex_configuration_equals_target=True,
                              compute_parameters=None) -> tuple[float, float, StaticConfiguration, ParameterOptimizeInfo]:
    """
    Finds the largest value of lambda for which problem_function(lambda)
    has a stable stationary state.

     - Must be able to find a stable configuration at lambda=0.
     - One can manually specify an initial_guess for lambda=0.
     - returns a lower- and upperbound for lambda. Stops when the difference < lambda_tol * lower_bound
     - furthermore returns config containing the solutions at the lower_bound. Also its
       accompanied problem has f and Is of lower_bound.
     - Also returns ParameterOptimizeInfo object containing information about the iteration.
     - Algorithm stops if lambda_tol is reached or when newton_iteration failed to converge or diverge.
     - Algorithm needs an estimate of the upperbound for lambda to work.

    Parameters
    ----------
    problem_function : func(lambda) -> StaticProblem
        Function with argument the optimization parameter lambda returning a valid
        StaticProblem object.
    initial_guess=None : valid initial_guess input for StaticProblem.compute()
        Initial guess for problem_function(0) used as starting point for iteration.
        At subsequent iterations the solution theta of highest valid lambda so far is used.
        None means problem_function(0).approximate() is used.
        Alternative input: initial_guess(lambda) -> theta. Initial guess used at every iteration.
    lambda_tol=DEF_MAX_PAR_TOL : float
        Target precision for parameter lambda. Stops iterating if
        upperbound - lowerbound < lambda_tol * lower_bound.
    estimated_upper_bound=1.0 : float
        Estimate for the upperbound for lambda.
    maxiter=DEF_MAX_PAR_MAXITER : int
        Maximum number of iterations.
    stepsize_reduction_factor=DEF_MAX_PAR_REDUCE_FACT : float
        Lambda is multiplied by this factor every time an upper_bound is found.
    require_stability=True : bool
        If True, convergence to a state that is dynamically unstable is
        considered diverged. (see StaticConfiguration.is_stable())
    require_vortex_configuration_equals_target=True : bool
        If True, A result of .compute() is only considered a solution if its
        vortex configuration matches its set "target" vortex configuration
        in the source static_problem.
    compute_parameters: dict or func(lambda) -> dict
        Keyword-argument parameters passed to problem_function(lambda).compute()
        defined as a dictionary or as a function with lambda as input that
        generates a dictionary.

    Returns
    -------
    lambda_lowerbound : float
        Lowerbound of lambda.
    lambda_upperbound : float
        Upperbound of lambda.
    config : StaticConfiguration
        Containing solutions at lambda=lambda_lowerbound
    iteration_info : ParameterOptimizeInfo
        Object containing information about the iteration.
    """

    if compute_parameters is None:
        compute_parameters = {}

    stable_status = None

    # prepare info handle
    info = ParameterOptimizeInfo(problem_function, lambda_tol, require_stability,
                                 require_vortex_configuration_equals_target, maxiter)

    # determine solution at lambda=0
    cur_problem = problem_function(0)

    if initial_guess is None:
        initial_guess = cur_problem.approximate()
    if hasattr(initial_guess, "__call__"):
        theta0 = initial_guess(0)
    else:
        theta0 = initial_guess
    if isinstance(theta0, StaticConfiguration):
        theta0 = theta0._th()
    compute_param = compute_parameters if isinstance(compute_parameters, dict) else compute_parameters(0)
    out = cur_problem.compute(initial_guess=theta0, **compute_param)
    config, status, newton_iter_info = out[0], out[1], out[2]
    is_solution = status==0
    if require_vortex_configuration_equals_target:
        is_target_vortex_config = config.satisfies_target_vortices()
        is_solution &= is_target_vortex_config
    if is_solution and require_stability:
        stable_status = config.is_stable()
        is_solution &= stable_status == 0
    theta = config.theta

    info._preset(is_solution)

    # return if no solution at lambda=0
    if not is_solution:
        return None, None, None, info

    # prepare iteration to find maximum lambda
    found_upper_bound = False
    lambda_stepsize = estimated_upper_bound
    lambda_val = lambda_stepsize
    theta0 = theta

    # start iteration to find maximum lambda
    iter_nr = 0
    while True:

        # determine solution at current lambda
        cur_problem = problem_function(lambda_val)
        if hasattr(initial_guess, "__call__"):
            theta0 = initial_guess(lambda_val)
            if isinstance(theta0, StaticConfiguration):
                theta0 = theta0._th()
        compute_param = compute_parameters if isinstance(compute_parameters, dict) else compute_parameters(lambda_val)
        out = cur_problem.compute(initial_guess=theta0, **compute_param)
        config, status, newton_iter_info = out[0], out[1], out[2]
        has_converged = status == 0
        if require_vortex_configuration_equals_target and has_converged:
            is_target_vortex_config = config.satisfies_target_vortices()
            has_converged &= is_target_vortex_config
        else:
            is_target_vortex_config = False

        theta = config.theta

        if status == 2:
            break

        if require_stability:
            if has_converged:
                stable_status = config.is_stable()
                is_stable = stable_status == 0
            else:
                is_stable = False
            is_solution = has_converged and is_stable
        else:
            is_stable = False
            is_solution = has_converged

        # update information on current iteration in info handle
        info._set(lambda_val, config if has_converged else None, lambda_stepsize,
                  has_converged, newton_iter_info, is_target_vortex_config, is_stable)

        # determine new lambda value to try (and corresponding initial condition)
        if is_solution:
            lambda_val += lambda_stepsize
            theta0 = theta.copy()
        else:
            lambda_val -= lambda_stepsize * (1 - stepsize_reduction_factor)
            lambda_stepsize*=stepsize_reduction_factor
            found_upper_bound = True
        if (lambda_stepsize / lambda_val) < lambda_tol:
            break
        if iter_nr >= (maxiter - 1):
            break
        if require_stability and has_converged:
            if stable_status == 2:
                break
        iter_nr += 1

    # determine lower- and upperbound on lambda
    info._finish(status, stable_status)
    lower_bound = lambda_val - lambda_stepsize
    upper_bound = lambda_val if found_upper_bound else np.inf

    if lower_bound is None:
        config = None
    else:
        out_problem = problem_function(lower_bound)
        config = StaticConfiguration(out_problem, theta0)
    return lower_bound, upper_bound, config, info


"""
APPROXIMATE STATE FINDING ALGORITHMS
"""

def london_approximation(circuit: Circuit, f, n, Is):
    """
    Core algorithm computing london approximation.
    """
    Nj = circuit.junction_count()
    if circuit._has_identical_critical_current():
        if np.abs(circuit.critical_current[0]) < 1E-12:
            return np.zeros(Nj, dtype=np.double)
    A, Nf = circuit.get_cycle_matrix(), circuit._Nf()
    Ic = circuit._Ic().copy()
    Ic[np.abs(Ic) > 1E-12] = Ic[np.abs(Ic) > 1E-12] ** -1
    L, iIc = circuit._L(), scipy.sparse.diags(Ic)
    df = 2 * np.pi * np.broadcast_to(n - f, (Nf,))
    Isc = np.broadcast_to(Is, (Nj,))
    return iIc @ (A.T @ circuit._AiIcpLA_solve(df - A @ (iIc + L) @ Isc) + Isc)


"""
STATIONAIRY STATE FINDING ALGORITHMS
"""


def static_compute(circuit: Circuit, theta0, Is, f, n, z=0,
                   cp=DefaultCPR(), tol=DEF_TOL, maxiter=DEF_NEWTON_MAXITER,
                   stop_as_residual_increases=True, stop_if_not_target_n=False):
    """
    Core algorithm computing stationary state of a Josephson Junction Circuit using Newtons method.

    Stand-alone method. The wrappers StaticProblem and StaticConfiguration are more convenient.

    Status
    ------
    Stops iterating if ( -> status):
     - residual is smaller than tol, target_n: 0 (converged)
     - residual smaller than tol, not target_n:  1 (diverged)
     - iteration number iter exceeds maxiter: 2 (indeterminate)
     - residual exceeds 0.5: 1 (diverged)
     - if get_n(theta) != n and stop_if_not_target_n==True: 1 (diverged)
     - resid(iter) > resid(iter-3) and stop_as_residual_increases==True : 1 (diverged)

    Parameters
    ------
    circuit: Circuit
        Josephson junction circuit
    theta0 : (Nj,) ndarray
        Initial guess
    Is : (Nj,) ndarray
        Current sources at each junction
    f : (Nf,) ndarray
        Frustration in each face
    n : (Nf,) int ndarray
        Number of vortices in each face
    z=0 : (Nf,) int ndarray or scalar
        Phase zone of each face
    cp=DefaultCPR() : CurrentPhaseRelation
        Current phase relation
    tol=DEF_TOL :  scalar
        Tolerance. is solution if |residual| < tol.
    max_iter=100 :  scalar
        Maximum number of newton iterations.
    stop_as_residual_increases=True : bool
        Iteration stops if error(iter) > error(iter - 3)
    stop_if_not_target_n=False : bool
        Iteration stops if n != target_n

    Returns
    -------
    theta : (Nj,) ndarray
        Gauge invariant phase difference of solution
    convergence_status : int
        * 0 -> converged
        * 1 -> diverged
        * 2 -> max_iter reached without converging or diverging.
    info : NewtonIterInfo
        Information about iteration (timing, steps, residuals, etc)
    """

    # prepare newton iter info
    info = NewtonIterInfo(tol, maxiter)

    # get circuit quantities and matrices
    Nj, Nf = circuit._Nj(), circuit._Nf()
    Mr, M, A = circuit._Mr(), circuit.get_cut_matrix(), circuit.get_cycle_matrix()
    L = circuit._L()
    Ic = np.broadcast_to(circuit.get_critical_current(), (Nj,))

    Is = np.ones((Nj,), dtype=np.double) * Is if np.array(Is).size == 1 else Is
    f = np.ones((Nf,), dtype=np.double) * f if np.array(f).size == 1 else f
    n = np.ones((Nf,), dtype=int) * n if np.array(n).size == 1 else n

    # iteration-0 computations
    df = 2 * np.pi * (f - z)
    theta = theta0.copy()
    I = cp.eval(Ic, theta)
    LIs = L @ Is
    Is_norm = scipy.linalg.norm(Is)

    # iteration-0 compute errors
    error1 = get_kirchhoff_error(circuit, I, Is,  precomputed_Is_norm=Is_norm)
    error2 = get_winding_error(circuit, theta, I, df)
    error = max(error1, error2)
    is_target_n = np.all(A @ (np.round(theta / (2 * np.pi))).astype(int) == z - n)
    info._set(error, is_target_n)

    # prepare newton iteration
    prev_error = np.inf
    iteration = 0

    while not (error < tol or (error > 0.5 and iteration > 5) or (stop_if_not_target_n and is_target_n) or
               (stop_as_residual_increases and error > prev_error) or iteration >= maxiter):
        # iteration computations

        q = cp.d_eval(Ic, theta)
        q[np.abs(q) < 0.1 * tol] = 0.1 * tol
        S = L + scipy.sparse.diags(1/q, 0)
        y = (I - Is) / q
        j = circuit.Asq_solve_sandwich(A @ (theta - y - LIs) + df, S)
        if np.any(np.isnan(j)) or np.any(np.isinf(j)):
            theta += 10 ** 10
        else:
            theta -= y + (A.T @ j) / q
        I = cp.eval(Ic, theta)

        # iteration error computations
        error1 = get_kirchhoff_error(circuit, I, Is, precomputed_Is_norm=Is_norm)
        error2 = get_winding_error(circuit, theta, I, df)
        error = max(error1, error2)
        is_target_n = np.all(A @ (np.round(theta / (2 * np.pi))).astype(int) == z - n)
        info._set(error, is_target_n)
        if iteration >= 3:
            prev_error = info.error[iteration - 3]

        iteration += 1

    return theta, info.get_status(), info

"""
STABILITY ALGORITHMS
"""

def compute_stability(circuit: Circuit, theta, cp):
    """
    Core implementation to determine if a configuration on a circuit is stable in the sense that
    the Jacobian is negative definite. Does not explicitly check if configuration is a stationairy point.

    Parameters
    ----------
    circuit : Circuit
        Circuit
    theta : (Nj,) array
        Gauge invariant phase difference of static configuration of circuit.
    cp : CurrentPhaseRelation
        Current-phase relation.

    Returns
    -------
    status : int
        0: stable, 1: unstable or 2: indeterminate
    """
    J = stability_scheme_0(circuit, theta, cp)
    status = is_positive_definite_superlu(-J)
    if status == 2:
        raise ValueError("Choleski factorization failed; unable to determine positive definiteness")
    return status

def is_positive_definite_superlu(X):
    """
    Determine if matrix is positive definite using superlu package.

    Parameters
    ----------
    X : sparse matrix
        Sparse matrix.

    Returns
    -------
    status : int
        0 -> positive definite, 1 -> not positive definite, 2 -> choleski factorization failed

    """
    eps = 10 * np.finfo(float).eps
    f = scipy.sparse.linalg.splu(X, diag_pivot_thresh=0)
    Up = (f.L @ scipy.sparse.diags(f.U.diagonal())).T
    if not np.allclose((Up - f.U).data, 0):
        return 1
    return int(~np.all(f.U.diagonal() > -eps))

def stability_scheme_0(circuit: Circuit, theta, cp):
    """
    Scheme to determine matrix for which the system is stable if it is negative definite.

    Works for mixed inductance but generally slower than scheme 1.

    Scheme 0: matrix is:
     * J = m @ X @ m.T
     * where X = -grad cp(Ic, theta) - A.T @ inv(A @ L @ A.T) @ A
     * and m = [M ; A @ L]
     * all-zero rows and columns are removed.
    """
    Nj, Nnr = circuit._Nj(), circuit._Nnr()
    A, M, L = circuit.get_cycle_matrix(),  circuit._Mr(), circuit._L()
    Ic = circuit._Ic()
    q = cp.d_eval(Ic, theta)
    AL = (A @ L @ A.T).tocoo()
    ALL = scipy.sparse.coo_matrix((AL.data, (AL.row + Nnr, AL.col + Nnr)), shape=(Nj, Nj)).tocsc()
    m = scipy.sparse.vstack([M, A @ L]).tocsc()
    J = - (m @ scipy.sparse.diags(q, 0) @ m.T + ALL)
    select = np.diff(J.indptr)!=0
    J = J[select, :][:, select]
    return J

