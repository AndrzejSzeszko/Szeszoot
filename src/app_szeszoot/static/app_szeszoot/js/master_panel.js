let divPlayers = $('#div-players');
let quizJson = JSON.parse($('#quizJson').text());
let button = $('#button');
let questionCount = quizJson['question_set'].length;
let questionCounter = $('#question-counter');
let answers = $('.answer');
let question = $('#question');
let timer = $('#timer');
let currentQuestionIndex = -1;
let currentCorrectAnswer = null;
let players = {};
let globalClock;
let answerTime = 20;
let socket = new WebSocket(
    `ws://${window.location.host}/ws/game/${gameId}/`
);


questionCounter.text(`${currentQuestionIndex + 1}/${questionCount}`);
console.log(typeof(quizJson), quizJson);


socket.onopen = function() {
    console.log('WebSockets connection created.')
};


socket.onmessage = function(e) {
    console.log('message incame');
    let data = JSON.parse(e.data);
    console.log('data', data);
    let message = data['message'];
    if (message['from_player_joined_signal']) {
        addPlayerToList(message);
    } else if (message['from_player']) {
        markPlayerAnswered(message);
    }
};


socket.onclose = function () {
    console.error('Socket closed unexpectedly.')
};


button.click(function () {
    currentQuestionIndex += 1;

    if ($(this).text() === 'Finish!') {
        let playersTotalPointsArrayOfArrays = getPlayersTotalPointsArrayOfArrays(players);
        let alertResultString = getAlertResultsString(playersTotalPointsArrayOfArrays);
        sendArrayOfWinnersToPlayers(playersTotalPointsArrayOfArrays);
        alert(alertResultString);
        window.location.pathname = pathnameToChangeToAfterFinishedGame
    }
    displayPlayersTotalScoreButNotPointsGainedLastly();
    displayQuestionCounter();
    markAllPlayersUnanswered();
    displayQuestion();
    displayAnswers();
    displayTimer();
    startTimer();
    changeButtonTextToNextQuestionOrFinish($(this));
    sendAnswersToPlayers();
});



function addPlayerToList(message) {
    let nickname = message['from_player_joined_signal']['nickname'];
    players[`${nickname}`] = new Array(questionCount).fill(null);
    console.log('players', players);
    divPlayers.after(`
            <p id="${nickname}" class="p-player">
                <span id="nickname">${nickname}</span>
                <span id="gained-points"></span>
                <span id="total-points"></span>
            </p>
    `)
}



function markPlayerAnswered(message) {
    let nickname = message['from_player']['nickname'];
    let pointsCoefficient = (answerTime * 1000 - message['from_player']['millisecondsToAnswer']) / (answerTime * 1000);
    let pointsCoefficientMultiplicatedAndRounded = Math.floor(pointsCoefficient * 1000);
    players[nickname][`${currentQuestionIndex}`] = pointsCoefficientMultiplicatedAndRounded * message['from_player']['is_correct'];
    $(`#${nickname}`)
        .css('font-weight', 'Bold')
        .attr('answered', 'true');
    let allCurrentPlayers = $('.p-player');
    let currentPlayersThatAnsweredYet = $('.p-player[answered="true"]');
    if (allCurrentPlayers.length === currentPlayersThatAnsweredYet.length) {
        endOfTimeOrAllPlayersAnswered()
    }
}



function displayPlayersTotalScoreButNotPointsGainedLastly() {
    $('.p-player').each(function () {
        let nickname = $(this).attr('id');
        $(this)
            .find('#gained-points')
            .text('')
            .next()
            .text(`${players[nickname].reduce(sumElemInArray)}`)
    });
}



function displayQuestionCounter() {
    questionCounter.text(`${currentQuestionIndex + 1}/${questionCount}`);
}



function markAllPlayersUnanswered() {
    $('.p-player').removeAttr('style answered');
}



function displayQuestion() {
    question
        .removeClass('invisible')
        .text(quizJson['question_set'][currentQuestionIndex]['question_content']);
}



