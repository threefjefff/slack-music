import json
import cherrypy
from apollo import Apollo

@cherrypy.expose
class ApolloController(object):
    def __init__(self):
        self._apollo = Apollo()

    def _cp_dispatch(self, vpath):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        data = cherrypy.request.json
        if data["type"] == "url_verification":
            return self._apollo.challenge(data)
        else:
            cherrypy.response.status = '400'
            return {"error": "command not recognised"}

if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(ApolloController(), '/slack', conf)
