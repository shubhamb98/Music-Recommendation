from flask import Flask,redirect, url_for, request,render_template

app = Flask(__name__)
import functions

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method== 'POST':
        asd=request.form['user_id']
        print(asd)
    return render_template('index.html', result=functions.song_df['user_id'].unique())

#@app.route()

if __name__ == '__main__':
    app.run(debug=True)
