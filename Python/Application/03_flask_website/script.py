from flask import Flask,render_template,request,make_response,session
from werkzeug import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/files'
@app.route("/")
def home():
    session["test"] = "anyvalue"
    if 'checks' in request.cookies:
        val = request.cookies.get("checks")
    else:
        val = "done"
    return render_template("home.html",name=val)
app.add_url_rule("/","index",home)

@app.route("/about/",methods=['POST','GET'])
def about():

    if request.method == 'POST':
        """ username = request.form['firstname']
        password = request.form['lastname']
        dct = {'User': username,'Pass' : password } """
        ses_val = session["test"]
        f = request.files['file1']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        res = make_response(render_template('about.html',name=[request.form,ses_val]))
        any = "other"
        res.set_cookie("checks",value=any,max_age=60*60*24*365*2)
        return res
    else:
        username = request.args.get('firstname')
        password = request.args.get('lastname')
        dct = {'User': username,'Pass' : password }
        res = make_response()
        any = "other"
        res.set_cookie("check",value=any)
        return render_template('about.html',name=dct)


if __name__ == "__main__":

    app.secret_key = os.urandom(24)
    app.run(debug=True)
