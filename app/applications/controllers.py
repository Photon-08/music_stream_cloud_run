from flask import Flask, render_template, request, redirect, session
from flask import current_app as app
from applications.models import User, Admin, Music, album, flag_user, music_rating, block_music
from .database import db
from werkzeug.utils import secure_filename
import os
from sqlalchemy import text
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import flask
import ast




app.secret_key = 'BAD_SECRET_KEY'
def viz():
    #for creating data visualization
    all_songs = Music.query.all()
    artist_list = []
    song_list = []
    genre_list = []

    for song in all_songs:
        song_list.append(song.Name)
    print(song_list)

    for song in all_songs:
        artist_list.append(song.Artist)

    for song in all_songs:
        genre_list.append(song.Genre)


    sns.set_theme()
    ax = sns.histplot(artist_list)
    ax = ax.set(xlabel='Artist Names', ylabel='Count', title="Histogram of Artists")
    plt.savefig('static/charts/artist_plot.png')
    plt.clf() 

    
    ax = sns.histplot(genre_list)
    ax = ax.set(xlabel='Genre', ylabel='Count', title="Histogram of Genre")
    plt.savefig('static/charts/genre_plot.png')
    plt.clf()


        
    """
    sns.set_theme()
    ax = sns.histplot(artist_list)
    ax = ax.set(xlabel='Artist Names', ylabel='Count', title="Histogram of Artists")
    plt.savefig('static/charts/artist_plot.png')
    plt.clf() 
    """

    """
    sns.histplot(genre_list)
    plt.savefig('static/charts/genre_plot.png')
    plt.clf()
    """


    all_users = User.query.all()
    print("$$$$$$$$$$$$$$$$$$$$$$$")
    print(all_users, len(all_users))
    print("$$$$$$$$$$$$$$$$$$$$$$$")

    num_user = len(all_users)
    # Set the total number of users
    total_users = num_user

    all_songs = Music.query.all()
    num_play = {}

    for items in all_songs:
        num_play[items.Name] = items.play_count
    
    song_names = list(num_play.keys())
    song_play_num = list(num_play.values())

    ax = sns.barplot(x=song_names,y=song_play_num)
    ax = ax.set(xlabel='Song Names', ylabel='Count', title="Play Counts of Each Songs")
    
    plt.savefig('static/charts/song_count_plot.png')
    plt.clf() 
    

    

    return "OK"
viz()

def remove_user():
    ##############################################
    #to remove the Blocked Users
    
    creators = User.query.filter_by(role='creator').all()
    
    creator_list = []
    for i in creators:
        creator_list.append(i.user_name)

    flagged_creators = flag_user.query.all()
    #if len(flagged_creators) >0:
    flagged_creators_dict = {}
    for i in flagged_creators:
        flagged_creators_dict[i.name] = i.flag
    

    creator_dict = {}
    for i in creator_list:
        if i in flagged_creators_dict:
            creator_dict[i] = flagged_creators_dict[i]
        else:
            creator_dict[i] = "Green"


    for flagged_creator in flagged_creators_dict:
        flag='Unknown'
        print("Flagged User: {}".format(flagged_creator))
        if flagged_creators_dict[flagged_creator] == "Block":
            item = Music.query.filter_by(Artist=flagged_creator).first()
            try:
                db.session.delete(item)
                db.session.commit()
                #flag=True
            except:
                print("Not Found in Music")

            a = album.query.filter_by(artist=flagged_creator).first()
            try:    
                db.session.delete(a)
                db.session.commit()
                #flag=True
            except:
                print("Not Found in Album")

            u = User.query.filter_by(user_name=flagged_creator).first()
            try:
                db.session.delete(u)
                db.session.commit()
                flag = True

                flagged_creators = flag_user.query.all()
                flagged_list = []
                for i in flagged_creators:
                    flagged_list.append(i.name)
                
                
                return flagged_list
            except:
                flag = False
                
                print("Not Found in Users table")
                return ["Not Blocked"]
            
        else:
            return ["Not Blocked"]
    """
    if flag:
        return "Block"
    else:
        return "Not Blocked
    """
    
    

