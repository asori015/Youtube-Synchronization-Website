var socket = io.connect('http://' + document.domain + ':' + location.port);

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

socket.on( 'my response', function( msg ) {
    console.log( msg )
    if( typeof msg.user_name !== 'undefined' ) {
        $( 'h3' ).remove()
        $( 'div.message_holder' ).append( '<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' )
    }
})

socket.on('startup', function(json) {
    player.loadVideoById(json['url'])
    player.seekTo(json['seconds'])
    if(json['state'] == 'True'){
        player.playVideo()
    }
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

function onStateChange(event){
    console.log(event.data)
}
