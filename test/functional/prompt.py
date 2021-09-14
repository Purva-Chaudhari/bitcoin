import logging
import struct
import sys
import threading

from test_framework.p2p import (
    P2PInterface,
    p2p_lock,
)
from test_framework.messages import (
    CAddress,
    NODE_NETWORK,
    NODE_WITNESS,
    msg_addr,
    msg_getaddr,
    msg_verack
)

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, assert_greater_than
import random
import time

from test_framework.test_node import TestNode
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal



def check_node_connections(*, node, num_in, num_out):
	info = node.getnetworkinfo()
	assert_equal(info["connections_in"], num_in)
	assert_equal(info["connections_out"], num_out)


class AddrReceiver(P2PInterface):
    num_ipv4_received = 0
    test_addr_contents = False
    _tokens = 1
    send_getaddr = True

    def __init__(self, test_addr_contents=False, send_getaddr=True):
        super().__init__()
        self.test_addr_contents = test_addr_contents
        self.send_getaddr = send_getaddr

    def on_addr(self, message):
        self.received_addrs = []
        for addr in message.addrs:
            self.received_addrs.append(addr.ip)


    @property
    def addr_received(self):
        return self.num_ipv4_received != 0

    def on_version(self, message):
        self.send_message(msg_verack())
        if (self.send_getaddr):
            self.send_message(msg_getaddr())

    def getaddr_received(self):
        return self.message_count['getaddr'] > 0

class TestPrompt(BitcoinTestFramework):
	counter = 0
	mocktime = int(time.time())
	def set_test_params(self):
		self.num_nodes = 1
		self.setup_clean_chain = True
    		
	def run_test(self):
	        node = self.nodes[0]
	        peer_info = node.getpeerinfo()
	        import pdb; pdb.set_trace()
	        self.log.info("Connect to an inbound peer")
	        inbound_peer = node.add_p2p_connection(AddrReceiver(test_addr_contents=True, send_getaddr=False))
	        
	        self.log.info("Connect to an outbound-full-relay peer")
	        full_outbound_peer = node.add_outbound_p2p_connection(AddrReceiver(), p2p_idx=0, connection_type="outbound-full-relay")
	        
	        self.log.info('Advertising address')
	        
	        check_node_connections(node=self.nodes[0], num_in=1, num_out=1)
	        
	        self.log.info('Check that we send a getaddr message upon connecting to an outbound-full-relay peer')
	        full_outbound_peer.sync_with_ping()
	        assert full_outbound_peer.getaddr_received()
	        
	        self.log.info('Check that we do not send a getaddr message upon connecting to an block-relay-only peer')
	        block_relay_peer = node.add_outbound_p2p_connection(AddrReceiver(), p2p_idx=1, connection_type="block-relay-only")
	        block_relay_peer.sync_with_ping()
	        assert_equal(block_relay_peer.getaddr_received(), False)
	        
	        self.log.info('Check that we send a getaddr message upon connecting to an addr-fetch peer')
	        addr_fetch_peer = node.add_outbound_p2p_connection(AddrReceiver(), p2p_idx=1, connection_type="addr-fetch")
	        addr_fetch_peer.sync_with_ping()
	        assert addr_fetch_peer.getaddr_received()
	        
	        self.log.info('Check that we send do not a getaddr message upon connecting to an inbound peer')
	        inbound_peer.sync_with_ping()
	        assert_equal(inbound.getaddr_received(), False)
	        
	        
	   
	        
	        self.log.info("Disconnect from peers")
	        self.nodes[0].disconnect_p2ps()
	        
	      
if __name__ == '__main__':
	TestPrompt().main()