remove_user()
#controllers
@app.route("/home", methods=["GET","POST"])
def homepage():
    if request.method == "GET":
        #this will show the logged in/not logged in status in the navbar
        if session["user_name"]:
            app_status=session["user_name"]
        else:
            app_status = "Not Logged In"

        if session["role"] != "ADMIN":
            musics = Music.query.all() #contains all the music details from db
            musics = list(reversed(musics))
            print("-----------")
            for i in musics:
                print(i.path)
            
            albums = album.query.all()

            album_dict_path = {} #{album_name: [path_list]}
            album_dict_songs = {}
            final_album_dict={} #{album_name: {song_name:song_path}}
            for al in albums:
                #
                album_name = al.album_name
                path_list = []
                final_path_list = []
                
                song_list = al.song_name.split(",")
                final_song_list = []
                for song in song_list:
                    final_song_list.append(song.strip(" "))

                print(final_song_list)
                print("###########")
                print(song_list)
                print("###########")

                for song in final_song_list:
                    print("Song name {}".format(song))
                    print(len(song))
                    path = Music.query.with_entities(Music.path).filter_by(Name=song)
                    #print(path)
                    path_list.append(path)
                    print(type(path))

                print("%%%%%%Printing paths%%%%%")
                print("Path List:{}".format(path_list))
                

                    
            
                for i in path_list:
                    
                    for j in i:
                        
                        final_path_list.append(j)
                
                album_dict_path[album_name] = final_path_list
                album_dict_songs[album_name] = final_song_list

                print(album_dict_path)
                print(album_dict_songs)

                song_path_dict = dict(map(lambda i,j : (i,j) , final_song_list,final_path_list))
                
                final_album_dict[album_name] = song_path_dict

                print(final_album_dict)


            # Get the song play count from the hidden input field.
            if 'play-count{{ loop.index }}' in request.form:
                #The form field was submitted with the request.
                play_count = int(request.form.get('play-count{"index"}'))

            

                

            
            else:
                # The form field was not submitted with the request.
                play_count = 1
            


            
            # Retrieve the SongPlayCount object from the database.
            song_play_count = Music.query.all()

            # If the SongPlayCount object does not exist, create a new one.
            #if not song_play_count:
            #    song_play_count = SongPlayCount(song_id=music.id)

            # Update the play count.

            for i in song_play_count:
                i.play_count += play_count

            # Commit the changes to the database.
            db.session.commit()   

            ###########################For Search Function##############################################

            search_string = request.form.get("search")

            #music_search = Music.query.filter(Music.Name.contains(search_string))
            #album_search = album.query.filter(album.album_name.contains(search_string))

            music_search = Music.query.filter_by(Name=search_string).all()
            #album_search = album.query.filter_by(album.album_name.contains(search_string))

            if search_string:
                if len(search_string)>0:
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    
                    print(search_string," : ",music_search)
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")



                    albums = album.query.filter_by(album_name=search_string).all()

                    album_dict_path = {} #{album_name: [path_list]}
                    album_dict_songs = {}
                    final_album_dict={} #{album_name: {song_name:song_path}}
                    for al in albums:
                        #
                        album_name = al.album_name
                        path_list = []
                        final_path_list = []
                        
                        song_list = al.song_name.split(",")
                        final_song_list = []
                        for song in song_list:
                            final_song_list.append(song.strip(" "))

                        print(final_song_list)
                        print("###########")
                        print(song_list)
                        print("###########")

                        for song in final_song_list:
                            print("Song name {}".format(song))
                            print(len(song))
                            path = Music.query.with_entities(Music.path).filter_by(Name=song)
                            #print(path)
                            path_list.append(path)
                            print(type(path))

                        print("%%%%%%Printing paths%%%%%")
                        print("Path List:{}".format(path_list))
                        

                            
                    
                        for i in path_list:
                            
                            for j in i:
                                
                                final_path_list.append(j)
                        
                        album_dict_path[album_name] = final_path_list
                        album_dict_songs[album_name] = final_song_list

                        print(album_dict_path)
                        print(album_dict_songs)

                        song_path_dict = dict(map(lambda i,j : (i,j) , final_song_list,final_path_list))
                        
                        final_album_dict[album_name] = song_path_dict

                        print(final_album_dict)

                    
                    return render_template("search_output.html", user_name=session['user_name'], role=session['role'], musics=list(music_search), 
                                albums=final_album_dict)
            ###########################For Search Function##############################################
            ############################################################################################

            ###########################For Rating Function##############################################
            ############################################################################################

            """
            rating_song_name = request.form.get("Song Name")
            user_rating = request.form.get("Rating")

            if user_rating:
                user_rating = int(user_rating)

            song_object = list(music_rating.query.filter_by(song=rating_song_name).first())

            if len(song_object)>0:
                rating_list = song_object[0].ratings
                rating_list.append(user_rating)

                db.session.commit()
            """

            song_object = list(music_rating.query.all())
            all_songs = list(Music.query.all())
            song_name_list = []
            for song in all_songs:
                s = song.Name
                song_name_list.append(s)

            song_rating_dict = {}

            for obj in song_object:
                new_list = []
                rating_list = str(obj.ratings)
                rating_list = rating_list.split(",")
                for r in rating_list:
                    rating = int(r)
                    new_list.append(rating)

                song_rating_dict[obj.song] = round(np.array(new_list).mean(),2)

            print("-----------------------------------------")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("Rating Dict: {}".format(song_rating_dict))
            print("-----------------------------------------")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

            return render_template("index.html",user_name=session['user_name'], role=session['role'], musics=musics, 
                                albums=final_album_dict, rating_dict = song_rating_dict, song_names = song_name_list)

        if session['role'] == "ADMIN":
            return redirect("/admin_dashboard")
    
    if request.method == "POST":
        print("POST")
        rating_song_name = request.form.get("songname", '')
        user_rating = request.form.get("rating")
        print("AAAAAAAA")
        print(rating_song_name, user_rating)
        print("AAAAAAAAA")
        
    
        
                    
        song_object = list(music_rating.query.filter_by(song=rating_song_name).all())

        if len(song_object)>0:
            print("Line 466: {}".format(song_object))
            rating_list =  song_object[0].ratings
            rating_list = str(rating_list)+","+str(user_rating)

            """
            rating_list = rating_list.split(",")
            rating_list.append(int(user_rating))
            """

            song_object[0].ratings = str(rating_list)

            print("Rating List: {}".format(rating_list))

            db.session.commit()
        else:
            new_rating = music_rating(song=rating_song_name,ratings=str(user_rating))
            db.session.add(new_rating)
            db.session.commit()
        return redirect("/home")
    
