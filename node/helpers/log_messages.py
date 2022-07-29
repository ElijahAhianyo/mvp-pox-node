try:
    from helpers.singleton import Singleton
except ImportError:
    from singleton import Singleton

import json, os

JSON_FILE_NAME = 'log_messages.json'

class Log(metaclass = Singleton):
    __messages = {}
    __logger = None
    def __init__(self, logger = None) -> None:
        self.getJson()
        self.__logger = logger

    def getJson(self):
        try:
            with open(JSON_FILE_NAME) as f:
                self.__messages = json.load(f)
        except json.decoder.JSONDecodeError:
            print('**** invalid json format')
        except FileNotFoundError:
            print('**** log file not found')
        except Exception as e:
            print('**** uncown error: ', str(e))

    @property
    def message(self):
        return self.__messages

    def add(self, key, **kwargs):
        message = self.__messages[key] if self.__messages.get(key) else key
        try:
            message = message.format(**kwargs)
        except KeyError:pass

        try:
            self.__logger.info(message)
        finally:
            return message

if __name__ == '__main__':
    import sys
    sys.path.extend(['/var/www/mvp-pox-node/node', '/home/vagrant/etny/node/etny-repo'])
    import config
    logger = config.logger
    log = Log(logger=logger).add
    # log = Log().add
    print(os.path.join(os.getcwd(), 'log_messages.json'))
    print(log('skipped_not_main', req_id = 'something'))
    print(log('already_assigned', req_id = 'something2'))
    print(log('dp_created'))
    print(log('dp_canceling', req = 'req value'))
    print(log('dp_canceled', req = 'req value'))
    print(log('tx_hash', _hash = 'haslsdjf'))
    print(log("was_not_approved_in_last_blocks", blocks_count = 20))