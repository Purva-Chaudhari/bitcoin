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



class TestPrompt(BitcoinTestFramework):
	def set_test_params(self):
		self.num_nodes = 1
		self.setup_clean_chain = False
    		
	def run_test(self):
	        node = self.nodes[0]
	        peer_info = node.getpeerinfo()
	        import pdb; pdb.set_trace()
	        #node.generatetoaddress(1, node.get_deterministic_priv_key().address)
	        self.log.info("Connect to an inbound peer")
	        inbound_peer = node.add_p2p_connection(P2PInterface())
	        inbound_peer.send_message(msg_verack())
	        self.log.info("Check addr received is not received by inbound peer")
	        assert_equal( inbound_peer.message_count['addr'],0)
	        
	        
	        self.log.info("Connect to an outbound-full-relay peer")
	        full_outbound_peer = node.add_outbound_p2p_connection(P2PInterface(), p2p_idx=0, connection_type="outbound-full-relay")
	        full_outbound_peer.send_message(msg_verack())
	        self.log.info("Check addr received by outbound-full-relay peer")
	        assert_equal( full_outbound_peer.message_count['addr'],1)
	        
	        
	        self.log.info("Connect to an block-only-relay peer")
	        block_relay_peer = node.add_outbound_p2p_connection(P2PInterface(), p2p_idx=1, connection_type="block-relay-only")
	        self.log.info("Check addr received is not received by block-only-relay peer")
	        assert_equal( block_relay_peer.message_count['addr'],0)
	        
	        self.log.info("Connect to an addr-fetch peer")
	        addr_fetch_peer = node.add_outbound_p2p_connection(P2PInterface(), p2p_idx=2, connection_type="addr-fetch")
	        self.log.info("Check addr received by addr-fetch peer")
	        assert_equal( addr_fetch_peer.message_count['addr'],1)
	        	        
	        check_node_connections(node=self.nodes[0], num_in=1, num_out=3)
	        
	        self.log.info("Disconnect from peers")
	        self.nodes[0].disconnect_p2ps()
	
	        
	   
		
if __name__ == '__main__':
	TestPrompt().main()

