from flask import Flask, render_template, request
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

import subprocess
import sys
from io import StringIO

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']

    language, _, code = command.partition(':')
    code = code.strip()

    result = ''

    if language == 'R':
        # Execute R code using the subprocess module
        result = subprocess.check_output(['C:/Program Files/R/R-4.2.0/bin/x64/R.exe', '--slave', '-e', code], stderr=subprocess.STDOUT, text=True)
    elif language == 'Julia':
        # Execute Julia code using the subprocess module
        result = subprocess.check_output(['julia', '-e', code], stderr=subprocess.STDOUT, text=True)
    elif language == 'Python':
        # Execute Python code and capture the standard output
        try:
            temp_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            exec(code)
            sys.stdout = temp_stdout
            result = captured_output.getvalue()
        except Exception as e:
            result = str(e)
    elif language == 'Shell':
        # Execute shell command using the subprocess module
        result = subprocess.run(code, shell=True, capture_output=True, text=True).stdout
#     with open('history.txt', 'a') as history_file:
#         history_file.write(f'{command}\n')
#         history_file.write(result)
#         history_file.write('\n')
    return result



if __name__ == '__main__':
    app.run(debug=True)
