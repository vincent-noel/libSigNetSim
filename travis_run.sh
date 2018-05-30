#!/bin/bash

if [[ "$2" = "docker" ]]; then
    if [[ "$1" = "before_install" ]]; then
        pip install docker-compose || exit 1;
        docker login -u signetsim -p $5 || exit 1;

    elif [[ "$1" = "install" ]]; then
        if [[ "$4" = "python2" ]]; then
            docker-compose build notebook-py2 || exit 1;
        else
            docker-compose build notebook || exit 1;
        fi

    elif [[ "$1" = "script" ]]; then
        if [[ "$4" == "python2" ]]; then
            docker run --name notebook -p 8888:8888 -d signetsim/notebook:develop-py2 || exit 1;
        else
            docker run --name notebook -p 8888:8888 -d signetsim/notebook:develop || exit 1;
        fi

        WEB_RETURN=`wget -q -O - localhost:8888 | grep \<title\> | cut -d">" -f2 | cut -d"<" -f1 | cut -d" " -f1`
        exit `expr ${WEB_RETURN} != Jupyter`;

    elif [[ "$1" == "after_script" ]]; then
        if [[ "$4" == "python2" ]]; then
            docker push signetsim/notebook:develop-py2 || exit 1;
        else
            docker push signetsim/notebook:develop || exit 1;
            docker tag signetsim/notebook:develop signetsim/notebook:develop-py3 || exit 1;
            docker push signetsim/notebook:develop-py3 || exit 1;
        fi

    else
        exit 0;
    fi

else
    if [[ "$1" = "before_install" ]]; then
        pip install coveralls || exit 1;

        if [[ "$4" = "python3" ]]; then
            docker pull signetsim/travis_testenv:stretch-python3 || exit 1;

        else
            docker pull signetsim/travis_testenv:stretch || exit 1;

        fi

    elif [[ "$1" = "install" ]]; then

        if [[ "$4" = "python3" ]]; then
            docker run -di --name test_env -v $(pwd):/home/travis/build/vincent-noel/libSigNetSim signetsim/travis_testenv:stretch-python3 bash || exit 1;
            docker exec test_env chown -R www-data:www-data /home/travis/ || exit 1;
            docker exec test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim; bash scripts/install_dep-debian.sh 3" || exit 1;
            docker exec test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim; scripts/install.sh 3" || exit 1;

        else
            docker run -di --name test_env -v $(pwd):/home/travis/build/vincent-noel/libSigNetSim signetsim/travis_testenv:stretch bash || exit 1;
            docker exec test_env chown -R www-data:www-data /home/travis/ || exit 1;
            docker exec test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim; bash scripts/install_dep-debian.sh 2" || exit 1;
            docker exec test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim; scripts/install.sh 2" || exit 1;
        fi

        docker exec test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim/libsignetsim/lib/integrate/; make"
        docker exec test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim/libsignetsim/lib/plsa/; make all"
    elif [[ "$1" = "script" ]]; then
        docker exec -u www-data test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim/; bash ./scripts/run_tests.sh $2 $3 $4"

    elif [[ "$1" = "after_script" ]]; then
        coveralls

    else
        exit 0;

    fi
fi