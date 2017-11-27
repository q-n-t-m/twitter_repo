import tweepy
import csv
import codecs

CONSUMER_KEY = '' # enter your own in between the quotes
CONSUMER_SECRET = '' # enter your own in between the quotes
ACCESS_KEY = '' # enter your own in between the quotes
ACCESS_SECRET = '' # enter your own in between the quotes

# Create a twitter client (in accordance with twitter documentation):
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api_client = tweepy.API(auth)

# I want to be able to auto-sort in descending order.
# I want to add headers to the CSV output

# add function to add to SQL db

# -------------------------------------------------------------------------------

# 1. Main function incorporating all the other functions below - use this as a dispatcher:

def generate_csv(expression_in, count_in, tweet_file_name, freq_file_name):
    tweets = get_tweets(expression_in, count_in) # calls on gets_tweets function
    write_to_csv(tweets, tweet_file_name) # calls on write_to_csv function and writes tweets to csv
    my_tweet_string = [x[2] for x in tweets] # calls on 3rd item which is the tweets from get_tweets function
    tweet_string = aggregate_tweets(my_tweet_string) # calls on aggregate_tweets function which outputs tweets as a list
    frequencies = get_word_freq(tweet_string) # calls on get_word_freq function which counts instances of words in tweets
    frequencies = filter_words(my_blacklist, frequencies) # calls on filter_words which applies blacklist to freq table(s)
    write_freq_to_csv(frequencies, freq_file_name) # calls on write_freq_to_csv which writes 'clean' freq table to csv

    return

# here's how to run it in your console:
# import twitter
# twitter.generate_csv("iphonex", 100, "iphonex.csv", "iphonex_freq.csv")

# the functions below can be run in isolation but are all called upon in the above function...

# -------------------------------------------------------------------------------

# 2. Function to get tweets based on 1 keyword:

def get_tweets(expression_in, count_in):
    got_tweets = []
    tweets = tweepy.Cursor(api_client.search,
                           q=expression_in,
                           result_type='recent',
                           include_entities=True,
                           lang="en").items(count_in)
    for t in tweets:
        #got_tweets.append(t.text)
        got_tweets.append((t.author.screen_name, t.author.followers_count, t.text))
    return got_tweets

# -------------------------------------------------------------------------------

# 3. Function to print and format tweets:

def print_tweets(tweet_info_list):
    for t in tweet_info_list:
        print("user {}, with {} followers, tweeted:".format(t[0], t[1]))
        print(t[2])
        print("\n")
    return

# -------------------------------------------------------------------------------

# 4. Function to generate multiple tweet csv's and freq tables based on 4 keywords:

def auto_gen_csv(marketing_list):
    for m in marketing_list:
        generate_csv(m[0], m[1], m[2], m[3])

    return

my_marketing_list = [('tesco', 25, 'tesco_tweets.csv', 'tesco_freq.csv'), ('sainsbury', 25, 'sainsbury_tweets.csv', 'sainsbury_freq.csv'), ('asda', 25, 'asda_tweets.csv', 'asda_freq.csv'), ('waitrose', 25, 'waitrose_tweets.csv', 'waitrose_freq.csv')]

# -------------------------------------------------------------------------------

# 5. Function to write to csv:

def write_to_csv(tweets, csv_file_name): #tweet_info_list
    with codecs.open(csv_file_name, 'w', encoding='utf8') as my_file:
        writer = csv.writer(my_file, dialect='excel')
        writer.writerows(tweets)
    return

# -------------------------------------------------------------------------------

# 6. Function to ?:

def on_status(self, status):
    with open('file.txt', 'w') as f:
        f.write('Author,Date,Text')
        writer = csv.writer(f)
        writer.writerow([status.author.screen_name, status.created_at, status.text])

# -------------------------------------------------------------------------------

# 7. Function to aggregate tweets:

def aggregate_tweets(tweets_list_in):
    tweet_string_out = ' '.join(tweets_list_in)

    return tweet_string_out

# alternate way:
'''def aggregate_tweets2(tweets_list_in):
    tweet_string_out = ''
    for tweet in tweets_list_in:
        tweet_string_out = tweet_string_out + ' ' + tweet

    return tweet_string_out[1:]'''

