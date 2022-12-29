function play_random_music() {
    document.getElementById("media_music").src = "/music?music=random"
    document.getElementById("media_music").play()
    document.getElementById("media_video").pause()
    document.getElementById("media_music_now_playing").innerHTML = "random"
}
function load_songs() {
    request('get', '/music?music=get_list', [], function (args) {
        let media_music_list = document.getElementById("media_music_list")
        music_playlist = JSON.parse(args)
        for (let i = 0; i < music_playlist.length; i++) {
            media_music_list.insertAdjacentHTML("beforeend", "<h2 onclick=play_music(this)>" + music_playlist[i] + "</h2>")
        }
    })
}
function play_music(obj) {
    document.getElementById("media_music").src = "/music?music=" + obj.innerHTML
    document.getElementById("media_music").play()
    document.getElementById("media_video").pause()
    document.getElementById("media_music_now_playing").innerHTML = obj.innerHTML
}

function stop_media() {
    document.getElementById("media_music").pause()
}

function continue_media() {
    document.getElementById("media_music").play()
    document.getElementById("media_video").pause()
}