from gevent import monkey; monkey.patch_all()
import os
import pathlib
import json
import threading

import requests
from websocket import create_connection
import gevent

API_VERSION = 'v1'

def _check_for_error(r):
    if not r.ok:
        print(json.dumps(json.loads(r.text), indent=4))
    r.raise_for_status()


class _Base:
    def __init__(self, token, host):
        self.token = token
        self.host = host

    def _get_route(self):
        return f'{self.host}/{API_VERSION}'

    def _get_headers(self):
        return {'Authorization': f'Bearer {self.token}'}

    def _make_request(self, method, url, params=None, files=None, list=False):
        if method == 'POST':
            r = requests.post(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                json=params,
                files=files
            )
        elif method == 'GET':
            r = requests.get(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                params=params
            )
        elif method == 'DELETE':
            r = requests.delete(
                f'{self._get_route()}{url}',
                headers=self._get_headers()
            )

        _check_for_error(r)

        if r.content:
            if list:
                return r.json()['data']
            else:
                return r.json()



class _Project(_Base):
    def __init__(self, token, host, key, ws):
        super().__init__(token, host)
        self.key = key
        self.ws = ws

    def get_info(self):
        return self._make_request('GET', f'/projects/{self.key}')

    def update_rounds(self, rounds):
        return self._make_request('POST', f'/projects/{self.key}', params={'rounds': rounds})

    def update_schedule(self, schedule):
        return self._make_request('POST', f'/projects/{self.key}', params={'schedule': schedule})

    def update_paused(self, paused):
        return self._make_request('POST', f'/projects/{self.key}', params={'paused': paused})

    def update_auto_increment(self, auto_increment):
        return self._make_request('POST', f'/projects/{self.key}', params={'autoIncrement': auto_increment})

    def update_optimizer_params(self, optimizer_params):
        return self._make_request('POST', f'/projects/{self.key}', params={'optimizerParams': optimizer_params})

    def delete_project(self):
        return self._make_request('DELETE', f'/projects/{self.key}')

    def add_contributor(self, email, role='member'):
        return self._make_request('POST', f'/projects/{self.key}/contributors', params={'email': email, 'role': role})

    def delete_contributor(self, email):
        return self._make_request('DELETE', f'/projects/{self.key}/contributors', params={'email': email})

    def get_next_schedule(self):
        return self._make_request('GET', f'/projects/{self.key}/schedule')

    def increment_round(self):
        return self._make_request('POST', f'/projects/{self.key}/increment')

    def create_datalink(self, datalink_key, description=None):
        params = {'key': datalink_key}
        if description:
            params['description'] = description
        return self._make_request('POST', f'/projects/{self.key}/datalinks', params=params)

    def get_datalinks(self):
        return self._make_request('GET', f'/projects/{self.key}/datalinks', list=True)

    def get_datalink(self, datalink_key):
        return self._make_request('GET', f'/projects/{self.key}/datalinks/{datalink_key}')

    def delete_datalink(self, datalink_key):
        return self._make_request('DELETE', f'/projects/{self.key}/datalinks/{datalink_key}')

    def get_rounds(self):
        return self._make_request('GET', f'/projects/{self.key}/rounds', list=True)

    def get_round(self, round):
        return self._make_request('GET', f'/projects/{self.key}/rounds/{round}')

    def get_stats(self, round=None, datalink_key=None):
        params = {}
        if round is not None:
            params['round'] = round
        if datalink_key is not None:
            params['datalink'] = datalink_key
        return self._make_request('GET', f'/projects/{self.key}/stats', params, list=True)

    def get_stats_avg(self):
        return self._make_request('GET', f'/projects/{self.key}/stats/avg')

    def get_submissions(self, datalink_key=None, round=None, owned=None):
        params = {}
        if round is not None:
            params['round'] = round
        if datalink_key is not None:
            params['datalink'] = datalink_key
        if owned is not None:
            params['owned'] = owned
        return self._make_request('GET', f'/projects/{self.key}/submissions', params, list=True)

    def upload_optimizer(self, path):
        with open(path, 'rb') as f:
            self._make_request('POST', f'/projects/{self.key}/optimizers', files={'optimizer': f})

    def report_stats(self, scores, num_samples, round, datalink_key):
        return self._make_request('POST', f'/projects/{self.key}/stats', params={
            'round': round,
            'scores': scores,
            'numPoints': num_samples,
            'datalink': datalink_key
        })

    def push_model(self, path, datalink_key, params=None):
        if params is not None:
            self._make_request('POST', f'/projects/{self.key}/models/{datalink_key}/params', params=params)

        if datalink_key is None:
            url = f'/projects/{self.key}/models'
        else:
            url = f'/projects/{self.key}/models/{datalink_key}'
        with open(path, 'rb') as f:
            self._make_request('POST', url, files={'modelfile': f})

    def pull_model(self, filepath, datalink_key=None, round=None, throw_error=False):
        params = {}
        if round is not None:
            params['round'] = round

        if datalink_key is None:
            url = f'{self._get_route()}/projects/{self.key}/models'
        else:
            url = f'{self._get_route()}/projects/{self.key}/models/{datalink_key}'
        r = requests.get(url, headers=self._get_headers(), params=params)
        _check_for_error(r)

        directory = os.path.dirname(filepath)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True) 

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)


class DynamoFL(_Base):
    def __init__(self, token, host='https://api.dynamofl.com'):
        super().__init__(token, host)

        self.wshost = self.host.replace('http', 'ws', 1)
        self.project_callbacks = {}
        self.on_round_threads = {}

        self.ws = create_connection(self.wshost)
        self.ws.send('{ "action": "auth", "token": "' + self.token + '" }')

        t = threading.Thread(target=self._gevent_ws_loop)
        t.setDaemon(False)
        t.start()

    def _gevent_ws_loop(self):
        while True:
            res = self.ws.recv()
            j = json.loads(res)
            if 'data' in j and 'project' in j['data'] and 'key' in j['data']['project']:
                project_key = j['data']['project']['key']
            if j['event'] == 'project-complete':
                if project_key in self.on_round_threads:
                    self.on_round_threads[project_key].kill()
                    del self.project_callbacks[project_key]
                    if not len(self.project_callbacks.keys()):
                        return
            if j['event'] == 'round-complete':
                if project_key in self.on_round_threads:
                    self.on_round_threads[project_key].kill()
                if project_key in self.project_callbacks:
                    callback = self.project_callbacks[project_key]
                    self.on_round_threads[project_key] = gevent.spawn(callback, j['data']['project'])
            if j['event'] == 'round-error':
                if project_key in self.on_round_threads:
                    print('Federation error occured:\n  ' + j['data']['errorMessage'])

    def on_new_round(self, project_key, callback):
        info = self._make_request('GET', f'/projects/{project_key}')
        # if info['isComplete']:
        #     g.join()
        #     return
        self.project_callbacks[project_key] = callback
        self.on_round_threads[project_key] = gevent.spawn(callback, info)

    def get_user(self):
        return self._make_request('GET', f'/user')

    def create_project(self, base_model_path, params):
        j = self._make_request('POST', '/projects', params=params)

        project = _Project(self.token, self.host, j['key'], self.ws)
        project.push_model(base_model_path, None)

        return project

    def get_project(self, project_key):
        j = self._make_request('GET', f'/projects/{project_key}')
        return _Project(self.token, self.host, j['key'], self.ws)

    def get_projects(self):
        return self._make_request('GET', f'/projects', list=True)



