from logging import FileHandler
from logging import ERROR, Formatter

import os
import re
from socket import error as socket_error
import sys

from flask import Flask, request, jsonify, render_template
from flask.logging import default_handler

import paramiko

# Some "project" related constants
ROOT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
LOGS_DIRECTORY = ROOT_DIRECTORY + os.sep + 'logs'

app = Flask(__name__, static_url_path='')

# Configure (custom) Logging
def custom_file_logging():
    if not os.path.isdir(LOGS_DIRECTORY):
        os.mkdir(LOGS_DIRECTORY)

    file_handler = FileHandler(LOGS_DIRECTORY+os.sep+'main_log.log')
    file_handler.setLevel(ERROR)
    file_handler.setFormatter(Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    return file_handler

app.logger.removeHandler(default_handler)
app.logger.addHandler(custom_file_logging())

# Logic

@app.route('/processes/dashboard', methods=['GET'])
def dashboard():
    return render_template('/processes/dashboard.html')

@app.route('/processes/fetch', methods=['POST'])
def get_processes():
    # Some basic request data validation
    host = request.form.get('host')
    if not host:
        app.logger.info('Invalid host received in request! Request data: '
                        +str(request.form))
        return jsonify({'success': False, 'msg': 'Host is not provided'})
    
    username = request.form.get('username')
    if not username:
        app.logger.info('Invalid username received in request! Request data: '
                        +str(request.form))
        return jsonify({'success': False, 'msg': 'Username is not provided'})

    password = request.form.get('password', '')
    output = []
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=host,
            username=username,
            password=password
        )
        
        stdin, stdout, stderr = ssh_client.exec_command(
            'ps -eo cmd,pid,%cpu'
        )
            
        results = stdout.readlines()
        results = results[1:]
            
        for result in results:
            result = result.strip()
            result = re.split('\s+', result)
            if len(result) < 3:
                app.logger.error('Invalid row received: %s', str(result))
                continue
            
            output.append({
                'command': " ".join((result[0:-2])),
                'pid': result[-2],
                'cpu': result[-1]
            })
        ssh_client.close()
    except paramiko.BadHostKeyException as e:
        app.logger.error('Bad host key error: %s', e)
        o = {
            'success': False,
            'msg': 'Cannot establish SHH connection (Bad host key)!'
        }
    except paramiko.AuthenticationException as e:
        app.logger.error('Authentication error: %s', e)
        o = {
            'success': False,
            'msg': 'Cannot establish SHH connection (Authentication error)!'
        }
    except paramiko.SSHException as e:
        app.logger.error('General SSH error: %s', e)
        o = {
            'success': False,
            'msg': 'Cannot establish SHH connection (General SSH error)'
        }
    except socket_error as e:
        app.logger.error('General socket error: %s', e)
        o = {'success': False, 'msg': 'Cannot establish SHH connection!'}
    else:
        o = {'data': output, 'success': True}
    
    return jsonify(o)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
