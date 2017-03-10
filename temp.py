import requests
from urllib.parse import urljoin

from workable_api.secrets.secrets import *


# Workable API Client
class WorkableAPIClient:
    def __init__(self):
        self.subdomain = 'rossi-motors'
        self.root_endpoint = 'https://www.workable.com/spi/v3/accounts/'
        self.auth_token = 'Bearer {}'.format(API_TOKEN)

    def get_response(self, endpoint):
        headers = {'Authorization': self.auth_token, 'Content-Type': 'application/json'}
        url = urljoin(self.root_endpoint, endpoint)
        r = requests.get(url, headers=headers)
        return r.json()

    def test_api(self):
        """Call to / endpoint"""
        resp = self.get_response('')
        print(resp)

    def get_jobs(self):
        api_endpoint = '{subdomain}/jobs'.format(subdomain=self.subdomain)
        resp = self.get_response(api_endpoint)
        print(resp)

    def get_job_data(self, job_shortcode):
        api_endpoint = '{subdomain}/jobs/{shortcode}'.format(subdomain=self.subdomain, shortcode=job_shortcode)
        resp = self.get_response(api_endpoint)
        print(resp)

    def get_job_candidates(self, job_shortcode):
        api_endpoint = '{subdomain}/jobs/{job_shortcode}/candidates'.format(subdomain=self.subdomain, job_shortcode=job_shortcode)
        resp = self.get_response(api_endpoint)
        print(resp)

if __name__ == '__main__':
    workable_client = WorkableAPIClient()

    workable_client.get_jobs()
    workable_client.get_job_data('125CFA4F51')
    workable_client.get_job_candidates('125CFA4F51')
