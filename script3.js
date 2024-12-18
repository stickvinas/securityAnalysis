window.addEventListener("DOMContentLoaded", function () {
    let container = document.getElementById("main")
    let saveToJsonButton = document.getElementById("saveJsonButton")
    let loadToJsonButton = document.getElementById("loadJsonButton")
    let postDataButton = document.getElementById("postDataButton")
    let fillRandomButton = document.getElementById("fillRandomButton")
    let varBlock = createVarBlock();
    let funcBlock = createFuncBlock();
    let qFuncBlock = createQFuncBlock();

    let jsonData = localStorage.getItem("jsonData3")
    if (jsonData) {
        data = convertJsonToData(jsonData)
        varBlock.setData(data)
        funcBlock.setData(data)
        qFuncBlock.setData(data)
    }

    container.append(varBlock.block);
    container.append(funcBlock.block);
    container.append(qFuncBlock.block);

    saveToJsonButton.onclick = () => {
        saveJSONToFile(convertDataToJson(varBlock, funcBlock, qFuncBlock))
    }

    loadToJsonButton.onclick = () => {
        loadJSONFromFile()
            .then((result) => {
                let data = convertJsonToData(result)
                varBlock.setData(data)
                funcBlock.setData(data)
                qFuncBlock.setData(data)
            })
            .catch((e) => console.log(e))
    }

    postDataButton.onclick = () => {
        postDataButton.disabled = true
        let body = convertDataToJson(varBlock, funcBlock, qFuncBlock)
        localStorage.setItem("jsonData3", body)
        postData("http://127.0.0.1:9090/calcAndDraw_hdd", body,
            () => {
                document.querySelectorAll('#imageGallery .plot').forEach(img => {
                    img.src += '?t=' + new Date().getTime();
                });
            },
            () => { },
            () => postDataButton.disabled = false)
    }

    fillRandomButton.onclick = () => {
        varBlock.fillRandom(0.85)
        funcBlock.fillRandom(0.85)
        qFuncBlock.fillRandom(0.85)
    }
});

function createVarBlock() {
    let varNames = [
        "Эффективность функционирования хранилища данных",
        "Качество программного обеспечения (ПО)",
        "Корректность ПО",
        "Надежность программного обеспечения",
        "Доступность программного обеспечения",
        "Возможность интенсивного использования ПО",
        "Прослеживаемость ПО",
        "Функциональная полнота ПО",
        "Обеспечение требуемой последовательности работ при проектировании хранилища",
        "Практичность ПО",
        "Устойчивость к ошибкам данных программного обеспечения",
        "Эффективность выполнения транзакций",
        "Степень мотивации персонала, осуществляющего эксплуатацию хранилища данных",
        "Удобство тестирования ПО"
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

    return NewBlock(["Название переменной", "Начальное значение", "Предельное значение"], "var", rowNameFunc, cellNameFunc)
}

function createFuncBlock() {
    let flArray = new Array();
    flArray.push(
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1,
        4, 6, 9, 10, 13,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        1, 2, 3, 4, 6, 9, 10,
        1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        1, 2, 3, 4, 8, 10, 12, 13, 14, 5, 6,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14,
        1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 9,
        5, 7, 11, 13, 14);
    power = 3;

    rowNameFunc = function (i) {
        if (i >= flArray.length) {
            return "";
        }
        return RowNameWithIndex("f", i + 1)
    }

    cellNameFunc = function (i, j) {
        if (i >= flArray.length) {
            return "";
        }
        return PolynomicCellName("X", flArray[i], "(t)", power - j)
    }

    return NewBlock(["Функции", "", "", "", ""], "x", rowNameFunc, cellNameFunc)
}


function createQFuncBlock() {
    let varNames = [
        "ζ_i – увеличение количества источников новых данных, предназначенных для интеграции с данными хранилища",
        "ζ_i - частота изменения периодов сдачи финансовой отчетности предприятия",
        "ζ_i - сокращение квалифицированной поддержки вендора, вызванное ужесточением режима санкций",
        "ζ_i - рост интенсивности перехода на Open Source решения при развитии хранилища данных",
        "ζ_i - увеличение количества новых стандартов при реализации Open Source решений",
    ]

    let rowNameFunc = function (i) {
        if (i >= varNames.length) {
            return ""
        }

        let sp = document.createElement("span")
        sp.innerHTML = varNames[i].replace("_i", `<sub>${i + 1}</sub>`)
        return sp;
    }

    let cellNameFunc = function (i, j) {
        if (i >= varNames.length) {
            return "";
        }

        return PolynomicCellName("t", "", "", power - j)
    }

    return NewBlock(["Функция", "", "", "", ""], "qfunc", rowNameFunc, cellNameFunc)
}

function convertDataToJson(varBlock, funcBlock, qFuncBlock) {
    let result = {
        start: new Array(0),
        max_values: new Array(0),
        coef: new Array(0),
        q: new Array(0)
    }

    var data = varBlock.getData()
    for (let i = 0; i < data.length; i++) {
        result.start.push(data[i][0])
        result.max_values.push(data[i][1])
    }

    data = funcBlock.getData();
    for (let i = 0; i < data.length; i++) {
        result.coef[i] = data[i]
    }

    data = qFuncBlock.getData();
    for (let i = 0; i < data.length; i++) {
        result.q[i] = data[i]
    }

    return JSON.stringify(result)
}

function convertJsonToData(jsonString) {
    let data = {
        var: new Array(),
        x: new Array(),
        qfunc: new Array()
    }

    let parsedJson = JSON.parse(jsonString)
    for (let i = 0; i < parsedJson.start.length; i++) {
        data.var.push([parsedJson.start[i], parsedJson.max_values[i]])
    }

    for (let i = 0; i < parsedJson.q.length; i++) {
        data.qfunc.push(parsedJson.q[i])
    }

    for (let i = 0; i < parsedJson.coef.length; i++) {
        data.x.push(parsedJson.coef[i])
    }

    return data
}