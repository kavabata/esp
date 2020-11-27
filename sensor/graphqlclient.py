from urequests import post
import wifi
import config
import json

wifi.get_connection()

class GraphQLClient:
    def __init__(self, endpoint, useGet=False):
        self.endpoint = config.get_value('api')
        self.useGet = useGet
        self.token = None

    def execute(self, query, variables=None):
        print(query)
        return self._send(query, variables)

    def inject_token(self, token):
        self.token = token


    def shrink_query(self, query):
        query = query.replace(r'\n', ' ')
        query = query.replace(r'\t', ' ')

        while query != query.replace('  ', ' '):
            query = query.replace('  ', ' ')

        return query

    def _send(self, query, variables):
        query = self.shrink_query(query)

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if self.token is not None:
            headers['Authorization'] = '{}'.format(self.token)

        if self.endpoint:

            try:
                response = post(
                    self.endpoint,
                    headers=headers,
                    json=dict(query=query, variables=variables))

                return response.content.decode('utf-8')
            except OSError as e:
                print('Cant send graphql')
                pass

            return 'skip'
        else:
            return 'no api connected'

client = GraphQLClient(config.get_value('api'))

def send_sensor_value(sensor_type, value):
    query = ('''
    mutation{
    sensorValue(key: "%s", sensorType: "%s", value: "%s")
    }
    ''' % (config.get_value('key'), sensor_type, value))
    client.execute(query)

def send_controller_value(controller, value):
    query = ('''
    mutation{
    controllerCall(key: "%s", controller: "%s", value: "%s")
    }
    ''' % (config.get_value('key'), controller, value))
    client.execute(query)

def send_config_value(config_key, value):
    query = ('''
    mutation{
    configValue(key: "%s", name: "%s", value: "%s")
    }
    ''' % (config.get_value('key'), config_key, value))
    client.execute(query)

def update_config():
    query = ('''
    {
        getConfig(key: "%s") {
            key
            value
        }
    }
    ''' % (config.get_value('key')))
    res = client.execute(query)
    c = json.loads(res)

    for x in c['data']['getConfig']:
        if "key" in x and "value" in x:
            config.write_conf(x['key'], x['value'])
