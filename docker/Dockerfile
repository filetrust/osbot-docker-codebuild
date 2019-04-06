FROM    python:3.7-alpine
RUN     echo "in docker build"

RUN     pip3 install pbx_gs_python_utils
RUN     pip3 install python-coveralls pytest-cov==2.5.0
RUN     pip3 install boto3 pytest pytest-json
RUN     pip3 install elasticsearch google-api-python-client oauth2client

CMD     echo 'this is an message from the docker container' && ls -la /