let plagCountSpan = document.getElementById("plagCount")
let totalSentencesSpan = document.getElementById("totalSentences")
let plagPercentageSpan=document.getElementById("plagPercent")

let plagCount=parseInt(plagCountSpan.innerText)
let totalSentences=parseInt(totalSentencesSpan.innerText)
let perecentage = Math.round((plagCount/totalSentences)*100)
plagPercentageSpan.innerText=perecentage