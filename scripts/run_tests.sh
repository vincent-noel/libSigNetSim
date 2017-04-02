if [ $1 = "sbml-test-suite" ]; then
    python -m unittest libsignetsim.tests.sbmltestsuite.TestSuite
else
    python -m unittest libsignetsim.simulation.tests.TestTimeseries
    python -m unittest libsignetsim.simulation.tests.TestSteadyStates
    python -m unittest libsignetsim.optimization.tests.TestOptimization
    python -m unittest libsignetsim.sedml.tests.TestBiomodelsURI
    python -m unittest libsignetsim.sedml.tests.TestSteadyStatesScan
    python -m unittest libsignetsim.combine.tests.TestRunSedmls
    python -m unittest libsignetsim.tests.biomodels.TestBiomodelsCompatibility
fi