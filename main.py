from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import PyPDF2, io, re, random
from typing import List, Dict

app = FastAPI(title="CareerVerse AI")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class CareerVerseEngine:
    def __init__(self):
        self.skill_db = {
            "Python":["python"],"JavaScript":["javascript","js","node"],"TypeScript":["typescript"],
            "React":["react","next.js"],"Angular":["angular"],"Vue":["vue","nuxt"],
            "Java":["java","spring"],"C++":["c++","cpp"],"Go":["golang","go"],
            "SQL":["sql","mysql","postgresql"],"MongoDB":["mongodb"],"Redis":["redis"],
            "AWS":["aws","ec2","s3","lambda"],"Azure":["azure"],"GCP":["gcp"],
            "Docker":["docker"],"Kubernetes":["kubernetes","k8s"],
            "Machine Learning":["machine learning","ml"],"Deep Learning":["deep learning","neural"],
            "TensorFlow":["tensorflow"],"PyTorch":["pytorch"],"NLP":["nlp"],
            "Computer Vision":["computer vision","cv"],"Data Science":["data science"],
            "Statistics":["statistics"],"Power BI":["power bi"],"Tableau":["tableau"],
            "Pandas":["pandas"],"NumPy":["numpy"],"Scikit-learn":["scikit","sklearn"],
            "Git":["git","github"],"Linux":["linux","bash"],"REST API":["rest","api"],
            "HTML":["html"],"CSS":["css","tailwind"],"Figma":["figma"],"Testing":["testing","jest"],
            "CI/CD":["ci/cd","jenkins"],"GraphQL":["graphql"],"Firebase":["firebase"],
            "Swift":["swift","ios"],"Kotlin":["kotlin","android"],"Rust":["rust"]
        }
        
        self.skill_details = {
            "Python":{"difficulty":"Easy","time_to_learn":"4-8 weeks","demand":"Very High","salary_impact":"+30%","prerequisites":"None","category":"Programming","why_learn":"Python is the #1 language for AI, Data Science, and Web Development. Most versatile and in-demand skill in 2025. Used by Google, NASA, Netflix. Average salary boost: 30%."},
            "JavaScript":{"difficulty":"Easy","time_to_learn":"4-8 weeks","demand":"Very High","salary_impact":"+25%","prerequisites":"HTML/CSS","category":"Programming","why_learn":"Runs the entire internet. Every website uses JavaScript. Essential for Frontend, Backend (Node.js), and Full Stack roles. 98% of websites use it."},
            "TypeScript":{"difficulty":"Medium","time_to_learn":"2-4 weeks","demand":"High","salary_impact":"+15%","prerequisites":"JavaScript","category":"Programming","why_learn":"Adds type safety to JavaScript. Used by Microsoft, Slack, Airbnb. Reduces bugs by 15% in production. Becoming industry standard."},
            "React":{"difficulty":"Medium","time_to_learn":"4-8 weeks","demand":"Very High","salary_impact":"+28%","prerequisites":"JavaScript","category":"Frontend","why_learn":"Most popular frontend framework. Used by Facebook, Instagram, Netflix, WhatsApp. 80% of job listings require React skills."},
            "Angular":{"difficulty":"Hard","time_to_learn":"6-10 weeks","demand":"Medium","salary_impact":"+20%","prerequisites":"TypeScript","category":"Frontend","why_learn":"Google's enterprise framework. Complete solution for large-scale apps. Preferred by banks and enterprise companies."},
            "Vue":{"difficulty":"Easy","time_to_learn":"2-4 weeks","demand":"Medium","salary_impact":"+15%","prerequisites":"JavaScript","category":"Frontend","why_learn":"Simplest framework to learn. Used by Alibaba, Xiaomi, GitLab. Fastest growing framework in Asia."},
            "Java":{"difficulty":"Medium","time_to_learn":"8-12 weeks","demand":"High","salary_impact":"+25%","prerequisites":"None","category":"Programming","why_learn":"Enterprise backbone. Powers Android apps, banking systems, and large-scale applications. 3 billion devices run Java."},
            "C++":{"difficulty":"Hard","time_to_learn":"8-12 weeks","demand":"Medium","salary_impact":"+20%","prerequisites":"None","category":"Programming","why_learn":"High-performance computing. Used in game engines, trading systems, and embedded devices. Unmatched speed and control."},
            "Go":{"difficulty":"Medium","time_to_learn":"2-4 weeks","demand":"High","salary_impact":"+22%","prerequisites":"Programming basics","category":"Programming","why_learn":"Google's language for cloud services. Used by Docker, Kubernetes, Uber. Perfect for microservices and concurrent systems."},
            "SQL":{"difficulty":"Easy","time_to_learn":"2-4 weeks","demand":"Very High","salary_impact":"+20%","prerequisites":"None","category":"Database","why_learn":"Data is the new oil. SQL is required for EVERY Data, Backend, and Analytics role. Most common interview topic."},
            "MongoDB":{"difficulty":"Easy","time_to_learn":"2-4 weeks","demand":"High","salary_impact":"+15%","prerequisites":"None","category":"Database","why_learn":"Leading NoSQL database. Perfect for modern apps with flexible data. Used by Uber, eBay, Adobe."},
            "Redis":{"difficulty":"Easy","time_to_learn":"1-2 weeks","demand":"Medium","salary_impact":"+10%","prerequisites":"None","category":"Database","why_learn":"Lightning-fast caching. Used by Twitter, GitHub, Snapchat for real-time features. Boosts app performance 100x."},
            "AWS":{"difficulty":"Hard","time_to_learn":"8-12 weeks","demand":"Very High","salary_impact":"+35%","prerequisites":"Networking basics","category":"Cloud","why_learn":"Largest cloud provider (32% market). AWS certification can double your salary. Powers Netflix, Airbnb, NASA."},
            "Azure":{"difficulty":"Hard","time_to_learn":"8-12 weeks","demand":"High","salary_impact":"+30%","prerequisites":"Networking basics","category":"Cloud","why_learn":"Microsoft's cloud. Preferred by enterprises. Integrates perfectly with Microsoft tools. Growing rapidly."},
            "GCP":{"difficulty":"Hard","time_to_learn":"8-12 weeks","demand":"Medium","salary_impact":"+25%","prerequisites":"Networking basics","category":"Cloud","why_learn":"Google's cloud. Leader in AI/ML services and data analytics. Used by Spotify, PayPal, Toyota."},
            "Docker":{"difficulty":"Medium","time_to_learn":"2-4 weeks","demand":"Very High","salary_impact":"+25%","prerequisites":"Linux basics","category":"DevOps","why_learn":"Standard for containerization. Deploy apps anywhere consistently. Required for all DevOps and Backend roles."},
            "Kubernetes":{"difficulty":"Hard","time_to_learn":"6-10 weeks","demand":"Very High","salary_impact":"+35%","prerequisites":"Docker","category":"DevOps","why_learn":"Orchestrates containers at scale. Essential for cloud-native roles. Top 3 highest paying tech skill."},
            "Machine Learning":{"difficulty":"Hard","time_to_learn":"8-12 weeks","demand":"Very High","salary_impact":"+40%","prerequisites":"Python, Statistics","category":"AI/ML","why_learn":"AI is transforming every industry. ML engineers are highest paid tech pros. Used in healthcare, finance, autonomous vehicles."},
            "Deep Learning":{"difficulty":"Hard","time_to_learn":"8-12 weeks","demand":"High","salary_impact":"+45%","prerequisites":"Machine Learning","category":"AI/ML","why_learn":"Powers ChatGPT, self-driving cars, medical diagnosis. Most cutting-edge field. Companies paying $300K+ for experts."},
            "TensorFlow":{"difficulty":"Medium","time_to_learn":"4-8 weeks","demand":"High","salary_impact":"+30%","prerequisites":"Python, ML","category":"AI/ML","why_learn":"Google's ML framework. Industry standard for production ML. Used by Airbnb, Coca-Cola, Intel."},
            "PyTorch":{"difficulty":"Medium","time_to_learn":"4-8 weeks","demand":"High","salary_impact":"+30%","prerequisites":"Python, ML","category":"AI/ML","why_learn":"Facebook's ML framework. #1 for research. Used by Tesla, OpenAI, Stanford. More intuitive than TensorFlow."},
            "NLP":{"difficulty":"Hard","time_to_learn":"6-10 weeks","demand":"High","salary_impact":"+30%","prerequisites":"Python, ML","category":"AI/ML","why_learn":"Natural Language Processing. Powers chatbots, translators, voice assistants. ChatGPT runs on NLP. Exploding field."},
            "Computer Vision":{"difficulty":"Hard","time_to_learn":"6-10 weeks","demand":"High","salary_impact":"+30%","prerequisites":"Python, ML","category":"AI/ML","why_learn":"Teaches computers to see. Used in face recognition, medical imaging, autonomous vehicles. 50% growth in CV jobs."},
            "Data Science":{"difficulty":"Medium","time_to_learn":"8-12 weeks","demand":"Very High","salary_impact":"+35%","prerequisites":"Python, Statistics","category":"Data","why_learn":"Sexiest job of 21st century. Extract insights from data. Used by every major company. 650% job growth since 2012."},
            "Statistics":{"difficulty":"Medium","time_to_learn":"4-8 weeks","demand":"High","salary_impact":"+25%","prerequisites":"Math basics","category":"Data","why_learn":"Foundation of data science and ML. Critical for A/B testing, experimentation, and decision making."},
            "Power BI":{"difficulty":"Easy","time_to_learn":"2-4 weeks","demand":"High","salary_impact":"+15%","prerequisites":"None","category":"Data","why_learn":"Microsoft's BI tool. Create stunning dashboards. Used by 97% of Fortune 500. Essential for business analytics."},
            "Tableau":{"difficulty":"Easy","time_to_learn":"2-4 weeks","demand":"High","salary_impact":"+15%","prerequisites":"None","category":"Data","why_learn":"#1 data visualization tool. Used by Amazon, Walmart, Netflix. Transforms complex data into beautiful insights."},
            "Pandas":{"difficulty":"Easy","time_to_learn":"1-2 weeks","demand":"High","salary_impact":"+10%","prerequisites":"Python","category":"Data","why_learn":"Python's data manipulation library. Essential for any data work. Used in 80% of data science projects."},
            "NumPy":{"difficulty":"Easy","time_to_learn":"1-2 weeks","demand":"High","salary_impact":"+10%","prerequisites":"Python","category":"Data","why_learn":"Numerical computing for Python. Foundation of all ML libraries. 50x faster than regular Python lists."},
            "Scikit-learn":{"difficulty":"Medium","time_to_learn":"2-4 weeks","demand":"High","salary_impact":"+20%","prerequisites":"Python, ML","category":"AI/ML","why_learn":"Most popular ML library. Simple and efficient. Used in 70% of ML projects. Perfect for beginners."},
            "Git":{"difficulty":"Easy","time_to_learn":"1-2 weeks","demand":"Essential","salary_impact":"+10%","prerequisites":"None","category":"Tools","why_learn":"Version control is mandatory. Every developer uses Git daily. Track changes, collaborate, deploy confidently."},
            "Linux":{"difficulty":"Medium","time_to_learn":"4-8 weeks","demand":"High","salary_impact":"+20%","prerequisites":"None","category":"Tools","why_learn":"Most servers run Linux. Essential for DevOps, Backend, Cloud roles. Powers 96% of top 1M servers."},
            "REST API":{"difficulty":"Easy","time_to_learn":"1-2 weeks","demand":"Essential","salary_impact":"+15%","prerequisites":"Programming basics","category":"Backend","why_learn":"How apps communicate. Essential for any web/mobile developer. Used in every modern application."},
            "HTML":{"difficulty":"Very Easy","time_to_learn":"1-2 weeks","demand":"Essential","salary_impact":"+5%","prerequisites":"None","category":"Frontend","why_learn":"Building block of the web. Every website starts with HTML. First skill every web developer learns."},
            "CSS":{"difficulty":"Easy","time_to_learn":"2-4 weeks","demand":"Essential","salary_impact":"+10%","prerequisites":"HTML","category":"Frontend","why_learn":"Makes websites beautiful. From simple styles to complex animations. Frontend developers must master CSS."},
            "Figma":{"difficulty":"Easy","time_to_learn":"1-2 weeks","demand":"Medium","salary_impact":"+5%","prerequisites":"None","category":"Design","why_learn":"Industry standard for UI/UX design. Collaborate in real-time. Used by Microsoft, Uber, Zoom."},
            "Testing":{"difficulty":"Medium","time_to_learn":"2-4 weeks","demand":"High","salary_impact":"+15%","prerequisites":"Programming basics","category":"Quality","why_learn":"Ensures code quality. Reduces bugs and production issues. TDD is standard practice at top tech companies."},
            "CI/CD":{"difficulty":"Medium","time_to_learn":"2-4 weeks","demand":"High","salary_impact":"+20%","prerequisites":"Git, Docker","category":"DevOps","why_learn":"Automates deployment. Code to production in minutes. Essential for modern software delivery."},
            "GraphQL":{"difficulty":"Medium","time_to_learn":"1-2 weeks","demand":"Medium","salary_impact":"+10%","prerequisites":"REST API","category":"Backend","why_learn":"Modern API query language. Fetch exactly what you need. Used by Facebook, GitHub, Shopify."},
            "Firebase":{"difficulty":"Easy","time_to_learn":"1-2 weeks","demand":"Medium","salary_impact":"+10%","prerequisites":"None","category":"Backend","why_learn":"Google's backend-as-a-service. Build apps without servers. Perfect for startups and MVPs."},
            "Swift":{"difficulty":"Medium","time_to_learn":"6-10 weeks","demand":"Medium","salary_impact":"+20%","prerequisites":"Programming basics","category":"Mobile","why_learn":"Apple's language for iOS apps. Build apps for iPhone, iPad, Mac. 1.5 billion Apple devices worldwide."},
            "Kotlin":{"difficulty":"Medium","time_to_learn":"4-8 weeks","demand":"Medium","salary_impact":"+20%","prerequisites":"Java","category":"Mobile","why_learn":"Modern Android development. Google's preferred language. 70% of top Android apps use Kotlin."},
            "Rust":{"difficulty":"Hard","time_to_learn":"6-10 weeks","demand":"Medium","salary_impact":"+25%","prerequisites":"C++","category":"Programming","why_learn":"Most loved language 7 years running. Memory safe and blazing fast. Used by Mozilla, Dropbox, Cloudflare."}
        }
        
        self.course_db = {
            "Python":[{"name":"Python Full Course (freeCodeCamp)","url":"https://www.youtube.com/watch?v=rfscVS0vtbw","type":"YouTube","duration":"4h"},{"name":"Python for Everybody (Coursera)","url":"https://www.coursera.org/specializations/python","type":"Free Audit","duration":"8 weeks"}],
            "JavaScript":[{"name":"JavaScript Full Course (Bro Code)","url":"https://www.youtube.com/watch?v=lfmg-EJ8gm4","type":"YouTube","duration":"8h"},{"name":"JavaScript.info","url":"https://javascript.info","type":"Free","duration":"Self-paced"}],
            "TypeScript":[{"name":"TypeScript Full Course","url":"https://www.youtube.com/watch?v=30LWjhZzg50","type":"YouTube","duration":"3h"}],
            "React":[{"name":"React Full Course (freeCodeCamp)","url":"https://www.youtube.com/watch?v=bMknfKXIFA8","type":"YouTube","duration":"12h"},{"name":"React Official Docs","url":"https://react.dev/learn","type":"Free","duration":"Self-paced"}],
            "Angular":[{"name":"Angular Full Course","url":"https://www.youtube.com/watch?v=3qBXWUpoPHo","type":"YouTube","duration":"10h"}],
            "Vue":[{"name":"Vue.js Full Course","url":"https://www.youtube.com/watch?v=FXpIoQ_rT_c","type":"YouTube","duration":"5h"}],
            "Java":[{"name":"Java Full Course (Bro Code)","url":"https://www.youtube.com/watch?v=xk4_1vDrzzo","type":"YouTube","duration":"12h"}],
            "C++":[{"name":"C++ Full Course (Bro Code)","url":"https://www.youtube.com/watch?v=-TkoO8Z07hI","type":"YouTube","duration":"6h"}],
            "Go":[{"name":"Golang Full Course","url":"https://www.youtube.com/watch?v=un6ZyFkqFKo","type":"YouTube","duration":"7h"}],
            "SQL":[{"name":"SQL Full Course (freeCodeCamp)","url":"https://www.youtube.com/watch?v=HXV3zeQKqGY","type":"YouTube","duration":"4h"},{"name":"SQL W3Schools","url":"https://www.w3schools.com/sql","type":"Free","duration":"2 weeks"}],
            "MongoDB":[{"name":"MongoDB Full Course","url":"https://www.youtube.com/watch?v=c2M-rlkkT5o","type":"YouTube","duration":"4h"}],
            "Redis":[{"name":"Redis Full Course","url":"https://www.youtube.com/watch?v=G1rOthIU-uo","type":"YouTube","duration":"3h"}],
            "AWS":[{"name":"AWS Full Course (freeCodeCamp)","url":"https://www.youtube.com/watch?v=RrKRN9zRBWs","type":"YouTube","duration":"10h"},{"name":"AWS Training","url":"https://aws.amazon.com/training","type":"Free","duration":"Self-paced"}],
            "Azure":[{"name":"Azure Full Course","url":"https://www.youtube.com/watch?v=NKEFWyqJ5XA","type":"YouTube","duration":"6h"}],
            "GCP":[{"name":"GCP Full Course","url":"https://www.youtube.com/watch?v=IUU6OR8yHCc","type":"YouTube","duration":"7h"}],
            "Docker":[{"name":"Docker Full Course (TechWorld with Nana)","url":"https://www.youtube.com/watch?v=3c-iBn73dDE","type":"YouTube","duration":"2h"},{"name":"Docker Official Guide","url":"https://docs.docker.com/get-started","type":"Free","duration":"2 weeks"}],
            "Kubernetes":[{"name":"Kubernetes Full Course (TechWorld with Nana)","url":"https://www.youtube.com/watch?v=X48VuDVv0do","type":"YouTube","duration":"4h"}],
            "Machine Learning":[{"name":"ML Full Course (freeCodeCamp)","url":"https://www.youtube.com/watch?v=NWONeJKn6kc","type":"YouTube","duration":"7h"},{"name":"ML by Andrew Ng","url":"https://www.coursera.org/learn/machine-learning","type":"Free Audit","duration":"11 weeks"}],
            "Deep Learning":[{"name":"Deep Learning Full Course","url":"https://www.youtube.com/watch?v=6M5VXKLf4D4","type":"YouTube","duration":"8h"}],
            "TensorFlow":[{"name":"TensorFlow Full Course","url":"https://www.youtube.com/watch?v=tPYj3fFJGjk","type":"YouTube","duration":"7h"},{"name":"TensorFlow Official","url":"https://www.tensorflow.org/tutorials","type":"Free","duration":"Self-paced"}],
            "PyTorch":[{"name":"PyTorch Full Course","url":"https://www.youtube.com/watch?v=Z_ikDlimN6A","type":"YouTube","duration":"6h"}],
            "NLP":[{"name":"NLP Full Course","url":"https://www.youtube.com/watch?v=dIUTsHM2ZBo","type":"YouTube","duration":"6h"}],
            "Computer Vision":[{"name":"OpenCV Full Course","url":"https://www.youtube.com/watch?v=oXlwWbU8l2o","type":"YouTube","duration":"4h"}],
            "Data Science":[{"name":"Data Science Full Course","url":"https://www.youtube.com/watch?v=ua-CiDNNj30","type":"YouTube","duration":"8h"}],
            "Statistics":[{"name":"Statistics Full Course","url":"https://www.youtube.com/watch?v=xxpc-HPKN28","type":"YouTube","duration":"8h"}],
            "Power BI":[{"name":"Power BI Full Course","url":"https://www.youtube.com/watch?v=g0m5sEHPU-s","type":"YouTube","duration":"6h"}],
            "Tableau":[{"name":"Tableau Full Course","url":"https://www.youtube.com/watch?v=aHaOIvR00So","type":"YouTube","duration":"5h"}],
            "Pandas":[{"name":"Pandas Full Course","url":"https://www.youtube.com/watch?v=vmEHCJofslg","type":"YouTube","duration":"4h"}],
            "NumPy":[{"name":"NumPy Full Course","url":"https://www.youtube.com/watch?v=QUT1VHiLmmI","type":"YouTube","duration":"1h"}],
            "Scikit-learn":[{"name":"Scikit-learn Full Course","url":"https://www.youtube.com/watch?v=pqNCD_5r0IU","type":"YouTube","duration":"3h"}],
            "Git":[{"name":"Git Full Course","url":"https://www.youtube.com/watch?v=RGOj5yH7evk","type":"YouTube","duration":"1h"}],
            "Linux":[{"name":"Linux Full Course","url":"https://www.youtube.com/watch?v=sWbUDq4S6Y8","type":"YouTube","duration":"6h"}],
            "REST API":[{"name":"REST API Full Course","url":"https://www.youtube.com/watch?v=Q-BpqyOT3a8","type":"YouTube","duration":"2h"}],
            "HTML":[{"name":"HTML Full Course (Bro Code)","url":"https://www.youtube.com/watch?v=HGTJBPNC-Gw","type":"YouTube","duration":"4h"}],
            "CSS":[{"name":"CSS Full Course (Bro Code)","url":"https://www.youtube.com/watch?v=wRNinF7YQqQ","type":"YouTube","duration":"6h"}],
            "Figma":[{"name":"Figma Full Course","url":"https://www.youtube.com/watch?v=jwCmIBJ8Jtc","type":"YouTube","duration":"2h"}],
            "Testing":[{"name":"Testing Full Course","url":"https://www.youtube.com/watch?v=oOvURgHcd4w","type":"YouTube","duration":"4h"}],
            "CI/CD":[{"name":"CI/CD Full Course","url":"https://www.youtube.com/watch?v=7K1RitzACmQ","type":"YouTube","duration":"2h"}],
            "GraphQL":[{"name":"GraphQL Full Course","url":"https://www.youtube.com/watch?v=ed8SzALpx1Q","type":"YouTube","duration":"5h"}],
            "Firebase":[{"name":"Firebase Full Course","url":"https://www.youtube.com/watch?v=fgdpvwEWJ9M","type":"YouTube","duration":"5h"}],
            "Swift":[{"name":"Swift Full Course","url":"https://www.youtube.com/watch?v=comQ1-x2a1Q","type":"YouTube","duration":"6h"}],
            "Kotlin":[{"name":"Kotlin Full Course","url":"https://www.youtube.com/watch?v=F9UC9DY-vIU","type":"YouTube","duration":"4h"}],
            "Rust":[{"name":"Rust Full Course","url":"https://www.youtube.com/watch?v=BpPEoZW5IiY","type":"YouTube","duration":"13h"}]
        }

        # Interview resources for EVERY skill
        self.interview_resources = {
            "Python":[{"name":"Python Interview Questions (InterviewBit)","url":"https://www.interviewbit.com/python-interview-questions/"},{"name":"Python Cheat Sheet","url":"https://www.pythoncheatsheet.org/"}],
            "JavaScript":[{"name":"JS Interview Questions","url":"https://www.interviewbit.com/javascript-interview-questions/"},{"name":"JS Cheat Sheet","url":"https://htmlcheatsheet.com/js/"}],
            "React":[{"name":"React Interview Questions","url":"https://www.interviewbit.com/react-interview-questions/"},{"name":"React Cheat Sheet","url":"https://devhints.io/react"}],
            "SQL":[{"name":"SQL Interview Questions","url":"https://www.interviewbit.com/sql-interview-questions/"},{"name":"SQL Practice (LeetCode)","url":"https://leetcode.com/problemset/database/"}],
            "Machine Learning":[{"name":"ML Interview Questions","url":"https://www.interviewbit.com/machine-learning-interview-questions/"},{"name":"ML Cheat Sheet","url":"https://ml-cheatsheet.readthedocs.io/"}],
            "Docker":[{"name":"Docker Interview Questions","url":"https://www.interviewbit.com/docker-interview-questions/"}],
            "AWS":[{"name":"AWS Interview Questions","url":"https://www.interviewbit.com/aws-interview-questions/"}],
            "Git":[{"name":"Git Interview Questions","url":"https://www.interviewbit.com/git-interview-questions/"}]
        }
        
        self.roles = {
            "AI/ML Engineer":{"required":["Python","Machine Learning","Deep Learning","TensorFlow","PyTorch","NLP","Computer Vision","Data Science"],"salary":"6-15 LPA","growth":"35%","companies":"Google, Microsoft, Amazon, TCS, Infosys","market_size":"2.3M jobs globally","future_scope":"AI will create 97M new jobs by 2025","market_rate":"Avg ₹8L fresher, ₹20L+ experienced"},
            "Data Scientist":{"required":["Python","SQL","Statistics","Machine Learning","Pandas","NumPy","Tableau","Power BI"],"salary":"5-12 LPA","growth":"36%","companies":"Amazon, Netflix, Accenture, Deloitte, TCS","market_size":"1.8M jobs globally","future_scope":"28% growth by 2026","market_rate":"Avg ₹6L fresher, ₹15L+ experienced"},
            "Full Stack Developer":{"required":["JavaScript","React","Node.js","SQL","MongoDB","HTML","CSS","Git","Docker"],"salary":"4-10 LPA","growth":"26%","companies":"Flipkart, Swiggy, Zomato, Freshworks, TCS","market_size":"5.2M jobs globally","future_scope":"#1 most demanded tech role","market_rate":"Avg ₹5L fresher, ₹12L+ experienced"},
            "Frontend Developer":{"required":["HTML","CSS","JavaScript","React","TypeScript","Figma"],"salary":"3-8 LPA","growth":"25%","companies":"CRED, PhonePe, MakeMyTrip, Paytm","market_size":"3.1M jobs globally","future_scope":"25% annual growth","market_rate":"Avg ₹4L fresher, ₹10L+ experienced"},
            "Backend Developer":{"required":["Python","Java","SQL","Docker","REST API","Redis","Linux"],"salary":"5-12 LPA","growth":"26%","companies":"Razorpay, PhonePe, Swiggy, Zomato","market_size":"2.8M jobs globally","future_scope":"Always in high demand","market_rate":"Avg ₹5L fresher, ₹14L+ experienced"},
            "DevOps Engineer":{"required":["Docker","Kubernetes","AWS","CI/CD","Linux","Git"],"salary":"6-14 LPA","growth":"30%","companies":"HashiCorp, Datadog, Accenture, Infosys","market_size":"1.5M jobs globally","future_scope":"35% YoY adoption growth","market_rate":"Avg ₹7L fresher, ₹18L+ experienced"}
        }

        self.jobs_db = {
            "AI/ML Engineer":[{"title":"ML Engineer","company":"Google","location":"Bangalore","type":"Full-time"},{"title":"AI Intern","company":"Microsoft","location":"Hyderabad","type":"Internship"},{"title":"Data Scientist","company":"TCS","location":"Mumbai","type":"Full-time"}],
            "Data Scientist":[{"title":"Data Scientist","company":"Accenture","location":"Bangalore","type":"Full-time"},{"title":"Data Analyst Intern","company":"Deloitte","location":"Mumbai","type":"Internship"},{"title":"Business Analyst","company":"TCS","location":"Chennai","type":"Full-time"}],
            "Full Stack Developer":[{"title":"Full Stack Developer","company":"Flipkart","location":"Bangalore","type":"Full-time"},{"title":"SDE Intern","company":"Swiggy","location":"Bangalore","type":"Internship"},{"title":"Web Developer","company":"Zomato","location":"Gurgaon","type":"Full-time"}],
            "Frontend Developer":[{"title":"Frontend Developer","company":"CRED","location":"Bangalore","type":"Full-time"},{"title":"UI Intern","company":"PhonePe","location":"Bangalore","type":"Internship"},{"title":"React Developer","company":"Paytm","location":"Noida","type":"Full-time"}],
            "Backend Developer":[{"title":"Backend Developer","company":"Razorpay","location":"Bangalore","type":"Full-time"},{"title":"SDE Intern","company":"PhonePe","location":"Bangalore","type":"Internship"}],
            "DevOps Engineer":[{"title":"DevOps Engineer","company":"Infosys","location":"Pune","type":"Full-time"},{"title":"Cloud Intern","company":"Accenture","location":"Bangalore","type":"Internship"}]
        }

        self.mcq_db = {
            "Python":[{"q":"File extension for Python?","options":[".py",".python",".pyth",".pt"],"answer":0},{"q":"How to create variable?","options":["x = 5","var x = 5","int x = 5","x := 5"],"answer":0},{"q":"Output: print(2**3)?","options":["6","8","9","5"],"answer":1}],
            "Machine Learning":[{"q":"Supervised learning uses?","options":["Labeled data","Unlabeled data","Games","None"],"answer":0},{"q":"Classification algorithm?","options":["Linear Regression","K-Means","Decision Tree","PCA"],"answer":2},{"q":"Overfitting means?","options":["Good train, bad test","Bad both","Too simple","None"],"answer":0}],
            "React":[{"q":"React created by?","options":["Facebook","Google","Microsoft","Twitter"],"answer":0},{"q":"What is JSX?","options":["JavaScript XML","Java Syntax","JSON XML","None"],"answer":0},{"q":"State management hook?","options":["useState","useEffect","useContext","useReducer"],"answer":0}],
            "SQL":[{"q":"SQL stands for?","options":["Structured Query Language","Simple Query Language","Standard Query Language","None"],"answer":0},{"q":"Get data command?","options":["SELECT","GET","FETCH","RETRIEVE"],"answer":0},{"q":"Primary key is?","options":["Unique identifier","Foreign key","Index","None"],"answer":0}]
        }

    def extract_text(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        return " ".join([p.extract_text() or "" for p in reader.pages])

    def extract_email(self, text):
        m = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        return m.group(0) if m else ""

    def extract_name(self, text):
        for line in text.split('\n')[:10]:
            c = line.strip()
            if 2<len(c)<30 and not any(k in c.lower() for k in ['resume','cv','email','phone','address','linkedin','github','@']):
                if re.match(r'^[A-Za-z\s]+$', c): return c.title()
        return "Student"

    def extract_skills(self, text):
        t = text.lower()
        return [s for s,p in self.skill_db.items() if any(pt in t for pt in p)]

    def get_mcq(self, skill):
        if skill in self.mcq_db: return self.mcq_db[skill]
        return [{"q":f"What is {skill}?","options":["Technology","Cooking","Driving","Farming"],"answer":0},{"q":f"Is {skill} useful?","options":["Yes","No","Maybe","Never"],"answer":0},{"q":f"Learn {skill}?","options":["Yes","No","Maybe","Never"],"answer":0}]

    def analyze(self, pdf_file, target_role, user_name):
        text = self.extract_text(pdf_file) if pdf_file else ""
        name = self.extract_name(text) if not user_name else user_name
        email = self.extract_email(text) if text else ""
        skills = self.extract_skills(text) if text else []
        
        role_data = self.roles.get(target_role, self.roles["Full Stack Developer"])
        required = role_data.get("required",[])
        found = [s for s in skills if s in required]
        missing = [s for s in required if s not in skills]
        match = round(len(found)/len(required)*100) if required else 0
        
        found_details = []
        for s in found:
            d = self.skill_details.get(s, {"difficulty":"N/A","time_to_learn":"N/A","demand":"N/A","salary_impact":"N/A","why_learn":"","category":"N/A"})
            interview = self.interview_resources.get(s, [])
            found_details.append({"skill":s,**d,"interview_resources":interview})
        
        missing_details = []
        for s in missing:
            d = self.skill_details.get(s, {"difficulty":"N/A","time_to_learn":"N/A","demand":"N/A","salary_impact":"N/A","why_learn":"","category":"N/A"})
            courses = self.course_db.get(s, [])
            missing_details.append({"skill":s,**d,"courses":courses[:2]})
        
        xp = match * 10
        level = max(1, min(10, match//10 + 1))
        ranks = ["Beginner","Learner","Explorer","Practitioner","Skilled","Advanced","Expert","Master","Guru","Legend"]
        
        quests = []
        for skill in missing[:5]:
            courses = self.course_db.get(skill, [{"name":f"Learn {skill}","url":f"https://www.youtube.com/results?search_query=learn+{skill.replace(' ','+')}","type":"YouTube","duration":"Self-paced"}])
            mcq = self.get_mcq(skill)
            quests.append({"title":f"Learn {skill}","desc":f"Master {skill} with video tutorials","xp":200,"type":"skill","courses":courses,"mcq":mcq,"skill":skill})
        
        roadmap = []
        for i in range(0, len(missing), 3):
            chunk = missing[i:i+3]
            tasks = [{"skill":s,"resources":self.course_db.get(s,[{"name":f"Learn {s}","url":f"https://www.youtube.com/results?search_query=learn+{s.replace(' ','+')}","type":"YouTube","duration":"Self-paced"}])[:2],"project":f"Build a {s} project"} for s in chunk]
            roadmap.append({"phase":f"Phase {i//3+1}","tasks":tasks})
        
        jobs = self.jobs_db.get(target_role, [])
        
        # Gather ALL interview resources based on user's skills AND role requirements
        all_interview = []
        for s in found[:6]:
            if s in self.interview_resources:
                for r in self.interview_resources[s]:
                    all_interview.append({"skill":s,**r})
        
        return {
            "user_name": name,"user_email": email if email else "Not found",
            "profile": {"target_role":target_role,"skills":skills,"role_info":{k:v for k,v in role_data.items()}},
            "skill_gap": {"found":found,"missing":missing,"match":match,"found_details":found_details,"missing_details":missing_details},
            "xp": {"total":xp,"level":level,"rank":ranks[min(level-1,9)],"match_percent":match},
            "quests": quests,"roadmap": roadmap,"jobs": jobs,"total_quests": len(quests),
            "interview_resources": all_interview
        }

engine = CareerVerseEngine()

@app.get("/")
async def root(): return {"status":"CareerVerse AI Ready"}

@app.post("/analyze-resume")
async def analyze(file: UploadFile = File(None), target_role: str = Form("AI/ML Engineer"), user_name: str = Form("")):
    try:
        contents = await file.read() if file else None
        pdf_file = io.BytesIO(contents) if contents else None
        return JSONResponse(content=engine.analyze(pdf_file, target_role, user_name))
    except Exception as e:
        raise HTTPException(500,str(e))