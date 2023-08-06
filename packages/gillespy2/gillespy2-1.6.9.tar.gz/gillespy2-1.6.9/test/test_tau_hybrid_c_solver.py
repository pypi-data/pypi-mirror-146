import unittest

import gillespy2
import numpy
from gillespy2 import TauHybridCSolver
from example_models import Example, ExampleNoTspan
from gillespy2.core.gillespyError import SimulationError


class BoundaryConditionTestModel(gillespy2.Model):
    def __init__(self):
        gillespy2.Model.__init__(self, name="BoundaryConditionTestModel")
        s1 = gillespy2.Species(name="S1", boundary_condition=True, initial_value=0.001, mode='continuous')
        s2 = gillespy2.Species(name="S2", boundary_condition=False, initial_value=0.002, mode='continuous')
        s3 = gillespy2.Species(name="S3", boundary_condition=False, initial_value=0.001, mode='continuous')
        s4 = gillespy2.Species(name="S4", boundary_condition=True, initial_value=0.002, mode='continuous')
        self.add_species([s1, s2, s3, s4])

        k1 = gillespy2.Parameter(name="k1", expression="0.75")
        k2 = gillespy2.Parameter(name="k2", expression="0.25")
        self.add_parameter([k1, k2])

        reaction1 = gillespy2.Reaction(name="reaction1", propensity_function="vol*k1*S1*S2",
                                       reactants={s1: 1, s2: 1},
                                       products={s3: 1})
        reaction2 = gillespy2.Reaction(name="reaction2", propensity_function="vol*k2*S3",
                                       reactants={s3: 1},
                                       products={s1: 1, s2: 1})
        reaction3 = gillespy2.Reaction(name="reaction3", propensity_function="vol*k2*S3",
                                       reactants={s1: 1, s2: 2, s3: 1},
                                       products={s4: 1})
        self.add_reaction([reaction1, reaction2, reaction3])

        self.timespan(numpy.linspace(0, 20, 51))


# The output has a roughly predictable output, each species (approx.) approaching a particular value:
#   S1 -> 0     S2 -> 0.15      S3 -> 1.0 (should be approx. constant throughout)
class RateRuleTestModel(gillespy2.Model):
    def __init__(self):
        gillespy2.Model.__init__(self, name="RateRuleTestModel")
        s1 = gillespy2.Species(name="S1", initial_value=0.015, mode='continuous')
        s2 = gillespy2.Species(name="S2", initial_value=0.0, mode='continuous')
        s3 = gillespy2.Species(name="S3", initial_value=1.0, mode='continuous')
        self.add_species([s1, s2, s3])

        k1 = gillespy2.Parameter(name="k1", expression="1.0")
        self.add_parameter([k1])

        rule1 = gillespy2.RateRule(name="rule1", variable="S1", formula="-k1*S1")
        rule2 = gillespy2.RateRule(name="rule2", variable="S2", formula="k1*S1")
        rule3 = gillespy2.RateRule(name="rule3", variable="S3", formula="0.015-(S1+S2)")
        self.add_rate_rule([rule1, rule2, rule3])

        self.timespan(numpy.linspace(0, 20, 51))


class TestTauHybridCSolver(unittest.TestCase):
    def test_rate_rules(self):
        """
        Ensure that models provided with SBML rate rules work properly.
        Rate rule expressions are assumed valid and are tested in the Expressions test case.
        """
        model = RateRuleTestModel()
        solver = TauHybridCSolver(model=model)
        results = model.run(solver=solver, number_of_trajectories=1)

        self.assertAlmostEqual(results["S1"][-1], 0.0, places=3)
        self.assertAlmostEqual(results["S2"][-1], 0.015, places=3)
        self.assertTrue(numpy.all(results["S3"] == 1.0))

    def test_boundary_conditions(self):
        """
        Ensure that species marked with `boundary_condition=True` work properly.
        Boundary condition species should have a constant value throughout the simulation.
        Non-boundary condition species should change with the expected reaction rate.
        """
        model = BoundaryConditionTestModel()
        solver = TauHybridCSolver(model=model)
        results = model.run(solver=solver, number_of_trajectories=1)

        for spec_name, species in model.listOfSpecies.items():
            with self.subTest(msg="Unexpected species output for boundary condition setting",
                              boundary_condition=species.boundary_condition):
                spec_results = results[spec_name]
                is_uniform = numpy.all(spec_results == species.initial_value)
                self.assertTrue(species.boundary_condition == is_uniform)

    def test_run_example__with_increment_only(self):
        model = ExampleNoTspan()
        solver = TauHybridCSolver(model=model)
        results = solver.run(increment=0.2)

    def test_run_example__with_tspan_only(self):
        model = Example()
        solver = TauHybridCSolver(model=model)
        results = solver.run()

    def test_run_example__with_tspan_and_increment(self):
        with self.assertRaises(SimulationError):
            model = Example()
            solver = TauHybridCSolver(model=model)
            results = solver.run(increment=0.2)


if __name__ == '__main__':
    unittest.main()
