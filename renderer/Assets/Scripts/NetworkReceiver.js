//@input Asset.InternetModule serviceModule
//@input string apiEndpoint

var pollInterval = 10.0;
var lastPoll = 0.0;

function pollActivity() {
    var req = RemoteServiceHttpRequest.create();
    req.url = script.apiEndpoint;
    req.method = RemoteServiceHttpRequest.HttpRequestMethod.Get;
    
    script.serviceModule.performHttpRequest(req, function (res) {
        if (res.statusCode === 200) {
            try {
                var data = JSON.parse(res.body);
                if (data.state) {
                    print("Received activity: " + data.state);
                    
                    // safety check before calling
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