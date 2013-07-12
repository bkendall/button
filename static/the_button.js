var btn = $('button#the_button');
var messages = $('textarea#messages');
var host = $('div#hostname').html();
var ws = new WebSocket('ws://' + host + '/ws');

function set_state(state) {
    if (state === 1) {
        btn.removeClass('btn-danger');
        btn.addClass('btn-success');
    } else if (state === 0) {
        btn.removeClass('btn-success');
        btn.addClass('btn-danger');
    } else {
        console.log('Unknonwn state');
    }
};

messages.on('change', function() {
    messages.scrollTop(messages[0].scrollHeight);
});

ws.onerror = function() {
    console.log('WS has an error.');
}

ws.onopen = function() {
    ws.send(JSON.stringify(
        {'init': true}
    ));
};

ws.onmessage = function(e) {
    var data = $.parseJSON(e.data);
    if (data.state !== undefined) {
        set_state(data.state);
    }
    if (data.message !== undefined) {
        var date = new Date();
        messages.append(date.toLocaleTimeString() + ': ' +
                        data.message + '\n');
        messages.change();
    }
};

btn.click(function() {
    ws.send(JSON.stringify(
        {'state': btn.hasClass('btn-danger') ? 0 : 1}
    ));
});
