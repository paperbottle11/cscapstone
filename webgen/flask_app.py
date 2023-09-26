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
                return send_from_directory("gen", "gen.html")
            except:
                return redirect('/origin')
        else: 
            print("generating")
            html, css, js = generate(request.args["q"])
            insertIdx = html.find("<body>")
            html = html[:insertIdx+6] + "\n<a id=\"home\" href=\"/origin\">Home</a>\n" + html[insertIdx+6:]
            css = "#home {\ndisplay: block;\npadding: 10px 20px;\ntext-decoration: none;\nborder-radius: 5px;\nborder-style: solid;\nborder-width: 1px;\nfont-weight: bold;\nbackground-color: #ddd;\ncolor: black;\nfloat: left;\n}\n#home:hover {\nbackground-color: #555;\ncolor: white;\n}\n" + css
            with open("gen/gen.html", "w") as f:
                f.write(html)
                f.close()
            with open("gen/gen.css", "w") as f:
                f.write(css)
                f.close()
            with open("gen/gen.js", "w") as f:
                f.write(js)
                f.close()
            print("serving generated site")
            lastQuery = request.args["q"]
            return send_from_directory("gen", "gen.html")
    return send_from_directory(app.static_folder, path="index.html")

@app.route('/gen/<path:filename>')
def gen_assets(filename):
    return send_from_directory("gen", filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)