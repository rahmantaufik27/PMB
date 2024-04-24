from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hellow World<style>body { display: flex; align-items: center; justify-content: center; height: 100vh; }</style>'

if __name__ == "__main__":
    app.run()

