from flask import Flask, request, render_template, jsonify
import subprocess
import shlex

app = Flask(__name__)

def run_command(command):
    try:
        result = subprocess.run(shlex.split(command), capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deploy', methods=['POST'])
def deploy_cluster():
    cluster_name = request.form['cluster_name']
    memory = request.form['memory']
    cpus = request.form['cpus']
    driver = request.form['driver']
    command = f"minikube start --name {cluster_name} --memory {memory} --cpus {cpus} --driver={driver}"
    output = run_command(command)
    return jsonify({'output': output})

@app.route('/delete', methods=['POST'])
def delete_cluster():
    cluster_name = request.form['cluster_name']
    command = f"minikube delete --name {cluster_name}"
    output = run_command(command)
    return jsonify({'output': output})

@app.route('/status', methods=['POST'])
def status_cluster():
    cluster_name = request.form['cluster_name']
    command = f"minikube status --name {cluster_name}"
    output = run_command(command)
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
