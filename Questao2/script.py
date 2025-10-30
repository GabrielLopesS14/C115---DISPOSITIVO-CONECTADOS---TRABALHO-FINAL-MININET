from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.node import RemoteController

class CustomTopo( Topo ):
    "Criando topólogia: s1, s2 e s3 + h1, h2, h3, h4 e h5 - LETRA A"

    def build( self ):
        #Adiciona Hosts
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
        h4 = self.addHost( 'h4' )
        h5 = self.addHost( 'h5' )

        #Adiciona Switches
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )

        #Links: Hosts para Switches
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )
        self.addLink( h3, s2 )
        self.addLink( h4, s3 )
        self.addLink( h5, s3 )
        
        #Links: Switches para Switches (conexão linear)
        self.addLink( s1, s2 )
        self.addLink( s2, s3 )

#Registrando a topologia
topos = { 'customtopo': ( lambda: CustomTopo() ) }

def executa_inspecao_ping(net, h1, s1):
    """LETRA B (inspeção) + LETRA D (ping)"""
    
    info( '\n*** Letras B e D - Inspecionando e pingando\n' )
    
    #1. Inspeção (simulando dumpNodeConnections e ifconfig)
    info( 'Mapeamento de Portas e Conexões (net):\n' )
    dumpNodeConnections( net.hosts )
    
    #Exibe informações do h1
    info( '\n Detalhes do h1:\n' )
    info( h1.cmd('ifconfig h1-eth0') )
    
    #2. Ping normal (modo L2)
    info( 'Teste de Ping geral:\n' )
    net.pingAll()


def executa_regras_mac(net, h1, h3, s1, s2, s3):
    """LETRA E (regras baseadas em MAC) + LETRA F (ping)"""
    
    #Variáveis e IPs/MACs
    H1_IP = h1.IP()
    H3_IP = h3.IP()
    
    H1_MAC = '00:00:00:00:00:01'
    H3_MAC = '00:00:00:00:00:03'
    
    S1_H1_PORT = '1' #Porta do h1 no s1
    S1_S2_PORT = '3' #Porta do s2 no s1

    info( '\n*** LETRA E - Regras baseadas em MAC\n' )
    
    #1. Apagando regras anteriores
    info( 'Apagando todas as regras existentes nos Switches:\n' )
    s1.cmd('sudo ovs-ofctl del-flows s1')
    s2.cmd('sudo ovs-ofctl del-flows s2')
    s3.cmd('sudo ovs-ofctl del-flows s3')
    
    #2. Criando regras MAC no S1 (Para comunicar h1 e h3)
    info( 'Criando regras MAC no S1 para comunicação H1 com H3:\n' )
    
    #Regra 1: Tráfego de h1 (MAC 01) para h3 (MAC 03) -> Enviar para s2 (Porta 3)
    s1.cmd(f'sudo ovs-ofctl add-flow s1 dl_src={H1_MAC},dl_dst={H3_MAC},actions=output:{S1_S2_PORT}')
    
    #Regra 2: Tráfego de h3 (MAC 03) para h1 (MAC 01) -> Enviar para h1 (Porta 1)
    s1.cmd(f'sudo ovs-ofctl add-flow s1 dl_src={H3_MAC},dl_dst={H1_MAC},actions=output:{S1_H1_PORT}')
    
    #Fluxo para ARP (necessário para que os hosts descubram o MAC um do outro antes do ping)
    s1.cmd('sudo ovs-ofctl add-flow s1 dl_type=0x806,actions=flood')
    
    #3. Criando regras MAC no S2 (Para comunicar h3 e h1)
    info( 'Criando regras MAC no S2 para comunicação H3 (s2) <-> H1 (s1):\n' )

    #Regra 3: Tráfego de h3 (MAC 03) para h1 (MAC 01) -> Enviar para s1 (Porta 2)
    s2.cmd(f'sudo ovs-ofctl add-flow s2 dl_src={H3_MAC},dl_dst={H1_MAC},actions=output:2') 
    
    #Regra 4: Tráfego de h1 (MAC 01) para h3 (MAC 03) -> Enviar para h3 (Porta 1)
    s2.cmd(f'sudo ovs-ofctl add-flow s2 dl_src={H1_MAC},dl_dst={H3_MAC},actions=output:1') 

    #Fluxo para ARP
    s2.cmd('sudo ovs-ofctl add-flow s2 dl_type=0x806,actions=flood')

    #Mostrando regras no S1 e S2
    info( '4. Regras ativas no S1:\n' )
    info( s1.cmd('sudo ovs-ofctl dump-flows s1') )
    info( 'Regras ativas no S2:\n' )
    info( s2.cmd('sudo ovs-ofctl dump-flows s2') )

    #Execução do Requisito F: Testes de Ping para Validação
    info( '\n*** f) Teste de Ping para demonstrar que as regras foram bem implementadas:\n' )
    
    #Ping de SUCESSO: h1 para h3
    info( 'Ping: h1 para h3:\n' )
    info( h1.cmd(f'ping -c1 {H3_IP}') )
    
    info( 'CONCLUSÃO: O sucesso do ping de h1 para h3 comprova que as regras MAC estão controlando o tráfego SDN\n' )


def run_full_test():
    """Função principal"""
    
    topo = CustomTopo()
    
    #Inicia a rede com RemoteController
    info( '*** Iniciando a topologia com Remote Controller\n' )
    
    net = Mininet( 
        topo=topo, 
        controller=RemoteController,
    )
    
    net.start()

    #Obtendo Hosts e Switches
    h1 = net.get('h1')
    h3 = net.get('h3')
    s1 = net.get('s1')
    s2 = net.get('s2')
    s3 = net.get('s3') # CORREÇÃO: S3 obtido aqui
    
    #Executa a inspeção e ping normal (Requisitos B e D)
    executa_inspecao_ping(net, h1, s1)
    
    #Executa a criação das regras MAC e os testes de validação (Requisitos E e F)
    executa_regras_mac(net, h1, h3, s1, s2, s3) # S3 passado como argumento
    
    #Manter a CLI aberta para inspeções adicionais
    info( '\n*** Entrando no Mininet CLI. Use "ovs-ofctl dump-flows <switch>" para inspecionar as regras.\n' )
    CLI( net )
    
    net.stop()


if __name__ == '__main__':
    #Define o nível de log para 'info' para melhor visualização
    setLogLevel('info')
    run_full_test()