@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        search_string = request.form.get("search", '')

        #music_search = Music.query.filter(Music.Name.contains(search_string))
        #album_search = album.query.filter(album.album_name.contains(search_string))

        music_search = Music.query.filter_by(Name=search_string).all()
        music_by_genre_search = Music.query.filter_by(Genre=search_string).all()
        music_by_artist_search = Music.query.filter_by(Artist=search_string).all()
        #album_search = album.query.filter_by(album.album_name.contains(search_string))

        if search_string!="":
            
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            
            print(search_string," : ",music_search)
            print(search_string," : ",music_by_genre_search)
            print(search_string," : ",music_by_artist_search, len(music_by_artist_search))
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")



            albums = album.query.filter_by(album_name=search_string).all()

            album_dict_path = {} #{album_name: [path_list]}
            album_dict_songs = {}
            final_album_dict={} #{album_name: {song_name:song_path}}
            for al in albums:
                #
                album_name = al.album_name
                path_list = []
                final_path_list = []
                
                song_list = al.song_name.split(",")
                final_song_list = []
                for song in song_list:
                    final_song_list.append(song.strip(" "))

                print(final_song_list)
                print("###########")
                print(song_list)
                print("###########")

                for song in final_song_list:
                    print("Song name {}".format(song))
                    print(len(song))
                    path = Music.query.with_entities(Music.path).filter_by(Name=song)
                    #print(path)
                    path_list.append(path)
                    print(type(path))

                print("%%%%%%Printing paths%%%%%")
                print("Path List:{}".format(path_list))
                

                    
            
                for i in path_list:
                    
                    for j in i:
                        
                        final_path_list.append(j)
                
                album_dict_path[album_name] = final_path_list
                album_dict_songs[album_name] = final_song_list

                print(album_dict_path)
                print(album_dict_songs)

                song_path_dict = dict(map(lambda i,j : (i,j) , final_song_list,final_path_list))
                
                final_album_dict[album_name] = song_path_dict

                print(final_album_dict)

                #this block separates out search by Song name, Genre, Artist names

            if len(list(music_search))>0:

                return render_template("search_output.html", user_name=session['user_name'], role=session['role'], musics=list(music_search), 
                        albums=final_album_dict)
            if len(list(music_by_genre_search)) > 0:
                return render_template("search_output.html", user_name=session['user_name'], role=session['role'], musics=list(music_by_genre_search), 
                        albums=final_album_dict)
            else:
                return render_template("search_output.html", user_name=session['user_name'], role=session['role'], musics=list(music_by_artist_search), 
                        albums=final_album_dict)


