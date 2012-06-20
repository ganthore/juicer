# -*- coding: utf-8 -*-
import juicer.utils
import juicer.juicer
import json
import requests
import simplejson
import re

class Juicer(object):
    def __init__(self, args):
        self.args = args

        connect_params = juicer.utils.get_login_info(self.args)

        self.base_url = connect_params['base_url']
        self.auth = (connect_params['username'], connect_params['password'])
        self.headers = {'content-type': 'application/json'}

    def delete(self, url=""):
        return requests.delete(url, auth=self.auth, headers=self.headers,
                               verify=False)

    def get(self, url=""):
        return requests.get(url, auth=self.auth, headers=self.headers,
                            verify=False)

    def post(self, url="", data={}):
        return requests.post(url, json.dumps(data), auth=self.auth,
                             headers=self.headers, verify=False)

    def put(self, url="", data={}):
        return requests.put(url, json.dumps(data), auth=self.auth,
                            headers=self.headers, verify=False)

    def search_cart(self, query='/services/search/cart', output=[]):
        pass

    def search_rpm(self, name='', envs=[], query='/services/search/packages/', output=[]):
        output.append('Packages:')

        # if no envs listed, check all repositories
        if envs == None:
            data = {'regex':name}
            url = self.base_url + query

            _r = self.post(url, data)

            if _r.status_code != 200:
                _r.raise_for_status

            for pkg in json.loads(_r.text):
                output.append(pkg['filename'])

            return output
        else:
            output.append('Repository:')

            # get list of all repos, then parse down to the ones we want
            url = self.base_url + '/repositories/'
            _r = self.get(url)

            repo_list = json.loads(_r.text)

            for repo in repo_list:
                for enviro in envs:
                    if re.match(".*-{0}$".format(enviro), repo['id']):
                        data = {'regex':name,
                                'repoid':repo['id']}
                        url = self.base_url + query

                        _r = self.post(url, data)

                        if _r.status_code != 200:
                            _r.raise_for_status

                        for pkg in json.loads(_r.text):
                            output.append(pkg['filename'])
                            output.append(repo['id'])

            return output