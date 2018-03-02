#!bin/python

import requests

REPO_URL = 'http://repository-dasa.anri.go.id/'
# REPO_URL = 'http://127.0.0.1:5000/'

URLS_TO_TEST = [
    '{REPO_URL}scans?archiveFile=1106',
    '{REPO_URL}scans/283429/images/283453',
    '{REPO_URL}scans/3390/image?size=1200x',
]


def report():
    for i, url in enumerate(URLS_TO_TEST):
        counter = i + 1
        url = url.format(REPO_URL=REPO_URL)
        print '{counter}. benchmarking {url}'.format(**locals())
        response = requests.get(url)
        print '{response.status_code}: number of seconds: {seconds}'.format(response=response, seconds= response.elapsed.total_seconds())


if __name__ == '__main__':
    report()