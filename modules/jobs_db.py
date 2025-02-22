from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    
    job_id = Column(Integer, primary_key=True)
    job_title = Column(String(75),unique=True)


class Skill(Base):
    __tablename__ = 'skills'
    
    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String(50),unique=True)

class Jobskill(Base):
    __tablename__ = 'jobskills'
    
    job_skill_relation_id = Column(Integer, primary_key=True)
    priority_skill_no = Column(Integer)
    skill_type = Column(String(50),nullable=True)
    
    job_id = Column(Integer, ForeignKey('jobs.job_id'))  
    skill_id = Column(Integer, ForeignKey('skills.skill_id')) 

# Setup the database and session
engine = create_engine('sqlite:///job.db')  
Base.metadata.create_all(engine) 

Session = sessionmaker(bind=engine)  
session = Session() 

def AddJob(job_title):
    job1=Job(job_title=job_title)
    session.add(job1)
    session.commit()

def AddSkill(skill_name):
    if(not session.query(Skill).filter(Skill.skill_name==skill_name).first()):
       skill1=Skill(skill_name=skill_name)
       session.add(skill1)
       session.commit()

def AddJobSkill(job_id,skill_id,priority_skill_no,skill_type=None):
    if(not skill_type):
        jobskill1=Jobskill(job_id=job_id,skill_id=skill_id,priority_skill_no=priority_skill_no)
        session.add(jobskill1)
        session.commit()
    else:
        jobskill1=Jobskill(job_id=job_id,skill_id=skill_id,priority_skill_no=priority_skill_no,skill_type=skill_type)
        session.add(jobskill1)
        session.commit()

def GetJob(job_title=None,job_id=None):
    if(job_title):
       return session.query(Job).filter(Job.job_title == job_title).first()
    if(job_id):
        return session.query(Job).filter(Job.job_id == job_id).first()


def GetSkill(skill_name=None,skill_id=None):
    if(skill_name):
       return session.query(Skill).filter(Skill.skill_name == skill_name).first()
    if(skill_id):
        return session.query(Skill).filter(Skill.skill_id == skill_id).first()
    
def GetAllSkills():
    return session.query(Skill).all()

def GetJobSkills(job_id=None,skill_id=None):
    if(job_id):
        return session.query(Jobskill).filter(and_(Jobskill.job_id==job_id)).all()
    if(skill_id):
        return session.query(Jobskill).filter(and_(Jobskill.skill_id==skill_id)).first()

