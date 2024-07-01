window.addEventListener("DOMContentLoaded", () => {
    const body           = document.querySelector("body");
    const startSection   = document.querySelector("#start");
    const titleSection   = document.querySelector("#title");
    const gameSection    = document.querySelector("#game");
    const finishSection  = document.querySelector("#finish");
    const moneyDiv       = gameSection.querySelector(".money");
    const questionDiv    = gameSection.querySelector(".question");
    const subtitleSpan   = titleSection.querySelector(".subtitle");
    const finalScoreSpan = finishSection.querySelector(".final_score");

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
});