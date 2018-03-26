# INSTALLATION


## Prepare the environment (DEBIAN)

    sudo apt install postgresql python-psycopg2 libpq-dev libreadline-dev libapache2-mod-wsgi imagemagick gettext postfix libzmq-dev


## Create the postgres database

create a user "dasa" that is not a superuser, cannot create databases, and cannot create roles:

    $ sudo su postgres -c "createuser dasa -SDR"

create the main database:

    $ sudo su postgres -c "createdb dasa --owner=dasa"


add the following lines to `/etc/postgresql/8.4/main/pg_hba.conf`

    local   dasa    dasa                      md5

restart postgres

    $ service postgresql restart


## Checkout latest version

    git clone git://github.com/sejarah-nusantara/pagebrowser-ingbook.git where/you/want/to/install


## Run buildout scripts

We recommend using (virtualenv)[https://virtualenv.pypa.io]

    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/bin/activate

Now you are ready to install the software. In this example, we use the `development.cfg` which sets some settings for developers:

    $ python2.7 bootstrap.py  -c development.cfg
    $ bin/buildout -c development.cfg


There are some convenient scripts in the `/scripts/` directory, where you can run commands like:s

    fab -l
    fab install
    fab clean_install


## Run the code

For quick access (not for production!) run:

    $ cd where/you/have/installed
    $ bin/django runserver

and the service should be available on port 8080

For serious serving, we recommend mod_wsgi on apache.

## Log files

Log files are in `var/log/*.log`

They will grow in size.

If you are on Debian, and have logrotate installed, you might want to add a file called "dasa_site" in the directory /etc/logrotate.d
with the following contents:

    /where/you/have/installed/var/log/*.log {
        weekly
        missingok
        rotate 52
        compress
        delaycompress
        notifempty
        sharedscripts
    }
