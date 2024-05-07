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
        for h, s in [(h1, s1), (h2, s1), (h3, s2), (h4, s2), (h5, s4), (h6, s4)]:
            self.addLink(h, s)
    
topos = { 'mytopo': ( lambda: CustomTopology() ) }

def run():
    topo = CustomTopology()

    net = Mininet(topo=topo, controller=Controller)

    net.start()
    print('---- Informações das portas ----\n\n\n')
    dumpNodeConnections(net.hosts)

    print('---- Ping entre os dois nos com switch standalone ----\n\n\n')
    pingpar=net.pingPair()
    print(pingpar)
    d1 = net.get('h1')

    print('---- Apagando as regras ----\n\n\n')
    print(d1.cmd('sudo ovs-ofctl del-flows s1'))
    print(d1.cmd('sudo ovs-ofctl dump-flows s1'))

    print('---- Teste de ping sem regras ----\n\n\n')
    print(d1.cmd('ping -c1 192.168.0.2'))
    net['s1'].cmd('ovs-ofctl add-flow s1 action=normal')
    print(d1.cmd('sudo ovs-ofctl dump-flows s1'))

    print('---- Teste de ping switch normal ----\n\n\n')
    print(d1.cmd('ping -c1 192.168.0.2'))
    
    print('---- Apagando as regras ----\n\n\n')
    print(d1.cmd('sudo ovs-ofctl del-flows s1'))

    print('---- Criando as regras no switch s1 de portas ----\n\n\n')
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 in_port=1,actions=output:2')
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 in_port=2,actions=output:1')
    print(d1.cmd('sudo ovs-ofctl dump-flows s1'))

    print('---- Teste de ping das regras criadas ----\n\n\n')
    print(d1.cmd('ping -c1 192.168.0.2'))

    print('---- Criando as regras no switch s1 de mac ----\n\n\n')
    print(d1.cmd('sudo ovs-ofctl del-flows s1'))
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,actions=output:2')
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,actions=output:1')
    net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,action=flood')
    print(d1.cmd('sudo ovs-ofctl dump-flows s1'))
    print(d1.cmd('ping -c1 192.168.0.2'))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
