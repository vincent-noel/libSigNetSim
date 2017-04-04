OMIT=--omit=*/venv/*,*/virtualenv/*,*/dist-packages/*

if [ $1 = "sbml-test-suite" ]; then
    if [ $2 = "1.2" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l1v2
    elif [ $2 = "2.1" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v1
    elif [ $2 = "2.2" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v2
    elif [ $2 = "2.3" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v3
    elif [ $2 = "2.4" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v4
    elif [ $2 = "2.5" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v5
    elif [ $2 = "3.1" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l3v1
    fi
elif [ $1 = "biomodels" ]; then
    coverage run -a $OMIT -m unittest libsignetsim.tests.biomodels.TestBiomodelsCompatibility
else
    coverage run -a $OMIT -m unittest libsignetsim.model.tests.TestFindKineticLaws
    coverage run -a $OMIT -m unittest libsignetsim.model.tests.TestReduceModel
    coverage run -a $OMIT -m unittest libsignetsim.simulation.tests.TestTimeseries
    coverage run -a $OMIT -m unittest libsignetsim.simulation.tests.TestSteadyStates
    coverage run -a $OMIT -m unittest libsignetsim.optimization.tests.TestOptimization
    coverage run -a $OMIT -m unittest libsignetsim.sedml.tests.TestBiomodelsURI
    coverage run -a $OMIT -m unittest libsignetsim.sedml.tests.TestSteadyStatesScan
    coverage run -a $OMIT -m unittest libsignetsim.sedml.tests.TestLogscaleTimeseries
    coverage run -a $OMIT -m unittest libsignetsim.combine.tests.TestRunSedmls
    coverage run -a $OMIT -m unittest libsignetsim.combine.tests.TestShowCase
fi