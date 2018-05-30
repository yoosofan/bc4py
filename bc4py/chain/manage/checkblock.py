from bc4py.config import C, V, BlockChainError
from bc4py.chain.manage.checktx import check_tx
from bc4py.chain.difficulty import get_bits_by_hash, get_pos_bias_by_hash
import logging
from binascii import hexlify
import time


def check_block(block, cur):
    # Blockの正当性チェック
    if block.f_orphan:
        raise BlockChainError('Block is orphan.')
    elif len(block.txs) == 0:
        raise BlockChainError('Block don\'t have any txs.')
    elif block.getsize() > C.SIZE_BLOCK_LIMIT:
        raise BlockChainError('Block size is too large [{}b>{}b]'.format(block.getsize(), C.SIZE_BLOCK_LIMIT))
    bits = get_bits_by_hash(previous_hash=block.previous_hash, consensus=block.flag)[0]
    pos_bias = get_pos_bias_by_hash(previous_hash=block.previous_hash)[0]
    if block.bits != bits:
        raise BlockChainError('Block bits differ from calc. [{}!={}]'.format(block.bits, bits))
    elif block.pos_bias != pos_bias:
        raise BlockChainError('Block pos_bias differ from calc. [{}!={}]'.format(block.pos_bias, pos_bias))
    # TXチェック
    for tx in block.txs:
        check_tx(tx=tx, include_block=block, cur=cur)
    logging.debug("Checked block {} {}".format(C.consensus2name[block.flag], hexlify(block.hash).decode()))


def check_block_time(block):
    delay = int(time.time()) - block.create_time
    create_time = block.create_time - V.BLOCK_GENESIS_TIME
    if C.ACCEPT_MARGIN_TIME < abs(block.time-create_time):
        raise BlockChainError('Block time is out of range [{}<{}-{}={},{}]'
                              .format(C.ACCEPT_MARGIN_TIME, block.time, create_time, block.time - create_time, delay))
    if C.ACCEPT_MARGIN_TIME < delay:
        logging.warning("Long delay, for check new block. [{}<{}]"
                        .format(C.ACCEPT_MARGIN_TIME, delay))