from IPython.core.magic import Magics, cell_magic, magics_class
import requests, json, time
import os
from pprint import pprint

@magics_class
class RumbleDBLivyMagic(Magics):
    def spark_submit(self, host, command, file):
        data = {
            'file': file,
            'className': 'org.rumbledb.cli.Main',
            'args': ['--master', 'yarn-cluster', '--query', command, '--show-error-info', 'yes']
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(host + '/batches', data = json.dumps(data), headers=headers)
        return response.headers['Location']

    @cell_magic
    def jsoniq(self, line, cell=None):
        if cell is None:
            data = line
        else:
            data = cell

        start = time.time()
        location = self.spark_submit(os.environ["RUMBLEDB_HOST"], data, os.environ["RUMBLEDB_JAR_PATH"])
        r = requests.get(os.environ["RUMBLEDB_HOST"] + location, data=json.dumps({'kind': 'spark'}), headers={'Content-Type': 'application/json'})
        while True:
            r = requests.get(os.environ["RUMBLEDB_HOST"] + location + '/state', data=json.dumps({'kind': 'spark'}), headers={'Content-Type': 'application/json'})
            state = r.json()['state']
            if state == 'success' or state == 'dead':
                break
            time.sleep(0.1)
        end = time.time()
        r = requests.get(os.environ["RUMBLEDB_HOST"] + location + '/log', data=json.dumps({'kind': 'spark'}), params={'from': 0, 'size': 99999}, headers={'Content-Type': 'application/json'})
        response = r.json()
        print("Took: %s ms" % (end - start))
        pprint(response['log'][1:-1])
        