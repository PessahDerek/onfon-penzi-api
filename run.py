from flask import jsonify

from app import create_app, AuthMiddleware

app = create_app()

# app.wsgi_app = AuthMiddleware(app.wsgi_app)

@app.route('/')
def index():
    return jsonify({'message': 'Hello World'})


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
