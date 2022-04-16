from app import app


@app.route('/')
def index():
    return 'Aqui vai ser o index'