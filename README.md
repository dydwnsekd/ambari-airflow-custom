# Apache Airflow management pack for Apache Ambari (airflow-ambari-mpack)

[![Mpack version](https://img.shields.io/badge/Mpack%20version-1.5.4-brightgreen.svg)](https://github.com/miho120/ambari-airflow-mpack)
[![License](http://img.shields.io/:license-Apache%202-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.txt)

Mpack allows you to install/configure airflow directly from ambari.
Apache Airflow version included: 1.10.10

airflow 의존성 package 함께 설치
requirements-python[version].txt로 설치 진행
```
# airflow-service-mpack/common-services/AIRFLOW/1.10.10/package/scripts/airflow_scheduler_control.py airflow_webserver_control.py airflow_worker_control.py
pip install apache-airflow[all]==1.10.10 --constraint https://raw.githubusercontent.com/apache/airflow/1.10.10/requirements/requirements-python3.7.txt
```

#### Installing Apache Aiflow Mpack:
1. Stop Ambari server.
2. Install the Apache Airflow Mpack on Ambari server.
3. Start Ambari server.

```
ambari-server stop
tar -zxcf airflow-service-mpack.tar.gz airflow-service-mpack
ambari-server install-mpack --mpack=airflow-service-mpack.tar.gz
ambari-server start
```

#### Upgrading Apache Aiflow Mpack:
1. Stop Ambari server.
2. Upgrade the Apache Airflow Mpack on Ambari server.
3. Start Ambari server.

```
ambari-server stop
ambari-server upgrade-mpack --mpack=airflow-service-mpack.tar.gz
ambari-server start
```

### Installing Apache Airflow from Ambari:
1. Action - Add service.
2. Select Apache Airflow service.
3. Choose destination server.
4. You may configure Apache Airflow, change home folder.
5. Deploy!

![Add service](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/1.PNG)
![Select Apache Airflow service](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/2.PNG)
![Choose destination server](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/3.PNG)
![Choose destination server](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/3-1.PNG)
![configure Apache Airflow](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/4.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/5.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/6.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/8.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/10.PNG)

### Virtual environment support
"AIRFLOW_HOME/airflow_control.sh".
해당 프로젝트는 virtualenv에서 동작하는 것을 기본으로 동작하며, airflow_control.sh의 내용을 수정하려면 
airflow-service-mpack/common-services/AIRFLOW/1.10.10/package/scripts/airflow_setup.py
```
# 125line
export AIRFLOW_HOME={airflow_home}/ && source {airflow_home}/airflow_env/bin/activate && {airflow_home}/airflow_env/bin/airflow $1 --pid {airflow_home}/airflow-sys-$1.pid
```
수정

Example:
```
#!/bin/bash

export AIRFLOW_HOME=/usr/local/airflow/airflow/ && source /usr/local/airflow/airflow_venv/airflow/bin/activate && /usr/local/airflow/airflow_venv/airflow/bin/airflow $1 --pid /usr/local/airflow/airflow/airflow-sys-$1.pid
```

### Enjoy!