# -------------------------------------------------------------------------------
# 8. Blacklist filter:

def filter_words(blacklist, freq_list_in):
    return [f for f in freq_list_in if (f[0] not in blacklist) and ('@' not in f[0][0])]

my_blacklist = ['a', 'the', 'to', 'RT', 'with', 'have', 'for', 'it', 'and', 'we', 'that']

# -------------------------------------------------------------------------------
# 9. Frequency table:

def get_word_freq(string_in):
    freq_table = {}
    for w in string_in.split():
        if w in freq_table:
            freq_table[w] = freq_table[w]+1
        else:
            freq_table[w] = 1

    freq_table = list(freq_table.items())
    freq_table.sort(key=lambda x: x[1], reverse=True)
    return freq_table

# -------------------------------------------------------------------------------
# 10. Write frequency table to CSV:

def write_freq_to_csv(freq_table, csv_file_name):
    with codecs.open(csv_file_name, 'w', encoding='utf8') as my_file:
        writer = csv.writer(my_file, dialect='excel')
        writer.writerows(freq_table)
    return

# -------------------------------------------------------------------------------


# get stuff to run in console:

# import twitter2
# my_tweets = twitter2.get_tweets("iphonex", 10)
# my_tweets_string = [x[2] for x in my_tweets]
# tweet_string = twitter2.aggregate_tweets(my_tweets_string)
# frequencies = twitter2.get_word_freq(tweet_string)
# frequencies
# [('#iPhoneX', 6), ('RT', 3), ('that', 2), ('have', 2), ('to', 2), ('was', 2), ('a', 2), ('the', 2), ('in', 2), ('be', 2), ('for', 2), ('Tone', 1), ('Reflection', 1), ('Download:', 1), ('https://t.co/aT9rH2gkjQ', 1), ('#ringtone', 1), ('#m4r', 1), ('https://t.co/Ml44fgXady', 1), ('Who’s', 1), ('getting', 1), ('new', 1), ('#iPhoneX?', 1), ('#IphoneX:', 1), ('You', 1), ('questions,', 1), ('we', 1), ('answers', 1), ('-', 1), ('CNET', 1), ('https://t.co/L3BP0gaiEw', 1), ('@THErealDVORAK', 1), ('Hate', 1), ('say', 1), ('it,', 1), ('but', 1), ('article', 1), ('just', 1), ('click', 1), ('bait.', 1), ('That', 1), ('20', 1), ('second', 1), ('read,', 1), ('WTH?', 1), ('How', 1), ('do', 1), ('you', 1), ('show', 1), ('off', 1), ('most', 1), ('anticipated', 1), ('product', 1), ('years?', 1), ('#Apple', 1), ('https://t.co/B3byiumOBy', 1), ('#display', 1), ('81,48%', 1), ('#screenToBody.', 1), ('Official', 1), ('Image', 1), ('on', 1), ('#apple', 1), ('website', 1), ('#iphoneX.', 1), ('#Test', 1), ('with', 1), ('#photoshop', 1), ('selected', 1), ('#pixel…', 1), ('https://t.co/AYX912qxlX', 1), ('@TylerTremallose:', 1), ('lets', 1), ('iphoneX', 1), ('besties', 1), ('&lt;3', 1), ('Most', 1), ('of', 1), ('my', 1), ('apps', 1), ('already', 1), ('updating', 1), ('display', 1), ('@BI_RetailNews:', 1), ('Unboxing', 1), ('—', 1), ("here's", 1), ('everything', 1), ('inside', 1), ('and', 1), ('what', 1), ("you'll", 1), ('need', 1), ('get', 1), ('https://t.co/1l6TqCGin5', 1), ('https://t.co/Mx3aQ2…', 1), ('@justinheintz:', 1), ('The', 1), ('@PulseRadioAZ', 1), ('app', 1), ('fully', 1), ('supports', 1), ('#iOS11,', 1), ('support', 1), ('will', 1), ('added', 1), ('future', 1), ('update…no', 1), ('ETA', 1)]
# twitter2.write_to_csv(my_tweets, 'my_tweets.csv')
