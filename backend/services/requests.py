from flask import jsonify


def ok_response(data, code=200):
    return jsonify(data), code
