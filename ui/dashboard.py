import streamlit as st
import requests
import time

st.set_page_config(layout="wide", page_title="Kudzu Dynamic Dashboard")
st.title("🌱 Kudzu BFT: Scalable Simulator")

COORD = "http://127.0.0.1:5000"

try:
    # 1. Fetch System Configuration
    data = requests.get(f"{COORD}/metrics", timeout=0.5).json()
    config = data['config']
    metrics = data['metrics']
    live = data['live_block']
    faults = data['faults']
    
    N = config['n']
    F = config['f']
    P = config['p']
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.header(f"Network: {N} Nodes")
        st.info(f"Configuration:\nN={N} | F={F} | P={P}")
        
        if st.button("🚀 Inject Block", type="primary"):
            try: requests.post(f"{COORD}/inject_block")
            except: pass
        
        st.divider()
        st.subheader("Fault Injection")
        # Dynamic Target Input (0 to N-1)
        target = st.number_input("Target Node", 0, N-1, 0)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💀 Kill"):
                requests.post(f"{COORD}/fault", json={'target': target, 'params': {'drop': 1.0, 'delay': 0}})
        with c2:
            if st.button("✅ Reset"):
                requests.post(f"{COORD}/fault", json={'target': target, 'params': {'drop': 0.0, 'delay': 0}})

    # --- MAIN VIEW ---
    
    # 1. Feasibility Engine (Dynamic Math)
    st.subheader("System Feasibility")
    dead_nodes = sum(1 for s in faults.values() if s == "DEAD")
    active_nodes = N - dead_nodes
    
    fast_req = N - P
    slow_req = N - F - P
    
    if active_nodes >= fast_req:
        status = "✅ OPTIMAL"
        pred = "Fast Path"
        col = "green"
    elif active_nodes >= slow_req:
        status = "⚠️ DEGRADED"
        pred = "Slow Path"
        col = "orange"
    else:
        status = "❌ FAILED"
        pred = "IMPOSSIBLE"
        col = "red"
        
    c1, c2, c3 = st.columns(3)
    c1.metric("Active / Total", f"{active_nodes} / {N}")
    c2.markdown(f"**Status:** :{col}[{status}]")
    c3.metric("Prediction", pred)
    
    st.divider()
    
    # 2. Dynamic Lifecycle Visualization
    st.subheader("Block Lifecycle")
    with st.container(border=True):
        st.markdown(f"**Block ID:** `{live['id']}` | **Status:** `{live['status']}` | **Leader:** Node `{live['leader']}`")
        
        st.write("### Dispersal")
        # DYNAMIC COLUMNS: Creates exactly N boxes
        cols = st.columns(N)
        for i in range(N):
            status = faults.get(str(i), "HEALTHY")
            if status == "DEAD":
                bg, icon = "#444", "💀"
            elif i in live['fragments']:
                bg, icon = "#4CAF50", "📦"
            else:
                bg, icon = "#333", "..."
            
            border = "2px solid yellow" if i == live['leader'] else "none"
            
            # Use HTML for better scaling with many nodes
            cols[i].markdown(
                f'<div style="background:{bg};padding:5px;text-align:center;border-radius:4px;border:{border};font-size:12px">{i}<br>{icon}</div>', 
                unsafe_allow_html=True
            )
            
        st.write("### Voting")
        v_cols = st.columns(N)
        for i in range(N):
            icon = "✅" if i in live['votes'] else "⏳"
            v_cols[i].caption(f"{icon}")

    st.divider()
    m1, m2 = st.columns(2)
    m1.metric("Total Finalized", metrics['finalized'])
    m2.metric("Fast Path", metrics['fast_path'])

except Exception as e:
    st.warning("Connecting to Coordinator...")

time.sleep(1)
st.rerun()