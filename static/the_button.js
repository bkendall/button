var btn = $('button#the_button');
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

ws.onopen = function() {
    if (ws.readyState != 1) {
        console.log('WS not open.');
        return;
    }
    ws.send(JSON.stringify({'init': true}));
};

ws.onmessage = function(e) {
    var data = $.parseJSON(e.data);
    set_state(data.state);
};

btn.click(function() {
    if (ws.readyState != 1) {
        console.log('WS not open to send.');
        return;
    }
    var state = btn.hasClass('btn-danger') ? 0 : 1;
    var data = JSON.stringify({'state': state});
    ws.send(data);
});
