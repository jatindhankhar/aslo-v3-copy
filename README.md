# aslo-v3
Upcoming Software center for SugarLabs (ASLO V3)


## Setup Instructions

### Install virtualenv

`pip install virtualenv`

### Create a vritualenv
`virtualenv ~/envs/flask-dev`

### Activate virtualenv
`source ~/envs/flask-dev/bin/activate`

### Install Dependencies
`pip install -r requirements.txt`

### Install Redis

``` bash

cd /tmp
wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
make
make test
sudo make install
```
 For a more comprehensive guide follow this [Tutorial from DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04)

Make sure redis is running by logging in `redis-cli`

### Run the Flask Server

`python app.py` will start Flask server listening on all interfaces `0.0.0.0` and port `5000`
