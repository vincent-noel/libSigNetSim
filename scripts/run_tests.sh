if [ $1 = "sbml-test-suite" ]; then
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.tests.sbmltestsuite.TestSuite
elif [ $1 = "biomodels" ]; then
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.tests.biomodels.TestBiomodelsCompatibility
else
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.model.tests.TestFindKineticLaws
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.model.tests.TestReduceModel
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.simulation.tests.TestTimeseries
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.simulation.tests.TestSteadyStates
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.optimization.tests.TestOptimization
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.sedml.tests.TestBiomodelsURI
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.sedml.tests.TestSteadyStatesScan
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.sedml.tests.TestLogscaleTimeseries
    coverage run -a --omit=*/venv/*,*/virtualenv/* -m unittest libsignetsim.combine.tests.TestRunSedmls
fi