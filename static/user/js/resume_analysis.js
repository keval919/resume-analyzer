let url=null;
let numberOfPages = null;
let current_page_num=1;
let resume_ref=null
let analysis_data=null

function current_resume_ref(){
    let current_url=window.location.href;
    let url_split=current_url.split("/");
    resume_ref=url_split[url_split.length-1]
}
current_resume_ref();
function get_resume(){
    xhr=new XMLHttpRequest();
    xhr.open("GET","/get_resume/"+resume_ref,true);
    xhr.responseType = 'arraybuffer';
    xhr.onload=function (){
        let resume=new Blob([xhr.response], { type: 'application/pdf' });
        url = URL.createObjectURL(resume);
        render_resume_page(current_page_num);
    }
    xhr.send();
}
get_resume();
function render_resume_page(page_no){
const canvas = document.getElementById('resume-render-canvas');
    const context = canvas.getContext('2d');
    // Load the PDF document
    pdfjsLib.getDocument(url).promise.then(function (pdfDoc) {
        numberOfPages = pdfDoc.numPages;
        // Fetch the first page
        pdfDoc.getPage(page_no).then(function (page) {
            const viewport = page.getViewport({ scale:1 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;

            // Render the page onto the canvas
            const renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            page.render(renderContext);
        });
    }).catch(function (error) {
        console.error('Error loading PDF:', error);
    });

}

let prev_button=document.getElementById('left-shift');
prev_button.addEventListener("click",load_prev_page);
function load_prev_page(){
    if(current_page_num>1){
        current_page_num-=1;
        render_resume_page(current_page_num);
        if(current_page_num==1){
            prev_button.style.color="rgb(184, 184, 184)";
        }
        if(current_page_num<numberOfPages){
            next_button.style.color="rgb(255, 255, 255)";
        }
    }
}

let next_button=document.getElementById('right-shift');
next_button.addEventListener("click",load_next_page);
function load_next_page(){
    if(current_page_num<numberOfPages){
        current_page_num+=1;
        render_resume_page(current_page_num);
        if(current_page_num==numberOfPages){
            console.log("black")
        next_button.style.color="rgb(184, 184, 184)";
        }
        if(current_page_num>1){
            prev_button.style.color="white";
        }
    }
}

function ReqResumeanalysis(){
    xhr1=new XMLHttpRequest();
    xhr1.open("GET","/resume_analysis/"+resume_ref,true);
    xhr1.onload=function(){
        var responseData = JSON.parse(xhr1.responseText);
        analysis_data=responseData;
        document.getElementById("score").innerHTML=analysis_data["ATSScore"];
        if(analysis_data["ATSScore"]>75){
            document.getElementById("score").style.color="greenyellow"; 
        }
        else{
            document.getElementById("score").style.color="red"; 
        }
    }
    xhr1.send();
}
ReqResumeanalysis();

//let data={'name': {'name': 'DANIEL ANDERSON', 'tips': 'Name is in proper format'}, 'email': {'email': ['help@enhancv.com'], 'tips': 'Email is in proper format'}, 'phone_number': {'phone_number': ['+1-(234)-555-1234'], 'tips': ''}, /*'required_skills': {'skills': [(2, 'java', 'programming', 90), (3, 'c++', 'programming', 90), (4, 'javascript', 'programming', 90), (5, 'ruby', 'programming', 85), (6, 'problem solving', None, 90), (7, 'version control (git)', None, 85), (8, 'algorithms and data structures', None, 90), (9, 'debugging', None, 80), (10, 'database management', None, 75), (11, 'software development life cycle', None, 85), (12, 'unit testing', None, 80), (13, 'cloud computing (aws, azure)', None, 70), (14, 'collaboration (agile, scrum)', None, 75)]}, 'top_prob_job': {'top_prob_job': 'data scientist'}, */'required_keywords': {'leadership': {'manager': {'why': 'To demonstrate your ability to oversee a team, make decisions, set goals, and ensure tasks are completed on time and within budget.'}, 'team leader': {'why': 'To show you can guide, motivate, and support a group to reach common goals while fostering collaboration.'}}, 'skills': {'problem solving': {'why': 'To highlight your ability to analyze issues, find effective solutions, and overcome challenges.'}, 'time management': {'why': 'To show you can prioritize tasks, meet deadlines, and optimize productivity.'}, 'adaptability': {'why': 'To demonstrate your ability to adjust to changing environments, new technologies, or unexpected challenges.'}}, 'action_verbs': {'achieved': {'why': 'To emphasize your ability to accomplish goals and complete projects successfully with tangible results.'}, 'delivered': {'why': 'To show that you consistently complete tasks or meet deadlines.'}, 'optimized': {'why': 'To reflect your capacity to improve processes, workflows, or performance for better results.'}}}};


document.getElementById("name").addEventListener("click",ShowName);
function ShowName(){
        let data=analysis_data
        document.getElementById("email-analaysis").style.display="none";
        document.getElementById("phone-number-analaysis").style.display="none";
        document.getElementById("present-keywords-analaysis").style.display="none";
        document.getElementById("skills-analaysis").style.display="none";
        document.getElementById("job-analaysis").style.display="none";
        document.getElementById("name-analaysis").style.display="flex";
        document.getElementById("name-h1").innerHTML="Name: "+data["name"]["name"];
        document.getElementById("name-tips").innerHTML=data["name"]["tips"];
}

document.getElementById("email").addEventListener("click",ShowEmail);
function ShowEmail(){
    let data=analysis_data
    document.getElementById("name-analaysis").style.display="none";
    document.getElementById("phone-number-analaysis").style.display="none";
    document.getElementById("present-keywords-analaysis").style.display="none";
    document.getElementById("skills-analaysis").style.display="none";
    document.getElementById("job-analaysis").style.display="none";
    document.getElementById("email-analaysis").style.display="flex";
    document.getElementById("email-h1").innerHTML="Email: "+data["email"]["email"];
    document.getElementById("email-tips").innerHTML=data["email"]["tips"];
}

document.getElementById("phno").addEventListener("click",ShowPhNo);
function ShowPhNo(){
    let data=analysis_data
        document.getElementById("email-analaysis").style.display="none";
        document.getElementById("name-analaysis").style.display="none";
        document.getElementById("present-keywords-analaysis").style.display="none";
        document.getElementById("skills-analaysis").style.display="none";
        document.getElementById("job-analaysis").style.display="none";
    document.getElementById("phone-number-analaysis").style.display="flex";
    document.getElementById("pn-h1").innerHTML=data["phone_number"]["phone_number"];
    document.getElementById("pn-tips").innerHTML=data["phone_number"]["tips"];
}

document.getElementById("present-keywords").addEventListener("click",ShowPresentKeywords);
function ShowPresentKeywords(){
    let data=analysis_data
    document.getElementById("email-analaysis").style.display="none";
        document.getElementById("phone-number-analaysis").style.display="none";
        document.getElementById("name-analaysis").style.display="none";
        document.getElementById("skills-analaysis").style.display="none";
        document.getElementById("job-analaysis").style.display="none";
    document.getElementById("phone-number-analaysis").style.display="none";
    document.getElementById("present-keywords-analaysis").style.display="flex";
    leadership=[]
    skills=[]
    action_verbs=[]
    for(i in data["required_keywords"]["leadership"]){
        leadership.push(String(i)+" "+"-"+" "+String(data["required_keywords"]["leadership"][i]["why"]));
    }
    for(i in data["required_keywords"]["skills"]){
        skills.push(String(i)+" "+"-"+" "+String(data["required_keywords"]["skills"][i]["why"]));
    }
    for(i in data["required_keywords"]["action_verbs"]){
        action_verbs.push(String(i)+" "+"-"+" "+String(data["required_keywords"]["action_verbs"][i]["why"]));
    }
    document.getElementById("leadership-tips").innerHTML=leadership;
    document.getElementById("skills-key-tips").innerHTML=skills;
    document.getElementById("action_verbs-tips").innerHTML=action_verbs;
}

document.getElementById("sfrj").addEventListener("click",ShowSkills);
function ShowSkills(){
    let data=analysis_data
        document.getElementById("email-analaysis").style.display="none";
        document.getElementById("phone-number-analaysis").style.display="none";
        document.getElementById("present-keywords-analaysis").style.display="none";
        document.getElementById("name-analaysis").style.display="none";
        document.getElementById("job-analaysis").style.display="none";
        document.getElementById("skills-analaysis").style.display="flex";
    let skills=[]
    for(i in data["required_skills"]["skills"]){
        skills.push(" "+data["required_skills"]["skills"][i][1]+" ")
    }
    document.getElementById("skills-tips").innerHTML=skills;
}

document.getElementById("jsoycs").addEventListener("click",ShowJobTitle);
function ShowJobTitle(){
    let data=analysis_data
        document.getElementById("email-analaysis").style.display="none";
        document.getElementById("phone-number-analaysis").style.display="none";
        document.getElementById("present-keywords-analaysis").style.display="none";
        document.getElementById("skills-analaysis").style.display="none";
        document.getElementById("name-analaysis").style.display="none";
        document.getElementById("job-analaysis").style.display="flex";
    document.getElementById("job-tips").innerHTML=data["top_prob_job"]["top_prob_job"];
}