@app.route("/", methods=["GET","POST"])
def landing_page():
    
    if request.method == "GET":
        return render_template("auth_page.html")
    
    
    if request.method == "POST":
        print(request.form)
        if request.form.get("register"):
            #print("Reg")
            return redirect("/register")
        
        if request.form.get("login"):
            return redirect("/login")
        
        if request.form.get("admin"):
            return redirect("/admin")

@app.route("/register", methods=["GET","POST"])
def register():
    
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        print("-----------")
        print(request.form)
        if request.form.get("email"):
            user_email = request.form.get("email")

            
            if request.form.get('username'):
                user_name = request.form.get('username')
            

                

                if request.form.get('password'):
                    user_pass = request.form.get('password')
                    ##############################################
                    #to remove the Blocked Users
                    
                    ##############################################
                    user_int = User(user_name=user_name,password=user_pass)
                
                    db.session.add(user_int)
                    db.session.commit()
                    a= remove_user()
                    print("a: {}".format(a))
                    
                    #if a != "Block":
                    if user_name not in a:
                        return redirect("/login")
                    else:
                        
                        
                        return render_template("blocked_user_register.html")
                    #return redirect("/")
                    
                else:
                    return render_template("register.html")
            else:
                return render_template("register.html")
            

            
        #return "<!doctype html><h6>Registered</h6>"



