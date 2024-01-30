let availableKeywords = [
    "אסף איזון",
    "איתי אדלמן"
];

const resultsBox = document.querySelector(".results");
const inputBox = document.getElementById("input-box");
const searchArea = document.getElementById("results");


inputBox.onkeyup = function(){
    console.log(availableKeywords)
    let result = [];
    let input = inputBox.value;

    if (input.length){
        result = availableKeywords.filter((keyword) => {
            return keyword.includes(input);
        });

        display(result.sort());
    }

    else {
        searchArea.innerHTML = "";
    }
}

function display(result){
    let content = result.map((list) => {
        return "<li onclick=selectInput(this)>" + list + "</li>";
    });

    resultsBox.innerHTML = "<ul>" + content.join("") + "</ul>";
}

function selectInput(list){
    inputBox.value = list.innerHTML;
    resultsBox.innerHTML = "";
}