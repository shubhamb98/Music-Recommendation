from flask import Flask,redirect, url_for, request,render_template
import pandas as pd
app = Flask(__name__)
import functions

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method== 'POST':
        user_id=request.form['user_id']
        return redirect(url_for('pop_rmd',user_id=user_id))
    return render_template('index.html', result=functions.song_df['user_id'].unique())

@app.route('/pop_rec/<user_id>')
def pop_rmd(user_id):
    x=functions.popularity_based()
    return render_template('pop_rmd.html',  tables=x,show_table=1,user_id=user_id)

@app.route('/user_rec_ip',methods=['GET','POST'])
def user_rec_ip():
    if request.method== 'POST':
        user_id=request.form['user_id']
        return redirect(url_for('user_rec',user_id=user_id))
    return render_template('user_rec_ip.html', result=functions.song_df['user_id'].unique())

@app.route('/user_rec/<user_id>')
def user_rec(user_id):
    x=functions.item_similarity(user_id)
    return render_template('user_rec.html', tables=x, show_table=1,user_id=user_id)

@app.route('/song_rec_ip',methods=['GET','POST'])
def song_rec_ip():
    if request.method== 'POST':
        song=request.form['song']
        return redirect(url_for('song_rec',song=song))
    return render_template('song_rec_ip.html', result=functions.song_df['song'].unique())

@app.route('/song_rec/<song>')
def song_rec(song):
    print(song)
    print(type(song))
    x=functions.similar_songs(song)
    return render_template('song_rec.html', tables=x, show_table=1,song=song)

if __name__ == '__main__':
    app.run(debug=False)
