//@input Component.ScriptComponent animManager
//@input string currentState = "idle"

var animMap = {
    "reading": "Reading",
    "typing": "typing_loop",
    "stretching": "Stretching",
    "idle": "Idle"
};

script.animManager.setState('idle', 0);

function setActivity(activity) {
    if (animMap[activity]) {
        script.animManager.setState('typing_loop', 1);
        print(animMap[activity]);
//        script.bitmoji.getComponent("AnimationMixer").play(animMap[activity]);
    } else {
        print("MEOWMEOWMEOW")
//        script.bitmoji.getComponent("AnimationMixer").play(animMap["idle"]);
    }
}

// Listen for external updates
global.setActivity = setActivity;