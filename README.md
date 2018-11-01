
[![Build Status](https://travis-ci.org/sugarlabs/aslo-v3.svg?branch=master)](https://travis-ci.org/sugarlabs/aslo-v3)

## Contributions welcome and should be directed to [https://github.com/sugarlabs/aslo-v3](https://github.com/sugarlabs/aslo-v3), this repo is personal fork of the upstream. 

## Activities Platform (ASLOv3)
This repository hosts the upcoming version of ASLO (Software center) for SugarLabs.

## Requirements
* Python (3.x)
* Docker - For running build tasks
* Mongo - Primary Database Engine
* Celery - For running background tasks
* Redis - Broker for Background Tasks
* Imgur - For hosting Screenshots

## Hacking

Setup your development environment:
1. Install dependencies: python3-dev, docker, mongo, and redis.
2. Create virtualenv and install python dependencies:
```
$ git clone https://github.com/sugarlabs/aslo-v3.git
$ cd aslo-v3;
$ python3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
```

3. We use [honcho](https://github.com/nickstenning/honcho). Honcho looks for `.env` file in order to define the environment 
variables that will provide the configuration for our app. You can look default values into `aslo/settings.py`. Define at least `SECRET_KEY` to start. But certainly you will need more env to test it. Have fun ;)

``` bash 
$ cat >.env <<EOF
MONGO_DBNAME=aslo-dev
SECRET_KEY=123abc123abc123abc
GITHUB_HOOK_SECRET=aaaaabbbbbcccc
EOF
```

4. Execute `./start.sh` to run the server. It actually executes the gunicorn process and the celery worker. Check the Procfile.

## Contributing

We welcome and appreciate contributions of any kind (code, tests, documentation, bug fixes, etc). You can also check 
our [issues](https://github.com/sugarlabs/aslo-v3/issues) page in order to find tasks to contribute with.

### Code Style Guide
We follow [PEP8 Python Style Guide](https://www.python.org/dev/peps/pep-0008/) for Python code and we use 4 spaces for tab.
Regarding HTML, we prefer to stick with 2 spaces for tab.
