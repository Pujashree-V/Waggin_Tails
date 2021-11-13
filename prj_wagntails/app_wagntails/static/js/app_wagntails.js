var text_box = '<div class="chat-message-right pb-4">' +
    '<div></div><div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3"><div class="font-weight-bold mb-1">{sender}</div>' +
    '{message}' +
    '</div></div>';

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

function send(sender, receiver, message) {
    alert("im in send")
    $.post('/api/messages/', '{"sender": "' + sender + '", "receiver": "' + receiver + '","message": "' + message + '" }', function (data) {
        console.log(data);
        alert("I am in post")
        var box = text_box.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
    $.get('/api/messages/' + sender_id + '/' + receiver_id, function (data) {
        console.log(data);
        alert("im in get")
        if (data.length !== 0) {
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('chat-message-right', 'chat-message-left');
                box = box.replace('mr-3', 'ml-3')
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}
