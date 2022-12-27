function console_display(data) {
    if (data.includes("\n")) { data = data.replaceAll("\n", "<br>") }
    else { data = data + "<br>" }
    data = "<p class=response>" + data + "</p>"
    document.getElementById("console").insertAdjacentHTML("beforeend", data)
    document.getElementById("console").scrollTop = (document.getElementById("console").scrollHeight)
}

function console_event_listener() {
    document.body.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            let args = {}
            args["cmd"] = document.getElementById("shell_command_input").value
            if (args["cmd"] == "\nclear") {
                let outputs = document.getElementById("screen").querySelectorAll("p")
                for (let i = 0; i < outputs.length; i++) {
                    outputs[i].remove()
                }
                document.getElementById("shell_command_input").value = ""
                return
            }
            request("POST", "/shell", JSON.stringify(args), console_display)
            document.getElementById("shell_command_input").value = ""
        }
    });
}