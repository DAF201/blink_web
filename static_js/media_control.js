var CURRENT_MEDIA_TYPE = "MUSIC"
var MEDIA_PLAYING = false

function play_random_music() {
    document.getElementById("media_music").src = "/music?music=random"
    document.getElementById("media_music").play()
    document.getElementById("media_video").pause()
    document.getElementById("media_music_now_playing").innerHTML = "random"
    CURRENT_MEDIA_TYPE = "MUSIC"
    MEDIA_PLAYING = true
}
function play_random_video() {
    document.getElementById("media_video").src = "/video?video=random"
    document.getElementById("media_video").play()
    document.getElementById("media_music").pause()
    document.getElementById("media_video_now_playing").innerHTML = "random"
    CURRENT_MEDIA_TYPE = "VIDEO"
    MEDIA_PLAYING = true
}
function load_songs() {
    request("get", "/music?music=get_list", [], function (args) {
        let media_music_list = document.getElementById("media_music_list")
        music_playlist = JSON.parse(args)
        for (let i = 0; i < music_playlist.length; i++) {
            media_music_list.insertAdjacentHTML("beforeend", "<h2 onclick=play_music(this)>" + music_playlist[i] + "</h2>")
        }
    })
}
function load_videos() {
    request("get", "/video?video=get_list", [], function (args) {
        let media_video_list = document.getElementById("media_video_list")
        video_playlist = JSON.parse(args)
        for (let i = 0; i < video_playlist.length; i++) {
            media_video_list.insertAdjacentHTML("beforeend", "<h2 onclick=play_video(this)>" + video_playlist[i] + "</h2>")
        }
    })
}
function play_music(obj) {
    document.getElementById("media_music").src = "/music?music=" + obj.innerHTML
    document.getElementById("media_music").play()
    document.getElementById("media_video").pause()
    document.getElementById("media_music_now_playing").innerHTML = obj.innerHTML
    CURRENT_MEDIA_TYPE = "MUSIC"
    MEDIA_PLAYING = true
}
function play_video(obj) {
    document.getElementById("media_video").src = "/video?video=" + obj.innerHTML
    document.getElementById("media_video").play()
    document.getElementById("media_music").pause()
    document.getElementById("media_video_now_playing").innerHTML = obj.innerHTML
    CURRENT_MEDIA_TYPE = "VIDEO"
    MEDIA_PLAYING = true
}
function stop_media() {
    document.getElementById("media_music").pause()
    document.getElementById("media_video").pause()
    MEDIA_PLAYING = false
}
function continue_media() {
    if (CURRENT_MEDIA_TYPE == "MUSIC") {
        document.getElementById("media_music").play()
        document.getElementById("media_video").pause()
        return
    }

    if (CURRENT_MEDIA_TYPE == "VIDEO") {
        document.getElementById("media_video").play()
        document.getElementById("media_music").pause()
        return
    }
}
function media_toggle() {
    if (MEDIA_PLAYING) {
        stop_media()
        MEDIA_PLAYING = false
    } else {
        continue_media()
        MEDIA_PLAYING = true
    }
}