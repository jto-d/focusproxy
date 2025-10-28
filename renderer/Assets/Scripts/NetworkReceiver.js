//@input string apiEndpoint

var request = XMLHttpRequest();
var checkInterval = 5000;

function checkActivity() {
    request.open("GET", script.apiEndpoint, true);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var data = JSON.parse(request.responseText);
            if (data.activity) {
                global.setActivity(data.activity);
            }
        }
    };
    request.send();
}

var interval = script.createEvent("UpdateEvent");
interval.bind(function () {
    if (getTime() % checkInterval < 0.1) checkActivity();
})