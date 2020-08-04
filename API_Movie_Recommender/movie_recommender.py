import requests_with_caching
import json

def get_movies_from_tastedive(name):
    #q|type|limit are the parameters
    s = requests_with_caching.get('https://tastedive.com/api/similar',params ={'q':str(name),'type':'movies','limit':'5'})
    selection = json.loads(s.text)
    return selection

def extract_movie_titles(selection):
    e=[]
    for name in selection['Similar']['Results']:
        e.append(name['Name'])
    return e

def get_related_titles(e):
    a=[]
    for titles in e:
        newE = extract_movie_titles(get_movies_from_tastedive(titles))
        for mov in newE:
            if mov not in a:
                a.append(mov)
        
  #  print(a)
    return a

def get_movie_data(name):
    parameters ={}
    parameters['t']= name
    parameters['r']='json'
    infoReq = requests_with_caching.get('http://www.omdbapi.com/',params=parameters)
    #print(infoReq.text)
    info= json.loads(infoReq.text)
    return info
    
def get_movie_rating(name):
    info = get_movie_data(name)
    #Structure: Dictionary -> key:Ratings -> Key:Source & Key: Value
    if 'Rotten Tomatoes' in str(info):
        for sect in info['Ratings']:
            if 'Rotten Tomatoes' in sect.values():
                return int(sect['Value'].replace("%",""))
    else:
        return 0

def get_sorted_recommendations(e):
    rel = get_related_titles(e)
    ratings=[]
    comb = {}
    for movie in rel:
        r=get_movie_rating(movie)
        comb[movie] = r
 
    sorted_lst= sorted(comb.items(),key=lambda x: (x[1],x[0]), reverse=True)
    sorted_mov=[]
    for mov in sorted_lst:
        sorted_mov.append(mov[0])
    return sorted_mov