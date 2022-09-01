
import time, socket, urllib, os, sys, ntpath, ipfshttpclient, psutil
from ipfshttpclient.exceptions import StatusError
from ipfshttpclient.client.base import ResponseBase

from web3 import Web3
from eth_account import Account
from web3.middleware import geth_poa_middleware
from web3.exceptions import TimeExhausted, ContractLogicError
import configparser
from typing import Union


class IpfsInstance:
    
    _w3 = None
    _web3_provider = None
    _acct = None
    _etny = None
    _contract_address = None
    _contract_abi = None
    _ipfsuser = None
    _ipfspassword = None
    _ipfs_cloud = 'ipfs.ethernity.cloud'
    _ipfshash = "QmRBc1eBt4hpJQUqHqn6eA8ixQPD3LFcUDsn6coKBQtia5"
    _ipfsnode = None
    _client = None
    _local = True
    _private_key = None
    _address = None
    _config = None

    @property
    def __get_ipfs_executable_path(self) -> str:
        return os.path.join('.tmp', 'go-ipfs', 'ipfs')
        
    @property
    def __get_ipfs_address(self) -> str:
        addr = urllib.parse.urlsplit('http://127.0.0.1:5001')
        return '/'.join(['/dns', addr.hostname, 'tcp', str(addr.port), addr.scheme])

    def __init__(self) -> None:
        print('its init class')

        # get config
        self._configFile()

        # read abi
        self._readABI()

        # base config
        self._baseConfigs()

        # connect to ipfs
        self._connect_ipfs_gateway()

    def upload_ipfs(self, file, recursive=False) -> str:
        while True:
            try:
                if self._local and self._ipfsnode is not None:
                    self.__ipfs_swarm_connect(log=True)
            except Exception as e:
                print('error', e)
                continue
            res = self._add_to_ipfs(file, recursive)
            if isinstance(res, list):
                for item in res:
                    if item['Name'] == ntpath.basename(file):
                        return item['Hash']
            else:
                return res['Hash']

    def _add_to_ipfs(self, file, recursive=False) -> Union[ResponseBase, list, None]:
        while True:
            try:
                return self._client.add(file, recursive=recursive)
            except Exception:
                time.sleep(1)
                continue
            except StatusError:
                self.__log("You have reached request limit, please wait or try again later", 'warning')
                time.sleep(60)
                continue

    def _readABI(self) -> None:
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/pox.abi') as f:
                self._contract_abi = f.read()
        except FileNotFoundError as e:
            print(e)
            sys.exit()

    def _configFile(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), 'config'))
        self._config = config['DEFAULT']
        self._private_key = self._config['PRIVATE_KEY']
        self._address = self._config['ADDRESS']
        self._contract_address = self._config['contract_address']

    def _baseConfigs(self) -> None:
        self._w3 = Web3(Web3.HTTPProvider(self._web3_provider)) 
        self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        print(f'''
            self._private_key = {self._private_key}
            self._contract_address = {self._contract_address}
        ''')
        self._acct = Account.privateKeyToAccount(self._private_key) 
        self._etny = self._w3.eth.contract(address=self._w3.toChecksumAddress(self._contract_address), abi=self._contract_abi)

    def _connect_ipfs_gateway(self) -> None:
        while True:
            try:
                auth = None if not self._ipfsuser and not self._ipfspassword else (self._ipfsuser, self._ipfspassword)
                self._client = ipfshttpclient.connect(self.__get_ipfs_address, auth=auth)
                if self._local:
                    self._ipfsnode = socket.gethostbyname(self._ipfs_cloud) 
                    self._client.bootstrap.add(f'/ip4/{self._ipfsnode}/tcp/4001/ipfs/{self._ipfshash}')
                break
            except Exception as e:
                print(e)
                time.sleep(2)
                self._restart_ipfs()

    def _restart_ipfs(self) -> None:
        if self._local:
            for proc in psutil.process_iter():
                if proc.name() == "ipfs.exe":
                    proc.kill()
                if proc.name() == "ipfs":
                    proc.kill()
            cmd = 'start /B "" "%s" daemon > %s' % (self.__get_ipfs_executable_path, self.__get_ipfs_output_file_path())
            print(cmd)
            os.system(cmd)
        return None

    def __get_ipfs_output_file_path(self, fileName = 'ipfsoutput.txt') -> str:
        if not os.path.isdir(os.path.join('.tmp')):
            os.mkdir(os.path.join('.tmp'))
        return os.path.join('.tmp', fileName)

    def __ipfs_swarm_connect(self, log = False) -> None:
        cmd = "%s swarm connect /ip4/%s/tcp/4001/ipfs/%s > %s" % (
                    self.__get_ipfs_executable_path, 
                    self._ipfsnode,
                    self._ipfshash,
                    self.__get_ipfs_output_file_path())
        if log: print(cmd)
        os.system(cmd)


    