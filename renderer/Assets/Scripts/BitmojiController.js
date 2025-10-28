//@input Component.ScriptComponent animManager
//@input string currentState = "typing"
//@input SceneObject bookObject
//@input SceneObject monitorObject

var animMap = {
    "chatting": "Chatting",
    "typing": "Typing",
    "relaxing": "Relaxing",
    "reading": "Reading"
};

// hide the book at startup
if (script.bookObject) {
    script.bookObject.enabled = false;
}

if (script.monitorObject) {
    script.monitorObject.enabled = true;
}

script.animManager.setState('Typing', 0);

function setActivity(activity) {
    if (animMap[activity]) {
        script.animManager.setState(animMap[activity], 0);
        print(animMap[activity]);
        
        if (script.bookObject) {
            if (activity === "reading") {
                script.bookObject.enabled = true;
            } else {
                script.bookObject.enabled = false;
            }
        }
        if (script.monitorObject) {
            if (activity === "typing" || activity === "relaxing") {
                script.monitorObject.enabled = true;
            } else {
                script.monitorObject.enabled = false;
            }
        }
    } else {
        print("MEOWMEOWMEOW")
    }
}

// Listen for external updates
global.setActivity = setActivity;