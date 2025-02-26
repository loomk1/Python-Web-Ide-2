from flask import Flask, request, render_template_string, jsonify
import subprocess
import sys

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Web IDE</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/theme/material-darker.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/addon/edit/closebrackets.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/addon/edit/matchbrackets.min.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; margin: 0; padding: 20px; background-color: #1e1e1e; color: #d4d4d4; }
        .container { max-width: 1200px; margin: auto; padding: 20px; background: #252526; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); border-radius: 12px; display: flex; flex-direction: column; align-items: center; }
        .CodeMirror { height: 600px; border-radius: 8px; font-size: 14px; background: #1e1e1e; color: #d4d4d4; }
        .button-container { display: flex; justify-content: space-between; width: 100%; margin-top: 10px; }
        button { padding: 12px 15px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; transition: 0.3s; }
        button:hover { opacity: 0.8; }
        .run-button { background-color: #28a745; color: white; }
        .clear-button { background-color: #dc3545; color: white; }
        .download-button { background-color: #007acc; color: white; }
        .output-container { background: #1e1e1e; padding: 15px; border-radius: 8px; font-size: 14px; text-align: left; color: #d4d4d4; border: 1px solid #3c3c3c; width: 100%; height: 200px; overflow-y: auto; }
        .terminal { background: black; color: green; padding: 15px; border-radius: 8px; width: 100%; height: 250px; overflow-y: auto; margin-top: 10px; }
        h2, h3 { color: #569cd6; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Python Web IDE</h2>
        <form id="code-form">
            <textarea id="code" name="code" placeholder="Write your Python code here..."></textarea>
            <div class="button-container">
                <button type="button" class="run-button" onclick="runCode()">Run Code</button>
                <button type="button" class="clear-button" onclick="clearEditor()">Clear Code</button>
                <button type="button" class="download-button" onclick="downloadCode()">Download</button>
            </div>
        </form>
        <h3>Output</h3>
        <div id="output" class="output-container"></div>
        <h3>Terminal</h3>
        <div id="terminal" class="terminal"></div>
    </div>
    <script>
        var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
            mode: "python",
            theme: "material-darker",
            lineNumbers: true,
            indentUnit: 4,
            matchBrackets: true,
            autoCloseBrackets: true,
            tabSize: 4
        });
        function clearEditor() {
            editor.setValue("");
        }
        function runCode() {
            fetch("/run", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code: editor.getValue() })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("output").innerText = data.output;
                document.getElementById("terminal").innerText = data.output;
            });
        }
        function downloadCode() {
            const blob = new Blob([editor.getValue()], { type: "text/plain" });
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "code.py";
            a.click();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True)