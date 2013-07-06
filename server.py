import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os

connections = {}
properties = {
    'state': 0,
}

class BaseRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('button.html', host=self.request.host)

class ButtonWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        if self in connections:
            connections[self] = 0
            print 'Connection exists'
        else:
            connections[self] = 0
            self.write_message(json.dumps(
                {'state': properties['state']}
            ))

    def on_message(self, message):
        data = json.loads(message)
        if 'init' in data:
            self.write_message(json.dumps(
                {'state': properties['state']}
            ))
        elif 'state' in data:
            new_state = 0 if data['state'] == 1 else 1
            properties['state'] = new_state
            for conn, val in connections.iteritems():
                conn.write_message(json.dumps(
                    {'state': properties['state']}
                ))

    def on_close(self):
        if self not in connections:
            print 'Connection to delete does not exist'
        else:
            del connections[self]

settings = {
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
}

application = tornado.web.Application([
    (r'/', BaseRequestHandler),
    (r'/ws', ButtonWebSocket),
], **settings)

if __name__ == '__main__':
    application.listen(9900)
    tornado.ioloop.IOLoop.instance().start()
