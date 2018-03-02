from settings_test import *

INSTALLED_APPS = list(INSTALLED_APPS) + ['django_jenkins']

# make tests faster
SOUTH_TESTS_MIGRATE = False

# use nose to find tests
JENKINS_TEST_RUNNER = 'django_jenkins.nose_runner.CINoseTestSuiteRunner'

PROJECT_APPS = ['dasa']
