FROM    python:3.7-alpine
RUN     echo "in docker build for? Apine + GCC + Python Dependencies"

RUN     apk add --no-cache --virtual .build-deps gcc musl-dev
RUN     pip install cython
RUN     apk del .build-deps gcc musl-dev

RUN     pip3 install jira
RUN     pip3 install pbx_gs_python_utils osbot_aws
RUN     pip3 install python-coveralls pytest-cov==2.5.0
RUN     pip3 install boto3 pytest pytest-json
RUN     pip3 install elasticsearch google-api-python-client oauth2client

CMD     echo 'this is an message from the docker container'