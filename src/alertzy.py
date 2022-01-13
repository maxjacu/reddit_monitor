import threading
from absl import logging
import requests
import os


class Alertzy:

    def __init__(self, service_name="Reddit Monitor"):
        self.use_module = True
        self.lock = threading.Lock()
        self.alertzy_key = os.getenv('ALERTZY_KEY')
        self.service_name = service_name
        if not self.alertzy_key:
            self.use_module = False
            logging.warning('Alertzy was not configured. Notifications will not be sent to your '
                            'iPhone through the Alertzy app.')
        else:
            # pass
            self.send_notification('Monitoring has started.', title=service_name)

    def send_notification(self, message, title, url=None, image_url=None):
        # https://alertzy.app/
        if self.use_module:
            with self.lock:
                assert self.alertzy_key is not None
                try:
                    requests.post('https://alertzy.app/send', data={
                        'accountKey': self.alertzy_key,
                        'title': title,
                        'message': message,
                        'link': url,
                        'image': image_url,
                    })
                except Exception:
                    return False
                return True
