import websocket
import json
import gzip
import time
import threading

class BtcmexWebSocket:

    def __init__(self, endpoint, api_key=None, api_secret=None):

        self.endpoint = endpoint

        self.ws = websocket.WebSocketApp(self.endpoint,
                                on_message = self.on_message,
                                on_open=self.on_open,
                                on_error = self.on_error,
                                on_close = self.on_close)
        send_ping = threading.Thread(target=self.send_ping)
        send_ping.start()

    def run(self):
        while True:
            try:
                self.ws.run_forever()
                print('Web Socket process ended.')
            except:
                pass

    def stop(self):
        self.ws.keep_running = False
        print('Stop Web Socket Connection')

    def on_message(self, message):
        if message == 'pong':
            print(message)
            return
        m = json.loads(message)


    def on_error(self, error):
        print("Error: " + str(error))
        error = gzip.decompress(error).decode()
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        self.ws.send(
            json.dumps({'op': 'subscribe', 'args': 'trade:XBTUSD' }))
        print("### opened ###")


    def send_ping(self):
        while 1:
            try:
                self.ws.send("ping")
                time.sleep(15)
            except Exception as e:
                print(e)
                time.sleep(2)


if __name__ == '__main__':
    ws = BtcmexWebSocket(
        endpoint='wss://www.btcmex.com/realtime')
    ws.run()

