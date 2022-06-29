'''
In this example script, get his followers, and get followers from a base profile,
crosses the information and starts interacting with the followers of the base profile,
if the profile is public he will like three photos if it is private he will request to follow the user
'''

from api import Instagram
import time
USERNAME = 'YOU'            #Your username
PASSWORD = 'PASS'           #Your password
USERNAME_BASED_PROFILE = '' #Profile that you will use the followers as a base
FOLLOWERS_ANALYSE=300       #Number of followers to analyze

insta_follower = Instagram(user=USERNAME, password=PASSWORD)                
insta_follower.login()
print('getting my followers')
my_folowers=insta_follower.get_folowers_by_username(USERNAME)
print('getting my followed')
my_following=insta_follower.get_following_by_username(USERNAME)
my_folowers_=[]
for x in my_folowers:
    my_folowers_.append(x['username'])
my_following_=[]
for x in my_following:
    my_following_.append(x['username'])

print('getting followers from base user')
user_following=insta_follower.get_folowers_by_username(USERNAME_BASED_PROFILE,300)

following=[]

for x in user_following:
    print(x['username'])
    if x['username'] not in my_following_ and x['username'] not in my_folowers_:
        if x['is_private']==True:  
            insta_follower.follow_user_by_id(x['pk'])
            following.append(x)
            print('followed')
        else:
            user=insta_follower.get_user_by_username(x['username'])
            if user['edge_owner_to_timeline_media']['count']>=3:range_=3
            else:range_=user['edge_owner_to_timeline_media']['count']
            for y in range(range_):
                print(f'like post {y}')
                id_post=user['edge_owner_to_timeline_media']['edges'][y]['node']['id']
                insta_follower.like_post_by_id(id_post)
    time.sleep(5)
            











