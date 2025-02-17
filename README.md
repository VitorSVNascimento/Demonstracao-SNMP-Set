# Demonstracao-SNMP-Set
 Projeto usando para demonstrar o uso de mensagens snmp set

# Instale as bibliotecas
 ``` dnf install net-snmp```

 # Edite o arquivo de configuração para liberar o write
 ![Screenshot from 2025-02-17 11-24-04](https://github.com/user-attachments/assets/bc7d0064-f835-42da-966e-333261acae85)

# Para editar use o comando
  ``` snmpset -v 2c -c senha 127.0.0.1 oid s "valor"```
