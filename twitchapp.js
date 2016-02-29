var twitch_api_root = "https://api.twitch.tv/kraken"
var channel_apis = {"channels": "https://api.twitch.tv/kraken/channels/" + twitch_username};

function getTwitch(api_url, token, callback){
    var hdr = {'Accept': 'application/vnd.twitchtv.v3+json'}
    if(token) hdr['Authorization'] = 'OAuth ' + token;
    $.ajax({dataType: "json",
            url: api_url,
            type: "GET",
            headers: hdr,
            success: function(data) { console.log('success', data);
                                      callback(data);},
            error: function(data) { console.log('error', data);
                                      callback(data);}
            });
}

function show_stat(ret){
    $("#result").html(ret["status"]);
    $("#game").html(ret["game"]);
}

function setTwitch(api_url, token, callback, settings){
    $.ajax({dataType: "json",
            url: api_url,
            type: "PUT",
            contentType: "application/json",
            data: JSON.stringify(settings),
            headers: {'Accept': 'application/vnd.twitchtv.v3+json',
                      'Authorization': 'OAuth ' + token},
            success: function(data) { console.log('success', data);
                                      callback(data);},
            error: function(data) { console.log('error', data);
                                      callback(data);}
            });
}

function get_twitch_apis(root_resp){
    if(!root_resp["token"]["valid"]) {
        alert("fuck!");
        return;
    }

    twitch_username = root_resp["token"]["user_name"];
    channel_apis = root_resp["_links"];
}

$(document).ready(function(){
    /*
    $("#load").click(function(){
        getTwitch(twitch_api_root, access_token, get_twitch_apis);
    });
    */

    $("#getinfo").click(function(){
        // $(this).hide();
        // $("#result").html("MOE");
        getTwitch(channel_apis["channels"], null, show_stat);
    });
    $("#setinfo").click(function(){
        setTwitch(channel_apis["channels"], access_token, show_stat, stat);
    });
});
