#!/usr/bin/python

from __future__ import print_function
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class NetworkTopo( Topo ):
    # Builds network topology
    def build( self, **_opts ):

        s1 = self.addSwitch ( 's1', failMode='standalone' )

        # Adding hosts
        h1 = self.addHost( 'h1', ip='192.168.0.1/28' )
        h2 = self.addHost( 'h2', ip='192.168.0.2/28' )

        
        # Connecting hosts to switches
        for d, s in [ (h1, s1), (h2, s1)]:
            self.addLink( d, s )



def run():
    topo = NetworkTopo()
    net = Mininet( topo=topo)
    net.start()
    CLI( net, script="nodes.sh")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
