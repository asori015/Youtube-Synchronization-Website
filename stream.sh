#ffmpeg -re -i /home/asl345/rtorrent/download/untold-history/ep1.mkv -vcodec copy -loop -1 -c:a aac -b:a 160k -ar 44100 -strict -2 -f flv http://localhost:8081/supersecret
ffmpeg \
    -re -i /home/asl345/rtorrent/download/untold-history/ep1.mkv -vcodec copy -loop -1 -c:a aac -b:a 160k -ar 44100 -strict -2 \
    -f mpegts \
		-codec:v mpeg1video -s 640x480 -b:v 1000k -bf 0 \
	http://localhost:8081/supersecret
	# -f v4l2 \
		# -framerate 25 -video_size 640x480 -i /home/asl345/rtorrent/download/untold-history/ep1.mkv \
    # -re -i /home/asl345/rtorrent/download/untold-history/ep1.mkv -vcodec copy -loop -1 -c:a aac -b:a 160k -ar 44100 -strict -2 -f flv http://localhost:8081/supersecret
	# -f mpegts \
		# -codec:v mpeg1video -s 640x480 -b:v 1000k -bf 0 \
	# http://localhost:8081/supersecret

# ffmpeg \
