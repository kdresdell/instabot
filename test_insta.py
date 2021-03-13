import instaloader
import requests

L = instaloader.Instaloader()

Pinsta_username = 'waiting4_wind'
Pinsta_password = 'mFrance&201805'

L.login(Pinsta_username, Pinsta_password)

profile = instaloader.Profile.from_username(L.context, Pinsta_username)


print(profile.biography)
print(profile.followers)
print(profile.followees)

post_iterator = profile.get_posts()
print(post_iterator.count)


img = profile.get_profile_pic_url()
response = requests.get(img)

file = open(Pinsta_username+".jpg", "wb")
file.write(response.content)
file.close()
