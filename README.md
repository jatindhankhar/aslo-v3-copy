[![Build Status](https://travis-ci.org/jatindhankhar/aslo-v3.svg?branch=master)](https://travis-ci.org/jatindhankhar/aslo-v3)

### aslo-v3
This repo hosts the upcoming version of ASLO (Software centre) for SugarLabs

### Instructions

#### Install Dependenices
**Python 3.x** supported 

* **Docker (System)** - For running build tasks
* **Mongo (System)** - Primary Database Engine
* **Redis (System)** - Broker for Background Tasks
* **Celery** - For running background tasks
* **Imgur** - For hosting Screenshots
* **Flower (Optional)** - Dashboard for Celery

Install most of the app/python dependencies  by running `pip install -r requirements.txt `

##### How to Run

`honcho` which is used in this project, looks for `.env` file, so define all the environment variables like `GITHUB_HOOK_SECRET`, `IMGUR_CLIENT_ID` , `IMGUR_CLIENT_SECRET` and others defined in the `default_settings.py` 

**A sample example**

``` bash 
$ cat >.env <<EOM
PORT=5000
GITHUB_HOOK_SECRET="XXXXXXXX"
IMGUR_CLIENT_ID="XXXXXXXXXXXXXXXX"
IMGUR_CLIENT_SECRET="XXXXXXXXXXXXXXX"
REDIS_URI=redis://localhost:6789/0
EOM

```
Run `./start.sh` to run the server 

Run `flower -A worker --port=5555` to run the dashboard server 