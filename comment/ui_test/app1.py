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
    print(end_points)
    shodan=data.get('recon_shodan')    
    subdomain_enum=data.get('recon_subdomain_enum')
    resolver=data.get('recon_resolver')
    dirsearch=data.get('recon_dirsearch')
    paramspider=data.get('recon_paramspider')
    nmap=data.get('recon_nmap')
    arjun=data.get('recon_arjun')
    recon_list=[]
    if shodan : 
        recon_list.append(shodan)
    if subdomain_enum : 
        recon_list.append(subdomain_enum)
    if resolver : 
        recon_list.append(resolver)
    if dirsearch : 
        recon_list.append(dirsearch)
    if paramspider : 
        recon_list.append(paramspider)
    if nmap : 
        recon_list.append(nmap)
    if arjun : 
        recon_list.append(arjun)
    print(recon_list)

    nuclei=data.get('exploit_nuclei')    
    sqlmap=data.get('exploit_sqlmap')
    lfi=data.get('exploit_lfi')
    xsstrike=data.get('exploit_xsstrike')
    xspear=data.get('exploit_xspear')
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
    print(exploit_list)

    my_recon=recon(end_points[0])
    my_recon.recon(recon_list)
    print(my_recon.endpoint_with_params)

        
    my_recon_reports = my_recon.reports

    my_threads = {'xsstrike': "xsstrike", 'xspear': "xspear", 'lfi': 50, 'sqlmap': 10, 'nuclei': 5}
    my_delays = {'xsstrike1': 5, 'xspear1': 5, 'lfi1': 0, 'sqlmap1': 5, 'nuclei': 10}
    my_exploit=exploitation(my_recon.endpoint_with_params,my_threads,my_delays)
    my_exploit.exploitation(exploit_list)
    my_exploit_reports = my_exploit.reports
    
    print(my_exploit_reports)
    
    output_file = f'output/results.json'
    with open(output_file, 'w') as f:
        json.dump({'recon': my_recon_reports, 'exploit': my_exploit_reports}, f)
    
    return redirect(url_for('results', filename='results.json'))


@app.route('/results/<filename>')
def results( filename):
    with open(f'output/{filename}', 'r') as f:
        results = json.load(f)
    return render_template('results.html', results=results)

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    app.run(debug=True)