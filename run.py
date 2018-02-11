from flask import Flask, render_template, request, jsonify, make_response
import uuid
import json

from helpers import convert_to_normal_dict, get_files

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ip')
def get_ip():
    return jsonify(origin=request.remote_addr)


@app.route('/uuid')
def get_uuid():
    return jsonify(uuid=str(uuid.uuid4()))


@app.route('/user-agent')
def view_user_agent():
    return jsonify(user_agent=request.headers.get('User-Agent'))


@app.route('/headers')
def get_headers():
    return jsonify(
        dict(args=convert_to_normal_dict(request.args), headers=dict(request.headers), origin=request.remote_addr,
             url=request.url))


@app.route('/get')
def view_get():
    """
        args = request.args ImmutableMultiDict
        headers = request.headers   EnvironHeaders
    :return:
    """
    return jsonify(
        dict(args=convert_to_normal_dict(request.args), headers=dict(request.headers), origin=request.remote_addr,
             url=request.url))


@app.route('/post', methods=['POST'])
def view_post():
    return jsonify(
        args=convert_to_normal_dict(request.args),
        data=json.dumps(request.json),
        files=get_files(),
        form=request.form,
        headers=dict(request.headers),
        json=request.json,
        origin=request.remote_addr,
        url=request.url)


@app.route('/anything')
def view_anything():
    headers = dict(request.headers)
    headers['Referer'] = request.referrer
    return jsonify(
        args=convert_to_normal_dict(request.args),
        data=json.dumps(request.json),
        files=get_files(),
        form=request.form,
        headers=headers,
        json=request.json,
        method=request.method,
        origin=request.remote_addr,
        url=request.url)


@app.route('/encoding/utf8')
def view_encoding():
    with open('utf8-demo.txt', 'r', encoding='utf8') as f:
        txt = f.read()
    resp = make_response(txt)
    return txt


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)