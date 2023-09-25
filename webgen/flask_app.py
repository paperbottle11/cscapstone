from flask import Flask, send_from_directory, redirect, request, render_template
from generate import generate

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return redirect('/origin')

global lastQuery
lastQuery = ""

@app.route('/origin', methods=['GET'])
def home():
    global lastQuery
    if request.method == 'GET' and "q" in request.args:
        if request.args["q"] == "": return redirect('/origin')
        elif request.args["q"] == lastQuery: 
            print("serving lastQuery")
            try:
                return send_from_directory(app.root_path, path='gen.html')
            except:
                return redirect('/origin')
        else: 
            print("generating")
            lastQuery = request.args["q"]
            html = generate(lastQuery)
            with open("gen.html", "w") as f:
                f.write(html)
                f.close()
            print("serving generated site")
            return send_from_directory(app.root_path, path='gen.html')
    return send_from_directory(app.static_folder, path='index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)