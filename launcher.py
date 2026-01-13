import subprocess
import sys
import time
import os

def get_user_config():
    """Interactively ask user for configuration with validation."""
    while True:
        print("\n" + "="*40)
        print("   🌱 KUDZU BFT SIMULATOR SETUP   ")
        print("="*40)
        
        try:
            # Get inputs with defaults
            n_input = input("Enter Total Nodes (N) [Press Enter for 7]: ").strip()
            N = int(n_input) if n_input else 7
            
            f_input = input("Enter Byzantine Faults (f) [Press Enter for 1]: ").strip()
            F = int(f_input) if f_input else 1
            
            p_input = input("Enter Passive/Slow Nodes (p) [Press Enter for 1]: ").strip()
            P = int(p_input) if p_input else 1
            
            # THE KUDZU FORMULA CHECK: n >= 3f + 2p + 1
            min_required = (3 * F) + (2 * P) + 1
            
            if N < min_required:
                print(f"\n❌ INVALID CONFIGURATION!")
                print(f"   For f={F} and p={P}, you need at least {min_required} nodes.")
                print(f"   Current N={N} is too small.")
                print(f"   Formula: N >= 3f + 2p + 1")
                print("   Please try again.\n")
                continue
                
            print(f"\n✅ Configuration Accepted: N={N}, f={F}, p={P}")
            return N, F, P
            
        except ValueError:
            print("❌ Error: Please enter valid integers.")

# --- MAIN EXECUTION ---

# 1. Get Configuration
N, F, P = get_user_config()

print(f"\n--- STARTING KUDZU BFT SIMULATION (N={N}, F={F}, P={P}) ---")

# 2. Start Coordinator
print("1. Launching Coordinator...")
# Pass the user's config to the Coordinator
coord = subprocess.Popen([
    sys.executable, "-m", "core.coordinator",
    "--n", str(N), "--f", str(F), "--p", str(P)
])
time.sleep(2)

# 3. Start Replicas
print(f"2. Launching {N} Replicas...")
procs = []
for i in range(N):
    p = subprocess.Popen([
        sys.executable, "-m", "core.replica",
        "--id", str(i), 
        "--n", str(N), 
        "--f", str(F), 
        "--p", str(P)
    ])
    procs.append(p)
    # Stagger slightly to prevent socket race conditions
    time.sleep(0.1)

# 4. Start Dashboard
print("3. Launching Dashboard...")
dash = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "ui/dashboard.py"])

print("\n✅ SYSTEM ONLINE")
print("   -> Dashboard: http://localhost:8501")
print("   -> Press Ctrl+C to stop")

try:
    coord.wait()
except KeyboardInterrupt:
    print("\nStopping...")
    coord.terminate()
    dash.terminate()
    for p in procs: p.terminate()