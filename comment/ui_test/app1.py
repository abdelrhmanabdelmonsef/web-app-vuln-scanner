from flask import Flask, json, request, render_template, jsonify, redirect, send_from_directory, url_for
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../exploitation'))

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

# Now you can import the module from the parent directory

from lfi import lfi
from api import reporting # type: ignore

app = Flask(__name__)

class Operations:
    @staticmethod
    def get_file_content(file_path):
        with open(file_path, 'r') as file:
            return file.read().splitlines()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    end_points = data.get('endpoints')
    selected_scans = data.get('scans')
    
    errors = []
    reports = {}

    if 'ip_resolving' in selected_scans:
        scan_name='ip_resolving'
    elif 'recon' in selected_scans:
        scan_name="recon"
    
    
    output_file = 'output/results.json'
    with open(output_file, 'w') as f:
        json.dump({'errors': errors, 'reports': reports}, f)
    if scan_name=='recon':
        return jsonify({'redirect': url_for('recon', filename='results.json')})
    elif scan_name=='ip_resolving':
        return jsonify({'redirect': url_for('ip_resolving', filename='results.json')})
    else:
        return jsonify({'error': 'No valid scan selected'}), 400

@app.route('/results/<filename>')
def recon(filename):
    with open(f'output/{filename}', 'r') as f:
        results = json.load(f)
    return render_template('results.html', results=results)

@app.route('/results1/<filename>')
def ip_resolving(filename):
    with open(f'output/{filename}', 'r') as f:
        results = json.load(f)
    return render_template('results1.html', results=results)

@app.route('/results1/data/<path:filename>')
def serve_file(filename):
    return send_from_directory('data', filename)


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    app.run(debug=True)
