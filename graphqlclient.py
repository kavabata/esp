from urequests import post
import wifi
import config

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