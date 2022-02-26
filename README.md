# Python Screenshare
I digged up my projects folder and found some cool stuff I made in 2020 / 2021. I think this one was from 2020.

Since it was an old project, the code is a bit messy, since I don't plan on doing anything with it I won't tidy up the code and make it more professional, but it should be good enough if you're looking for python screenshare examples.


I've made both TCP version and a UDP version.

The TCP version averages on around 10fps on my local network.
The UDP version averages on around 30fps on my local network.

I've used zstd lib with the UDP version so you might need to pip install it to make it work.

Note: If you're browsing on github because you want to find a high fps screenshare, the best solution is to incorparate a caching system to save on network resources, I haven't done it in this project, but it's just something to keep in mind
