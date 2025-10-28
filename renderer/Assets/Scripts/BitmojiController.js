//@input SceneObject bitmoji
//@input string currentState = "idle"

var animMap = {
    "reading": "Reading",
    "typing": "Typing",
    "stretching": "Stretching",
    "idle": "Idle"
};

function setActivity(activity) {
    if (animMap[activity]) {
        script.bitmoji.getComponent("AnimationMixer").play(animMap[activity]);
    } else {
        script.bitmoji.getComponent("AnimationMixer").play(animMap["idle"]);
    }
}

// Listen for external updates
global.setActivity = setActivity;