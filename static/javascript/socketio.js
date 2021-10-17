var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

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

var socket = io.connect(window.location.host);

socket.on( 'connect', function() {
    socket.emit( 'my event', {
        data: 'User Connected'
    } )
    // using j query
    var form = $( '#chatform' ).on( 'submit', function( e ) {
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
        $('input.url').val('').focus() //clear text field
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

socket.on( 'my response', function( msg ) {
    console.log( msg )
    if( typeof msg.user_name !== 'undefined' ) {
        $( 'h3' ).remove()
        $( 'div.message_holder' ).append( '<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' )
    }
})

socket.on('startup', function(json) {
    console.log(json)
    init = json
})

socket.on('new url', function(json) {
    if(json['new url'] != ''){
        player.loadVideoById(json['new url'])
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

console.log('test')
