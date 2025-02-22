const doc_id=document.getElementById("doc");
const back_flip_id=document.getElementById("back-flip");
let rref=null

let doc_click_flag=0;
doc_id.addEventListener("click",doc_click_animation);
function doc_click_animation(){
    if(doc_click_flag==0){
    let interval_id=null;
    clearInterval(interval_id);
    interval_id=setInterval(onhover,20);
    let rotateY=-45;
    let rotateX=35;
    console.log("hii");
    function onhover(){
        if(rotateX==0 && rotateY<=0){
            clearInterval(interval_id);
            doc_click_flag=1;
        }
        else{
            if(rotateX>0){
                rotateX=rotateX-1;
            }
            if(rotateY<0){
                rotateY=rotateY+1.2857142857;
            }
            doc_id.style.transform = "rotateY("+rotateY+"deg) rotateX("+rotateX+"deg)";
        }
    }
}
    }    

back_flip_id.addEventListener("click",doc_unclick_animation);
function doc_unclick_animation(){
    if(doc_click_flag==1){
    let interval_id=null;
    clearInterval(interval_id);
    interval_id=setInterval(onhover,20);
    let rotateY=0;
    let rotateX=0;
    function onhover(){
        if(rotateX==35 && rotateY<=-45){
            clearInterval(interval_id);
            doc_click_flag=0
        }
        else{
            if(rotateX<35){
                rotateX=rotateX+1;
            }
            if(rotateY>-45){
                rotateY=rotateY-1.2857142857;
            }
            doc_id.style.transform = "rotateY("+rotateY+"deg) rotateX("+rotateX+"deg)";
        }
    }
}
}

function send_doc(){
    let doc=document.getElementById("resume-file-upload").files[0];
    let formData = new FormData();
    formData.append('doc', doc);
    xhr=new XMLHttpRequest()
    xhr.open("POST","/upload_resume",true)
    xhr.onload=function(){
        document.getElementById("a").href="/ra/"+xhr.responseText;
        resume_ref=xhr.responseText;
        rref=resume_ref
        get_resume_doc(resume_ref);
    }
    xhr.send(formData);
}
const doc_upload_id=document.getElementById("doc-upload");

doc_upload_id.addEventListener("click",upload_doc);
function upload_doc(){
  document.getElementById("resume-file-upload").value="";
  var id=null;
  clearInterval(id);
  id=setInterval(fun,1000);
  function fun(){
    if(document.getElementById("resume-file-upload").value!=""){
        send_doc();
        clearInterval(id);
    }
        document.body.addEventListener('click', fn, true);
        function fn(){
            clearInterval(id);
        } 
}
}

document.body.addEventListener('click', function(event) {
    if (!event.target.closest('#doc')) {
        doc_unclick_animation();
    }
  });
  

function get_resume_doc(resume_ref){
    xhr2=new XMLHttpRequest();
    xhr2.open("GET","/get_resume/"+String(resume_ref),true);
    console.log(resume_ref)
    xhr2.responseType = 'arraybuffer';
    xhr2.onload=function (){
        let resume=new Blob([xhr2.response], { type: 'application/pdf' });
        url = URL.createObjectURL(resume);
        pdf_render(url)
    }
    xhr2.send();
}

function pdf_render(url){

    // The canvas element to render the PDF page
    const canvas = document.getElementById('pdf-render-canvas');
    const context = canvas.getContext('2d');

    // Load the PDF document
    pdfjsLib.getDocument(url).promise.then(function (pdfDoc) {
        // Fetch the first page
        pdfDoc.getPage(1).then(function (page) {
            const viewport = page.getViewport({ scale:1 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;

            // Render the page onto the canvas
            const renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            page.render(renderContext);
            let doc_upload_label_id=document.getElementById("resume-upload-label");
            doc_upload_label_id.innerHTML="Resume";
            doc_upload_id.style.width="17%";
            doc_upload_id.style.left="22.5%";
            document.getElementById("back-flip").style.left="52.5%";
            display_input_info();
        });
    }).catch(function (error) {
        console.error('Error loading PDF:', error);
    });
}

function display_input_info(){
    const element = document.getElementById("left-of-doc-text");
    element.style.display="none";
    const element2 = document.getElementById("options-data");
    element2.style.display="flex";
}

upload_button=document.getElementById("a")
upload_button.addEventListener("click",upload_info);
function upload_info(){
    let name=document.getElementById("name").value
    let job=document.getElementById("job").value
    let formdata=new FormData();
    formdata.append("name",name);
    formdata.append("job",job);
    xhr3=new XMLHttpRequest();
    xhr3.open("POST","/info/"+String(rref),true);
    xhr3.send(formdata)
}