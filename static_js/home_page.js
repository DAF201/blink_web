function skip_displaying() {
    hide_element([this.param[0]])
    replace_innerHTML(this.param[1], announcement_document)
    show_element([this.param[1]])
    document.getElementById("login").style.display = "block"
    document.getElementById("announcement_media").style.display = "block"
    document.getElementById("media_section").style.display = "block"
    document.body.removeEventListener("click", skip_displaying)
}
let announcement_document = "Hello, this is DAF201. Sadly, Blink-in turns to be APIs only currently due to some personal reasons. Thank you for your understanding!"
let displaying_announcement = ""
async function on_load_display() {
    add_onload_event_listeners()
    load_songs()
    load_videos()
    for (let i = 0; i < announcement_document.length + 1; i++) {
        replace_innerHTML("announcement", displaying_announcement)
        displaying_announcement += announcement_document[i]
        if (including(announcement_document[i], ",", ".")) {
            await sleep(500)
        } else {
            await sleep(100)
        }
    }
    document.getElementById("login").style.display = "block"
    document.getElementById("announcement_media").style.display = "block"
    document.getElementById("media_section").style.display = "block"
    document.body.removeEventListener("click", skip_displaying)
}
function add_onload_event_listeners() {
    document.body.addEventListener("click", skip_displaying)
    document.body.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("login").click();
        }
        if (event.code === "KeyS") {
            if (document.getElementById("media_music_now_playing").innerHTML != "None" || document.getElementById("media_video_now_playing").innerHTML != "None") {
                media_toggle()
            }
        }
        if (event.code === "KeyF") {
            if (document.getElementById("media_music_now_playing").innerHTML != "None" || document.getElementById("media_video_now_playing").innerHTML != "None") {
                if (CURRENT_MEDIA_TYPE == "VIDEO") {
                    document.getElementById("media_video").requestFullscreen()
                }
            }
        }
    });
    document.getElementById("media_music").addEventListener("ended", (event) => {
        play_random_music()
        MEDIA_PLAYING = true
        CURRENT_MEDIA_TYPE = "MUSIC"
    })
    document.getElementById("media_music").addEventListener("play", (event) => {
        MEDIA_PLAYING = true
        CURRENT_MEDIA_TYPE = "MUSIC"
    })
    document.getElementById("media_video").addEventListener("ended", (event) => {
        play_random_video()
        MEDIA_PLAYING = true
        CURRENT_MEDIA_TYPE = "VIDEO"
    })
    document.getElementById("media_video").addEventListener("play", (event) => {
        print("TEST")
        MEDIA_PLAYING = true
        CURRENT_MEDIA_TYPE = "VIDEO"
    })
    document.body.param = ["announcement", "announcement_finished"]
}
