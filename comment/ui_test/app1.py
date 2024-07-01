from flask import Flask, json, request, render_template, jsonify, redirect, url_for 
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, parent_dir)
from recon import recon
from exploitation import exploitation 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.form
    end_points = data.get('endpoints').split('\n')
    selected_recon = data.get('recon')
    nuclei=data.get('nuclei')    
    sqlmap=data.get('sqlmap')
    lfi=data.get('lfi')
    xsstrike=data.get('xsstrike')
    xspear=data.get('xspear')
    exploit_list=[]
    if nuclei : 
        exploit_list.append(nuclei)
    if lfi : 
        exploit_list.append(lfi)
    if sqlmap : 
        exploit_list.append(sqlmap)
    if xsstrike : 
        exploit_list.append(xsstrike)
    if xspear : 
        exploit_list.append(xspear)
    # my_recon=recon(end_points,selected_recon)
    my_threads = {'xsstrike': "xsstrike", 'xspear': "xspear", 'lfi': 50, 'sqlmap': 10, 'nuclei': 5}
    my_delays = {'xsstrike1': 5, 'xspear1': 5, 'lfi1': 0, 'sqlmap1': 5, 'nuclei1': 10}
    # my_exploit=exploitation(my_recon.end_point_with_parameter,my_threads,my_delays)
    # my_exploit.exploitation()

    output_file = f'output/{selected_recon}_results.json'
    with open(output_file, 'w') as f:
        json.dump({'recon': my_threads, 'exploit': my_delays}, f)
    
    return redirect(url_for('results', scan_type=selected_recon, filename=f'{selected_recon}_results.json'))

@app.route('/results/<scan_type>/<filename>')
def results(scan_type, filename):
    with open(f'output/{filename}', 'r') as f:
        results = json.load(f)
    return render_template('results.html', results=results, scan_type=scan_type)

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    app.run(debug=True)