import hashlib
from reedsolo import RSCodec

class MerkleTree:
    def __init__(self, data_fragments):
        self.leaves = [self._hash(f) for f in data_fragments]
        self.tree = self._build_tree(self.leaves)
        self.root = self.tree[-1][0]

    def _hash(self, data):
        if isinstance(data, str): data = data.encode()
        return hashlib.sha256(data).hexdigest()

    def _build_tree(self, leaves):
        tree = [leaves]
        current_level = leaves
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if i+1 < len(current_level) else left
                combined = self._hash(left + right)
                next_level.append(combined)
            tree.append(next_level)
            current_level = next_level
        return tree

    def get_proof(self, index):
        proof = []
        for level in self.tree[:-1]:
            is_right_node = index % 2 == 1
            sibling_index = index - 1 if is_right_node else index + 1
            node = level[sibling_index] if sibling_index < len(level) else level[index]
            proof.append(node)
            index //= 2
        return proof

    @staticmethod
    def verify_proof(fragment, proof, root, index):
        current_hash = hashlib.sha256(fragment if isinstance(fragment, bytes) else fragment.encode()).hexdigest()
        for sibling_hash in proof:
            if index % 2 == 1:
                current_hash = hashlib.sha256((sibling_hash + current_hash).encode()).hexdigest()
            else:
                current_hash = hashlib.sha256((current_hash + sibling_hash).encode()).hexdigest()
            index //= 2
        return current_hash == root

# PARALLEL WORKER FUNCTIONS (Must be top-level)
def worker_encode(data_bytes, n, k):
    try:
        rsc = RSCodec(n - k)
        encoded = rsc.encode(data_bytes)
        chunk_size = (len(encoded) + n - 1) // n
        fragments = [encoded[i:i + chunk_size] for i in range(0, len(encoded), chunk_size)]
        while len(fragments) < n: fragments.append(b'')
        fragments = fragments[:n]
        mt = MerkleTree(fragments)
        return fragments, mt.root, [mt.get_proof(i) for i in range(n)]
    except:
        return None, None, None