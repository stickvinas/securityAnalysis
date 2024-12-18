console.log("script4.js загружен!");
window.addEventListener("DOMContentLoaded", function () {
    console.log("DOM загружен!");
    let container = document.getElementById("main")
    let saveToJsonButton = document.getElementById("saveJsonButton")
    let loadToJsonButton = document.getElementById("loadJsonButton")
    let postDataButton = document.getElementById("postDataButton")
    let recoveryBlock = createRecoveryBlock();
    let failureBlock = createFailureBlock();
    
    if (!postDataButton) {
        console.error("Ошибка: Кнопка 'postDataButton' не найдена в DOM!");
        return;
    }

    console.log("Кнопка найдена. Привязываем событие.");
    postDataButton.onclick = () => {
        console.log("Кнопка 'Рассчитать' нажата!");
    };

    let jsonData = localStorage.getItem("jsonData4")
    if (jsonData) {
        data = convertJsonToData(jsonData)
        recoveryBlock.setData(data)
        failureBlock.setData(data)
    }

    container.append(recoveryBlock.block);
    container.append(failureBlock.block);

    saveToJsonButton.onclick = () => {
        saveJSONToFile(convertDataToJson(recoveryBlock, failureBlock))
    }

    loadToJsonButton.onclick = () => {
        loadJSONFromFile()
            .then((result) => {
                let data = convertJsonToData(result)
                recoveryBlock.setData(data)
                failureBlock.setData(data)
            })
            .catch((e) => console.log(e))
    }

    postDataButton.onclick = () => {
        postDataButton.disabled = true
        let body = convertDataToJson(recoveryBlock, failureBlock)
        localStorage.setItem("jsonData4", body)
        console.log("Отправка данных на сервер:", body);
        postData("https://securityanalysis.onrender.com/calcAndDraw_pc", body,
            () => {
                document.querySelectorAll('#imageGallery .plot').forEach(img => {
                    img.src += '?t=' + new Date().getTime();
                });
            },
            () => { },
            () => postDataButton.disabled = false)
    }
});

function createRecoveryBlock() {
    let varNames = [
        "Компьютер 1",
        "Компьютер 2",
        "Компьютер 3",
        "Компьютер 4",
        "Компьютер 5",
    ]

    let rowNameFunc = function (i) {
        if (i >= varNames.length) {
            return ""
        }

        return varNames[i];
    }

    let cellNameFunc = function (i, j) {
        if (i >= varNames.length) {
            return "";
        }

        return " ";
    }

    return NewBlock(["Интенсивности потоков восстановления", ""], "recovery", rowNameFunc, cellNameFunc)
}

function createFailureBlock() {
    let varNames = [
        "Компьютер 1",
        "Компьютер 2",
        "Компьютер 3",
        "Компьютер 4",
        "Компьютер 5",
    ]

    let rowNameFunc = function (i) {
        if (i >= varNames.length) {
            return ""
        }

        return varNames[i];
    }

    let cellNameFunc = function (i, j) {
        if (i >= varNames.length) {
            return "";
        }

        return " ";
    }

    return NewBlock(["Интенсивности потоков отказа", ""], "failure", rowNameFunc, cellNameFunc)
}

function convertDataToJson(recoveryBlock, failureBlock) {
    let result = {
        mu: new Array(0),
        lat: new Array(0)
    }

    var data = recoveryBlock.getData()
    for (let i = 0; i < data.length; i++) {
        result.mu.push(data[i][0])
    }

    var data = failureBlock.getData()
    for (let i = 0; i < data.length; i++) {
        result.lat.push(data[i][0])
    }

    return JSON.stringify(result)
}

function convertJsonToData(jsonString) {
    let data = {
        recovery: new Array(),
        failure: new Array()
    }

    let parsedJson = JSON.parse(jsonString)
    for (let i = 0; i < parsedJson.mu.length; i++) {
        data.recovery.push([parsedJson.mu[i]])
    }

    for (let i = 0; i < parsedJson.lat.length; i++) {
        data.failure.push([parsedJson.lat[i]])
    }

    return data
}