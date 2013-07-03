var btn = $('button#the_button');
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

var host = $('div#hostname').html();
var ws = new WebSocket('ws://' + host + '/ws);
ws.onopen = function() {
    ws.send('{}');
};
ws.onmessage = function(e) {
    data = $.parseJSON(e.data);
    console.log(data);
    set_state(data.state);
};

btn.click(function() {
    state = btn.hasClass('btn-danger') ? 0 : 1;
    ws.send(JSON.stringify({'state': state}));
});
