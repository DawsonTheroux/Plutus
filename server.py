import os
import json

from flask import Flask, render_template, send_from_directory, request
import plotly.express as px
import plotly.io as pio

CONF_DIR = "conf/"
app = Flask(__name__, static_folder='static', template_folder="public")

@app.route('/')
def index():
    conf_file_data = {}

    for conf_file in os.listdir(CONF_DIR):
        conf_filepath = os.path.join(CONF_DIR, conf_file)
        if conf_file == "default.json":
            continue;
        if os.path.isfile(conf_filepath):
            with open(conf_filepath, 'r') as open_file:
                conf_file_data[conf_file.split(".")[0]] = open_file.read()

    return render_template('index.html', conf_file_data=conf_file_data)

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    conf_name = request.args.get('config')
    if request.method == 'GET':
        conf_filepath = os.path.join(CONF_DIR, f"{conf_name}.json")
        config = ""

        # If the config file doesn't exist, then create it using the default config.
        if not os.path.isfile(conf_filepath):
            with open(os.path.join(CONF_DIR, "default.json"), 'r') as open_file:
                config = open_file.read()
            with open(os.path.join(CONF_DIR, f"{conf_name}.json"), 'w') as open_file:
                open_file.write(config)
        else:
            with open(conf_filepath, 'r') as open_file:
                config = open_file.read()

        return render_template('modify.html', conf_name=conf_name, config_string=config)

    if request.method == 'POST':
        modified_config = request.get_json()
        if modified_config:
            with open(os.path.join(CONF_DIR, f"{conf_name}.json"), 'w') as open_file:
                open_file.write(json.dumps(modified_config))
            return "File upload successful!", 200

# Next up is adding the file upload functionality and handling the plutus object to generate the report.
I am here
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    conf_name = request.args('config')

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        pass


if __name__ == '__main__':
    app.run(debug=True, port=8080)
