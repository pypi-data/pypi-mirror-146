from IPython.core.magic import Magics, cell_magic, magics_class
import requests, json, time
import os
from pprint import pprint

@magics_class
class RumbleDBServerMagic(Magics):
    @cell_magic
    def jsoniq(self, line, cell=None):
        if cell is None:
            data = line
        else:
            data = cell

        start = time.time()                                                         
        response = json.loads(requests.post(os.environ["RUMBLEDB_SERVER"], data=data).text)                   
        end = time.time()                                                              
        print("Took: %s ms" % (end - start))

        if 'warning' in response:
            print(json.dumps(response['warning']))
        if 'values' in response:
            for e in response['values']:
                print(json.dumps(e))
        elif 'error-message' in response:
            return print(response['error-message'])
        else:
            return print(response)
