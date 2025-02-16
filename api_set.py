from flask import Flask, request, jsonify, render_template
from pysnmp.hlapi import *
from pysnmp.smi.rfc1902 import v2c
from flask_cors import CORS

HOST='0.0.0.0'
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": '*'}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/snmpset', methods=['POST'])
def snmp_set():
    data = request.json
    agent_ip = data.get('ip')
    oid = data.get('oid')
    value_type = data.get('type')
    value = data.get('value')
    community = data.get('community')
    
    if not all([agent_ip, oid, value_type, value]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    value_map = {
        'integer': v2c.Integer,
        'string': v2c.OctetString,
    }
    
    if value_type not in value_map:
        return jsonify({'error': 'Invalid type'}), 400
    
    value_class = value_map[value_type]
    
    try:
        # Envia o comando SNMP SET para o agente, utilizando os parâmetros fornecidos.
        error_indication, error_status, error_index, var_binds = next(
            setCmd(SnmpEngine(),  # Cria uma instância do SNMP engine.
                   CommunityData(community, mpModel=1),  # Define os dados da comunidade SNMP (versão 2c).
                   UdpTransportTarget((agent_ip, 161)), # Define o alvo SNMP (endereço IP e porta).
                   ContextData(), # Dados do contexto SNMP (geralmente vazio).
                   ObjectType(ObjectIdentity(oid), value_class(value))) # Define o OID e o valor a ser atribuído.
        )
        
        if error_indication:
            # Retorna o erro SNMP, caso tenha ocorrido.
            return jsonify({'error': str(error_indication)}), 500
        elif error_status:
            # Retorna o status de erro SNMP, caso tenha ocorrido.
            return jsonify({'error': f'{error_status.prettyPrint()} at {error_index and var_binds[int(error_index)-1] or "?"}'}), 500
        else:
            return jsonify({'success': 'SNMP set successful'})
    except Exception as e:
         # Se ocorrer alguma exceção inesperada, retorna o erro.
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host=HOST)
