import pdfplumber
import re
from modules.keywords import keywords_dic
from modules.jobs_db import GetAllSkills,GetJob,GetJobSkills,GetSkill
'''
from keywords import keywords_dic
from jobs_db import GetAllSkills,GetJob,GetJobSkills,GetSkill'''
import spacy
import json

nlp = spacy.load('en_core_web_sm')

pdf_url="C:/Users/victus/Downloads/DanielAndersonResume (1) (1).pdf"

class ResumeExtract:
    def __init__(self,url):
         with pdfplumber.open(url) as pdf:
              self.text = ''
              for page in pdf.pages:
                  self.text += page.extract_text()
         self.lowertext=self.text.lower()
    
    def gettext(self):
         return self.text
    
    def getname(self):
         '''name_patter=r"^[a-zA-Z]+ [a-zA-Z]+|^[a-zA-Z]+"
         name=re.findall(name_patter,self.text)'''
         doc = nlp(self.text)
         name=""
         for ent in doc.ents:
             if ent.label_ == "PERSON":
                   name=ent.text.split("\n")[0]
                   break
         return name
              
    
    def getphonenum(self):
         a=" hello my name is +65-456 565 7895 jhdfjksd"
         phone_num_pattern=r"\+?\d{1,2}?[\s._-]*?\(?\d{3}\)?[\s._-]*\d{3}[\s._-]*\d{4}"
         phone_num=re.findall(phone_num_pattern,self.text)
         return phone_num

    def getemail(self):
         email_pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
         emails=re.findall(email_pattern,self.text)
         return emails
    
    def required_keywords(self):
         keywords_not_present={}
         keywords=keywords_dic()
         for i in keywords.keys():
              keywords_not_present[i]={}
              for j in keywords[i].keys():
                   if j not in self.lowertext:
                        dic={}
                        keywords_not_present[i][j]=keywords[i][j]
         return keywords_not_present
    
    def getskills(self):
         skills=[]
         allskills=GetAllSkills()
         for i in allskills:
              if i.skill_name in self.lowertext:
                   skills.append((i.skill_id,i.skill_name))
         return skills

class Data:
     def job_title_data(self,job_title):
          try:
                job_id=GetJob(job_title=job_title).job_id
                return GetJobSkills(job_id=job_id)
          except:
               return "none"
             
     
     def required_skills(self,job_title_data):
          try:
            required_skills=[]
            for i in job_title_data:
               skill=GetSkill(skill_id=i.skill_id)
               required_skills.append((skill.skill_id,skill.skill_name,i.skill_type,i.priority_skill_no))
            return required_skills
          except:
               return "none"
     
     def probable_jobs(self,resume_skills):
          jobs_id=[]
          for i in resume_skills:
               jobs_id.append(GetJobSkills(skill_id=i[0]).job_id)
          jobs=[]
          for j in jobs_id:
               jobs.append(GetJob(job_id=j).job_title)
          job_freq={}
          for k in jobs:
               job_freq[k]=jobs.count(k)
          return job_freq


class ResumeAnalysis:
     def __init__(self,url,job_title,name):
          self.resume_data=ResumeExtract(url)
          self.data=Data()
          self.resume_skills=self.resume_data.getskills()
          self.job_title_data=self.data.job_title_data(job_title)
          self.skills=self.data.required_skills(self.job_title_data)
          self.probable_jobs=self.data.probable_jobs(self.resume_skills)

     def GetName(self):
          name=self.resume_data.getname()
          if(len(name.split())<2 and not len(name.split())==0):
              return {"name":name,"tips":"Add your full name in resume","flag":0}
          elif(name):
              return {"name":name,"tips":"Name is in proper format","flag":1}
          else:
              return {"name":"","tips":"Name is not in proper format","flag":0}
          
     def GetEmails(self):
          email=self.resume_data.getemail()
          if(len(email)):
               return {"email":email,"tips":"Email is in proper format","flag":1}
          return {"email":"","tips":"Add Email in resume (professional)","flag":0}
     
     def GetPhNo(self):
          ph=self.resume_data.getphonenum()
          if(len(ph)):
               return {"phone_number":ph,"tips":"Phone Number is in proper format","flag":1}
          return {"phone_number":"","tips":"Add Phone Number in resume (professional)","flag":0}
     

     def required_skills(self):
          skills=[]

          for i in self.skills:
               flag=1
               for j in self.resume_skills:
                     if(i[0]==j[0]):
                         flag=0
                         break
               if(flag):
                    skills.append(i)
          return {"skills":skills}
     
     def top_prob_job(self):
          freq=[]
          job_freq=[]
          for i in self.probable_jobs.keys():
               freq.append(self.probable_jobs[i])
               job_freq.append(i)
          print(freq)
          print()
          print(job_freq)
          max_index=freq.index(max(freq))
          return {"top_prob_job":job_freq[max_index]}
               
     def required_keywords(self):
          return self.resume_data.required_keywords()
     #13
def ATSScore(data):
     score=0
     if(data["name"]["flag"]==1):
          score+=1
     if(data["email"]["flag"]==1):
          score+=1
     if(data["phone_number"]["flag"]==1):
          score+=1
     leadership_keys=[]
     for i in data["required_keywords"]["leadership"].keys():
          leadership_keys.append(i)
     skills_keys=[]
     for i in data["required_keywords"]["skills"].keys():
          skills_keys.append(i)
     action_verbs_keys=[]
     for i in data["required_keywords"]["action_verbs"].keys():
          action_verbs_keys.append(i)
     keywords_imp=(len(leadership_keys)+len(skills_keys)+len(action_verbs_keys))/13
     score+=keywords_imp
     return (score/4)*100