@app.route("/login",methods=["GET","POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        user_pass = request.form.get('password')
        print("Username: {}".format(username))

        #if username and user_pass:
        user = User.query.filter_by(user_name=username).first()
        if user is None: #to check for unregistered users
            return render_template('login_error_nreg.html')
        elif user.user_name == username and user_pass == user.password:
            
            #saving the username and id in session
            session["user_name"] = user.user_name
            #session["user_id"] = user.id
            session["role"] = user.role

            return redirect("/home")
        
        else:
            return render_template('login_error.html')


@app.route("/logout",methods=["GET","POST"])
def logout():

    session.pop("user_id",None)
    session.pop("role",None)
    session.pop("user_name",None)

    return redirect("/")

@app.route("/admin",methods=["GET","POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        user_pass = request.form.get('password')
        print("Username: {}".format(username))

        #if username and user_pass:
        admin = Admin.query.filter_by(username=username).first()
        if admin.username == username and user_pass == admin.password:
            
            #saving the username and id in session
            session["user_name"] = admin.username
            session["user_id"] = admin.id
            session["role"] = "ADMIN"

            return redirect("/home")
        else:
            return render_template('login_error.html')
        

@app.route("/creator_signup",methods=["GET","POST"])
def creator_regis():
    #if request.method == "GET":


    #fetching the logged in user details
    user_object = User.query.filter_by(user_name=session["user_name"]).first()
    user_object.role = "creator"
    db.session.commit()
    session["role"] = "creator"
    print("User has been Registered as a Creator")
    #print(app.upload_folder)

    return redirect("/creator")
upload_flag = False
@app.route("/creator",methods=["GET","POST"])
def file_upload():
    if request.method == 'POST':

        if request.form.get("create-album"):
            return redirect("/create-album")
        # check if the post request has the file part
        if 'file' in request.files:
            flag = False
            file = request.files['file']  
            filename = secure_filename(file.filename)
            print("File Name: {}".format(filename))
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #will be stored in the db
            path_name = os.path.join(app.config['UPLOAD_FOLDER'], filename).lstrip("/static/")
            song_name = request.form.get("song_name")
            artist_name = session['user_name']
            genre = request.form.get("genre")

            new_song = Music(Name=song_name, Genre=genre, Artist=artist_name, path=path_name)
            db.session.add(new_song)
            db.session.commit()
            flag=True
            if flag:
                uploaded_status="Song Sucefully Uploaded"
                upload_flag = True
                viz()
                return render_template("creator_page.html", upload_alert=uploaded_status)
            else:
                uploaded_status = "Please upload your song"
                return render_template("creator_page.html", upload_alert=uploaded_status)

        song_to_be_removed = request.form.get("songname","")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("Song to be removed: {}".format(song_to_be_removed))
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        if song_to_be_removed != "":
            #remove_song = Music.query.filter_by(Name=song_to_be_removed).first()
            remove_song = Music.query.filter(Music.Name.ilike(f'%{song_to_be_removed}%')).first()
            print(remove_song)

            rating_song = music_rating.query.filter_by(song=song_to_be_removed).first()

            db.session.delete(remove_song)
            db.session.commit()
            uploaded_status = "Song Has been Removed!"
            try:
                db.session.delete(rating_song)
                db.session.commit()
            except:
                print("The Song: {} does not exist in the rating table!")
        song_to_be_edited = request.form.get("songname_edit", "")
        if song_to_be_edited != '':
            song = Music.query.filter(Music.Name.ilike(f'%{song_to_be_edited}%')).first()
            new_name = request.form.get("new_name", '')
            if new_name!='':
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                print("Edit Name: {}, old name: {}".format(new_name, song_to_be_edited))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                try:
                    song.Name = new_name
                    db.session.commit()
                    uploaded_status = "Song Has been Updated!"
                except:
                    uploaded_status = "Song Has Not been Updated!"
                    print("Constraint Issue")

        
        return render_template("creator_page.html", upload_alert=uploaded_status)


    if request.method == "GET":

        all_songs = list(Music.query.all())
        song_list = []
        for song in all_songs:
            song_list.append(song.Name)
        return render_template("creator_page.html", user_name=session["user_name"], role=session["role"], song_names = song_list)


@app.route("/create-album",methods=["GET","POST"])
def create_album():
    if request.method == "POST":

        album_name_user = request.form.get("album")
        songs = request.form.get("songs")
        
        artist_name = request.form.get('artist')

        albums = album(album_name=album_name_user, artist=artist_name, song_name=songs)
        db.session.add(albums)
        db.session.commit()

        return redirect("/home")

    if request.method == "GET":
        creator_songs = Music.query.filter_by(Artist=session["user_name"]).all()
        
        for song in creator_songs:
            print(song.Name)
        return render_template("album_creation.html", songs=creator_songs) #
    
@app.route("/admin_dashboard",methods=["GET","POST"])
def admin_dashboard():
    if request.method == "GET":
        if session['role'] == "ADMIN":

            all_users = User.query.all()
            num_user = len(all_users)

            num_songs = len(Music.query.all())

            songs = Music.query.all()
            singer_list = []
            for i in songs:
                singer_list.append(i.Artist)
            uniq_singer_array = np.unique(np.array(singer_list))
            uniq_singer_list = list(uniq_singer_array)
            singers = ''
            for i in range(len(uniq_singer_list)):
                if i != 0:
                    singers = singers + ", " + uniq_singer_list[i]
                else:
                    singers = singers + uniq_singer_list[i]





            #to remove the Blocked Users
            creators = User.query.filter_by(role='creator').all()
            
            creator_list = []
            for i in creators:
                creator_list.append(i.user_name)

            flagged_creators = flag_user.query.all()
            #if len(flagged_creators) >0:
            flagged_creators_dict = {}
            for i in flagged_creators:
                flagged_creators_dict[i.name] = i.flag
            

            creator_dict = {}
            for i in creator_list:
                if i in flagged_creators_dict:
                    creator_dict[i] = flagged_creators_dict[i]
                else:
                    creator_dict[i] = "Green"
            for i in flagged_creators_dict:
                creator_dict[i] = flagged_creators_dict[i]
            print(creator_dict)

            print(flagged_creators_dict)

            remove_flagged_user_list = []
            for flagged_creator in flagged_creators_dict:
                print("Flagged User: {}".format(flagged_creator))
                if flagged_creators_dict[flagged_creator] == "Block":
                    item = Music.query.filter_by(Artist=flagged_creator).first()
                    try:
                        db.session.delete(item)
                        db.session.commit()
                    except:
                        print("Not Found in Music")

                    a = album.query.filter_by(artist=flagged_creator).first()
                    try:    
                        db.session.delete(a)
                        db.session.commit()
                    except:
                        print("Not Found in Album")

                    u = User.query.filter_by(user_name=flagged_creator).first()
                    try:
                        db.session.delete(u)
                        db.session.commit()
                    except:
                        print("Not Found in Users table")
                        
                    """
                    f = flag_user.query.filter_by(name=flagged_creator).first()
                    db.session.delete(f)
                    db.session.commit()
                    """
                    print ("message: {} deleted!".format(item))

            #####################################################################
            ####################Song Blacklist###################################
            #####################################################################
            song_list = list(Music.query.all())
            song_list_for_blacklist = []

            for i in song_list:
                song_list_for_blacklist.append(i.Name)


            return render_template("admin_dashboard.html",user_count = num_user, song_num = uniq_singer_list, 
                            singer=singers, creators=creator_dict, song_names=song_list_for_blacklist)
            """else:
                return render_template("admin_dashboard.html",user_count = num_user, song_num = uniq_singer_list, 
                                singer=singers)
            """
        

            
        else:
            return redirect("/admin")   
    if request.method == "POST":
        creator_name = request.form.get('creator', "")
        flag_type = request.form.get("choice", "")

        if creator_name != "":
            if flag_type != '':
                try:
                    flagged_creators = flag_user(name=creator_name, flag=flag_type)
                    db.session.add(flagged_creators)
                    db.session.commit()
                except Exception:
                    # If there's a UNIQUE constraint violation, update the existing record
                    db.session.rollback()  # Rollback the current transaction
                    flagged_creators = flag_user.query.filter_by(name=creator_name).first()
                    flagged_creators.flag = flag_type
                    db.session.commit()
        
        song_blacklist = request.form.get("songname_block","")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Song Blacklist: {}".format(song_blacklist))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if song_blacklist != '':
            
            try:
                new_entry = block_music(name=song_blacklist,status='Blacklisted')
                db.session.add(new_entry)
                db.session.commit()
            except:
                print("Constraint Error")
                db.session.rollback()
                print(block_music.query.all())


        return redirect('/admin_dashboard')



        
            
            
