let questionCounter = $('#question-counter');
let buttons = $('.btn');
let startTime;
let stopTime;

buttons.prop('disabled', true);


let socket = new WebSocket(
    `ws://${window.location.host}/ws/game/${gameId}/`
);


socket.onopen = function () {
    console.log('Socket connection created')
};


socket.onmessage = function (e) {
    console.log('Message income');
    let data = JSON.parse(e.data);
    let message = data['message'];
    console.log(message);
    if (message['from_master']) {
        if (message['from_master']['endOfTime']) {
            greyOutButtons(buttons)
        } else if (message['from_master']['arrayOfWinners']) {
            displayRank(message);
            window.location.pathname = pathnameToChangeToAfterFinishedGame
        } else {
            displayQuestionCounter(message);
            activateButtons(buttons, message);
            startTime = Date.now()
        }

    }
};


socket.onclose = function () {
    console.error('Socket closed unexpectedly.')
};


buttons.click(function () {
    stopTime = Date.now();
    greyOutButtons(buttons);
    blackOutButton($(this));
    sendMessageToGameMaster($(this));
});



function displayQuestionCounter(message) {
    let questionCounterData = message['from_master']['questionCount'];
    questionCounter.text(`Question ${questionCounterData[0] + 1}/${questionCounterData[1]}:`);
}



function greyOutButtons(buttons) {
    buttons
        .prop('disabled', true)
        .removeClass()
        .addClass('btn col-6');
}


function blackOutButton(button) {
    button
        .removeClass()
        .addClass('btn col-6')
        .css('background-color', 'black');
}



function sendMessageToGameMaster(button) {
    let messageToSend = {
        'from_player': {
            'nickname': nickname,
            'is_correct': JSON.parse((button).attr('is_correct')),
            'millisecondsToAnswer':JSON.parse(stopTime - startTime),
        }
    };
    socket.send(JSON.stringify({
        'message': messageToSend
    }))
}



function activateButtons(buttons, message) {
    buttons.each(function (index, element) {
        let elemId = $(this).attr('id');
        $(this)
            .removeClass()
            .addClass(`col-6 btn btn-${elemId}`)
            .removeAttr('style')
            .prop('disabled', false)
            .attr('is_correct', message['from_master']['answers'][index]['is_correct'])
            .find('p')
            .text(message['from_master']['answers'][index]['answer_content']);
    });
}



function displayRank(message) {
    let rank = message['from_master']['arrayOfWinners'].indexOf(`${nickname}`);
    alert(`Congratulations! You ranked number ${rank + 1}!`);
}
