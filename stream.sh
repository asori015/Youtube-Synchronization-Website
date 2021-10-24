ffmpeg -re -i ~/rtorrent/download/untold-history/ep9.mkv -c:v libx264 -preset veryfast -tune zerolatency -c:a aac -ar 44100 -f flv \
rtmp://localhost:5000/live/MYSTREAM
#ffmpeg -re -i ~/rtorrent/download/untold-history/ep9.mkv -c:v libx264 -preset veryfast -tune zerolatency -c:a aac -ar 44100 -f flv \
#rtmp://not-facebook391.herokuapp.com:1935/live/MYSTREAM
#ffmpeg -re -i ~/rtorrent/download/untold-history/ep9.mkv -c:v libx264 -preset veryfast -tune zerolatency -c:a aac -ar 44100 -f flv \
#rtmp://streamy-app.herokuapp.com/live/


#ffmpeg -re -i ~/rtorrent/download/untold-history/ep9.mkv -vcodec libx264 -b:v 5M -acodec aac -b:a 256k -f flv \
#rtmp://lax.contribute.live-video.net/app/live_249421641_v1GnwqvHCwvTWdb6LFY5Dy7wRDLTas
