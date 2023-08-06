import pytest

import kep_solver.model as model
import kep_solver.graph as graphing
import kep_solver.fileio as fileio


@pytest.fixture(scope="module")
def test1_graph():
    instance = fileio.read_json("tests/test_instances/test1.json")
    graph = graphing.CompatibilityGraph(instance)
    return graph


@pytest.fixture(scope="module")
def test3b_graph():
    instance = fileio.read_json("tests/test_instances/test3b.json")
    graph = graphing.CompatibilityGraph(instance)
    return graph


@pytest.fixture(scope="module")
def test4_graph():
    instance = fileio.read_json("tests/test_instances/test4.json")
    graph = graphing.CompatibilityGraph(instance)
    return graph


@pytest.fixture(scope="module")
def test5_graph():
    instance = fileio.read_json("tests/test_instances/test5.json")
    graph = graphing.CompatibilityGraph(instance)
    return graph


def test_transplant_count_test1(test1_graph):
    obj = model.TransplantCount()
    cycles = test1_graph.findCycles(3)
    for cycle in cycles:
        indices = [int(v.donor.id) for v in cycle]
        if indices == [1, 2]:
            assert obj.value(test1_graph, cycle) == 2
        if indices == [1, 2, 3]:
            assert obj.value(test1_graph, cycle) == 3


def test_transplant_count_test5(test5_graph):
    obj = model.TransplantCount()
    chains = test5_graph.findChains(3)
    for chain in chains:
        indices = [int(v.donor.id) for v in chain]
        if indices == [1, 2]:
            assert obj.value(test5_graph, chain) == 2
        if indices == [1, 3, 4]:
            assert obj.value(test5_graph, chain) == 3


def test_effective_twoway_count_test1(test1_graph):
    obj = model.EffectiveTwoWay()
    cycles = test1_graph.findCycles(3)
    for cycle in cycles:
        indices = [int(v.donor.id) for v in cycle]
        if indices == [1, 2]:
            assert obj.value(test1_graph, cycle) == 1
        if indices == [1, 2, 3]:
            assert obj.value(test1_graph, cycle) == 0


def test_effective_twoway_count_test4(test4_graph):
    obj = model.EffectiveTwoWay()
    cycles = test4_graph.findCycles(3)
    graphing.build_alternates_and_embeds(cycles)
    for cycle in cycles:
        indices = [int(v.donor.id) for v in cycle]
        if indices == [1, 2]:
            assert obj.value(test1_graph, cycle) == 1
        if indices == [1, 2, 4]:
            assert obj.value(test1_graph, cycle) == 1
        if indices == [2, 4, 3]:
            assert obj.value(test1_graph, cycle) == 0


def test_backarcs_test3b(test3b_graph):
    obj = model.BackArcs()
    cycles = test3b_graph.findCycles(3)
    graphing.build_alternates_and_embeds(cycles)
    for cycle in cycles:
        indices = [int(v.donor.id) for v in cycle]
        if indices == [1, 2]:
            assert obj.value(test1_graph, cycle) == 0
        if indices == [1, 2, 3]:
            assert obj.value(test1_graph, cycle) == 2
        if indices == [1, 3]:
            assert obj.value(test1_graph, cycle) == 0
        if indices == [1, 3, 4]:
            assert obj.value(test1_graph, cycle) == 3
        if indices == [1, 4]:
            assert obj.value(test1_graph, cycle) == 0
        if indices == [1, 4, 3]:
            assert obj.value(test1_graph, cycle) == 3
        if indices == [3, 4]:
            assert obj.value(test1_graph, cycle) == 0


def test_backarcs_test5(test5_graph):
    obj = model.BackArcs()
    chains = test5_graph.findChains(3)
    graphing.build_alternates_and_embeds(chains)
    for chain in chains:
        indices = [int(v.donor.id) for v in chain]
        if indices == [1, 2]:
            assert obj.value(test1_graph, chain) == 0
        if indices == [1, 3, 4]:
            assert obj.value(test1_graph, chain) == 2


def test_threeway_count_test1(test1_graph):
    obj = model.ThreeWay()
    cycles = test1_graph.findCycles(3)
    for cycle in cycles:
        indices = [int(v.donor.id) for v in cycle]
        if indices == [1, 2]:
            assert obj.value(test1_graph, cycle) == 0
        if indices == [1, 2, 3]:
            assert obj.value(test1_graph, cycle) == 1


def test_threeway_count_test3b(test3b_graph):
    obj = model.ThreeWay()
    cycles = test3b_graph.findCycles(3)
    graphing.build_alternates_and_embeds(cycles)
    for cycle in cycles:
        indices = [int(v.donor.id) for v in cycle]
        if indices == [1, 2]:
            assert obj.value(test1_graph, cycle) == 0
        if indices == [1, 2, 3]:
            assert obj.value(test1_graph, cycle) == 1
        if indices == [1, 3]:
            assert obj.value(test1_graph, cycle) == 0
        if indices == [1, 3, 4]:
            assert obj.value(test1_graph, cycle) == 1
        if indices == [1, 4]:
            assert obj.value(test1_graph, cycle) == 0
        if indices == [1, 4, 3]:
            assert obj.value(test1_graph, cycle) == 1
        if indices == [3, 4]:
            assert obj.value(test1_graph, cycle) == 0


def test_threeway_count_test5(test5_graph):
    obj = model.ThreeWay()
    chains = test5_graph.findChains(3)
    for chain in chains:
        indices = [int(v.donor.id) for v in chain]
        if indices == [1, 2]:
            assert obj.value(test5_graph, chain) == 0
        if indices == [1, 3]:
            assert obj.value(test5_graph, chain) == 0
        if indices == [1, 3, 4]:
            assert obj.value(test5_graph, chain) == 1
