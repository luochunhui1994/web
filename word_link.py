from flask import Flask,render_template,request,url_for
app = Flask(__name__,static_url_path='',static_folder='./static')
@app.route("/")
def index():

    return render_template("word1.html")

@app.route('/gets',methods=['POST'])
def test():
    s1= request.values.get('test')
    print(s1)
    return  render_template('word2.html',data1=s1)

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.2',port=5000)