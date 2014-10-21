qxlc
====

Multipurpose flask-app written in Python 3.

Currently implemented:
* Short link server
* Paste server
* *Private* image server.

The image server functionality currently doesn't resize images or confirm that they are images at all. Because of this,
it is set up to require an API key.

This is a work in progress. Its current stable state runs at http://qx.lc, and development at http://dev.qx.lc

#### Finding pastes with incorrect md5sums.

I don't yet know how this might happen, but incase it does, do this:

```
echo "select id, data from qxlc_data where type = 1;" | sqlite3 qxlc.db | python3 script.py pastes | sqlite3 qxlc.db
echo "select id, data from qxlc_data where type = 2;" | sqlite3 qxlc.db | python3 script.py images | sqlite3 qxlc.db
```

If you are experiencing pasting something and having the resulting url have different content, the above may fix it.

#### Installing
You can install qx.lc on your own server using nginx and uwsgi. You will need python3, nginx, uwsgi and virtualenv
installed.

##### 1)

Clone qxlc into /var/www/qxlc/ using git. `git clone https://github.com/daboross/qxlc.git /var/www/qxlc/`

##### 2)

Chown /var/www/qxlc/ to whatever user your going to run qx.lc with. I use the user 'azd'.
```
[sudo] chown -Rc azd:azd /var/www/qxlc/
```

##### 3)

Create a virtualenv for qxlc to run in. I used the directory `/var/www/envs/qxlc/`, but feel free to use any dir. This
directory should be owned by the user you are running qxlc under (in my case 'azd').
```
[sudo] mkdir /var/www/envs/
[sudo] chown -Rc azd:azd /var/www/envs
cd /var/www/envs/
virtualenv -p python3.4 qxlc
```

##### 4)

Activate the new virtualenv, and install all required dependencies.
```
source /var/www/envs/qxlc/bin/activate
pip install -r /var/www/qxlc/requirements.txt
```

##### 5)

Configure uwsgi to run qxlc. This can be done by creating a `/etc/uwsgi/apps-available/qxlc.ini` file, and putting the
following contents:
```
[uwsgi]
# Bind to localhost port 3032
socket = 127.0.0.1:3032
# Use the qxlc installation in /var/www/qxlc/
wsgi-file = /var/www/qxlc/qxlc.wsgi
# Use the virtualenv in /var/www/envs/qxlc/
virtualenv = /var/www/envs/qxlc/
callable = application
# Use azd as the user/group for running qxlc
uid = azd
gid = azd
# We aren't really loaded enough to need multiple processors
processes = 1
# Enable threads so that the github_pull function can use a ThreadPoolExecutor to execute
# Since we're enabling threads anyways, might as well use two of them for serving content
threads = 2
# Don't give write permission to group or other
umask = 022
```
You probably want to change the `uid` and `gid` settings to match the user you are running qxlc under. You can also
change the `processes` and `threads` options to optimize for your machine. If you are running multiple uwsgi apps on the
machine you can also change the `:3032` part of the `socket` option, just be sure to change it in the nginx
configuration file as well.

Then enable the app by using `[sudo] ln -s /etc/uwsgi/apps-available/qxlc.ini /etc/uwsgi/apps-enabled/`.

##### 6)

Configure nginx to run qxlc. This can be done by creating a `/etc/nginx/sites-available/qxlc` file, and putting the
following contents:
```
# Handle http requests for qx.lc
server {
    # replace 107.161.17.250 and 2604:180:1::d4c6:e0de with your ipv4 and ipv6 addresses respectively.
    listen 107.161.17.250:80;
    listen [2604:180:1::d4c6:e0de]:80;
    # replace qx.lc with your server name
    server_name qx.lc;

    location / {
        include uwsgi_params;
        # This should be the same as the `socket` option in the uwsgi conf
        uwsgi_pass 127.0.0.1:3032;
    }
}
```

If qxlc is the only web server running on the configured IP address, you can also add the following section to the
configuration file to redirect all traffic to that IP address to qxlc. This will also handle www.<address>/<address>
redirection.
```
# Redirect all http requests for unknown sites to qx.lc
server {
    listen 107.161.17.250:80 default_server;
    listen [2604:180:1::d4c6:e0de]:80 default_server;
    # replace 'qx.lc' with your webserver address
    return 301 $scheme://qx.lc/$request_uri;
}
```

##### 7)

Copy `/var/www/qxlc/config.default.json` to `/var/www/qxlc/config.json`. Then edit the config with the values you need for your setup.

"base_url" should be the base URL for the qxlc app. It shouldn't have an ending slash. In my case, 'http://qx.lc'. This
url is used for giving out links.

"database" should be the SQLAlchemy database URL for the database to store links and IDs in.

##### 8)

Restart uwsgi and reload nginx, and you should be good to go!

```
[sudo] service uwsgi restart
[sudo] service nginx reload
```
