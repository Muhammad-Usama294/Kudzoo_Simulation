from flask import Flask, request, jsonify
import socket
import json
import logging
import argparse

# Disable Flask logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Parse args to get N, F, P from launcher
parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=7)
parser.add_argument("--f", type=int, default=1)
parser.add_argument("--p", type=int, default=1)
# We use parse_known_args because Flask also looks at sys.argv
args, _ = parser.parse_known_args()

state = {
    'replicas': {},
    'config': {'n': args.n, 'f': args.f, 'p': args.p}, # Store config here
    'metrics': {'finalized': 0, 'fast_path': 0, 'slow_path': 0},
    'live_block': {
        'id': "Waiting...", 'status': 'IDLE', 
        'votes': [], 'fragments': [], 'path': None,
        'leader': 0, 'view': 0
    },
    'faults': {}
}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    state['replicas'][data['id']] = data['port']
    if data['id'] not in state['faults']:
        state['faults'][data['id']] = "HEALTHY"
    return jsonify({'status': 'ok'})

@app.route('/inject_block', methods=['POST'])
def inject():
    N = state['config']['n']
    
    # SMART ROTATION: Keep rotating until we find a HEALTHY leader
    attempts = 0
    while attempts < N:
        # Increment View
        state['live_block']['view'] += 1
        new_view = state['live_block']['view']
        leader_id = new_view % N
        
        # Check if this leader is DEAD
        status = state['faults'].get(leader_id, "HEALTHY")
        
        if status != "DEAD":
            # Found a living leader!
            break
            
        # If dead, loop again (Skipping this node)
        attempts += 1
        
    # If all nodes are dead
    if attempts >= N:
        return jsonify({'status': 'all_nodes_dead'}), 503

    # Reset Live State
    state['live_block'] = {
        'id': "Pending...", 'status': 'PROPOSING', 
        'votes': [], 'fragments': [], 'path': None,
        'leader': leader_id, 'view': new_view
    }
    
    # Send to the Healthy Leader
    if leader_id in state['replicas']:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', state['replicas'][leader_id]))
            s.sendall(json.dumps({'type': 'INJECT', 'view': new_view}).encode())
            s.close()
            return jsonify({'status': 'ok', 'leader': leader_id})
        except: pass
        
    return jsonify({'status': 'leader_down'}), 500

@app.route('/report', methods=['POST'])
def report():
    t = request.json['type']
    rid = request.json['replica_id']
    
    if t == 'FRAGMENT':
        state['live_block']['id'] = request.json['block_id']
        if rid not in state['live_block']['fragments']:
            state['live_block']['fragments'].append(rid)
            
    elif t == 'VOTE':
        if rid not in state['live_block']['votes']:
            state['live_block']['votes'].append(rid)
            state['live_block']['status'] = 'VOTING'
            
    elif t == 'FINALIZED':
        if state['live_block']['status'] != 'FINALIZED':
            state['metrics']['finalized'] += 1
            path = request.json['path']
            if path == 'FAST': state['metrics']['fast_path'] += 1
            else: state['metrics']['slow_path'] += 1
            state['live_block']['status'] = 'FINALIZED'
            state['live_block']['path'] = path

    return jsonify({'status': 'ack'})

@app.route('/fault', methods=['POST'])
def fault():
    target = int(request.json['target'])
    params = request.json['params']
    
    if params['drop'] > 0.5: state['faults'][target] = "DEAD"
    elif params['delay'] > 0: state['faults'][target] = "SLOW"
    else: state['faults'][target] = "HEALTHY"

    if target in state['replicas']:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', state['replicas'][target]))
            s.sendall(json.dumps({'type': 'FAULT', 'params': params}).encode())
            s.close()
        except: pass
    return jsonify({'status': 'ok'})

@app.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify({
        'config': state['config'],
        'node_count': len(state['replicas']),
        'metrics': state['metrics'],
        'live_block': state['live_block'],
        'faults': state['faults']
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)