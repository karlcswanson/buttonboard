from signal import pause
import json
import threading
import time
import logging
import sys
from logging.handlers import RotatingFileHandler


from gpiozero import Button
from pythonosc import udp_client

buttons = []
FORMAT = '%(asctime)s %(levelname)s:%(message)s'


class OSCConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = udp_client.SimpleUDPClient(self.host, self.port)

        try:
            self.s.send_message('/login/', 'Now Connected')
        except:
            logging.warning('Connection Error')

    def send(self, path, value):
        logging.debug('sending {} to: {}:{}{}'.format(value, server.host, server.port, path))

        try:
            self.s.send_message(path, value)
        except:
            logging.warning(' Error sending {} to: {}:{}{}'.format(value, server.host, server.port, path))

class ContactButton:
    def __init__(self, cfg):
        self.cfg = cfg
        self.button_number = cfg['button']
        self.pin = cfg['pin']

        self.button = Button(self.pin, pull_up = True)

        if 'onPress' in self.cfg:
            self.button.when_pressed = self.on_press

        if 'onRelease' in self.cfg:
            self.button.when_released = self.on_release

    def on_press(self):
        server.send(self.cfg['onPress']['path'], self.cfg['onPress']['value'])
        logging.debug('Button {} pressed at GPIO: {}'.format(self.button_number, self.pin))

    def on_release(self):
        server.send(self.cfg['onRelease']['path'], self.cfg['onRelease']['value'])
        logging.debug('Button {} released at GPIO: {}'.format(self.button_number, self.pin))


def read_json_config(file):
    global config_tree
    with open(file) as config_file:
        config_tree = json.load(config_file)

    for i in config_tree['buttons']:
        buttons.append(ContactButton(i))

def logging_init():
    formatter = logging.Formatter(FORMAT)
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    sthandler = logging.StreamHandler(sys.stdout)
    fhandler = logging.handlers.RotatingFileHandler('buttonboard.log',
                                                    maxBytes=10*1024*1024,
                                                    backupCount=5)

    sthandler.setFormatter(formatter)
    fhandler.setFormatter(formatter)

    log.addHandler(sthandler)
    log.addHandler(fhandler)

def heartbeat():
    while True:
        logging.debug('sending heartbeat LOW')
        server.send('/d3/brightness', 0)
        time.sleep(1)
        logging.debug('sending heartbeat HIGH')
        server.send('/d3/brightness', 1)
        time.sleep(1)

def main():
    logging_init()
    read_json_config('config.json')
    global server
    server = OSCConnection(config_tree['host'], config_tree['port'])

    if 'heartbeat' in config_tree:
        heartbeat_t = threading.Thread(target=heartbeat)
        heartbeat_t.start()
    pause()

if __name__ == '__main__':
    main()
