from flask import Response, jsonify

from app import create_app

app = create_app()

@app.route('/')
def index():
    return jsonify({'message': 'Hello World'})

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
