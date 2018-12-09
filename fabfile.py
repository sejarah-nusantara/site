#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013ff.
#


from __future__ import with_statement
import os

import datetime
import requests
from fabric.api import local, env, cd, run, sudo, settings
from fabric.api import task
from fabric.contrib import files
from time import sleep
import sys
import ConfigParser
from env import CONFIG

sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
try:
    from secret import config as secretconfig
except ImportError:
    secretconfig = {}


env.use_ssh_config = True

configparser = ConfigParser.ConfigParser()
configparser.read(os.path.join(THIS_DIR, 'base.cfg'))

PAGEBROWSER_CSS_TEMPLATE = os.path.join(THIS_DIR, 'deploy', 'pagebrowser.css')

DOC_CONFIGS = '[%s]' % ', '.join(CONFIG.keys())

APACHE_LOCATION = '/etc/apache2/'

DJANGO_PORT = configparser.get('ports', 'django')
PAGEBROWSER_PORT = configparser.get('ports', 'pagebrowser')
# POSTGRES_PORT = json.get('ports', 'postgres')
# PAGEBROWSER_SERVERNAME = 'dasa10.gerbrandy.com/pagebrowser'
DB_NAME = 'dasa'


def get_from_cfg(where, section, item):
    cfg_files = CONFIG[where]['config']
    for cfg_file in cfg_files:
        configparser.read(os.path.join(THIS_DIR, cfg_file))
        try:
            return configparser.get(section, item)
        except ConfigParser.NoSectionError:
            pass


def get_config(where):
    try:
        config = CONFIG[where]
    except KeyError:
        print 'Please choose one of'
        for key in CONFIG:
            print '\t- {}'.format(key)
        print '(not "{where}")'.format(where=where)
        print

        raise Exception("Location should be one of %s" % CONFIG.keys())
    config['dest_directory_static'] = os.path.join(config['installation_dir'], 'static')
    config['dest_directory_media'] = os.path.join(config['installation_dir'], 'media')
    config['backup_dir'] = os.path.join(config['installation_dir'], 'backups')
    if 'db_name' not in config:
        config['db_name'] = DB_NAME
    config['db_user'] = DB_NAME
    config['user_media_dir'] = os.path.join(config['installation_dir'], 'user_media')
#    json['db_password'] = json.get('db_password', '')
    config['sudo_host_string'] = config.get('sudo_host_string', config['host_string'])
    config['static_file_location'] = os.path.join(config['installation_dir'], 'static')
    config['media_file_location'] = os.path.join(config['installation_dir'], 'user_media')
    config['pagebrowser_user'] = get_from_cfg(where, 'pagebrowser', 'user')
    config['pagebrowser_url'] = get_from_cfg(where, 'django_settings', 'pagebrowser_url')
    config['pagebrowser_port'] = get_from_cfg(where, 'ports', 'pagebrowser')
    config['repository_port'] = get_from_cfg(where, 'ports', 'repository')
    config['repository_public_url'] = get_from_cfg(where, 'django_settings', 'repository_public_url')

    if where in secretconfig:
        for key in secretconfig[where]:
            config[key] = secretconfig[where][key]

    class Config(dict):
        def __init__(self, config):
            for k in config:
                setattr(self, k, config[k])
                self[k] = config[k]
    return Config(config)


@task
def install(where='local'):
    """install the site for the first time"""
    config = get_config(where)
    print 'using configuration: %s' % config
    with settings(host_string=config['host_string']):
        if not files.exists(config['installation_dir']):
            run('git clone %(git_repo)s %(installation_dir)s' % config)
            with cd(config['installation_dir']):
                run('git submodule init')
                run('git submodule update --init')

    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('python2.7 bootstrap.py -c %(cfg)s' % config)
        deploy(where)
        secs = 4
        sleep(secs)
        init_db(where)


@task
def init_db(where=None):
    """initialize the database"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('bin/django syncdb --noinput')
#         run('bin/django migrate dasa')


@task
def deploy(where=None, with_buildout=True):
    """deploy everything"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('git pull')
        run('git submodule update')

        run('mkdir -p downloads')
        if with_buildout != 'False':
            run('bin/buildout -v -c %(cfg)s' % config)
        run('bin/django syncdb')
