from __future__ import print_function

import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections


class CustomTopology(Topo):
    def build(self,**_opts):
        # Adicionando hosts
        h1 = self.addHost('h1', ip='192.168.0.1/28', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='192.168.0.2/28', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='192.168.0.3/28', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', ip='192.168.0.4/28', mac='00:00:00:00:00:04')
        h5 = self.addHost('h3', ip='192.168.0.5/28', mac='00:00:00:00:00:05')
        h6 = self.addHost('h4', ip='192.168.0.5/28', mac='00:00:00:00:00:05')

        # Adicionando switches
        s1 = self.addSwitch('s1', failMode='standalone')
        s2 = self.addSwitch('s2', failMode='standalone')
        s3 = self.addSwitch('s3', failMode='standalone')
        s4 = self.addSwitch('s4', failMode='standalone')
        s5 = self.addSwitch('s5', failMode='standalone')


        # Adicionando links entre hosts e switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)

        # Adicionando link entre switches
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s3, s5)
        self.addLink(s1,h1)
        self.addLink(s2,h2)
        self.addLink(s4,h3)
        self.addLink(s4,h4)
        self.addLink(s5,h5)
        self.addLink(s5,h6)

        # Connecting hosts to switches
        for h, s in [(h1, s1), (h2, s1)]:
            self.addLink(h, s)
    
topos = { 'mytopo': ( lambda: CustomTopology() ) }

# def run():
#     topo = CustomTopology()

#     net = Mininet(topo=topo)

#     net.start()

#     d1 = net.get('d1')
#     d2 = net.get('d2')
#     print(d2.cmd('ping -c1 10.0.0.1'))
#     server_output = d1.cmd('sudo iperf -s -p 5555 -b 10M -i 1 &')
    
#     client_output=d2.cmd('sudo iperf -c 10.0.0.1 -p 5555 -b 10M -i 1 -t 10')
#     print('Server output:')
#     print(server_output)

#     print('Client output:')
#     print(client_output)
#     CLI(net)
#     net.stop()


# if __name__ == '__main__':
#     setLogLevel('info')
#     run()
