FROM    jupyter/base-notebook
RUN     echo "in docker build"

RUN     pip install pbx_gs_python_utils osbot_aws boto3 osbot-jupyter

USER    root
RUN     wget -q https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
RUN     apt-get update
RUN     apt-get install unzip -y
RUN     unzip ngrok-stable-linux-amd64.zip

#ADD     start-notebook.sh .
#RUN     chmod +x start-notebook.sh
#USER    $NB_UID

CMD     echo "oss jupyter is ready for you"