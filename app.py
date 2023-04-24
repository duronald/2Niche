from flask import Flask, render_template, session
from flask_session import Session
import requests, json, geocoder, math

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'mysecretkey'
Session(app)

@app.route('/')
def home():

    session['username'] = 'John'
    return render_template('home.html', username=session['username'])

@app.route('/entryForm/')
def entryForm():

    return render_template('entryForm.html', username=session['username'])

from flask import request

@app.route('/third/', methods=["POST"])
def third():
    searchbox = request.form["searchbox"]
    rating= request.form["customRange2"]
    radius = request.form["customRange3"]
    print(searchbox)
    print(rating)
    print(radius)
    # Python program to get a set of 
    # places according to your search 
    # query using Google Places API
      
    # importing required modules
    
      
    # enter your api key here
    #api_key = 'AIzaSyD2JJs3Cdwy0imhviCwk1NXsGpmEzBbmCE'
    api_key = 'AIzaSyA5Yd1uHgI-__Gkz4gD9dN8hVbdVhuLacw'
    # url variable store url
    #url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    urlPhoto = "https://maps.googleapis.com/maps/api/place/photo?"

    g = geocoder.ip('me')

    print(g.latlng)
    # The text string on which to search
    # query = input('Search query: ')
      
    location = str(g.latlng[0]) + '%2C' + str(g.latlng[1])
    # get method of requests module
    # return response object
    # r = requests.get(url + 'query=' + query +
    #                         '&key=' + api_key)

    #apirest = url + 'query=' + query + '&key=' + api_key
    apirest = url + "keyword=" + str(searchbox) + '&location=' + location + "&radius=" + str(radius) + '&key=' + api_key
    if (str(searchbox) == ""):
        apirest = url + 'location=' + location + "&radius=" + str(radius) + '&key=' + api_key
    apirestPhoto = urlPhoto + 'maxwidth=400' + '&photo_reference=' 

    #for i in range(100):
    r = requests.get(apirest)
    print(apirest)
    # json method of response object convert
    #  json format data into python format data
    x = r.json()
    #print(x)
    # now x contains list of nested dictionaries
    # we know dictionary contain key value pair
    # store the value of result key in variable y
    y = x['results']
      
    # keep looping upto length of y
    bottom25 = {}
    count = 0
    dictOfReviews = {}
    for i in range(len(y)):
          
        # Print value corresponding to the
        # 'name' key at the ith index of y

        if(y[i]['rating'] < float(rating)):
            print("lol this place sucks")
        else:
            print(y[i]['name'])
            try:
                print(y[i]['user_ratings_total'])
                dictOfReviews[y[i]['name']] = [y[i]['user_ratings_total'], y[i]['rating'], y[i]['photos'][0]['photo_reference'], apirestPhoto + y[i]['photos'][0]['photo_reference'] + '&key=' + api_key, y[i]['plus_code']['compound_code'], str(y[i]['photos'][0]['html_attributions'][0][9:]).split('"', 1)[0]]  
            except:
                print("something happened!")

    sortedDictofReviews = sorted(dictOfReviews.items(), key=lambda x:x[1])
    print(sortedDictofReviews)

    #print(len(sortedDictofReviews))
    stripSortDictOfReviews = sortedDictofReviews
    
    for i in range((math.ceil(len(sortedDictofReviews) / 5))*3):
        #print(len())
        try:
            stripSortDictOfReviews.pop()
        except:
            print("something happened when popping ")

    session['username'] = 'John'

    print("\n\n\n\n\n")
    #print(sortedDictofReviews[1][1][5][0][9:].split('"', 1)[0])
    #print(stripSortDictOfReviews[1])
    return render_template('third.html', locations=stripSortDictOfReviews, username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)