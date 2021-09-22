

const fileUploader = document.getElementById('file');
const feedback = document.getElementById('feedback');
const progressbar = document.getElementById('progress');
const progressLabel = document.getElementById('progress-label')
const feedbackval = document.getElementById('feedback')
const alertModal = document.getElementById('alert-modal');
const alertExtension = document.getElementById('alert-modal-ext');
// const modalClose = document.getElementById('close');

const reader = new FileReader();

fileUploader.addEventListener('change', (event) => {
  const files = event.target.files;
  const file = files[0];
  reader.readAsDataURL(file);
  
  reader.addEventListener('progress', (event) => {
    if (event.loaded && event.total) {
      const percent = (event.loaded / event.total) * 100;
      progressbar.value = percent;
      progressLabel.innerHTML = Math.round(percent) + '%';
      
      if (percent === 100) {
        let msg = `<span style="color:#00FF7F;">File <u><b>${file.name}</b></u> has been uploaded successfully.</span>`;
        feedback.innerHTML = msg;

        setTimeout(function(){
          alertExtension.classList.remove("d-none");
        }, 500); 
      }
    }

    
  });
});




fileUploader.onchange = () => {
   // Check if any file is selected.
  if (fileUploader.files.length > 0) {
    for (const i = 0; i <= fileUploader.files.length - 1; i++) {

        const fsize = fileUploader.files.item(i).size;
        const filesize = Math.round((fsize / 1024));
        // The size of the file.
        if (filesize >= 20480) {
         
         
          alertModal.classList.remove("d-none");
          progressbar.classList.add('d-none');
          feedback.classList.add('d-none');
          progressLabel.classList.add('d-none');

          
          setTimeout(function(){
            alert('will reload!!');
            window.location.reload();
          }, 1000); 
        } else {
          progressbar.classList.remove('d-none')
            document.getElementById('size').innerHTML = '<b>Size:'
            + filesize + '</b> KB';

            
        }
    }
  }
}





var loadingDiv = document.getElementById('loading');

function showSpinner() {
  loadingDiv.style.visibility = 'visible';
}

