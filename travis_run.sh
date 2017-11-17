#!/bin/bash

if [ $2 = "docker" ]; then
    if [ $1 = "before_install" ]; then
        pip install docker-compose || exit 1;
        apt-get -qq update; apt install wget
        docker login -u signetsim -p $3 || exit 1;

    elif [ $1 = "install" ]; then
        docker-compose build || exit 1;

    elif [ $1 = "script" ]; then
        docker run --name notebook -p 8888:8888 -d signetsim/notebook:develop || exit 1;
        WEB_RETURN=`wget -q -O - localhost:8888 | grep \<title\> | cut -d">" -f2 | cut -d"<" -f1 | cut -d" " -f1"`
        exit `expr ${WEB_RETURN} != Jupyter`;


    elif [ $1 == "after_script" ]; then
        docker push signetsim/notebook:develop || exit 1;

    else
        exit 0;
    fi

else
    if [ $1 = "before_install" ]; then
        pip install coveralls || exit 1;
        docker pull signetsim/travis_testenv:stretch || exit 1;

    elif [ $1 = "install" ]; then
        docker run -di --name test_env -v $(pwd):/home/travis/build/vincent-noel/libSigNetSim signetsim/travis_testenv:stretch bash || exit 1;
        docker exec test_env chown -R www-data:www-data /home/travis/ || exit 1;
        docker exec test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim; bash scripts/install_dep.sh" || exit 1;
        docker exec test_env /bin/bash -c "cd /home/travis/build/vincent-noel/libSigNetSim; scripts/install.sh" || exit 1;

    elif [ $1 = "script" ]; then
        echo docker exec -u www-data test_env /bin/bash -c "cd /home/travis/; bash /home/travis/build/vincent-noel/libSigNetSim/scripts/run_tests.sh $2 $3"
        docker exec -u www-data test_env /bin/bash -c "cd /home/travis/; bash /home/travis/build/vincent-noel/libSigNetSim/scripts/run_tests.sh $2 $3"

    elif [ $1 = "after_script" ]; then
        coveralls

    else
        exit 0;

    fi

fi
