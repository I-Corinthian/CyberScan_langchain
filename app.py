import streamlit as st
import time
import re
import subprocess
import shutil
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    instruction: str
    target: str
    results: List[str]
    errors: List[str]
    tasks: List[dict]
    allowed_domains: List[str]

def breakdown_task(state: AgentState) -> AgentState:
    targets = re.findall(r'\b[\w.-]+\.[a-z]{2,}\b', state["instruction"])
    target = targets[0] if targets else "unknown"
    state["target"] = target
    state["results"].append(f"Task breakdown: target is {target}")
    state["tasks"] = [
        {"tool": "validate", "target": target},
        {"tool": "nmap", "target": target},
        {"tool": "gobuster", "target": target},
        {"tool": "ffuf", "target": target},
        {"tool": "final_report", "target": target}
    ]
    return state

def validate_node(state: AgentState) -> AgentState:
    allowed_scope = state.get("allowed_domains", [])
    target = state["target"]
    if allowed_scope:
        if any(scope.strip() in target for scope in allowed_scope):
            state["results"].append(f"Validation: {target} is within allowed scope.")
        else:
            state["errors"].append(f"Validation error: {target} is out of allowed scope.")
    else:
        state["results"].append(f"No allowed domain restrictions provided. Proceeding with {target}.")
    return state

def nmap_node(state: AgentState) -> AgentState:
    target = state["target"]
    st.info(f"Running nmap scan on {target}...")
    if shutil.which("nmap") is None:
        state["errors"].append("nmap not found. Please install nmap.")
        return state
    cmd = ["nmap", "-Pn", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        state["results"].append(f"nmap scan on {target}:\n{output.strip()}")
    except Exception as e:
        state["errors"].append(f"nmap scan failed: {str(e)}")
    return state

def gobuster_node(state: AgentState) -> AgentState:
    target = state["target"]
    st.info(f"Running gobuster scan on {target}...")
    if shutil.which("gobuster") is None:
        state["errors"].append("gobuster not found. Please install gobuster.")
        return state

    cmd = ["gobuster", "-u", f"http://{target}", "-w", "common.txt"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        state["results"].append(f"gobuster scan on {target}:\n{output.strip()}")
    except Exception as e:
        state["errors"].append(f"gobuster scan failed: {str(e)}")
    return state

def ffuf_node(state: AgentState) -> AgentState:
    target = state["target"]
    st.info(f"Running ffuf scan on {target}...")
    if shutil.which("ffuf") is None:
        state["errors"].append("ffuf not found. Please install ffuf.")
        return state
    cmd = ["ffuf", "-u", f"http://{target}/FUZZ", "-w", "common.txt"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        state["results"].append(f"ffuf scan on {target}:\n{output.strip()}")
    except Exception as e:
        state["errors"].append(f"ffuf scan failed: {str(e)}")
    return state

def final_report_node(state: AgentState) -> AgentState:
    report = "### Final Report\n\n**Results:**\n" + "\n".join(state["results"])
    if state["errors"]:
        report += "\n\n**Errors:**\n" + "\n".join(state["errors"])
    state["results"].append(report)
    return state

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("breakdown", breakdown_task)
    graph.add_node("validate", validate_node)
    graph.add_node("nmap", nmap_node)
    graph.add_node("gobuster", gobuster_node)
    graph.add_node("ffuf", ffuf_node)
    graph.add_node("final", final_report_node)
    
    graph.set_entry_point("breakdown")
    graph.add_edge("breakdown", "validate")
    graph.add_edge("validate", "nmap")
    graph.add_edge("nmap", "gobuster")
    graph.add_edge("gobuster", "ffuf")
    graph.add_edge("ffuf", "final")
    
    return graph.compile()

def main():
    st.title("LangGraph-based Agentic Cybersecurity Pipeline")
    
    instruction = st.text_input(
        "Enter a security task instruction:",
        "Scan google.com for open ports and discover directories"
    )
    allowed_domains_input = st.text_input(
        "Enter allowed domains (comma-separated). Leave empty for no restrictions:",
        ""
    )
    
    if st.button("Run Pipeline"):
        allowed_domains = [d.strip() for d in allowed_domains_input.split(",") if d.strip()]
        
        state: AgentState = {
            "instruction": instruction,
            "target": "",
            "results": [],
            "errors": [],
            "tasks": [],
            "allowed_domains": allowed_domains  
        }
        graph = build_graph()
        final_state = graph.invoke(state)
        
        st.success("Pipeline execution finished.")
        st.markdown("## Pipeline Results")
        
        # Format results with headings and code blocks
        formatted_results = ""
        for idx, res in enumerate(final_state["results"], start=1):
            formatted_results += f"**Result {idx}:**\n```\n{res}\n```\n\n"
        st.markdown(formatted_results)
        
        if final_state["errors"]:
            st.error("### Errors encountered:")
            formatted_errors = ""
            for idx, err in enumerate(final_state["errors"], start=1):
                formatted_errors += f"**Error {idx}:**\n```\n{err}\n```\n\n"
            st.markdown(formatted_errors)

if __name__ == "__main__":
    main()
