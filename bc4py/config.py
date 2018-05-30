#!/user/env python3
# -*- coding: utf-8 -*-


class C:  # 起動中に変更してはいけない
    # base currency info
    BASE_CURRENCY_NAME = 'PyCoin'
    BASE_CURRENCY_UNIT = 'PC'
    BASE_CURRENCY_DESCRIPTION = 'Base currency.'

    # consensus
    BLOCK_GENESIS = 0
    BLOCK_POW = 1
    BLOCK_POS = 2
    HYBRID = 3
    consensus2name = {0: 'GENESIS', 1: 'POW', 2: 'POS', 3: 'HYBRID'}

    # tx type
    TX_GENESIS = 0  # Height0の初期設定TX
    TX_TRANSFER = 1  # 送受金
    TX_POW_REWARD = 2  # POWの報酬TX
    TX_POS_REWARD = 3  # POSの報酬TX
    TX_MINT_COIN = 4  # 新規貨幣を鋳造
    TX_CREATE_CONTRACT = 5  # コントラクトアドレスを作成
    TX_START_CONTRACT = 6  # コントラクトの開始TX
    TX_FINISH_CONTRACT = 7  # コントラクトの終了TX
    txtype2name = {
        0: 'GENESIS', 1: 'TRANSFER', 2: 'POW_REWARD', 3: 'POS_REWARD', 4: 'MINT_COIN',
        5: 'CREATE_CONTRACT', 6: 'START_CONTRACT', 7: 'FINISH_CONTRACT'}

    # message format
    MSG_NONE = 0  # no message
    MSG_PLAIN = 1  # 明示的にunicode
    MSG_BYTE = 2  # 明示的にbinary
    msgtype2name = {0: 'NONE', 1: 'PLAIN', 2: 'BYTE'}

    # difficulty
    DIFF_RETARGET = 20  # difficultyの計算Block数
    DIFF_MULTIPLY = 2  # Diffの変化の急さ、採掘間隔が短いなら小さい方が良い

    # block params
    MATURE_HEIGHT = 20  # 採掘されたBlockのOutputsが成熟する期間
    CHECKPOINT_SPAN = 200  # checkpointの作成間隔

    # account
    ANT_RESERVED = '@0'  # 未使用
    ANT_UNKNOWN = '@1'  # 使用済みだがTag無し
    ANT_OUTSIDE = '@2'  # 外部への入出金
    ANT_CONTRACT = '@3'  # コントラクトアドレス
    account2name = {
        ANT_RESERVED: '@Reserved', ANT_UNKNOWN: '@Unknown',
        ANT_OUTSIDE: '@Outside', ANT_CONTRACT: '@Contract'}

    # Block/TX/Fee limit
    ACCEPT_MARGIN_TIME = 30  # 新規データ受け入れ時間マージンSec
    SIZE_BLOCK_LIMIT = 1000*1000  # 1Mb block
    SIZE_TX_LIMIT = 200*1000  # 200kb tx
    CASHE_SIZE = 5000
    # REORG_LIMIT = 6  # Blockの撒き戻り制限
    MINTCOIN_FEE = 10 * 1000000  # 新規Mintcoin発行GasFee
    CONTRACT_CREATE_FEE = 10 * 1000000  # コントラクト作成GasFee


class V:  # 起動時に設定される変数
    # BLock params
    BLOCK_GENESIS_HASH = None
    BLOCK_PREFIX = None
    BLOCK_CONTRACT_PREFIX = None
    BLOCK_GENESIS_TIME = None
    BLOCK_TIME_SPAN = None
    BLOCK_HALVING_SPAN = None
    BLOCK_REWARD = None
    BLOCK_CONSENSUS = None
    BLOCK_POW_RATIO = None

    # base coin
    COIN_DIGIT = None
    COIN_MINIMUM_PRICE = None  # Gasの最小Price

    # database path
    SUB_DIR = None
    DB_HOME_DIR = None
    DB_BLOCKCHAIN_PATH = None
    DB_ACCOUNT_PATH = None

    # encryption key
    ENCRYPT_KEY = None

    # mining
    MINING_ADDRESS = None
    MINING_MESSAGE = None
    MINING_OBJ = None
    STAKING_OBJ = None
    PC_OBJ = None

    # logging debug
    F_MINING_POWER_SAVE = 0.0
    F_DEBUG = None

    # API streaming
    NEW_CHAIN_INFO_QUE = None


class P:
    # 0Blockより1000Block毎にCheckPointを作成する
    CHECK_POINTS = dict()  # { height: blockhash,..}
    UNCONFIRMED_TX = set()  # {txhash,..}
    F_NOW_BOOTING = True  # 起動中


class Debug:
    F_WS_FULL_ERROR_MSG = True
    F_LIMIT_INCLUDE_TX_IN_BLOCK = 0  # 1blockに入れるTXの最大数(0=無効)


class BlockChainError(Exception):
    pass