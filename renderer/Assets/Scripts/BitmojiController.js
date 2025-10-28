//@input Component.ScriptComponent animManager
//@input string currentState = "typing"

var animMap = {
    "chatting": "Chatting",
    "typing": "Typing",
    "relaxing": "Relaxing",
    "reading": "Reading"
};

script.animManager.setState('Typing', 0);

function setActivity(activity) {
    if (animMap[activity]) {
        script.animManager.setState(animMap[activity], 0);
        print(animMap[activity]);
//        script.bitmoji.getComponent("AnimationMixer").play(animMap[activity]);
    } else {
        print("MEOWMEOWMEOW")
//        script.bitmoji.getComponent("AnimationMixer").play(animMap["idle"]);
    }
}

// Listen for external updates
global.setActivity = setActivity;