//@input Component.ScriptComponent pollingScript
//@input string deviceName
//@input Component.InteractionComponent touchComponent
//@input Component.RenderMeshVisual boxVisual
//@input Component.Text textComponent

var hasDisappeared = false;

function hideButton() {
    if (hasDisappeared) return;
    
    hasDisappeared = true;
    script.boxVisual.enabled = false;
    script.textComponent.enabled = false;
    script.touchComponent.enabled = false;
    print("Button hidden");
}

var delayedEvent = script.createEvent("DelayedCallbackEvent");
delayedEvent.bind(hideButton);
delayedEvent.reset(10.0);

script.touchComponent.onTap.add(function () {
    if (script.pollingScript && script.pollingScript.api.setTargetComputer) {
        script.pollingScript.api.setTargetComputer(script.deviceName);
        print("BUTTON PRESS");
        
        hideButton();

    } else {
        print("ERROR");
    }
});