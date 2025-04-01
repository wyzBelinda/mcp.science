# Python Code Execution Service

This repository provides a secure sandboxed environment for executing Python code with controlled resource usage. The system is designed to safely execute untrusted Python code while preventing potential security risks.

## Overview

The Python Code Execution Service consists of several components:

1. **FastMCP Server** (`fastmcp.py`) - An API server that receives code execution requests
2. **Code Execution Tool** (`python_code_execution` tool) - Processes requests and invokes the secure execution environment
3. **Safe Execution Script** (`safe_execute.py`) - Command-line interface for the secure execution environment
4. **Local Python Executor** (`local_python_executor.py`) - Core module that handles the sandboxed code execution. It is adopted from [smolagents](https://github.com/huggingface/smolagents/blob/main/src/smolagents/local_python_executor.py) with added security
5. **Printing and Logging** Encourages the LLM to print their results

## Features

- **Sandbox Security**: Executes code in a secure environment with strict limitations
- **Resource Management**: Controls CPU time and memory usage to prevent resource abuse
- **Allowed Imports**: Restricts module imports to a predefined safe list
- **Error Handling**: Captures and provides informative error messages

## Usage

### Command Line

```bash
python src/core/code_act/safe_execute.py --code 'print("Hello, world!")'
```

#### Options:
- `--code` (required): Python code to evaluate
- `--authorized-imports`: List of authorized Python modules (defaults to a safe set)
- `--max-print-length`: Maximum length of print outputs
- `--max-memory-mb`: Maximum memory usage in MB (default: 20)
- `--max-cpu-time-sec`: Maximum CPU time in seconds (default: 15)

### API Server

The system also provides an API server for code execution requests:

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

mcp = FastMCP("python_code_execution")

@mcp.tool()
async def python_code_execution(code: str) -> TextContent:
    # Tool implementation that calls safe_execute.py
    ...
```

## Security Considerations

This service implements multiple security layers:

1. **No File Access**: Prevents reading or writing to the file system
2. **No Network Access**: Blocks all network operations
3. **Memory Limits**: Prevents memory-based denial of service attacks
4. **CPU Time Limits**: Prevents infinite loops and computation-based attacks
5. **Import Restrictions**: Only allows trusted modules to be imported

## Implementation Notes

The core execution functionality (`local_python_executor.py`) is adapted from OpenAI's code_interpreter implementation, with additional safety measures for memory and CPU time limitations.

## Limitations

- Only standard library modules from the allowed list can be imported
- Code execution is limited to 15 seconds by default
- Memory usage is restricted to 20MB by default
- No file system access or network operations are permitted
- Dynamic code execution (eval, exec) is not allowed

## Example

```python
# Example code that can be executed
import math
import statistics

data = [12, 15, 18, 22, 13, 17, 16]
mean = statistics.mean(data)
median = statistics.median(data)
print(f"Mean: {mean}, Median: {median}")
```