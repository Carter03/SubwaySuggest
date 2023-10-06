const eel = require("/eel.js")

eel.expose(reload);
function reload() {
    console.log("test reload");
    window.location.reload();
}

eel.expose(kill);
function kill() {
    window.close();
}