#         run('bin/django migrate dasa')
        run('bin/django collectstatic --noinput')
        install_translations(where)
        # also update the pagebrowser
        deploy_pagebrowser(where, restart=False)

        run('bin/circusd --daemon circus.ini')
        run('bin/circusctl reloadconfig')

    test_live_site(where)


@task
def collectstatic(where=None):
    """run the django collectstatic command for generate static file list"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('bin/django collectstatic --noinput')


@task
def git_pull(where=None):
    """update the code quicklyk without re-running buildout or generating images"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('git pull')
        run('git submodule update')
        collectstatic(where)
        restart(where)


@task
def migrate(where='local'):
    """migrate the database (to reflect changes in the models)"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):

        run('bin/django syncdb')
        try:
            run('bin/django schemamigration dasa --auto')
        except:
            pass
        run('bin/django migrate dasa')


@task
def copy_data(source, dest):
    """copy data between website instances, i.e. fab copy_data:production,local moves data from production to local instance"""
    """migrate data of the stie from source to dest"""
    if dest != 'local':
        if not raw_input('You are about to change data in an instance that is not the local instance. Are you sure? [y/n]') == 'y':
            return
    src_config = get_config(source)
    dst_config = get_config(dest)

    # dump a sql file at the source
    # with settings(host_string=src_config['host_string']):
    #     run('pg_dump dasa --clean -F p -f "/tmp/dasa.sql"' % src_config)

    with settings(host_string=dst_config['host_string']), cd(dst_config['installation_dir']):
        # # # transfer the file
        # run('rsync -avz %s:/tmp/dasa.sql /tmp/dasa.sql' % (src_config['host_string']))
        # # create a backup of the data
        # now = unicode(datetime.datetime.now()).replace(' ', '_')
        # run('mkdir -p {backups_dir}'.format(**dst_config))
        # # run("pg_dump dasa -F p -f /home/dasa/backups/dasa_{now}.dump".format(**locals()))
        #
        # # run("""psql dasa -t -c "select 'drop table \\"' || tablename || '\\" cascade;' from pg_tables where schemaname = 'public'" | psql dasa""".format(**dst_config))
        # run('psql -f "/tmp/dasa.sql" dasa' % dst_config)
        #
        # # clean up
        # run('rm /tmp/dasa.sql')
        #
        # copy the images
        #
        run('rsync -avz --exclude=cache %s:/home/dasa/site/user_media/* %s/user_media/' % (
            src_config['host_string'],
            dst_config['installation_dir']
            ))
        run('bin/django thumbnail clear')
        run('bin/django thumbnail cleanup')
        run('bin/django thumbnail clear')

        # copy the zope database
        run('rsync -avz {src_config[host_string]}://home/dasa/site/var/filestorage/* /home/dasa/site/var/filestorage'.format(**locals()))

        # dump the databse file and read it atdest

        run('touch bin/django.wsgi')


@task
def backup_db(where):
    config = get_config(where)
    #
    with settings(host_string=config['host_string']):
        config['now'] = unicode(datetime.datetime.now()).replace(' ', '_')
        run('mkdir -p %(backup_dir)s' % config)
        run("pg_dump %(db_name)s --clean -F p -f %(backup_dir)s/dasa_%(now)s.dump" % config)
        print 'output written to %(backup_dir)s/dasa_%(now)s.dump' % config


@task
def reset_thumbnails(where):
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('bin/django thumbnail clear')
        run('bin/django thumbnail cleanup')
        run('bin/django thumbnail clear_delete_all')
        run('bin/django thumbnail_cleanup')


@task
def configure_apache(where):
    raise Exception('USE package "dasa_deployment" instead')
    config = get_config(where)
    with settings(host_string=config['sudo_host_string']), cd(config['installation_dir']):

        context = {
            '__file__': __file__,
            'now': datetime.datetime.now(),
            'django_port': DJANGO_PORT,
            'pagebrowser_port': config['pagebrowser_port'],
            'repository_port': config['repository_port'],
        }
        context.update(config)
        for servername in [
            'icaatom.dasa.anri.go.id',
            'nodegoat.sejarah-nusantara.anri.go.id',
            'repository.dasa.anri.go.id',
#             'scanstore.dasa.anri.go.id',
#             'sejarah-nusantara.anri.go.id ',
            ]:
            template_fn = servername + '.conf.template'
            destination = os.path.join(APACHE_LOCATION, 'sites-available', servername + '.conf')
            context['servername'] = servername
            files.upload_template(
                os.path.join(THIS_DIR, 'deploy', 'apache', template_fn),
                destination,
                context=context,
                use_sudo=True,
                )

            if not files.exists(os.path.join(APACHE_LOCATION, 'sites-enabled', servername + '.conf')):
                sudo('a2ensite {servername}'.format(servername=servername))
        sudo('service apache2 reload')


@task
def reload_apache(where):
    config = get_config(where)
    with settings(host_string=config['sudo_host_string']), cd(config['installation_dir']):
        sudo('/etc/init.d/apache2 reload')


def start(where):
    """start the server"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('bin/circusd --daemon circus.ini')


