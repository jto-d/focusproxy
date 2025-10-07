//@input Component.ScriptComponent animManager
//@input string statesCSV = "idle_stretch,typing_loop,seated_idle"
//@input string durationsCSV = "2,10,20"
//@input float blend = 0.25
//@input bool loop = true

script.animManager.setState('idle', 0);

var delayedTyping = script.createEvent("DelayedCallbackEvent");
delayedTyping.bind(function(eventData)
{
    script.animManager.setState('typing_loop', 1);
});

delayedTyping.reset(10);
print("delayed started");

var delayedStretch = script.createEvent("DelayedCallbackEvent");
delayedStretch.bind(function(eventData)
{
    script.animManager.setState('idle_stretch', 1);
});

delayedStretch.reset(20);
print("delayed started");

var delayedTypingt = script.createEvent("DelayedCallbackEvent");
delayedTypingt.bind(function(eventData)
{
    script.animManager.setState('typing_loop', 1);
});

delayedTypingt.reset(24);
print("delayed started");


script.animManager.addParameter('isStretching', true);
//script.animManager.setParameter('isTyping', true);