function skip_displaying() {
    hide_element([this.param[0]])
    replace_innerHTML(this.param[1], announcement_document)
    show_element([this.param[1]])
    document.getElementById("login").style.display = "block"
    document.getElementById("media_section").style.display = "block"
    document.body.removeEventListener("click", skip_displaying)
}
let announcement_document = "Hello, this is DAF201.<br> Sadly, Blink-in turns to be APIs only currently due to some personal reasons.<br> Thank you for your understanding!"
let displaying_announcement = ""
async function on_load_display() {
    add_onload_event_listeners()
    load_songs()
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
    });
    document.getElementById("media_music").addEventListener("ended", (event) => {
        document.getElementById("media_music").src = "/music?music=random"
        document.getElementById("media_music").play()
    })
    document.body.param = ["announcement", "announcement_finished"]
}
function play_random_music() {
    document.getElementById("media_music").src = "/music?music=random"
    document.getElementById("media_music").play()
    request('get', '/music?music=get_title', [], function (args) {
        document.getElementById("media_music_now_playing").innerHTML = args
    })
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
    document.getElementById("media_music_now_playing").innerHTML = obj.innerHTML
}