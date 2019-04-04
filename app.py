from flask import Flask,redirect, url_for, request,render_template,flash,send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename
import functions,os
import random
current_path=os.getcwd()
UPLOAD_FOLDER = current_path+'/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


print('User Branch YO')

@app.route('/',methods=['GET','POST'])
def index():
    if request.method== 'POST':
        user_id=request.form['user_id']
        return redirect(url_for('pop_rmd',user_id=user_id))
    return render_template('index.html', result=functions.song_df['user_id'].unique())

@app.route('/pop_rec/<user_id>')
def pop_rmd(user_id):
    x=functions.popularity_based()
    saf = functions.song_artist_df_generator(x)
    spotif_res=functions.create_playlist(saf,playlist_name='test'+str(random.randint(1,101)))

    return render_template('pop_rmd.html',  tables=x,show_table=1,user_id=user_id,spotif_res=spotif_res)

@app.route('/user_rec_ip',methods=['GET','POST'])
def user_rec_ip():
    if request.method== 'POST':
        user_id=request.form['user_id']
        return redirect(url_for('user_rec',user_id=user_id))
    return render_template('user_rec_ip.html', result=functions.song_df['user_id'].unique())

@app.route('/user_rec/<user_id>')
def user_rec(user_id):
    x=functions.item_similarity(user_id)
    saf = functions.song_artist_df_generator(x)
    spotif_res = functions.create_playlist(saf, playlist_name='test' + str(random.randint(1, 101)))
    return render_template('user_rec.html', tables=x, show_table=1,user_id=user_id,spotif_res=spotif_res)

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
    saf = functions.song_artist_df_generator(x)
    spotif_res = functions.create_playlist(saf, playlist_name='test' + str(random.randint(1, 101)))
    return render_template('song_rec.html', tables=x, show_table=1,song=song,spotif_res=spotif_res)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    message=None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            message='No file part'
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            message='No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            message='file Uploaded Successfully!'
            filename=str(os.path.splitext(filename)[0])
            return redirect(url_for('song_labels',filename=filename))
    return render_template('upload.html',message=message)

@app.route('/song_labels/<filename>')
def song_labels(filename):
    print(filename)
    x=functions.cnn_model(filename)
    x['rank']=x.index+1
    return render_template('song_labels.html',filename=filename,tables=x,show_table=1)


if __name__ == '__main__':

    app.run(debug=True)
