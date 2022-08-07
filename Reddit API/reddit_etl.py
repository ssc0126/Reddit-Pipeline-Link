import requests
import configparser
import pathlib
import praw
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import time
import os



#Read Config File
config_file = "my_config.ini"
config_file_path = pathlib.Path(__file__).parent.absolute()
config = configparser.ConfigParser()
config.read(f"{config_file_path}/{config_file}")



#CONSTANT VARIABLES
CLIENT_ID = config.get('API', 'client_id')
SECRET_KEY = config.get('API', 'secret_key')
USER_AGENT = config.get('API', 'user_agent')
SUBREDDIT = 'teenagers'

def connect_api():
    try: 
        user_agent = USER_AGENT
        reddit = praw.Reddit(
        client_id = CLIENT_ID,
        client_secret = SECRET_KEY,
        user_agent= user_agent
        )
    except Exception as e:
        print('API Connection Error.')

    return reddit


def subreddit_post(instance):
    try:
        posts = instance.subreddit(SUBREDDIT).hot(limit=25)
        return posts
    except Exception as e:
        print("Subreddit Connetion Error!")


def url_comment_to_df(posts):
    post_list = []
    comment_list = []
    try:
        for submission in posts: 
            #if not submission.stickied:
            print('ID {}, TITLE: {}, 18+: {}, RATIO: {}'.format(submission.id, submission.title, submission.over_18, submission.upvote_ratio))
            post_dic = {'PostID': submission.id, 'Tile': submission.title, '18+': submission.over_18, 'Ratio': submission.upvote_ratio, 'Date': submission.created_utc}
            post_list.append(post_dic)

            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                print(20*'-')
                print('Parent ID:', comment.parent())
                print('Comment ID:', comment.id)
                print(comment.body_html)
                soup  = BeautifulSoup(comment.body_html, 'lxml')
                links = [a.get('href') for a in soup.find_all('a', href=True)]
                
                for i in links:
                    comment_dic = {'CommentID': comment.id, 'PostID': submission.id, 'URL': i, 'Date': comment.created_utc}
                    comment_list.append(comment_dic)
                
                comment_df = pd.DataFrame(comment_list)
                post_df = pd.DataFrame(post_list)
    except Exception as e:
         print('Subreddit Post Error!')

    return comment_df, post_df



def transform_df(comment_df, post_df):
    #remove reddit links
   comment_df = comment_df[comment_df['URL'].str.contains("r/|reddit|u/")==False]
   #convert to datetime
   comment_df['Date'] = pd.to_datetime(comment_df['Date'], unit='s')
   post_df['Date'] = pd.to_datetime(post_df['Date'], unit='s')

   return comment_df, post_df

def load_csv (comment_df, post_df):
    cwd = os.getvwd()
    file_name = datetime.today().strftime('%Y-%m-%d')
    if not os.path.exists(f"{cwd}\\FileDump"):
        os.makedirs(f"{cwd}\\FileDump")
        comment_df.to_csv(f"{cwd}\\FileDump\\{file_name}_commentdf.csv", index = False)
        post_df.to_csv(f"{cwd}\\FileDump\\{file_name}_postdf.csv", index = False)
    else:
        print('No directory to store files')

def main():
    reddit_instance = connect_api()
    subreddit_posts_object = subreddit_post(reddit_instance)
    _comments, _posts = url_comment_to_df(subreddit_posts_object)
    liger, tiger = transform_df(_comments, _posts)
    load_csv(liger, tiger)

if __name__ == "__main__":
  main()