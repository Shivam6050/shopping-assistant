import json
import sys


def main():
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)
        data = json.loads(input_data)
    except Exception as e:
        sys.stderr.write(f"Error parsing hook input JSON: {e}\n")
        sys.exit(0)

    # Log incoming payload for transparency
    sys.stderr.write(f"Interception Context: {json.dumps(data)}\n")

    # Find the command string within the input JSON payload
    command_line = ""
    if isinstance(data, dict):
        # Check standard places
        if "CommandLine" in data:
            command_line = data["CommandLine"]
        elif "arguments" in data and isinstance(data["arguments"], dict):
            command_line = data["arguments"].get("CommandLine", "")
        elif "args" in data and isinstance(data["args"], dict):
            command_line = data["args"].get("CommandLine", "")

    # Clean and check
    cmd_lower = command_line.strip().lower()

    # Block destructive commands
    destructive_patterns = ["rm -rf", "rm -f", "rmdir /", "remove-item"]
    for pattern in destructive_patterns:
        if pattern in cmd_lower:
            sys.stderr.write(
                f"Hook Blocked Execution: Destructive command pattern '{pattern}' detected in: '{command_line}'\n"
            )
            sys.exit(2)  # Exit code 2 tells the runner to block tool execution

    # Exit code 0 allows the tool call
    sys.exit(0)


if __name__ == "__main__":
    main()
