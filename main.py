from flask import Flask,render_template,request,redirect,session,send_from_directory,jsonify,send_file
from modules.database import user_exist,add_user,get_user_by_username,get_user_by_id
from modules.resume_analysis import ResumeAnalysis,ATSScore
from datetime import datetime
import os
from docx2pdf import convert
from modules.resume_user_data import GetResume,PutResume

main = Flask(__name__)
main.secret_key="11525"

@main.route("/signup",methods=["GET","POST"])
def signup():
    if(request.method=="POST"):
        username=request.form.get("username")
        password=request.form.get("pass")
        re_password=request.form.get("rpass")
        user_exists=user_exist(username)
        if(user_exists==1):
            print("user Already exist")
        else:
            if(password==re_password):
                add_user(username,password)
                return redirect("/login")
            else:
                print("Password Not Match")
        
    return render_template("/user/user_signup.html")


@main.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        username=request.form.get("username")
        password=request.form.get("pass")
        user_exists=user_exist(username)
        if(user_exist):
            user_data=get_user_by_username(username)
            if(password==user_data["password"] and username==user_data["username"]):
                session["user_id"]=user_data["id"]
                return redirect("/user")
            else:
                print("Invalid Password")
        else:
            print("User Not Exist")
    return render_template("/user/user_login.html")

@main.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect("/")

@main.route("/")
def home():
    try:
        if(session["user_id"]):
            return redirect("/user")
    except:
        return render_template("/user/home.html")

@main.route("/user")
def user():
    try:
       if(session["user_id"]):
          user_data=get_user_by_id(session["user_id"])
          return render_template("/user/user.html",user_data=user_data)
    except:
        return redirect("/")

@main.route("/admin")
def admin():
    return render_template("/admin/admin.html")

@main.route("/db_entry")
def db_entry():
    return render_template("/admin/db_entry.html")

@main.route("/db_show")
def db_show():
    return render_template("/admin/db_show.html")

@main.route("/ra/<string:time>",methods=["GET"])
def ra(time):
    return render_template("/user/resume_analysis.html")

@main.route("/resume_analysis/<string:time>",methods=["GET"])
def resume_analysis(time):
    resume_ref=GetResume(time)
    name=resume_ref.name
    job=resume_ref.job_title.lower()
    pdf_url="resumes/"+str(session["user_id"])+"&"+time+".pdf"
    resume_data=ResumeAnalysis(pdf_url,job,name)
    analysis={
        "name":resume_data.GetName(),
        "email":resume_data.GetEmails(),
        "phone_number":resume_data.GetPhNo(),
        "required_skills":resume_data.required_skills(),
        "top_prob_job":resume_data.top_prob_job(),
        "required_keywords":resume_data.required_keywords()
    }
    ATSscore=ATSScore(analysis)
    analysis["ATSScore"]=ATSscore
    return analysis

@main.route("/get_resume/<string:time>",methods=["GET"])
def get_resume(time):
    try:
       if(session["user_id"]):
           path=str(session["user_id"])+"&"+time+".pdf"
           print(path)
           return send_from_directory("resumes/",path,as_attachment=True)
    except:
        return redirect("/login")

@main.route("/info/<string:time>",methods=["POST"])
def info(time):
    name=request.form.get("name")
    job=request.form.get("job")
    PutResume(session["user_id"],job,name,time)
    return str("done")

@main.route("/upload_resume",methods=["POST"])
def upload_resume():
    try:
        if(session["user_id"]):
            doc=request.files["doc"]
            doc_name=doc.filename
            if(os.path.splitext(doc_name)[1]==".pdf"):
                time=datetime.now().strftime("%Y%m%d%H%M%S")
                path="resumes/"+str(session["user_id"])+"&"+time+".pdf"
                doc.save(path)
                return time
            if(os.path.splitext(doc_name)[1]==".docx"):
                time=datetime.now().strftime("%Y%m%d%H%M%S")
                path="doc_resume/"+str(session["user_id"])+"&"+time+".docx"
                new_path="resumes/"+str(session["user_id"])+"&"+time+".pdf"
                doc.save(path)
                convert(path,new_path)
                return time
    except:
        return redirect("/login")

@main.route("/res")
def res():
    return render_template("/user/resume_analysis.html")

if __name__ == "__main__":
    main.run(debug=True)