let SpeechRecognition = window.webkitSpeechRecognition;
let recognition = new SpeechRecognition();

const textArea=document.querySelector(".textArea")
const ins = document.getElementById('ins')
const mic=document.getElementById('mic')
const stop=document.getElementById('stop')

let content=''
recognition.continuous=true

recognition.onstart=function(){
    mic.classList.add('start')
    ins.innerText="Voice recognition is on"
}
recognition.onspeechend=function(){
    mic.classList.remove('start')
    ins.innerText="Press the mic"
    stop.classList.add('d-none')
    recognition.stop()
}
recognition.onerror=function(){
    mic.classList.remove('start')
    stop.classList.add('d-none')
    ins.innerText="Try again"
}
recognition.onresult=function(e){
    let current = e.resultIndex
    let transcript=e.results[current][0].transcript
    content+=transcript
    textArea.value=content

}
mic.addEventListener('click',function(){
    if(content.length){
        content+=''
    }
    stop.classList.remove('d-none')
    recognition.start()
})
stop.addEventListener('click',function(e){
    e.preventDefault();
    mic.classList.remove('start')
    ins.innerText="Press the mic"
    stop.classList.add('d-none')
    recognition.stop()
})
textArea.addEventListener('input',function(){
    content=this.value
})

