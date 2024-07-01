window.addEventListener("DOMContentLoaded", () => {
    const body            = document.querySelector("body");
    const startSection    = document.querySelector("#start");
    const titleSection    = document.querySelector("#title");
    const gameSection     = document.querySelector("#game");
    const finishSection   = document.querySelector("#finish");
    const moneyDiv        = gameSection.querySelector(".money");
    const questionDiv     = gameSection.querySelector(".question");
    const subtitleSpan    = titleSection.querySelector(".subtitle");
    const finalScoreSpan  = finishSection.querySelector(".final_score");
    const scoreboardTable = document.querySelector("#scoreboard");
    const playerCountSpan = document.querySelector("#player_count");

    const answerDiv = {
        A: gameSection.querySelector(".answers > .A"),
        B: gameSection.querySelector(".answers > .B"),
        C: gameSection.querySelector(".answers > .C"),
        D: gameSection.querySelector(".answers > .D"),
    };

    if (window.subtitle) subtitleSpan.innerText = window.subtitle;

    let startScreen = false;
    let gameStarted = false;
    let gameEnded = false;
    let index = -1;
    let selectedAnswer = "";
    let checkAnswer = false;

    const minIndex = 0;
    const maxIndex = window.questions.length - 1;

    const server_url = "/broadcast";
    const websocket = new WebSocket(server_url);

    const gotoQuestion = i => {
        if (gameEnded) return;
        if (gameStarted && !selectedAnswer) return;

        if (i < minIndex) {
            gameStarted = false;
            gameEnded   = false;
            index       = -1;
        } else if (i > maxIndex) {
            gameStarted = false;
            gameEnded   = true;
            index       = -1;
        } else {
            gameStarted    = true;
            gameEnded      = false;
            index          = i;
            selectedAnswer = "";
            checkAnswer    = false;
        }
    };

    const updateScreen = () => {
        if (startScreen) {
            startSection.classList.remove("hidden");
            titleSection.classList.add("hidden");
            gameSection.classList.add("hidden");
            finishSection.classList.add("hidden");
        } else if (gameEnded) {
            startSection.classList.add("hidden");
            titleSection.classList.add("hidden");
            gameSection.classList.add("hidden");
            finishSection.classList.remove("hidden");
        } else if (!gameStarted) {
            startSection.classList.add("hidden");
            titleSection.classList.remove("hidden");
            gameSection.classList.add("hidden");
            finishSection.classList.add("hidden");
        } else {
            startSection.classList.add("hidden");
            titleSection.classList.add("hidden");
            gameSection.classList.remove("hidden");
            finishSection.classList.add("hidden");
        }

        let question = window.questions[index];
        if (!question) return;

        moneyDiv.innerHTML    = question.money;
        questionDiv.innerHTML = question.question;
        answerDiv.A.innerHTML = question.answers[0];
        answerDiv.B.innerHTML = question.answers[1];
        answerDiv.C.innerHTML = question.answers[2];
        answerDiv.D.innerHTML = question.answers[3];

        for (let char of ["A", "B", "C", "D"]) {
            answerDiv[char].classList.remove("selected");
            answerDiv[char].classList.remove("correct");
            answerDiv[char].classList.remove("wrong");
        }

        if (selectedAnswer !== "") {
            answerDiv[selectedAnswer].classList.add("selected");
        }

        if (selectedAnswer && checkAnswer) {
            answerDiv[selectedAnswer].classList.remove("selected");
            answerDiv[selectedAnswer].classList.add(selectedAnswer === question.correct ? "correct" : "wrong");

            // Wrong answer selected - finish game early!
            if (selectedAnswer !== question.correct) {
                gameEnded = true;
            } else {
                updateScore(question.money);
            }

            window.setTimeout(function() {
                gotoQuestion(index + 1);
                updateScreen();
            }, 2000);
        }
    };

    const updateScore = new_score => {
        finalScoreSpan.textContent = new_score;

        websocket.send(JSON.stringify({
            player: window.player_name,
            score:  new_score,
        }));
    };

    body.addEventListener("keyup", event => {
        let key = event.key.toUpperCase();

        switch (key) {
            case "A":
            case "B":
            case "C":
            case "D":
                // Antwort auswählen oder abwählen
                if (selectedAnswer === key) selectedAnswer = "";
                else selectedAnswer = key;

                checkAnswer = false;
                break;

            case "ENTER":
            case "SPACE":
                // Antwort prüfen
                if (startScreen) {
                    startScreen = false;
                    gameStarted = false;
                } else if (!gameStarted) {
                    gotoQuestion(minIndex);
                }

                if (selectedAnswer !== "") checkAnswer = !checkAnswer;
                break;
        }

        updateScreen();
    });

    updateScreen();

    // -------- Websocket ------------
    websocket.onopen = event => {
        console.log("ON OPEN", event);

        websocket.send(JSON.stringify({
            player: window.player_name,
            score:  "0 €",
        }));
    }

    websocket.onerror = event => {
        console.log("ON ERROR", event);
    };

    websocket.onclose = event => {
        console.log("ON CLOSE", event);
    };

    websocket.onmessage = event => {
        console.log("ON MESSAGE", event);
        let data = event.data;
        
        if (data instanceof Blob) {
            const reader = new FileReader();
            reader.onload = event => {
                onWebsocketMessage(event.target.result);
            };
            reader.readAsText(data);
        } else {
            onWebsocketMessage(event.data);
        }
    };

    const players = {};

    const onWebsocketMessage = data => {
        data = JSON.parse(data);
        console.log("WS MESSAGE", data);

        players[data.player] = {
            player: data?.player || "No name",
            score:  data?.score  || "---",
        };

        updateScoreBoard();
    };

    const updateScoreBoard = function() {
        playerCountSpan.textContent = Object.keys(players).length;
        scoreboardTable.innerHTML = "";

        for (let key of Object.keys(players)) {
            let player = players[key];

            scoreboardTable.innerHTML += `<tr>
                <td class="player_name">${player.player}</td>
                <td class="player_score">${player.score}</td>
            </tr>`;
        }
    }
});
