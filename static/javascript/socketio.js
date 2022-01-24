// Youtube API initialization
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

ip = ""

var player;
var init;
function onYouTubeIframeAPIReady() {
    var url = 'M7lc1UVf-VE'
    if(init !== undefined){
        url = init['url']
    }
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: url,
        events: {
            'onReady': onPlayerReady
        },
        playerVars: {
            autoplay: 0
        }
    });
}

// Websocket initialization
var socket = io.connect(window.location.host);

// Socket connection event
socket.on( 'connect', function() {
    socket.emit( 'my event', {
        data: 'User Connected'
    } )

    // Setting up jquery forms
    var form = $('#chatform').on('submit', function(e) {
        e.preventDefault()
        let user_name = $( 'input.username' ).val()
        let user_input = $( 'input.message' ).val()
        socket.emit( 'my event', {
            user_name : user_name,
            message : user_input
        } )
        $( 'input.message' ).val( '' ).focus()
    } )

    var form = $('#youtubeurl').on('submit', function(e){
        e.preventDefault()
        let url = $('input.url').val()
        socket.emit('new url', {
            url : url
        })
        $('input.url').val('').focus() // clear text field
    })

    var form = $('#livestreamip').on('submit', function(e){
        e.preventDefault()
        ip = $('input.ip').val()
        // socket.emit('new ip', {
        //     ip : ip
        // })
        $('input.ip').val('').focus() // clear text field
    })
} )

function onPlayerReady(event) {
    // event.target.stopVideo()
    event.target.seekTo(init['seconds'])
    
    if(init['state'] == 'True'){
        event.target.playVideo()
    }
    else{
        event.target.stopVideo()
        // event.target.seekTo(init['seconds'])
    }
}

socket.on('my response', function(msg){
    console.log(msg) // debug
    if(typeof msg.user_name !== 'undefined'){
        $('h3').remove()
        $('div.message_holder').append('<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>')
    }
})

socket.on('startup', function(json) {
    console.log(json) // debug
    init = json
})

//
socket.on('new url', function(json) {
    if(json['new url'] != ''){
        player.loadVideoById(json['new url'])
    }
})

socket.on('new ip', function(json) {
    if(json['new ip'] != ''){
        console.log(json['new ip']) // debug
    }
})

socket.on('play', function(json){
    player.seekTo(json['seconds'])
    player.playVideo()
})

socket.on('pause', function(){
    player.pauseVideo()
})

function playFunction(){
    socket.emit('play')
}

function pauseFunction(){
    socket.emit('pause', {seconds:player.getCurrentTime()})
}

function debugFunction(){
    socket.emit('debug')
}

function flvPlayFunction(){
    if (flvjs.isSupported()) {
        console.log('flvjs supported') // debug
        var videoElement = document.getElementById('videoElement');
        var flvPlayer = flvjs.createPlayer({
            type: 'flv',
            url: ip
            //url: 'http://localhost:5000/live/MYSTREAM.flv'
        });
        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
        flvPlayer.play();
    }
}