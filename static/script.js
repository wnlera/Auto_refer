const searchButton = document.getElementById('search-button');
const searchInput = document.getElementById('search-input');


function create_link_text(link_number, jsonData) {
    for (let i = 0; i < jsonData.source_text.length; i++) {
        if (jsonData.source_text[i].b_link === link_number) {
            let link_title = jsonData.source_text[i]["title"];
            let link_text = `[<a href="#${link_number}" data-title="${link_title}" style="font-weight: bold" onclick="tempHighlight('rref${link_number}')">${link_number}</a>]`
            return link_text
        }
    }
}

let openTag = "@kibana-highlighted-field@";
let closeTag = "@/kibana-highlighted-field@";
let openStyle = "<mark>";
let closeStyle = "</mark>";


function create_text(jsonData) {
    let mainContainer = document.getElementById("myData");
    clear_text()
    let h3 = document.createElement("h3");
    h3.innerHTML = "Suitable sentences"
    mainContainer.appendChild(h3);
    for (let i = 0; i < jsonData.main_text.length; i++) {
        let p = document.createElement("p");
        let all_link_text = []
        for (let j = 0; j < jsonData.main_text[i]["b_link"].length; j++) {
            all_link_text.push(create_link_text(jsonData.main_text[i]["b_link"][j], jsonData))
        }
        let sentence = jsonData.main_text[i]["sentence"][0];
        sentence = sentence.replaceAll(openTag, openStyle);
        sentence = sentence.replaceAll(closeTag, closeStyle)

        p.innerHTML = sentence + all_link_text.join(' ');
        mainContainer.appendChild(p);
    }
}

function tempHighlight(refId) {
    let obj = document.getElementById(refId);
    let oldBody = obj.innerHTML;
    let newBody = "<mark>" + obj.innerHTML + "</mark>";
    obj.innerHTML = newBody;

    setTimeout(() => {
        obj.innerHTML = oldBody;
    }, 7000)

}


function create_ref(jsonData) {
    let mainContainer = document.getElementById("myRef");
    let h3 = document.createElement("h3");
    h3.innerHTML = "Reference"
    mainContainer.appendChild(h3);
    for (let i = 0; i < jsonData.source_text.length; i++) {
        let li = document.createElement("li");
        li.innerHTML = `<a name=${jsonData.source_text[i]["b_link"]} id="rref${jsonData.source_text[i]["b_link"]}">${jsonData.source_text[i]["title"]}</a>`;
        mainContainer.appendChild(li);
    }
}

function show_max_score(jsonData) {
    let maxScore = document.getElementById("maxScore");
    maxScore.textContent = "Max score: " + jsonData.max_score;
}


async function get_review(inputValue) {
    let url = 'http://localhost:5000/search/' + encodeURI(inputValue);
    const response = await fetch(url);
    return await response.json();
}


function clear_text() {
    let textContainer = document.getElementById("myData");
    textContainer.textContent = "";
    textContainer.innerHTML = "";
    let refContainer = document.getElementById("myRef");
    refContainer.textContent = "";
    refContainer.innerHTML = "";
}

searchButton.addEventListener('click', () => {
    const inputValue = searchInput.value;
    let infoDiv = document.getElementById("myInfo");
    infoDiv.textContent = "Searching: " + inputValue;
    clear_text()
    get_review(inputValue).then((data) => {
        if (data.main_text.length > 0) {
            infoDiv.textContent = "Results for: " + inputValue;
            show_max_score(data);
            create_text(data);
            create_ref(data);
        } else {
            clear_text()
            infoDiv.textContent = "Nothing found for: " + inputValue;
        }
    }).catch((e) => {
        console.log(e);
        clear_text()
        infoDiv.textContent = "Server error or timeout 😔";
    });
});

searchInput.addEventListener("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        searchButton.click();
    }
});