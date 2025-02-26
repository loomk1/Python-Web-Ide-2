from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Web IDE</title>
    <style>
        body { font-family: 'Inter', sans-serif; margin: 0; padding: 20px; background-color: #0d1117; text-align: center; color: #c9d1d9; }
        .container { max-width: 750px; margin: auto; padding: 20px; background: #161b22; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); border-radius: 12px; }
        textarea, input { width: 100%; border: none; border-radius: 8px; padding: 12px; font-size: 14px; margin-bottom: 10px; background: #21262d; color: #f8f8f2; outline: none; }
        textarea { height: 200px; resize: vertical; }
        button { padding: 12px 15px; background-color: #238636; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; width: 100%; font-weight: bold; transition: 0.3s; }
        button:hover { background-color: #2ea043; }
        pre { background: #0d1117; padding: 15px; white-space: pre-wrap; word-wrap: break-word; border-radius: 8px; font-size: 14px; text-align: left; color: #f0f6fc; border: 1px solid #30363d; }
        h2, h3 { color: #58a6ff; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Python Web IDE</h2>
        <form method="post">
            <textarea name="code" placeholder="Write your Python code here...">{{ code }}</textarea>
            <button type="submit">Run Code</button>
        </form>
        {% if output %}
            <h3>Output:</h3>
            <pre>{{ output }}</pre>
        {% endif %}
        <h3>Terminal</h3>
        <form method="post">
            <input type="text" name="command" placeholder="Enter terminal command">
            <button type="submit" name="run_command">Run Command</button>
        </form>
        {% if terminal_output %}
            <pre>{{ terminal_output }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    output = ""
    terminal_output = ""
    
    if request.method == "POST":
        if "code" in request.form:
            code = request.form.get("code", "")
            try:
                output = subprocess.check_output(["python3", "-c", code], stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output
        elif "command" in request.form:
            command = request.form.get("command", "")
            try:
                terminal_output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                terminal_output = e.output
    
    return render_template_string(TEMPLATE, code=code, output=output, terminal_output=terminal_output)

if __name__ == "__main__":
    app.run(debug=True)