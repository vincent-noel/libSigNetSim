
if [ "$3" = "python3" ]; then
    coverage_binary="coverage3"
else
    coverage_binary="coverage2"
fi

if [ $1 = "sbml-test-suite" ]; then
    if [ $2 = "1.2" ]; then
        $coverage_binary run -a -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l1v2 || exit 1;

    elif [ $2 = "2.1" ]; then
        $coverage_binary run -a -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v1 || exit 1;

    elif [ $2 = "2.2" ]; then
        $coverage_binary run -a -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v2 || exit 1;

    elif [ $2 = "2.3" ]; then
        $coverage_binary run -a -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v3 || exit 1;

    elif [ $2 = "2.4" ]; then
        $coverage_binary run -a -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v4 || exit 1;

    elif [ $2 = "2.5" ]; then
        $coverage_binary run -a -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l2v5 || exit 1;

    elif [ $2 = "3.1" ]; then
        $coverage_binary run -a -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l3v1 || exit 1;

    elif [ $2 = "3.2" ]; then
        $coverage_binary run -a -m unittest libsignetsim.tests.sbmltestsuite.TestSuite_l3v2 || exit 1;

    fi

elif [ $1 = "biomodels" ]; then
    $coverage_binary run -a -m unittest libsignetsim.tests.biomodels.TestBiomodelsCompatibility || exit 1;

elif [ $1 = "models" ]; then
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestFindKineticLaws || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestReduceModel || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestReduceModelMultiCompartment || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestModelDefinition || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestAnnotation || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestRenameSbmlId || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestUnits || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.math.tests.TestMath || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestXPaths || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestSubstitutions || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.model.tests.TestLocalParameters || exit 1;

elif [ $1 = "optimization" ]; then
    $coverage_binary run -a -m unittest libsignetsim.optimization.tests.TestOptimization || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.optimization.tests.TestOptimizationComp || exit 1;


elif [ $1 = "simulation" ]; then
    $coverage_binary run -a -m unittest libsignetsim.simulation.tests.TestTimeseries || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.simulation.tests.TestSteadyStates || exit 1;

elif [ $1 = "combine" ]; then
    $coverage_binary run -a -m unittest libsignetsim.combine.tests.TestRunSedmls || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.combine.tests.TestShowCase || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.combine.tests.TestNoManifest || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.combine.tests.TestCreateArchive || exit 1;

elif [ $1 = "sedml" ]; then
    $coverage_binary run -a -m unittest libsignetsim.sedml.tests.TestBiomodelsURI || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.sedml.tests.TestSteadyStatesScan || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.sedml.tests.TestLogscaleTimeseries || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.sedml.tests.TestSpecificationL1V2 || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.sedml.tests.TestMath || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.sedml.tests.TestXMLChanges || exit 1;

elif [ $1 = "numl" ]; then
    $coverage_binary run -a -m unittest libsignetsim.numl.tests.test_example || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.numl.tests.test_example_notes || exit 1;
    $coverage_binary run -a -m unittest libsignetsim.numl.tests.test_experiment || exit 1;

elif [ $1 = "data" ]; then
    $coverage_binary run -a -m unittest libsignetsim.data.tests.test_readwrite_data || exit 1;

elif [ $1 = "uris" ]; then
    $coverage_binary run -a -m unittest libsignetsim.uris.tests.TestGOResolver || exit 1;

elif [ $1 = "continuation" ]; then
    $coverage_binary run -a -m unittest libsignetsim.continuation.tests.TestContinuation || exit 1;

elif [ $1 = "others" ]; then
    $0 models $2 $3 || exit 1;
    $0 simulation $2 $3 || exit 1;
    $0 optimization $2 $3 || exit 1;
    $0 sedml $2 $3 || exit 1;
    $0 combine $2 $3 || exit 1;
    $0 uris $2 $3 || exit 1;
    $0 data $2 $3 || exit 1;
    $0 numl $2 $3 || exit 1;
    $0 continuation $2 $3 || exit 1;

else
    exit 1;
fi
