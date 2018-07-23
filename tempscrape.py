import pandas as pd
import requests
import numpy as np
import re
import nltk
from textstat.textstat import textstat
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
#nltk.download('vader_lexicon')
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '91df6ca120d7407a877a64fabb100b49'
client_secret = '05a35b3ad63948c398d82dc8251d2bfb'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def scrape_lyrics(title, artist):
    ##Takes the Url and strips the html down to just the lyrics
    ##The Lyrics are placed into var clean
    title = title.replace(" ", "-")
    artist = artist.replace(" ", "-")
    url = url = 'https://genius.com/'+artist+'-'+title+'-lyrics'
    source = requests.get(url)
    if source.status_code == 404:
        print('Error')
        raise Exception('Incorrect track or artist')
    source = source.text
    source = source.split('<div class="lyrics">')[1]
    source = source.split('<!--/sse-->')[0]
    clean = re.sub('<[^>]+>', '', source).strip()
    return clean

def sentiment_analysis(lyrics):
    #in future get rid of brackets that have artist name
   sid = SentimentIntensityAnalyzer()
   ss = sid.polarity_scores(lyrics)
   return ss
    

#This will need to run for each line separately, otherwise its useless
def scansion_scanner(lyrics):
    sc = textstat.syllable_count(lyrics)
    return sc


#decided which formula to use from documentation and this guide
#https://pypi.org/project/textstat/
#http://www.readabilityformulas.com/articles/how-do-i-decide-which-readability-formula-to-use.php
def reading_level(lyrics):
    rl = textstat.flesch_reading_ease(lyrics)
    return rl
#100.00-90.00 	5th grade 	Very easy to read. Easily understood by an average 11-year-old student.
#90.0–80.0 	6th grade 	Easy to read. Conversational English for consumers.
#80.0–70.0 	7th grade 	Fairly easy to read.
#70.0–60.0 	8th & 9th grade 	Plain English. Easily understood by 13- to 15-year-old students.
#60.0–50.0 	10th to 12th grade 	Fairly difficult to read.
#50.0–30.0 	College 	Difficult to read.
#30.0–0.0 	College graduate 	Very difficult to read. Best understood by university graduates. 

def search_song_id(title, artist):
    search = title + ' ' + artist
    result = sp.search(q = search, limit = 1, type = 'track')
    result = result['tracks']
    result = result['items'][0]
    return result['id']

def playlistScan(id):    
    for ids in id:
        Pfeatures = sp.audio_features(ids)
        Pfeatures = ['valence']
    return


##InputGrabbers, commented out til GUI figured out
    ##title=Raw_Input('Song Title?')
    ##artist=Raw_Input('Artist name?')
title = 'look at me'
artist = 'xxxtentacion'


lyrics = scrape_lyrics(title, artist)
sentiment = sentiment_analysis(lyrics)
syllables = scansion_scanner(lyrics)
reading_level = reading_level(lyrics)
id = search_song_id(title, artist)


analysis = sp.audio_analysis(id)
features = sp.audio_features(id)