@task
def restart(where):
    """restart the server """
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        # restart django
#         run('{ctl_script} restart website'.format(**json))
        run('touch bin/django.wsgi')
        run('{ctl_script} restart pagebrowser'.format(**config))


@task
def solr_build_schema(where=None):
    """define the solr schema - when this is done, perhaps you want to call fab:solr_reindex to reindex all objects in the database"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('bin/django build_solr_schema > /tmp/schema.xml')
        # run('cp /tmp/schema.xml deploy/solr-json/schema.xml'.format(**config))
        run('cp /tmp/schema.xml {solr_schema}'.format(**config))
        # run('cp /tmp/schema.xml {solr_test_schema}'.format(**config))
        run('rm /tmp/schema.xml')
        run('bin/circusctl restart solr')


@task
def solr_reindex(where=None):
    """update the solr index"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        cmd = 'bin/django update_index dasa --batch-size=5000 --remove --verbosity=2'
        run(cmd)


@task
def solr_rebuild(where=None):
    """rebuild the solr index (use this if schema has changed)"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        cmd = 'bin/django rebuild_index --batch-size=5000 --verbosity=2'
        run(cmd)


def update_solr(where=None):
    """update solr index, removing any references to objects that have been removed (cf. build_solr_schema)."""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('bin/django update_index dasa --remove')


@task
def prepare_translations():
    """create a .csv file for editing thet ranslations
    (depends on po2csv from the translate-toolkit package)
    sudo apt-get install translate-toolkit
    """
    output_fn = '/home/jelle/Desktop/django.csv'
    local('po2csv apps/dasa/locale/id/LC_MESSAGES/django.po %(output_fn)s' % locals())
    print 'output written to %(output_fn)s' % locals()


@task
def install_translations(where='local'):
    """(re)create all .po files for the i18n translation machinery, and compile them"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):

        if where == 'local':
            # if we are local, we also generate new po files
            with cd('apps/dasa/'):
                run('../../bin/django makemessages -l id')
                run('../../bin/django makemessages -l en')
                run('../../bin/django compilemessages')
            with cd('project'):
#                 run('../bin/django makemessages -l id')
                run('../bin/django makemessages -l en')
                run('../bin/django compilemessages')
        else:  # otherwise, we just compile
            run('git pull')
            with cd('apps/dasa/'):
                run('../../bin/django compilemessages')
            with cd('project'):
                run('../bin/django compilemessages')
        restart(where)


@task
def deploy_pagebrowser(where=None, restart=True):
    """update code of the pagebrowser to latest version from git"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        #         run('cd src/INGSearch && git pull')
        run('cd src/INGBookDasa && git checkout master')
        run('cd src/INGBookDasa && git pull')
        if restart:
            run('bin/circusctl restart pagebrowser')


def publish_info_in_pagebrowser():
    """push all information we have availale in the CMS to the pagebrowser"""
    env.run('bin/django create_pagebrowser_books')


def import_and_index_resolutions():
    """read source documents, and import resolutions into the database. Then reindex solr"""
    sys.path.append(os.path.abspath('import_scripts'))
    import import_resolutioninstance
    import_resolutioninstance.ResolutionImporter().load_items()


@task
def import_realia(where=None):
    """load the realia fixture, and reindex teh realia"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('git pull')
        run('cd import_scripts;../bin/python import_realia.py load_fixture')
        run('bin/django update_index dasa.Realia')