'''
dataset = {
    "Software Engineer": {
        "Skills": {
            "Programming": {"Python": 95, "Java": 90, "C++": 90, "JavaScript": 90, "Ruby": 85},
            "Problem Solving": 90,
            "Version Control (Git)": 85,
            "Algorithms and Data Structures": 90,
            "Debugging": 80,
            "Database Management": 75,
            "Software Development Life Cycle": 85,
            "Unit Testing": 80,
            "Cloud Computing (AWS, Azure)": 70,
            "Collaboration (Agile, Scrum)": 75
        }
    },
    "Project Manager": {
        "Skills": {
            "Leadership": 95,
            "Communication": 90,
            "Risk Management": 85,
            "Time Management": 90,
            "Problem Solving": 80,
            "Agile Methodology": 75,
            "Budgeting": 85,
            "Stakeholder Management": 80,
            "Project Scheduling": 85,
            "Negotiation": 70
        }
    },
    "Data Scientist": {
        "Skills": {
            "Programming": {"Python": 95, "R": 90, "SQL": 90, "Java": 85, "SAS": 80},
            "Machine Learning": 95,
            "Data Analysis": 90,
            "Statistics": 80,
            "Data Visualization": 75,
            "Big Data Tools": 70,
            "Data Cleaning": 85,
            "Model Deployment": 80,
            "Data Wrangling": 75,
            "Deep Learning": 85
        }
    },
    "UX/UI Designer": {
        "Skills": {
            "User Research": 90,
            "Wireframing": 85,
            "Prototyping": 80,
            "Design Software": {"Sketch": 90, "Figma": 85, "Adobe XD": 80},
            "Interaction Design": 80,
            "Creativity": 70,
            "User Testing": 85,
            "Responsive Design": 80,
            "Branding": 75,
            "HTML/CSS Knowledge": 70
        }
    },
    "Marketing Manager": {
        "Skills": {
            "Digital Marketing": 95,
            "SEO/SEM": 90,
            "Content Strategy": 85,
            "Social Media Management": 80,
            "Analytical Skills": 85,
            "Campaign Management": 75,
            "Email Marketing": 80,
            "Market Research": 85,
            "Brand Strategy": 75,
            "Lead Generation": 70
        }
    },
    "Financial Analyst": {
        "Skills": {
            "Financial Modeling": 95,
            "Excel/Spreadsheets": 90,
            "Data Analysis": 85,
            "Problem Solving": 80,
            "Accounting Principles": 75,
            "Communication": 70,
            "Forecasting": 85,
            "Financial Reporting": 80,
            "Investment Analysis": 75,
            "Risk Assessment": 80
        }
    },
    "Sales Representative": {
        "Skills": {
            "Communication": 95,
            "Negotiation": 90,
            "Customer Service": 85,
            "Problem Solving": 80,
            "Product Knowledge": 75,
            "Time Management": 70,
            "Relationship Building": 90,
            "Cold Calling": 80,
            "Sales Presentations": 85,
            "Target Achievement": 75
        }
    },
    "Human Resources Manager": {
        "Skills": {
            "Employee Relations": 95,
            "Recruitment": 90,
            "Communication": 85,
            "Conflict Resolution": 80,
            "HR Software (HRIS)": 75,
            "Leadership": 80,
            "Payroll Management": 75,
            "Organizational Development": 85,
            "Training and Development": 80,
            "Employment Law Knowledge": 70
        }
    },
    "Web Developer": {
        "Skills": {
            "Programming": {"HTML": 90, "CSS": 90, "JavaScript": 90, "Python": 85, "PHP": 80},
            "Version Control (Git)": 85,
            "Responsive Design": 80,
            "Frameworks": {"React": 85, "Angular": 80, "Vue.js": 75},
            "Database Management": 70,
            "Backend Development": 75,
            "Cross-browser Compatibility": 80,
            "UI/UX Knowledge": 75,
            "Problem Solving": 85
        }
    },
    "Business Analyst": {
        "Skills": {
            "Requirements Gathering": 90,
            "Data Analysis": 85,
            "SQL": 80,
            "Problem Solving": 90,
            "Communication": 85,
            "Stakeholder Management": 75,
            "Documentation Skills": 80,
            "Business Process Modeling": 85,
            "Project Management": 75,
            "Data Visualization": 70
        }
    },
    "Product Manager": {
        "Skills": {
            "Product Strategy": 95,
            "Market Research": 90,
            "Roadmap Planning": 85,
            "Leadership": 80,
            "Communication": 90,
            "Cross-functional Collaboration": 75,
            "Product Lifecycle Management": 85,
            "Customer Experience Design": 80,
            "Agile Methodology": 75,
            "Negotiation": 70
        }
    },
    "Customer Support Representative": {
        "Skills": {
            "Communication": 95,
            "Customer Service": 90,
            "Problem Solving": 85,
            "Time Management": 80,
            "Empathy": 75,
            "Product Knowledge": 70,
            "Conflict Resolution": 85,
            "Active Listening": 90,
            "Multitasking": 75,
            "Patience": 70
        }
    },
    "Content Writer": {
        "Skills": {
            "Writing Skills": 95,
            "Research": 90,
            "SEO Writing": 85,
            "Creativity": 80,
            "Time Management": 75,
            "Grammar and Editing": 85,
            "Content Strategy": 75,
            "Storytelling": 80,
            "Audience Understanding": 70,
            "Technical Writing": 65
        }
    },
    "Software Tester": {
        "Skills": {
            "Test Automation": 90,
            "Manual Testing": 85,
            "Bug Tracking": 80,
            "Scripting": 75,
            "Quality Assurance": 85,
            "Attention to Detail": 90,
            "Regression Testing": 80,
            "Agile Methodology": 75,
            "Performance Testing": 70,
            "Collaboration": 70
        }
    },
    "Graphic Designer": {
        "Skills": {
            "Design Software": {"Adobe Photoshop": 90, "Illustrator": 85, "InDesign": 80},
            "Creativity": 90,
            "Typography": 85,
            "Layout Design": 80,
            "Branding": 75,
            "UX/UI Principles": 70,
            "Illustration": 80,
            "Photo Editing": 85,
            "Web Design": 75,
            "Animation": 70
        }
    },
    "Social Media Manager": {
        "Skills": {
            "Content Creation": 90,
            "SEO/SEM": 85,
            "Community Engagement": 90,
            "Analytics": 80,
            "Platform Knowledge": {"Instagram": 90, "LinkedIn": 85, "Twitter": 80},
            "Communication": 75,
            "Campaign Strategy": 80,
            "Brand Awareness": 75,
            "Content Calendar Management": 70,
            "Paid Advertising": 70
        }
    },
    "Network Engineer": {
        "Skills": {
            "Networking Protocols": 95,
            "Troubleshooting": 90,
            "Firewall Configuration": 85,
            "Cloud Computing": 80,
            "Security Principles": 85,
            "Server Management": 75,
            "Cisco Networking": 90,
            "VPN Setup": 80,
            "System Administration": 75,
            "Technical Support": 70
        }
    },
    "Database Administrator": {
        "Skills": {
            "SQL": 95,
            "Database Management": 90,
            "Performance Tuning": 85,
            "Backup and Recovery": 80,
            "Data Security": 85,
            "Cloud Databases": 75,
            "Database Design": 85,
            "Data Modeling": 80,
            "ETL Processes": 75,
            "SQL Server": 80
        }
    },
    "Operations Manager": {
        "Skills": {
            "Leadership": 90,
            "Project Management": 85,
            "Process Optimization": 95,
            "Problem Solving": 90,
            "Team Management": 80,
            "Communication": 85,
            "Data Analysis": 75,
            "Resource Allocation": 80,
            "Change Management": 70,
            "Supply Chain Management": 75
        }
    },
    "Cybersecurity Analyst": {
        "Skills": {
            "Network Security": 95,
            "Risk Management": 90,
            "Penetration Testing": 85,
            "Threat Intelligence": 90,
            "Security Tools (SIEM)": 85,
            "Compliance": 80,
            "Firewall Configuration": 75,
            "Cryptography": 80,
            "Vulnerability Assessment": 70,
            "Incident Response": 85
        }
    },
    "Event Coordinator": {
        "Skills": {
            "Organization": 90,
            "Communication": 95,
            "Negotiation": 85,
            "Budgeting": 80,
            "Vendor Management": 75,
            "Customer Service": 70,
            "Time Management": 80,
            "Multitasking": 75,
            "Event Planning": 85,
            "Problem Solving": 80
        }
    },
    "Legal Assistant": {
        "Skills": {
            "Legal Research": 90,
            "Document Preparation": 85,
            "Attention to Detail": 95,
            "Confidentiality": 90,
            "Communication": 80,
            "Time Management": 75,
            "Case Management": 80,
            "Legal Drafting": 75,
            "Client Communication": 70,
            "Litigation Support": 80
        }
    },
    "SEO Specialist": {
        "Skills": {
            "SEO Strategy": 95,
            "Google Analytics": 90,
            "Keyword Research": 85,
            "Content Optimization": 80,
            "Link Building": 85,
            "Technical SEO": 80,
            "On-Page SEO": 75,
            "Off-Page SEO": 75,
            "Site Audit": 80,
            "Competitor Analysis": 75
        }
    },
    "Retail Manager": {
        "Skills": {
            "Customer Service": 90,
            "Leadership": 85,
            "Inventory Management": 80,
            "Sales Strategy": 85,
            "Communication": 90,
            "Problem Solving": 75,
            "Store Operations": 80,
            "Employee Training": 75,
            "Visual Merchandising": 70,
            "Sales Forecasting": 75
        }
    },
    "Supply Chain Manager": {
        "Skills": {
            "Logistics": 90,
            "Inventory Management": 85,
            "Demand Forecasting": 80,
            "Supplier Relations": 80,
            "ERP Software": 75,
            "Project Management": 85,
            "Process Optimization": 75,
            "Data Analysis": 80,
            "Budgeting": 70,
            "Problem Solving": 75
        }
    }
}
job_titles=[]
for i in dataset.keys():
    job_titles.append(i)

for i in dataset.keys():
    job_id=GetJob(i.lower()).job_id
    skills=dataset[i]["Skills"]
    for j in skills.keys():
        if(type(skills[j])!=int):
            for k in skills[j].keys():
                print(k,j,skills[j][k])
                skill_id=GetSkill(k.lower()).skill_id
                AddJobSkill(job_id,skill_id,skills[j][k],j.lower())
        else:
            print(j,skills[j])
            skill_id=GetSkill(j.lower()).skill_id
            AddJobSkill(job_id,skill_id,skills[j])
'''
