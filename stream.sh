ffmpeg -re -i ~/rtorrent/download/untold-history/ep9.mkv -c:v libx264 -preset veryfast -tune zerolatency -c:a aac -ar 44100 -f flv rtmp://localhost:1935/live/STREAM_NAME
