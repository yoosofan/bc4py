#!/user/env python3
# -*- coding: utf-8 -*-

from bc4py.config import C, V
from bc4py.chain.utils import GompertzCurve
from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Hash import SHA256
from base64 import b64decode, b64encode
import multiprocessing
import os
import time
import bjson
import psutil


def set_database_path(sub_dir=None):
    V.SUB_DIR = sub_dir
    V.DB_HOME_DIR = os.path.join(os.path.expanduser("~"), 'blockchain-py')
    if not os.path.exists(V.DB_HOME_DIR):
        os.makedirs(V.DB_HOME_DIR)
    if sub_dir:
        V.DB_HOME_DIR = os.path.join(V.DB_HOME_DIR, sub_dir)
        if not os.path.exists(V.DB_HOME_DIR):
            os.makedirs(V.DB_HOME_DIR)
    V.DB_ACCOUNT_PATH = os.path.join(V.DB_HOME_DIR, 'account.dat')


def set_blockchain_params(genesis_block):
    assert 'spawn' in multiprocessing.get_all_start_methods(), 'Not found spawn method.'
    setting_tx = genesis_block.txs[0]
    params = bjson.loads(setting_tx.message)
    V.BLOCK_GENESIS_HASH = genesis_block.hash
    V.BLOCK_PREFIX = params.get('prefix')
    V.BLOCK_CONTRACT_PREFIX = params.get('contract_prefix')
    V.BLOCK_GENESIS_TIME = params.get('genesis_time')
    V.BLOCK_ALL_SUPPLY = params.get('all_supply')
    V.BLOCK_TIME_SPAN = params.get('block_span')
    V.BLOCK_REWARD = params.get('block_reward')
    V.CONTRACT_VALIDATOR_ADDRESS = params.get('validator_address')
    V.COIN_DIGIT = params.get('digit_number')
    V.COIN_MINIMUM_PRICE = params.get('minimum_price')
    V.CONTRACT_MINIMUM_AMOUNT = params.get('contract_minimum_amount')
    consensus = params.get('consensus')
    if isinstance(consensus, dict):
        V.BLOCK_CONSENSUS = consensus
        V.BLOCK_BASE_CONSENSUS = min(consensus.keys())
    else:
        # TODO: remove after test
        pow_ratio = params.get('pow_ratio')
        V.BLOCK_CONSENSUS = {C.BLOCK_YES_POW: pow_ratio, C.BLOCK_POS: 100 - pow_ratio}
        V.BLOCK_BASE_CONSENSUS = C.BLOCK_YES_POW
    GompertzCurve.setup_params()


def delete_pid_file():
    # PIDファイルを削除
    pid_path = os.path.join(V.DB_HOME_DIR, 'pid.lock')
    if os.path.exists(pid_path):
        os.remove(pid_path)


def make_pid_file():
    # 既に起動していないかPIDをチェック
    pid_path = os.path.join(V.DB_HOME_DIR, 'pid.lock')
    if os.path.exists(pid_path):
        with open(pid_path, mode='r') as fp:
            pid = int(fp.read())
        if psutil.pid_exists(pid):
            raise RuntimeError('Already running blockchain-py.')
        os.remove(pid_path)
    with open(pid_path, mode='w') as fp:
        fp.write(str(os.getpid()))


class AESCipher:
    @staticmethod
    def create_key(seed=None):
        if seed is None:
            return b64encode(os.urandom(AES.block_size)).decode()
        else:
            key = SHA256.new(seed.encode()).digest()[:AES.block_size]
            return b64encode(key).decode()

    @staticmethod
    def is_aes_key(key):
        try:
            return len(b64decode(key.encode(), validate=True)) == AES.block_size
        except:
            return False

    @staticmethod
    def encrypt(key, raw):
        assert type(raw) == bytes, "input data is bytes"
        key = b64decode(key.encode())
        raw = AESCipher._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    @staticmethod
    def decrypt(key, enc):
        assert type(enc) == bytes, 'Encrypt data is bytes'
        key = b64decode(key.encode())
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        raw = AESCipher._unpad(cipher.decrypt(enc[AES.block_size:]))
        if len(raw) == 0:
            raise ValueError("AES decryption error, not correct key.")
        else:
            return raw

    @staticmethod
    def _pad(s):
        pad = AES.block_size - len(s) % AES.block_size
        add = AES.block_size - len(s) % AES.block_size
        return s + add * pad.to_bytes(1, 'little')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class TimeWatch:
    def __init__(self, limit=0.1):
        self.data = [time.time()]
        self.calculate = None
        self.limit = limit

    def watch(self):
        self.data.append(time.time())

    def calc(self):
        # もし遅い操作があるならTrueを返す
        self.calculate = list()
        for i in range(len(self.data) - 1):
            self.calculate.append(round(self.data[i + 1] - self.data[i], 3))
        try:
            return max(self.calculate) > self.limit
        except ValueError:
            return False

    def show(self):
        def to_print(data):
            return str(data) + 'Sec'
        if self.calculate is None:
            self.calc()
        return ', '.join(map(to_print, self.calculate))
