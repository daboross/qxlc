qxlc
====

Multipurpose flask-app written in Python 3.

Currently implemented:
* Short link server
* Paste server

Will eventually contain:
* Image server

This is a work in progress. Its current state runs at http://qx.lc.

#### Finding pastes with incorrect md5sums.

I don't yet know how this might happen, but incase it does, do this:

```
echo "select id, data from qxlc_data where type = 1;" | sqlite3 qxlc.db | python3 script.py pastes | sqlite3 qxlc.db
echo "select id, data from qxlc_data where type = 2;" | sqlite3 qxlc.db | python3 script.py images | sqlite3 qxlc.db
```

If you are experiencing pasting something and having the resulting url have different content, the above may fix it.

#### Installing
You can install qx.lc on your own server through apache2. Here's what you need to do:

##### Step 1)

Clone qxlc into /var/www/qxlc/ using git. `git clone https://github.com/daboross/qxlc.git /var/www/qxlc/`

##### Step 2)

Chown /var/www/qxlc/ to whatever user your going to run qx.lc with. I use the user 'azd'.
`[sudo] chown -Rc azd:azd /var/www/qxlc/`

Add a qxlc host to apache2. Here's what I use for qx.lc, you may adjust accordingly:
```
<VirtualHost *:80>
    ServerName qx.lc
    ServerAdmin dabo@dabo.guru

    WSGIDaemonProcess qxlc user=azd group=azd threads=2
    WSGIScriptAlias / /var/www/qxlc/qxlc.wsgi
    <Directory /var/www/qxlc>
        WSGIProcessGroup qxlc
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
```
Replace 'azd' with the user who has read/write access to /var/www/qxlc.

Put virtualhost in the file `/etc/apache2/sites-available/qxlc.conf`, then use `[sudo] a2ensite qxlc.conf`.

##### Step 3)

Copy /var/www/qxlc/config.default.json to /var/www/qxlc/config.json. Then edit the config with the values you need for your setup.

"base_url" should be the base URL for the qxlc app. It shouldn't have an ending slash. In my case, 'http://qx.lc'.

"database" should be the SQLAlchemy database URL for the database to store links and IDs in.

"pushbullet" is the config for pushbullet notifications of errors. Put your push bullet api key in "api-key" and the device to notify in "device".

##### Step 4)

Restart apache2, and you should be good!
