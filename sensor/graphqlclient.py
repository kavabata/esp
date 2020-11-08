from urequests import post
import wifi
import config
import json

wifi.get_connection()

def shrink_query(query):
    query = query.replace(r'\n', ' ')
    query = query.replace(r'\t', ' ')

    while query != query.replace('  ', ' '):
        query = query.replace('  ', ' ')

    return query


class GraphQLClient:
    def __init__(self, endpoint, useGet=False):
        self.endpoint = config.get_value('api')
        self.useGet = useGet
        self.token = None

    def execute(self, query, variables=None):
        return self._send(query, variables)

    def inject_token(self, token):
        self.token = token

    def _send(self, query, variables):
        query = shrink_query(query)

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if self.token is not None:
            headers['Authorization'] = '{}'.format(self.token)

        if self.endpoint:
            response = post(
                self.endpoint,
                headers=headers,
                json=dict(query=query, variables=variables))

            return response.content.decode('utf-8')
        else:
            return 'no api connected'

def send_sensor_value(sensor_type, value):
    client = GraphQLClient(config.get_value('api'))

    query = ('''
    mutation{
    sensorValue(key: "%s", sensorType: "%s", value: "%s")
    }
    ''' % (config.get_value('key'), sensor_type, value))

    print(query)

    res = client.execute(query)

def send_controller_value(controller, value):
    client = GraphQLClient(config.get_value('api'))

    query = ('''
    mutation{
    controllerCall(key: "%s", controller: "%s", value: "%s")
    }
    ''' % (config.get_value('key'), controller, value))

    print(query)

    res = client.execute(query)

def send_config_value(config_key, value):
    client = GraphQLClient(config.get_value('api'))

    query = ('''
    mutation{
    configValue(key: "%s", name: "%s", value: "%s")
    }
    ''' % (config.get_value('key'), config_key, value))

    print('send_config_value')
    print(query)

    res = client.execute(query)

def update_config():
    client = GraphQLClient(config.get_value('api'))

    query = ('''
    {
        getConfig(key: "%s") {
            key
            value
        }
    }
    ''' % (config.get_value('key')))

    print('get_config')
    print(query)

    res = client.execute(query)
    c = json.loads(res)

    for x in c['data']['getConfig']:
        if "key" in x and "value" in x:
            config.write_conf(x['key'], x['value'])
