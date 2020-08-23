#!/usr/bin/env python3

import connexion

from inform_server import encoder

from flask_cors import CORS

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Inform API'}, pythonic_params=True)
    CORS(app.app)
    app.run(port=8080, debug=True)

