#!/usr/bin/python

from __future__ import print_function

import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class NetworkTopo(Topo):
    # Builds network topology
    def build(self, **_opts):

        s1 = self.addSwitch('s1', failMode='standalone')

        # Adding hosts
        d1 = self.addHost('d1')
        d2 = self.addHost('d2')


        # Connecting hosts to switches
        for d, s in [(d1, s1), (d2, s1)]:
            self.addLink(d, s)



def run():
    topo = NetworkTopo()

    net = Mininet(topo=topo)

    net.start()

    d1 = net.get('d1')
    d2 = net.get('d2')
    print(d2.cmd('ping -c1 10.0.0.1'))
    server_output = d1.cmd('sudo iperf -s -p 5555 -b 10M -i 1 &')
    
    client_output=d2.cmd('sudo iperf -c 10.0.0.1 -p 5555 -b 10M -i 1 -t 10')
    print('Server output:')
    print(server_output)

    print('Client output:')
    print(client_output)
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
