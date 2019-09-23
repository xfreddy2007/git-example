#YU-CHENG CHANG'S FINAL
import json
import requests
import codecs
import webbrowser
import unittest
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from your_app_data import APP_ID, APP_SECRET

FB_CACHE_FILE="cache_fb.json"
# FB_CACHE_FILE = None
APP_ID='704353093092570'
APP_SECRET='87f92146b424aa677447ef35ada5319b'

facebook_session = False # For dealing with others' code for getting data from FB

stopwords_file=open('stopwords.txt','r')
STOPWORDS=stopwords_file.read().splitlines()
stopwords_file.close()

# print(STOPWORDS)

def makeFacebookRequest(baseURL, params = {}):
    global facebook_session
    if not facebook_session:
        # OAuth endpoints given in the Facebook API documentation
        authorization_base_url = 'https://www.facebook.com/dialog/oauth'
        token_url = 'https://graph.facebook.com/oauth/access_token'
        redirect_uri = 'https://www.programsinformationpeople.org/runestone/oauth'

        scope = ['user_posts','pages_messaging','user_managed_groups','user_status','user_likes']
        facebook = OAuth2Session(APP_ID, redirect_uri=redirect_uri, scope=scope)
        facebook_session = facebook_compliance_fix(facebook)

        authorization_url, state = facebook_session.authorization_url(authorization_base_url)
        print('Opening browser to {} for authorization'.format(authorization_url))
        webbrowser.open(authorization_url)

        redirect_response = input('Paste the full redirect URL here: ')
        facebook_session.fetch_token(token_url, client_secret=APP_SECRET, authorization_response=redirect_response.strip())

    return facebook_session.get(baseURL, params=params)

check=0
n = input("Which data you want to use, 1:request from FB now, 2:cached data (please select 1 or 2):")
while check != 1:
	if n is "1":
	        baseurl = "https://graph.facebook.com/{}/feed".format("nytimes")
	        print(makeFacebookRequest(baseurl).text)
	        text_data_MT = makeFacebookRequest(baseurl).text
	        data_NYT_py = json.loads(text_data_MT) 

	        # dump_FBcache_data=json.dumps(data_NYT_py)
			# fb_file_w=open(FB_CACHE_FILE,'w')
			# fb_file_w.write(dump_FBcache_data)
			# fb_file_w.close() 
	        check=1
	elif n is "2":
	        fbcache_file = open(FB_CACHE_FILE, 'r') ## Open a file with the CACHE_FNAME file name.
	    
	        data_NYT_py = json.loads(fbcache_file.read())  ## Load the string into a Python object, saved in a variable called CACHE_DICTION.
	        fbcache_file.close()
	        print("load cache from",FB_CACHE_FILE)
	        check=1
	else:
		print("Sorry, you type the wrong option, please type 1 or 2")
		check=0






class Post(object):
	def __init__(self, fb_post_data={}):
		if 'message' in fb_post_data:
			self.message=fb_post_data["message"].encode('utf-8')
			self.edited_message=self.remove_stopwords()
		else:
			self.message = ''
			self.edited_message = ''
		# print(fb_post_data["message"])
	
		if "created_time" in fb_post_data:
			self.post_time=fb_post_data["created_time"]
		else:
			self.post_time= ''

		if "id" in fb_post_data:
			self.id=fb_post_data["id"]
		else:
			self.id= ''
	def __str__(self):
		return "{} at {}, {}".format(self.message,self.post_time,self.id)

	def remove_stopwords(self):
		# stopwords=["The","a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
		temp=[]
 		#print(stopwords)
		# print(self.message.split())
		for i_temp in self.message.split():
                        if i_temp not in STOPWORDS:
                                temp.append(i_temp)
				
		# print(temp)
		return temp

def commond_word(FB_data_ls):
	

	temp_d={}
	for message_one in FB_data_ls:
		# print(type(message_one))
		# print(message_one.remove_stopwords().encode('utf-8'))
		for word in message_one.edited_message:
			# print(type(message_one.edited_message))
			if word not in temp_d:
				temp_d[word]=1
			else:
				temp_d[word]+=1

	sorted_words = sorted(temp_d.items(), key=lambda x:x[1], reverse=True)
	return sorted_words[0]

## create a list of class Song

def create_class_list(in_dic,type):
        list_out=[]
        for i in in_dic:
                if type is "Post":
                        list_out.append(Post(i))
                if type is "Song":
                        list_out.append(Song(i))
        return list_out