function displayAnswers() {
    answers.each(function (index, element) {
        let elemId = $(this).attr('id');
        console.log(elemId);

        $(this)
            .removeClass()
            .addClass(`col-6 btn btn-${elemId} answer`)
            .find('p')
            .text(quizJson['question_set'][currentQuestionIndex]['answer_set'][index]['answer_content']);

        if (quizJson['question_set'][currentQuestionIndex]['answer_set'][index]['is_correct']) {
            currentCorrectAnswer = $(this).text();
            console.log('correct', currentCorrectAnswer);
        }
    });
}



function displayTimer() {
    timer
        .removeClass('invisible')
        .text(answerTime);
}




function startTimer() {
    let duration = answerTime - 1;
    globalClock = setInterval(displaySeconds, 1000);
    function displaySeconds() {
        timer.text(duration);
        duration -= 1;
        if (duration < 0) {
            endOfTimeOrAllPlayersAnswered(true)
        }
    }
}




function changeButtonTextToNextQuestionOrFinish(button) {
    button
        .text(currentQuestionIndex + 1 === questionCount ? 'Finish!' : 'Next question!')
        .prop('disabled', true);
}




function sendAnswersToPlayers () {
    let messageToPlayers = {
        'from_master': {
            'questionCount': [currentQuestionIndex, questionCount],
            'answers': quizJson['question_set'][currentQuestionIndex]['answer_set']
        }
    };
    socket.send(JSON.stringify({
        'message': messageToPlayers
    }))
}



function endOfTimeOrAllPlayersAnswered(endOfTime=false) {
    clearInterval(globalClock);
    button.prop('disabled', false);
    answers.each(highlightAnswerIfCorrectAndGreyOutOtherwise);
    $('.p-player').each(updatePlayerScore);
    if (endOfTime) {
        sendEndOfTimeMessageToPlayers()
    }
}



function highlightAnswerIfCorrectAndGreyOutOtherwise() {
    $(this)
        .removeClass()
        .addClass($(this).text() === currentCorrectAnswer ? 'btn btn-success col-6 answer' : 'btn col-6 answer');
}



function updatePlayerScore() {
    let nickname = $(this).attr('id');
    $(this)
        .find('#gained-points')
        .text(`+${players[nickname][currentQuestionIndex]}`)
        .css('color', `${players[nickname][currentQuestionIndex] ? '#00ff00' : 'red'}`)
        .next()
        .text(`${players[nickname].reduce(sumElemInArray)}`)
}



function sendEndOfTimeMessageToPlayers() {
    let messageToPlayers = {
        'from_master': {
            'questionCount': [currentQuestionIndex, questionCount],
            'endOfTime': true,
        }
    };
    socket.send(JSON.stringify({
        'message': messageToPlayers
    }))
}



function sumElemInArray (total, currentValue) {
    return total + currentValue
}



function getPlayersTotalPointsArrayOfArrays(players) {
    let playersTotalPoints = Object.keys(players).map(function (key) {
        return [key, players[key].reduce(sumElemInArray)]
    });

    playersTotalPoints.sort(function (a, b) {
        return b[1] - a[1]
    });

    return playersTotalPoints
}



function sendArrayOfWinnersToPlayers(resultsArrayOfArrays) {
    let arrayOfWinners = [];
    for (let arr of resultsArrayOfArrays) {
        arrayOfWinners.push(arr[0])
    }

    let messageToPlayers = {
        'from_master': {
            'questionCount': [currentQuestionIndex, questionCount],
            'arrayOfWinners': arrayOfWinners,
        }
    };
    socket.send(JSON.stringify({
        'message': messageToPlayers
    }))
}



function getAlertResultsString(playersTotalPoints) {
    let alertResultsStr = '';
    for (let player of playersTotalPoints) {
        alertResultsStr += `${player[0]}: ${player[1]}\n`
    }
    return alertResultsStr
}
