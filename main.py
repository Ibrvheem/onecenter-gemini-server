import sys
sys.dont_write_bytecode = True

from app import app

@app.get("/")
def index():
    return {'name':"onecenter", 'version':"0.0.1", 'status':"OK"}

@app.get('/health')
def health():
    # TODO do some checks here to confirm everything works
    return {'status':'OK'}, 200

if __name__ == '__main__':
    app.run(debug=True)