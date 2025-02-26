# CyberScan_langchain

```markdown
# LangGraph-based Agentic Cybersecurity Pipeline

A modular, agentic cybersecurity pipeline built using [LangGraph](https://github.com/langgraph/langgraph) and Streamlit. This project takes a high-level security instruction, breaks it into actionable tasks, and then executes various security scans (using tools like nmap, gobuster, and ffuf) to generate a comprehensive report.

## Features

- **Task Breakdown:** Extracts target information from a given security instruction.
- **Validation:** Checks whether the target is within allowed domains (if specified).
- **Network Scanning:** Uses **nmap** to scan for open ports.
- **Directory Enumeration:** Uses **gobuster** to enumerate directories.
- **Fuzzing:** Uses **ffuf** to perform fuzz testing on the target.
- **Reporting:** Compiles the results and any errors into a final report.
- **User Interface:** A clean Streamlit-based web UI for interacting with the pipeline.

## Prerequisites

### Python Dependencies

- Python 3.7 or later
- [Streamlit](https://streamlit.io/)
- [LangGraph](https://github.com/langgraph/langgraph)
- Other dependencies as listed in the [`requirements.txt`](requirements.txt) file.

You can install the Python dependencies via pip:

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


