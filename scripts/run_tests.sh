if [ $1 = "sbml-test-suite" ]; then
    coverage run --omit=*/venv/* -m unittest libsignetsim.tests.sbmltestsuite.TestSuite
elif [ $1 = "biomodels" ]; then
    coverage run --omit=*/venv/* -m unittest libsignetsim.tests.biomodels.TestBiomodelsCompatibility
else
    coverage run --omit=*/venv/* -m unittest libsignetsim.simulation.tests.TestTimeseries
    coverage run --omit=*/venv/* -m unittest libsignetsim.simulation.tests.TestSteadyStates
    coverage run --omit=*/venv/* -m unittest libsignetsim.optimization.tests.TestOptimization
    coverage run --omit=*/venv/* -m unittest libsignetsim.sedml.tests.TestBiomodelsURI
    coverage run --omit=*/venv/* -m unittest libsignetsim.sedml.tests.TestSteadyStatesScan
    coverage run --omit=*/venv/* -m unittest libsignetsim.combine.tests.TestRunSedmls
fi