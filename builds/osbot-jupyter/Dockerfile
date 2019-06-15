FROM    jupyter/base-notebook
RUN     echo "in docker build"

#install dependencies
RUN     pip install jira
RUN     pip install boto3 pytest pytest-json
RUN     pip install elasticsearch google-api-python-client oauth2client
RUN     pip uninstall -y pandas
RUN     pip install matplotlib
RUN     pip install pandas

#install jupyter apis used
RUN     pip install ipywidgets qgrid
RUN     jupyter nbextension enable --py --sys-prefix qgrid
RUN     jupyter labextension install qgrid

RUN     jupyter labextension install @jupyter-widgets/jupyterlab-manager

RUN     conda install -y -c conda-forge jupyter_nbextensions_configurator


#install OS_Bot APIs
RUN     pip install pbx_gs_python_utils osbot_aws osbot-jira osbot-gsuite osbot-jupyter


# setup ngrok
USER    root
RUN     wget -q https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
RUN     apt-get update
RUN     apt-get install unzip git -y
RUN     unzip ngrok-stable-linux-amd64.zip

#ADD     start-notebook.sh .
#RUN     chmod +x start-notebook.sh
#USER    $NB_UID