@task
def convert_realia():
    """convert realia (resolutions) from .csv file"""
    local('cd import_scripts;../bin/python import_realia.py')


@task
def convert_marginalia():
    """converts marginalia source file and creates a fixture (load it with 'import_marginalia')

    the source file is defined in MARGINALIA_SOURCES in import_marginalia.py
    """

    local('cd import_scripts;../bin/python import_marginalia.py import_marginalia')


@task
def import_marginalia(where='local'):
    """marginalia (journalentries): copy the local fixture to the server, and load it"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        if where != 'local':
            local('rsync -avz import_scripts/fixtures/dasa.journalentry.json {host_string}:{installation_dir}/import_scripts/fixtures/dasa.journalentry.json'.format(**config))

        run('cd import_scripts;../bin/python import_marginalia.py load_fixture')
        run('bin/django update_index dasa.JournalEntry -r')
    print 'The result should be visibile here: {url}marginalia_browse'.format(**config)


@task
def convert_appendices():
    """converts appendices source file and creates a fixture (load it with 'import_appendices')

    the source file is defined in MARGINALIA_SOURCES in import_appendices.py
    """
    local('cd import_scripts;../bin/python import_appendices.py import_appendices')


@task
def import_appendices(where='local'):
    """appendices (journalentries): copy the local fixture to the server, and load it"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        if where != 'local':
            local('rsync -avz import_scripts/fixtures/dasa.appendix.json {host_string}:{installation_dir}/import_scripts/fixtures/dasa.appendix.json'.format(**config))

        run('cd import_scripts;../bin/python import_appendices.py load_fixture')
        run('bin/django update_index dasa.Appendix -r')
    print 'The result should be visibile here: {url}browse-appendices/'.format(**config)


@task
def convert_corpusdiplomaticum():
    """converts diplomatieke brieven source file and creates a fixture (load it with 'import_diplomaticletters')

    the source file is defined in SOURCE in import_diplomaticletters.py
    """
    local('cd import_scripts;../bin/python import_corpusdiplomaticum.py import')


@task
def import_corpusdiplomaticum(where='local'):
    """diplomaticletters (journalentries): copy the local fixture to the server, and load it"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('cd import_scripts;../bin/python import_corpusdiplomaticum.py load_fixture')
        run('bin/django update_index dasa.CorpusDiplomaticumContract')
        run('bin/django update_index dasa.CorpusDiplomaticumPerson')
        run('bin/django update_index dasa.CorpusDiplomaticumContract')
    print 'The result should be visibile here: {url}corpusdiplomaticum_contracts_browse/'.format(**config)


@task
def convert_diplomaticletters():
    """converts diplomatieke brieven source file and creates a fixture (load it with 'import_diplomaticletters')

    the source file is defined in SOURCE in import_diplomaticletters.py
    """

    local('cd import_scripts;../bin/python import_diplomaticletters.py import')


@task
def import_diplomaticletters(where='local'):
    """diplomaticletters (journalentries): copy the local fixture to the server, and load it"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('cd import_scripts;../bin/python import_diplomaticletters.py load_fixture')
        run('bin/django update_index dasa.DiplomaticLetterRuler')
        run('bin/django update_index dasa.DiplomaticLetterLocation')
        run('bin/django update_index dasa.DiplomaticLetter')
    print 'The result should be visibile here: {url}browse_letters/'.format(**config)


@task
def convert_placards():
    """converts diplomatieke brieven source file and creates a fixture (load it with 'import_diplomaticletters')

    the source file is defined in SOURCE in import_diplomaticletters.py
    """

    local('cd import_scripts;../bin/python import_placards.py import')


