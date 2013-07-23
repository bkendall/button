import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os

connections = {}
properties = {
    'state': 0,
}

m_welcome = 'Welcome! There are %d total connections'
m_state = 'The state has been changed to %s'
m_user = 'There are now %d connections'

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
        for conn, val in connections.iteritems():
            if conn == self: continue
            conn.write_message(json.dumps(
                {'message': m_user % len(connections)}
            ))

    def on_message(self, message):
        data = json.loads(message)
        if 'init' in data:
            self.write_message(json.dumps(
                {'state': properties['state'],
                 'message': (m_welcome + '\n' + m_state) % 
                    (len(connections),
                    'on' if properties['state'] == 1 else 'off')
                }
            ))
        elif 'state' in data:
            new_state = 0 if data['state'] == 1 else 1
            properties['state'] = new_state
            for conn, val in connections.iteritems():
                conn.write_message(json.dumps(
                    {'state': properties['state'],
                     'message': m_state %
                        ('on' if properties['state'] == 1 else 'off')}
                ))
        elif 'message' in data:
            message = '%s: %s' % (str(id(self)), data['message'])
            for conn, val in connections.iteritems():
                conn.write_message(json.dumps(
                    {'message': message}
                ))

    def on_close(self):
        if self not in connections:
            print 'Connection to delete does not exist'
        else:
            del connections[self]
            for conn, val in connections.iteritems():
                conn.write_message(json.dumps(
                    {'message': m_user % len(connections)}
                ))

this_path = os.path.dirname(os.path.abspath(__file__))
settings = {
    'static_path': os.path.join(this_path, 'static'),
    'template_path': os.path.join(this_path, 'templates'),
}

application = tornado.web.Application([
    (r'/', BaseRequestHandler),
    (r'/ws', ButtonWebSocket),
], **settings)

if __name__ == '__main__':
    application.listen(9900)
    for (path, dirs, files) in os.walk(settings['template_path']):
        for item in files:
            tornado.autoreload.watch(os.path.join(path, item))
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