list_FB_post=create_class_list(data_NYT_py["data"],"Post")
print("__str__ output test")
for ii in range(len(list_FB_post)):
	# print(len(list_FB_post[ii].message))
	# print(len(list_FB_post[ii].edited_message))
	print(list_FB_post[ii])
# for ii in list_FB_post:
	# print(type(ii.edited_message)
	# print()

print(commond_word(list_FB_post))
#-------------------------------------------------------
# below is itunes part

CACHE_FILE="SI506finalproject_cache.json"
CACHE_DICTION = None


try:                                   
    print("open cache file")
    cache_file = open(CACHE_FILE, 'r') ## Open a file with the CACHE_FNAME file name.
    
    CACHE_DICTION = json.loads(cache_file.read())  ## Load the string into a Python object, saved in a variable called CACHE_DICTION.
    cache_file.close()
    print("load cache from",CACHE_FILE)
except:                                 # Begin the except clause of the try/except statement:
    CACHE_DICTION = {}     

def build_cache_key(name, mtype, result_n):
	return '#'.join(name.split()) + '_' + mtype +'_'+str(result_n)

def write_cache():
	dump_cache_data=json.dumps(CACHE_DICTION)
	file_w=open(CACHE_FILE,'w')
	file_w.write(dump_cache_data)
	file_w.close() 

def get_from_itunes(name,mtype='song'):
	
	baseurl = "https://itunes.apple.com/search" # important that this is in the function, not a global variable -- what if you wanted to use this function in another program?
	parameters = {}
	parameters["term"] = name
	parameters["entity"] =  mtype# should be Song or musicVideo
	parameters["limit"]=30
	response = requests.get(baseurl,params=parameters)

	cache_key_id=build_cache_key(name, mtype, parameters["limit"])
	#print('cache_key_id='+ cache_key_id)
	#print(CACHE_DICTION.keys())
	#print(cache_key_id in CACHE_DICTION)
	if cache_key_id in CACHE_DICTION:
		print("load data from cache file")
		return CACHE_DICTION[cache_key_id]
	else:
		print("ask data from itunes")
		
		itunes_result_obj = json.loads(response.text) 
		CACHE_DICTION[cache_key_id]=itunes_result_obj
		# for_cache_data=json.dumps(CACHE_DICTION)
		write_cache()
		# out_str=json.dumps(python_obj)
	# print(out_str)
	return CACHE_DICTION[cache_key_id]


search_key=input("Enter the key word for searching itunes, ex: Christmas :")
# search_result=get_from_itunes("Christmas")
search_result=get_from_itunes(search_key)

# print(get_from_itunes("The Bealtes","song"))  

class Song(object):
	def __init__(self, dic_song):	
		if "trackName" in dic_song:
			self.song_title=dic_song['trackName']
		else:
			self.song_title=''

		if 'trackTimeMillis' in dic_song:
			self.song_length=dic_song['trackTimeMillis']
		else:
			self.song_length=''

		if 'artistName' in dic_song:
			self.artist=dic_song['artistName']
		else:
			self.artist=''

		if 'collectionName' in dic_song:
			self.album=dic_song['collectionName']
		else:
			self.album=''

	def __str__(self):
		return "{} by {} in {}, {}".format(self.song_title,self.artist,self.album,self.song_length)


 
# single_song=Song({'song':'ABC', 'length':'128', 'artist':'Amy'})
# print(single_song)

## create a list of class Song
#list_Song=[]
#for i in search_result["results"]:
#	list_Song.append(Song(i))


list_Song=create_class_list(search_result["results"],"Song")
# use __str__
print("test __str__:")
for ii in range(len(list_Song)):
        print(list_Song[ii])
# sort
print("\nSorting")
sorted_songs = sorted(list_Song, key=lambda x: x.song_length)
print("sorted list:")
for song in sorted_songs:
	print("{}, {}, {}, {}\n".format(song.song_title,song.artist,song.album,str(song.song_length)))



def write_CSV(sorted_songs):
	#output the CSV file
	outfile = codecs.open("SampleOutput.csv","w",'utf-8-sig')
	# output the header row
	outfile.write("Song title, artist, album, length\n")
	# output each of the rows:
	for song in sorted_songs:
	# print("a")
		outfile.write('"{}","{}","{}","{}"\n'.format(song.artist,song.artist, song.album, song.song_length))
	# outfile.write("{}, {}, {}, {}\n".format(song.song_title,song.artist,song.album,str(song.song_length))

	outfile.close()


write_CSV(sorted_songs)

