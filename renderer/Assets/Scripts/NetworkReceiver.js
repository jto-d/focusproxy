//@input Asset.InternetModule serviceModule
//@input string apiEndpoint
//@input string targetComputer

var pollInterval = 10.0;
var lastPoll = 0.0;

function pollActivity() {
    var req = RemoteServiceHttpRequest.create();
    var endpoint = script.apiEndpoint;
    if (script.targetComputer) {
        var separator = endpoint.indexOf('?') === -1 ? '?' : '&';
        endpoint = endpoint + separator + 'computer=' + script.targetComputer;
    }
    req.url = endpoint;
    req.method = RemoteServiceHttpRequest.HttpRequestMethod.Get;
    
    script.serviceModule.performHttpRequest(req, function (res) {
        if (res.statusCode === 200) {
            try {
                var data = JSON.parse(res.body);
                if (data.state) {
                    print("Received activity: " + data.state);
                    
                    global.setActivity(data.state.toLowerCase());
                }
            } catch (err) {
                print("Error parsing response: " + err);
            }
        } else {
            print("HTTP error " + res.statusCode + ": " + res.body);
        }
    });
}

var updateEvent = script.createEvent("UpdateEvent");
updateEvent.bind(function (eventData) {
    if (getTime() - lastPoll > pollInterval) {
        pollActivity();
        lastPoll = getTime();
    }
});