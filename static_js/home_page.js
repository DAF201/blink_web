function skip_displaying() {
    hide_element([this.param[0]])
    replace_innerHTML(this.param[1], announcement_document)
    show_element([this.param[1]])
    document.getElementById("login").style.display = "block"
    document.getElementById("media_section").style.display = "block"
    document.body.removeEventListener("click", skip_displaying)
}
let announcement_document = "Hello, this is DAF201. Sadly, Blink-in turns to be APIs only currently due to some personal reasons. Thank you for your understanding!"
let displaying_announcement = ""
async function on_load_display() {
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
