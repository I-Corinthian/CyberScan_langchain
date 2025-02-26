# CyberScan_langchain

```markdown
# LangGraph-based Agentic Cybersecurity Pipeline

A modular, agentic cybersecurity pipeline built using [LangGraph](https://github.com/langgraph/langgraph) and Streamlit. This project takes a high-level security instruction, breaks it into actionable tasks, and then executes various security scans (using tools like nmap, gobuster, and ffuf) to generate a comprehensive report.

## Table of Contents

- [Features](#features)
- [System Design](#system-design)
- [Benchmarks](#benchmarks)
- [Limitations](#limitations)
- [Potential Improvements](#potential-improvements)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Features

- **Task Breakdown:** Extracts target information from a given security instruction.
- **Validation:** Checks whether the target is within allowed domains (if specified).
- **Network Scanning:** Uses **nmap** to scan for open ports.
- **Directory Enumeration:** Uses **gobuster** to enumerate directories.
- **Fuzzing:** Uses **ffuf** to perform fuzz testing on the target.
- **Reporting:** Compiles the results and any errors into a final report.
- **User Interface:** A clean Streamlit-based web UI for interacting with the pipeline.

## System Design

This pipeline is built using a graph-based architecture powered by LangGraph. The design consists of the following nodes:

- **Breakdown Node:** Parses the input instruction to extract the target domain.
- **Validation Node:** Validates the target against allowed domain restrictions.
- **Nmap Node:** Executes a network scan using nmap.
- **Gobuster Node:** Performs directory enumeration using gobuster.
- **FFUF Node:** Conducts fuzzing tests using ffuf.
- **Final Report Node:** Aggregates results and errors into a final report.

Each node represents a discrete task in the scanning process. The nodes are connected in a sequential manner, ensuring that each step is executed in order, and the results from each are aggregated and presented to the user through a Streamlit interface.

## Benchmarks

Benchmarks are dependent on the target and network conditions. For example, during a test run against **google.com**, typical results were:

- **nmap Scan:** Approximately 11.66 seconds to complete scanning of open ports.
- **gobuster Scan:** Completed within seconds; however, the output depends on the target's response and wildcard handling.
- **ffuf Scan:** Execution time varies based on thread count and target response times.

> **Note:** These benchmarks serve as a rough guide. Actual performance may vary due to network latency, target configuration, and the computational power of the host machine.

## Limitations

- **Synchronous Execution:** The pipeline currently runs synchronously. A long-running scan (such as a detailed nmap scan) can delay the overall process.
- **Error Handling:** While basic error capture is implemented, more granular error categorization and recovery mechanisms could be added.
- **Dependency on External Tools:** The pipeline relies on external command-line tools (nmap, gobuster, ffuf). Their availability and correct configuration in the host environment are crucial.
- **Scalability:** The sequential nature of the pipeline may not be optimal for high-volume or parallel scanning scenarios.
- **Wordlist Dependence:** The quality of directory and fuzzing results is dependent on the provided wordlist (`common.txt`), which may require customization based on the target environment.

## Potential Improvements

- **Asynchronous Execution:** Integrate asynchronous processing to run scans concurrently, reducing overall execution time.
- **Enhanced Error Handling:** Implement more robust error handling and logging, including retry mechanisms and detailed failure diagnostics.
- **Dynamic Pipeline Configuration:** Allow for dynamic branching or conditional task execution based on intermediate results.
- **Improved Output Formatting:** Enhance the reporting module to generate interactive or downloadable reports.
- **Customizable Wordlists:** Provide options for users to select or upload custom wordlists for gobuster and ffuf scans.
- **Integration with Other Tools:** Expand the pipeline by integrating additional security tools or APIs for a more comprehensive analysis.

## Prerequisites

### Python Dependencies

- Python 3.7 or later
- [Streamlit](https://streamlit.io/)
- [LangGraph](https://github.com/langgraph/langgraph)
- Other dependencies as listed in the [`requirements.txt`](requirements.txt) file.

Install the Python dependencies via pip:

```bash
pip install -r requirements.txt
```

### System Dependencies

The pipeline also relies on the following command-line tools, which need to be installed on your system:

- **nmap**
- **gobuster**
- **ffuf**

For Debian/Ubuntu-based systems, you can install them with:

```bash
sudo apt-get update && sudo apt-get install -y nmap gobuster ffuf
```

> **Note:** Ensure that these tools are accessible in your system's PATH.

### Wordlist File

The scanning tools (gobuster and ffuf) require a wordlist file. Create a file named `common.txt` in the project directory. You can use a sample wordlist like:

```txt
admin
administrator
login
user
index
home
dashboard
config
api
images
css
js
uploads
backup
old
test
includes
inc
lib
private
public
assets
static
media
temp
tmp
data
downloads
files
cgi-bin
```

Feel free to modify or expand this wordlist based on your requirements.

## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/cyberscan-langchain.git
   cd cyberscan-langchain
   ```

2. **Install Python and System Dependencies:**  
   Follow the instructions in the [Prerequisites](#prerequisites) section.

3. **Run the Application:**

   Launch the Streamlit app using the following command:

   ```bash
   streamlit run app.py
   ```

4. **Interact with the Pipeline:**  
   - Enter a security task instruction (e.g., "Scan google.com for open ports and discover directories").
   - Optionally, specify allowed domains (comma-separated) to restrict the scan.
   - Click on **Run Pipeline** to execute the scan.
   - View the results and any errors directly in the browser.

## Project Structure

```
├── app.py              # Main application file (Streamlit app)
├── common.txt          # Wordlist file for gobuster and ffuf scans
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```


