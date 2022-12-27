
function print(str) {
    console.log(str)
}
function replace_innerHTML(id, str) {
    document.getElementById(id).innerHTML = str
}
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function including(Obj, ...Objs) {
    return Objs.includes(Obj)
}
function hide_element(id) {
    for (let i = 0; i < id.length; i++) {
        document.getElementById(id[i]).style.display = "none"
    }
}
function show_element(id) {
    for (let i = 0; i < id.length; i++) {
        document.getElementById(id[i]).style.display = "block"
    }
}
function element_display_toggle(id) {
    for (let i = 0; i < id.length; i++) {
        if (document.getElementById(id[i]).style.display != "none") {
            document.getElementById(id[i]).style.display = "none"
        } else {
            document.getElementById(id[i]).style.display = "block"
        }
    }
}

function request(mathod, URL, param, callback = function () { }, callback_args = []) {
    let http_request = new XMLHttpRequest()
    try {
        http_request.open(mathod, URL)
        http_request.send(param)
        http_request.onloadend = function () {
            data_backup = http_request.responseText
            callback(http_request.responseText, callback_args)
        }
    } catch (err) {
        print(err)
    }
}