@task
def import_placards(where='local'):
    """diplomaticletters (journalentries): copy the local fixture to the server, and load it"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('cd import_scripts;../bin/python import_placards.py load_fixture')
        run('bin/django update_index dasa.Placard')
#     print 'The result should be visibile here: {url}/diplomaticletters-browse/'.format(**json)

@task
def convert_dehaan():
    """converts dehaan excel source file and creates a fixture (load it with 'import_dehaan')

    the source file is defined in SOURCE in import_dehaan.py
    """

    local('cd import_scripts;../bin/python import_dehaan.py import')


@task
def import_dehaan(where='local'):
    """dehaan: copy the local fixture to the server, and load it"""
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        run('cd import_scripts;../bin/python import_dehaan.py load_fixture')
        run('bin/django update_index dasa.dehaan')
#     print 'The result should be visibile here: {url}/dehaan-browse/'.format(**json)


def import_hartakarun_categories():
    local('cd import_scripts;../bin/python import_hartakarun_category.py')


@task
def test():
    """run tests on application and pagebrowser"""
    test_app()
    test_pagebrowser()


@task
def test_app():
    """run tests on application"""
    local('%s/bin/django test dasa -v 2 -x --failed --settings=project.settings_test' % THIS_DIR)


@task
def test_pagebrowser():
    """ run pagebrowser tests
    to run a specific test, do:
         bin/pagebrowser_test -vv -t test_with_selenium
    """
    local('{THIS_DIR}/bin/pagebrowser_test -vvv '.format(THIS_DIR=THIS_DIR))


def install_pagebrowser_skin(where=None):
    config = get_config(where)
    admin_url = 'http://%s@%s' % (config['pagebrowser_user'], config['pagebrowser_url'])
    pb = PageBrowser(admin_url)
    css = open(PAGEBROWSER_CSS_TEMPLATE).read()
    pb.set_property('book.css', css, 'text')
    pb.set_property('custom_logo', 'http://%(servername)s/static/images/header_logo.png' % config)


def fixup_scan_paths(where=None):
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        backup_db(where)
        run('bin/django fixup_file_paths')


@task
def generate_pagebrowser_i18n(where='local'):
    config = get_config(where)
    with settings(host_string=config['host_string']), cd(config['installation_dir']):
        src_dir = 'src/INGBook/Products/INGBook'
        run('bin/i18ndude rebuild-pot --pot {src_dir}/locales/pagebrowser.pot --exclude="resources" --create pagebrowser {src_dir}'.format(src_dir=src_dir))
        run('bin/i18ndude sync --pot {src_dir}/locales/pagebrowser.pot {src_dir}/locales/en/LC_MESSAGES/pagebrowser.po'.format(src_dir=src_dir))
        run('bin/i18ndude sync --pot {src_dir}/locales/pagebrowser.pot {src_dir}/locales/id/LC_MESSAGES/pagebrowser.po'.format(src_dir=src_dir))


@task
def test_live_site(where):
    msgs = []

    def warn(s):
        msgs.append('- WARNING: {}'.format(s))

    def msg(s):
        msgs.append('- {}'.format(s))

    config = get_config(where)
    site_url = config['url']

    # we do some simple functional tests
    for url, expected_result in [
        (config['repository_public_url'] + 'lists/get_component_for_viewer?ead_id=icaatom.cortsfoundation.org_386.ead.xml&xpath=/ead/archdesc/text()[1]', ''),
        (site_url, 'The Corts Foundation'),
        (site_url + 'archive/', ''),
        (site_url + 'marginalia_browse/'.format(**locals()), 'Jan. 1, 1659'),
        (site_url + 'archive_daily_journals/', '2457'),
        (site_url + 'hartakarun/item/15/introduction', 'Questionnaire'),
    ]:
        print 'testing {url}'.format(**locals())

        # get the url, but forget about pesky ssl certficiate checking..
        auth = config.get('auth', None)
        response = requests.get(url, verify=False, auth=auth)
        assert response.status_code == 200, response.status_code

        if expected_result not in response.content:
            print response.content
            msg = 'Expected to find {expected_result} in {response.url}'.format(**locals())
            print msg
            raise Exception(msg)
        print 'ok..'

    return


@task
def info():
    for where in CONFIG:
        print
        print '-' * 50
        print where
        print '-' * 50
        config = get_config(where)
        for k in config:
            print k, ':', config[k]
        print

    print '-' * 50
    print
    print 'To start/stop development server:'
    print ' > bin/django runserver'
    print 'and to make search and such work:'
    print ' > bin/circusd'
    print 'and to make the relation with the repo work'
    print ' > cd to_repo_installation_dir'
    print ' > bin/circusd'
    print 'start as a daemon:'
    print ' > bin/circusd --daemon circus.ini'


@task
def profile():
    local('bin/python profile.py')
