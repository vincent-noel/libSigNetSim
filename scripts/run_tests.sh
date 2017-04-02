if [ $1 = "sbml-test-suite" ]; then
    coverage run --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.tests.sbmltestsuite.TestSuite
elif [ $1 = "biomodels" ]; then
    coverage run --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.tests.biomodels.TestBiomodelsCompatibility
else
    coverage run --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.simulation.tests.TestTimeseries
    coverage -a run --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.simulation.tests.TestSteadyStates
    coverage -a run --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.optimization.tests.TestOptimization
    coverage -a run --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.sedml.tests.TestBiomodelsURI
    coverage -a run --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.sedml.tests.TestSteadyStatesScan
    coverage -a run --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.combine.tests.TestRunSedmls
fi