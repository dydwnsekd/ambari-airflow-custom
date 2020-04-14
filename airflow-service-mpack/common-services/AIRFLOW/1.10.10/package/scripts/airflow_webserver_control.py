import sys, os, pwd, grp, signal, time
from resource_management import *
from subprocess import call
from airflow_setup import *

class AirflowWebserver(Script):
	"""
	Contains the interface definitions for methods like install, 
	start, stop, status, etc. for the Airflow Server
	"""
	def install(self, env):
		import params
		env.set_params(params)
		self.install_packages(env)
		Logger.info(format("Installing Airflow Service"))
		# virtualevn setting ------------------------------------------
		Execute(format("python3 /datalabnas/hadoop3/get-pip.py"))
		Execute(format("pip3 install --upgrade configparser"))
		Execute(format("pip3 install virtualenv"))
		Execute(format("virtualenv {airflow_home}/airflow_env --python=python3"))
		# -------------------------------------------------------------
		Execute(format("export SLUGIFY_USES_TEXT_UNIDECODE=yes && {airflow_home}/airflow_env/bin/pip install --upgrade {airflow_pip_params} apache-airflow[all]==1.10.10 --constraint https://raw.githubusercontent.com/apache/airflow/1.10.10/requirements/requirements-python3.6.txt"))
		Execute(format("export SLUGIFY_USES_TEXT_UNIDECODE=yes && {airflow_home}/airflow_env/bin/pip install --upgrade {airflow_pip_params} apache-airflow[celery]==1.10.10 --constraint https://raw.githubusercontent.com/apache/airflow/1.10.10/requirements/requirements-python3.6.txt"))
		Execute(format("chmod 755 /bin/airflow /usr/bin/airflow"))
		Execute(format("useradd {airflow_user}"), ignore_failures=True)
		Execute(format("mkdir -p {airflow_home}"))
		airflow_make_startup_script(env)
		Execute(format("chown -R {airflow_user}:{airflow_group} {airflow_home}"))
		Execute(format("export AIRFLOW_HOME={airflow_home} && {airflow_home}/airflow_env/bin/airflow initdb"),
			user=params.airflow_user
		)

	def configure(self, env):
		import params
		env.set_params(params)
		airflow_configure(env)
		airflow_make_systemd_scripts_webserver(env)
		
	def start(self, env):
		import params
		self.configure(env)
		Execute("service airflow-webserver start")
		Execute('ps -ef | grep "airflow webserver" | grep -v grep | awk \'{print $2}\' | tail -n 1 > ' + params.airflow_webserver_pid_file,
			user=params.airflow_user
		)

	def stop(self, env):
		import params
		env.set_params(params)
		# Kill the process of Airflow
		Execute("service airflow-webserver stop")
		File(params.airflow_webserver_pid_file,
			action = "delete",
			owner = params.airflow_user
		)

	def status(self, env):
		import status_params
		env.set_params(status_params)
		#use built-in method to check status using pidfile
		check_process_status(status_params.airflow_webserver_pid_file)

	def initdb(self, env):
		import params
		env.set_params(params)
		self.configure(env)
		Execute(format("export AIRFLOW_HOME={airflow_home} && airflow initdb"),
			user=params.airflow_user
		)

if __name__ == "__main__":
	AirflowWebserver().execute()
