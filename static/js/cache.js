const localStoreCache = (cacheKey, data) => {
    window.localStorage.setItem(cacheKey, data)
    return window.localStorage.getItem(cacheKey)
}

const cacheToken = () => {
    let counter = document.getElementById("charcounter");
    let question = document.getElementById("questionfield");

    let charCount = question.value.length

    localStoreCache("question", question.value)
    let cachedChars = localStoreCache("charcount", charCount)
    let cachedTokens = localStoreCache("tokencount", charCount / 4)

    counter.textContent = "Count: " + cachedChars + " Token: " + cachedTokens
}

const cacheOptions = () => {
    let answerStyle = document.getElementById("answerStyleSelector");
    localStoreCache("answerStyle", answerStyle.value)
}

const loadCache = () => {
    let counter = document.getElementById("charcounter");
    let question = document.getElementById("questionfield");
    let answerStyle = document.getElementById("answerStyleSelector");


    if (window.localStorage.getItem("answerStyle")) {
        answerStyle.value = window.localStorage.getItem("answerStyle")
    }

    if (window.localStorage.getItem("question")) {
        question.value = window.localStorage.getItem("question")
    }

    if (window.localStorage.getItem("charcount") && window.localStorage.getItem("tokencount")) {
        counter.textContent = "Count: " + window.localStorage.getItem("charcount") + " Token: " + window.localStorage.getItem("tokencount")
    }

}


loadCache()

let textareaQuestionfield = document.getElementById("questionfield");
let answerStyleSelector = document.getElementById("answerStyleSelector");

textareaQuestionfield.addEventListener("input", cacheToken);
answerStyleSelector.addEventListener("input", cacheOptions);

