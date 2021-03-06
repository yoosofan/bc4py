#!/user/env python3
# -*- coding: utf-8 -*-

from bc4py import __version__, __chain_version__, __message__, __logo__
from bc4py.config import Debug
from bc4py.utils import set_database_path, set_blockchain_params
from bc4py.user.boot import *
from bc4py.user.network import broadcast_check, DirectCmd, sync_chain_loop, close_sync
from bc4py.user.api import create_rest_server
from bc4py.database.create import make_account_db
from bc4py.database.builder import builder
from p2p_python.utils import setup_p2p_params
from p2p_python.client import PeerClient
from p2p_python import config
from bc4py.for_debug import set_logger
import logging


def work(port, sub_dir=None):
    # BlockChain setup
    set_database_path(sub_dir=sub_dir)
    builder.set_database_path()
    make_account_db()
    genesis_block, network_ver, connections = load_boot_file()
    logging.info("Start p2p network-ver{} .".format(network_ver))

    # P2P network setup
    setup_p2p_params(network_ver=network_ver, p2p_port=port, sub_dir=sub_dir)
    pc = PeerClient()
    pc.event.addevent(cmd=DirectCmd.BEST_INFO, f=DirectCmd.best_info)
    pc.event.addevent(cmd=DirectCmd.BLOCK_BY_HEIGHT, f=DirectCmd.block_by_height)
    pc.event.addevent(cmd=DirectCmd.BLOCK_BY_HASH, f=DirectCmd.block_by_hash)
    pc.event.addevent(cmd=DirectCmd.TX_BY_HASH, f=DirectCmd.tx_by_hash)
    pc.event.addevent(cmd=DirectCmd.UNCONFIRMED_TX, f=DirectCmd.unconfirmed_tx)
    pc.event.addevent(cmd=DirectCmd.BIG_BLOCKS, f=DirectCmd.big_blocks)
    config.C.MAX_RECEIVE_SIZE = 2000 * 1000  # 2Mb
    pc.start()
    V.PC_OBJ = pc

    if pc.p2p.create_connection('tipnem.tk', 2000):
        logging.info("Connect!")

    for host, port in connections:
        pc.p2p.create_connection(host, port)
    set_blockchain_params(genesis_block)

    # BroadcastProcess setup
    pc.broadcast_check = broadcast_check

    # Update to newest blockchain
    builder.init(genesis_block)
    builder.db.sync = False  # more fast
    sync_chain_loop()

    # Mining/Staking setup (nothing)
    Debug.F_WS_FULL_ERROR_MSG = True
    # Debug.F_STICKY_TX_REJECTION = False  # for debug
    logging.info("Finished all initialize. (no mining and staking)")

    try:
        create_rest_server(f_local=True, port=port+1000, user='user', pwd='password')
        builder.db.batch_create()
        builder.close()
        pc.close()
        close_sync()
    except KeyboardInterrupt:
        logging.debug("KeyboardInterrupt.")


if __name__ == '__main__':
    set_logger(level=logging.DEBUG)
    logging.info("\n{}\n====\n{}, chain-ver={}\n{}\n"
                 .format(__logo__, __version__, __chain_version__, __message__))
    work(port=2000)
