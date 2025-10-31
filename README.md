# C115---DISPOSITIVO-CONECTADOS---TRABALHO-FINAL-MININET
Repositório contendo o conteúdo referente ao trabalho final MININET feito por Gabriel Lopes Silva e Pedro Tiso

Objetivo:

-Os arquivos da questão 1 estão incluídos no repositório contendo um pdf com os prints e comandos utilizados nessa questão

-O scrypt foi desenvolvido visando atender os requisitos exigidos na QUESTÃO 2 do pdf contido no repositótio;

Como Executar:

1. Deve possuir o Mininet instalado e funcional;
2.  Execute-o no seu terminal Linux:

    sudo python scrypt_mininet.py

Explicação do código:

-CustomTopo(Topo)

    *Essa clase é utilizada para criação da topologia;
    *Adiciona os hosts, switchs e as conexões.

-executa_inspecao_ping(net, h1, s1)

    *Por meio dessa função é feita a inspeção das informações requeridas e o primeiro teste ping(considera a primeira topologia criada);

-executa_regras_mac(net, h1, h3, s1, s2, s3)

    *Nessa função as regras anteriores são apagadas;
    *São criadas regras baseadas no endereço MAC;
    *São feitos testes de ping para comprovar o funcionamento;

-run_full_test()

    *Essa função organiza a sequencia das funcionalidades do projeto;
    *Cria a topologia incluindo a configuração do RemoteController;
    *Chama as funções de teste seguindo a ordem das alternativas do pdf;
    *Abre um CLI que permite testes adicionais;
    *Encerra o sistema.
