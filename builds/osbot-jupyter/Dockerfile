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
RUN     pip install ipywidgets qgrid jupyter_dashboards cufflinks
RUN     jupyter nbextension enable --py --sys-prefix qgrid

RUN     jupyter dashboards quick-setup --sys-prefix
RUN     jupyter nbextension install --py jupyter_dashboards --sys-prefix
RUN     jupyter nbextension enable --py jupyter_dashboards --sys-prefix
RUN     jupyter nbextension enable --py widgetsnbextension
RUN     jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN     pip install papermill

# setup ngrok, install git,unzip
USER    root
RUN     wget -q https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
RUN     apt-get update
RUN     apt-get install unzip git -y
RUN     unzip ngrok-stable-linux-amd64.zip

#install OS_Bot APIs
RUN     pip install pbx_gs_python_utils
#osbot_aws osbot-jira osbot-gsuite osbot-jupyter
RUN     git clone https://github.com/filetrust/GW-Bot.git
RUN     git clone https://github.com/owasp-sbot/OSBot-AWS.git
RUN     git clone https://github.com/owasp-sbot/OSBot-Utils.git
RUN     git clone https://github.com/filetrust/OSBot-Jupyter.git
RUN     git clone https://github.com/filetrust/OSBot-browser.git
RUN     git clone https://github.com/filetrust/OSBot-jira.git
