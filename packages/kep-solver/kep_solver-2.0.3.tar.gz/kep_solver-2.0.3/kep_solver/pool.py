"""Handling of KEP pools, which are just the rules, procedures and
algorithms for a particular KEP.
"""

from time import thread_time
from typing import Optional

from kep_solver.entities import Instance
from kep_solver.model import Objective, CycleAndChainModel
from kep_solver.graph import Exchange


class ModelledExchange:
    """An exchange as modelled, including its value for various
    objectives and any other relevant information.
    """

    def __init__(self, exchange: Exchange, values: list[float]):
        """Constructor for ModelledExchange. Contains the Exchange object, and
        also the value of this exchange for the various objectives in this
        model.

        :param exchange: The exchange
        :param values: The value of this exchange for each objective
        """
        self._exchange = exchange
        self._values = values

    @property
    def exchange(self) -> Exchange:
        """The underlying exchange."""
        return self._exchange

    @property
    def values(self) -> list[float]:
        """The values of this exchange."""
        return self._values

    def __str__(self) -> str:
        """A human-readable representation of this exchange."""
        return str(self._exchange)


class Solution:
    """A solution to one instance of a KEP. Contains the exchanges, and
    the set of objective values attained.
    """

    def __init__(
        self,
        exchanges: list[ModelledExchange],
        scores: list[float],
        possible: list[ModelledExchange],
        times: list[tuple[str, float]],
    ):
        """Constructor for Solution. This class essentially just stores
        any information that may be useful.

        :param exchanges: the list of selected exchanges
        :param scores: the list of scores achieved for each objective
        :param possible: the set of possible exchanges, and their
            values for each objective
        :param times: The time taken for various operations. Each is a
            tuple with a string description of the action, and the time
            (in seconds)
        """
        self._selected: list[ModelledExchange] = exchanges
        self._values: list[float] = scores
        self._possible: list[ModelledExchange] = possible
        self._times: list[tuple[str, float]] = times

    @property
    def times(self) -> list[tuple[str, float]]:
        """Get the time taken for various operations. Each element of
        the returned list is a tuple where the first item is a string
        description of some operation, and the second item is the time
        taken in seconds.

        :return: the list of times (and their descriptions)
        """
        return self._times

    @property
    def selected(self) -> list[ModelledExchange]:
        """Get the selected solution.

        :return: the list of exchanges selected.
        """
        return self._selected

    @property
    def values(self) -> list[float]:
        """Get the Objective values of the selected solution.

        :return: the list of objective values
        """
        return self._values

    @property
    def possible(self) -> list[ModelledExchange]:
        """Return a list of all the possible chains and cycles that may
        be selected.  For each chain/cycle, there is an associated list
        of values, such that the i'th value for a given chain/cycle is
        the value that chain/cycle has for the i'th objective.

        :return: a list of cycles/chains, and the value of said
            cycle/chain for each objective
        """
        return self._possible


class Pool:
    """A KEP pool."""

    def __init__(
        self, objectives: list[Objective], maxCycleLength: int, maxChainLength: int
    ):
        """Constructor for Pool. This represents a set of objectives, and
        parameters for running matchings (such as maximum cycle and chain
        lengths).

        :param objectives: the list of objectives
        :param maxCycleLength: The longest cycle length allowed.
        :param maxChainLength: The longest chain length allowed. Note that the
            length of a chain includes the non-directed donor.
        """
        # Create a copy of the list of objectives with the magic colon
        self._objectives: list[Objective] = objectives[:]
        self._maxCycleLength = maxCycleLength
        self._maxChainLength = maxChainLength

    def solve_single(
        self,
        instance: Instance,
        maxCycleLength: Optional[int] = None,
        maxChainLength: Optional[int] = None,
    ) -> Optional[Solution]:
        """Run a single instance through this pool, returning the solution, or
        None if no solution is found (e.g., if the solver crashes).

        :param instance: The instance to solve
        :param maxCycleLength: The longest cycle allowed. If not specified, we
            use the default from the Pool
        :param maxChainLength: The longest chain allowed. If not specified, we
            use the default from the Pool
        :return: A Solution object, or None if an error occured.
        """
        if maxCycleLength is None:
            maxCycleLength = self._maxCycleLength
        if maxChainLength is None:
            maxChainLength = self._maxChainLength
        t = thread_time()
        model = CycleAndChainModel(
            instance,
            self._objectives,
            maxChainLength=maxChainLength,
            maxCycleLength=maxCycleLength,
        )
        times = [("Model building", thread_time() - t)]
        t = thread_time()
        solution: list[Exchange] = model.solve()
        times.append(("Model solving", thread_time() - t))
        if solution is None:
            return None
        values = model.objective_values
        exchange_values: dict[Exchange, list[float]] = {
            exchange: model.exchange_values(exchange) for exchange in model.exchanges
        }
        solutions = [ModelledExchange(ex, exchange_values[ex]) for ex in solution]
        possible = [
            ModelledExchange(ex, exchange_values[ex]) for ex in exchange_values.keys()
        ]
        return Solution(solutions, values, possible, times)
