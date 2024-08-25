params = ['temperature', 'repetition'];

document.getElementById('submit').onclick = function () {
    document.getElementById('error_message').style.visibility = "hidden";
    document.getElementById('submit').disabled = true;
    document.getElementById('loading-symbol').style.visibility = 'visible';

    clearTable()

    let jsonParams = {}
    let creativity = document.getElementById('temperature').value

    jsonParams['temperature'] = creativity * 0.1
    jsonParams['top-k'] = creativity * 10
    jsonParams['top-p'] = creativity * 0.1
    jsonParams['n_gram'] = document.getElementById('l-repetitie').checked ? 0 : 2
    jsonParams['nsfw'] = document.getElementById('nsfw').checked;
    jsonParams['prompt'] = document.getElementById('prompt').value
    jsonParams['repetition'] = (-0.1 * document.getElementById('repetition').value) + 1.999

    fetch(url + "generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(jsonParams)
    }).then(async function (data) {
        if (data.ok) {
            return data.json()
        } else {
            const text = await data.text();
            throw new Error(text);
        }
    }).then(function (data) {
        fillOptions(data)
    }).catch((error) => {
        showError(error)
    }).finally(() => {
        document.getElementById('submit').disabled = false;
        document.getElementById('loading-symbol').style.visibility = 'hidden';
    })
}

function fillOptions(data) {
    let tbl_body = document.getElementById('output-container')

    for (let i = 0; i < data.length; i++) {
        tbl_body.innerHTML = tbl_body.innerHTML +
            `
        <div id="prompt-${i}" class="choices">
            <span id="inner-text-${i}"style="white-space: pre-line; color: #58504A">${data[i]}</span>
            <div>
                <button class="image-button button-behaviour" onclick="confirmPrompt(${i})">
                    <object style="pointer-events: none;" id="finalize-object" data="../../static/svg/arrow_right.svg" type="image/svg+xml" width="80%"></object>
                </button>
            </div>
        </div>
        `
    }

    document.documentElement.scrollIntoView({
        behavior: 'smooth',
        block: 'end'
    });
}

function clearText() {
    document.getElementById('result').value = ""
    document.getElementById('prompt').value = ""
    document.getElementById('finalize').disabled = true;
    document.getElementById('finalize-vertical').disabled = true;

    clearTable()
}

function clearTable() {
    document.getElementById('output-container').innerHTML = null
}

function fillResult(newText) {
    document.getElementById('result').value = newText
}

function confirmPrompt(e) {
    let newText;

    let innerHtml = document.getElementById(`inner-text-${e}`).innerHTML;
    let prompt = document.getElementById('prompt').value;
    let result = document.getElementById('result').value;

    if (result === "") {
        newText = prompt + "\n\n" + innerHtml;
    }

    if (result !== "") {
        newText = result + "\n\n" + prompt + "\n\n" + innerHtml;
    }

    newText = captilizeNewLines(newText)

    clearTable()
    fillResult(newText)

    document.getElementById('finalize').disabled = false;
    document.getElementById('finalize-vertical').disabled = false;
}

function captilizeNewLines(text){
    let textArr = text.split('\n')
    let arr = []
    for (let i = 0; i < textArr.length; i++){
        let currentWord = textArr[i]
        arr.push(currentWord.charAt(0).toUpperCase() + currentWord.slice(1))
    }
    return arr.join('\n')
}

function showError(error) {
    document.getElementById('error_message').innerHTML = error;
    document.getElementById('error_message').style.visibility = "visible";
}


for (let i = 0; i < params.length; i++) {
    document.getElementById(params[i]).addEventListener("input", (e) => {
            document.getElementById(`${params[i]}-value`).innerHTML = e.target.value
        }
    )

    document.getElementById(`${params[i]}-value`).innerHTML = document.getElementById(params[i]).value
}

const sendToEnd = function () {
    const form = document.createElement('form')

    form.method = 'POST'
    form.action = "/lyric_generator/end_page"

    const hidden_field = document.createElement('input');

    hidden_field.type = 'hidden'
    hidden_field.name = 'prompt'
    hidden_field.value = document.getElementById('result').value

    form.appendChild(hidden_field)

    document.body.appendChild(form)

    form.submit()
}

document.getElementById('finalize').onclick = sendToEnd;