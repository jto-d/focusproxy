//@input Component.ScriptComponent animManager
//@input string currentState = "typing"
//@input SceneObject bookObject

var animMap = {
    "chatting": "Chatting",
    "typing": "Typing",
    "relaxing": "Relaxing",
    "reading": "Reading"
};

// hide the book at startup
//if (script.bookObject) {
//    script.bookObject.enabled = false;
//}

script.animManager.setState('Typing', 0);

function setActivity(activity) {
    if (animMap[activity]) {
        script.animManager.setState(animMap[activity], 0);
        print(animMap[activity]);
        
//        if (script.bookObject) {
//            if (activity === "reading") {
//                script.bookObject.enabled = true;
//            } else {
//                script.bookObject.enabled = false;
//            }
//        }
    } else {
        print("MEOWMEOWMEOW")
    }
}

// Listen for external updates
global.setActivity = setActivity;