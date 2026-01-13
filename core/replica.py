import socket
import threading
import json
import time
import random
import requests
import argparse
from concurrent.futures import ProcessPoolExecutor
from core.crypto import worker_encode, MerkleTree

COORD_URL = "http://127.0.0.1:5000"

class KudzuReplica:
    def __init__(self, replica_id, n, f, p):
        self.id = replica_id
        self.n = n
        self.f = f
        self.p = p
        self.port = 6000 + replica_id
        self.cpu_pool = ProcessPoolExecutor(max_workers=1)
        self.view = 0
        self.votes = {}
        self.finalized = set()
        self.faults = {'delay': 0, 'drop': 0.0}
        self.running = True

    def _send(self, target_id, msg):
        if random.random() < self.faults['drop']: return
        if self.faults['delay'] > 0: time.sleep(self.faults['delay'] / 1000)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect(('127.0.0.1', 6000 + target_id))
            s.sendall(json.dumps(msg).encode())
            s.close()
        except: pass

    def broadcast(self, msg):
        threads = []
        for i in range(self.n):
            if i != self.id:
                t = threading.Thread(target=self._send, args=(i, msg))
                t.start()
                threads.append(t)
        for t in threads: t.join()

    def propose_block(self, view):
        # Leader Logic
        self.view = view
        block_id = f"B{self.view}-{int(time.time())}"
        print(f"[NODE {self.id}] LEADER for View {self.view}. Encoding...")
        
        future = self.cpu_pool.submit(worker_encode, b"DATA_PAYLOAD", self.n, self.n-2)
        fragments, root, proofs = future.result()
        
        if not fragments: return

        # AVID Distribution
        for i in range(self.n):
            msg = {
                'type': 'PROPOSAL', 'bid': block_id, 'view': self.view,
                'root': root, 'frag': list(fragments[i]), 'proof': proofs[i]
            }
            if i == self.id: self.handle_proposal(msg)
            else: self._send(i, msg)

    def handle_proposal(self, msg):
        if not MerkleTree.verify_proof(bytes(msg['frag']), msg['proof'], msg['root'], self.id): return
        
        # Artificial delay for animation
        time.sleep(0.2)
        try:
            requests.post(f"{COORD_URL}/report", json={
                'type': 'FRAGMENT', 'replica_id': self.id, 'block_id': msg['bid']
            })
        except: pass

        vote = {'type': 'VOTE', 'bid': msg['bid'], 'src': self.id}
        self.broadcast(vote)
        self.handle_vote(vote)

    def handle_vote(self, msg):
        bid = msg['bid']
        if bid not in self.votes: self.votes[bid] = set()
        self.votes[bid].add(msg['src'])
        
        if msg['src'] == self.id:
            try: requests.post(f"{COORD_URL}/report", json={'type': 'VOTE', 'replica_id': self.id})
            except: pass
        
        if bid in self.finalized: return

        count = len(self.votes[bid])
        path = None
        
        # DYNAMIC LOGIC
        if count >= (self.n - self.p): path = "FAST"
        elif count >= (self.n - self.f - self.p) and count < (self.n - self.p):
             # In a real system, we would wait for a timeout here.
             # For the simulation visualization, if we hit this number and time passes, it's Slow Path.
             pass 

        if path:
            self.finalized.add(bid)
            print(f"[NODE {self.id}] Finalized {bid} via {path}")
            time.sleep(0.2)
            try:
                requests.post(f"{COORD_URL}/report", json={
                    'type': 'FINALIZED', 'replica_id': self.id, 'path': path
                })
            except: pass

    def run(self):
        requests.post(f"{COORD_URL}/register", json={'id': self.id, 'port': self.port})
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', self.port))
        s.listen(10)
        while self.running:
            try:
                conn, _ = s.accept()
                data = conn.recv(16384)
                if data:
                    msg = json.loads(data.decode())
                    if msg['type'] == 'INJECT': self.propose_block(msg['view'])
                    elif msg['type'] == 'PROPOSAL': self.handle_proposal(msg)
                    elif msg['type'] == 'VOTE': self.handle_vote(msg)
                    elif msg['type'] == 'FAULT': self.faults = msg['params']
            except: pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int); parser.add_argument("--n", type=int, default=7); 
    parser.add_argument("--f", type=int, default=1); parser.add_argument("--p", type=int, default=1)
    args = parser.parse_args()
    KudzuReplica(args.id, args.n, args.f, args.p).run()