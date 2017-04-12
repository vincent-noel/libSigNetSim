OMIT=--omit=*/venv/*,*/virtualenv/*,*/dist-packages/*

if [ $1 = "sbml-test-suite" ]; then
    if [ $2 = "1.2" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l1v2 || exit 1;

    elif [ $2 = "2.1" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v1 || exit 1;

    elif [ $2 = "2.2" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v2 || exit 1;

    elif [ $2 = "2.3" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v3 || exit 1;

    elif [ $2 = "2.4" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v4 || exit 1;

    elif [ $2 = "2.5" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v5 || exit 1;

    elif [ $2 = "3.1" ]; then
        coverage run -a $OMIT -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l3v1 || exit 1;

    fi

elif [ $1 = "biomodels" ]; then
    coverage run -a $OMIT -m unittest libsignetsim.tests.biomodels.TestBiomodelsCompatibility || exit 1;

elif [ $1 = "others" ]; then
    coverage run -a $OMIT -m unittest libsignetsim.model.tests.TestFindKineticLaws || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.model.tests.TestReduceModel || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.model.tests.TestModelDefinition || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.model.tests.TestAnnotation || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.model.tests.TestRenameSbmlId || exit 1;

    coverage run -a $OMIT -m unittest libsignetsim.simulation.tests.TestTimeseries || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.simulation.tests.TestSteadyStates || exit 1;

    coverage run -a $OMIT -m unittest libsignetsim.optimization.tests.TestOptimization || exit 1;

    coverage run -a $OMIT -m unittest libsignetsim.sedml.tests.TestBiomodelsURI || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.sedml.tests.TestSteadyStatesScan || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.sedml.tests.TestLogscaleTimeseries || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.sedml.tests.TestSpecificationL1V2 || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.sedml.tests.TestMath || exit 1;

    coverage run -a $OMIT -m unittest libsignetsim.combine.tests.TestRunSedmls || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.combine.tests.TestShowCase || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.combine.tests.TestNoManifest || exit 1;

elif [ $1 = "simulation" ]; then
    coverage run -a $OMIT -m unittest libsignetsim.simulation.tests.TestTimeseries || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.simulation.tests.TestSteadyStates || exit 1;

elif [ $1 = "combine" ]; then
    coverage run -a $OMIT -m unittest libsignetsim.combine.tests.TestRunSedmls || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.combine.tests.TestShowCase || exit 1;
    coverage run -a $OMIT -m unittest libsignetsim.combine.tests.TestNoManifest || exit 1;


fi