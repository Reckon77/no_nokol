let plagCountSpan = document.getElementById("plagCount")
let totalSentencesSpan = document.getElementById("totalSentences")
let plagPercentageSpan=document.getElementById("plagPercent")

let plagCount=parseInt(plagCountSpan.innerText)
let totalSentences=parseInt(totalSentencesSpan.innerText)

const setPercentage=()=>{
    plagPercentageSpan.innerText=Math.round((plagCount/totalSentences)*100)
}
setPercentage()

const plagiarisedSentence=document.querySelectorAll(".plagiarisedSentence")
const orignalSentence=document.querySelectorAll(".orignalSentence")

for (let i = 0; i < plagiarisedSentence.length; i++) {
    plagiarisedSentence[i].addEventListener('click', function(e) {
        plagCount--
        totalSentences--
        plagCountSpan.innerText=plagCount
        totalSentencesSpan.innerText=totalSentences
        setPercentage()
      e.currentTarget.parentNode.remove();
      //this.closest('.single').remove() // in modern browsers in complex dom structure
      //this.parentNode.remove(); //this refers to the current target element 
      //e.target.parentNode.parentNode.removeChild(e.target.parentNode);
    }, false);
  }

  for (let i = 0; i < orignalSentence.length; i++) {
    orignalSentence[i].addEventListener('click', function(e) {
        totalSentences--
        totalSentencesSpan.innerText=totalSentences
        setPercentage()
      e.currentTarget.parentNode.remove();
      //this.closest('.single').remove() // in modern browsers in complex dom structure
      //this.parentNode.remove(); //this refers to the current target element 
      //e.target.parentNode.parentNode.removeChild(e.target.parentNode);
    }, false);
  }


 