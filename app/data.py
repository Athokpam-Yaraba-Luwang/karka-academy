# Karka AI & Tech Academy website · SiteSprint, Karka Infini AI 2026
# Built by Athokpam Yaraba Luwang · https://www.linkedin.com/in/yaraba-athokpam-856538343/
"""Site content for Karka AI & Tech Academy.

Everything the templates render lives here so the marketing team can edit
copy without touching markup. Facts (courses, stats, testimonials, partners,
contact) are taken from karka.academy and infini.karka.academy.

Items marked `# EXAMPLE` are illustrative and should be replaced with the
academy's real records before going live.
"""

from __future__ import annotations

SITE = {
    "name": "Karka AI & Tech Academy",
    "short": "Karka",
    "url": "https://www.karka.academy",
    "tagline": "Your future, powered by AI.",
    "description": (
        "Karka AI & Tech Academy, Nagercoil — AI-first career tracks in Full Stack, "
        "Gen AI, Data, Design and more. Real client internships, on-site mentors and "
        "Pay After Placement: ₹0 upfront, pay only after you get hired."
    ),
    "phone": "+91 94875 30243",
    "phone_raw": "+919487530243",
    "whatsapp": "919487530243",
    "email": "contact@karka.academy",
    "city": "Nagercoil",
    "region": "Tamil Nadu",
    "address": "Nagercoil, Tamil Nadu, India",
    "maps": "https://maps.google.com/?cid=15414470293799306704",
    "maps_embed": (
        "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d1959.1854741572813!2d77.431108!3d8.180149"
        "!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b04f15dde0aa367%3A0xd5eb331016b805d0"
        "!2sKarka%20AI%20%26%20Tech%20Academy%20%7C%20Internships%20%26%20Job%20Placements"
        "!5e1!3m2!1sen!2sus!4v1792784363109!5m2!1sen!2sus"
    ),
    "socials": {
        "instagram": "https://www.instagram.com/karka.ai/",
        "linkedin": "https://www.linkedin.com/company/karka-academy/",
        "facebook": "https://www.facebook.com/karkasoftwareacademy/",
    },
    "rating": 4.8,
    "rating_count": 200,
    "founded": 2020,
    "ig_handle": "@karka.ai",
    "ig_followers": "14.7k",
    "author": "Athokpam Yaraba Luwang",
    "author_url": "https://www.linkedin.com/in/yaraba-athokpam-856538343/",
    "ig_bio": ["AI-First Career Academy", "Making GenZs AI Ready", "Jobs · Internships · Projects"],
}

# From the LinkedIn company overview.
MISSION = {
    "problem": [
        ("Self-learning", "isn't effective", "for most graduates."),
        ("Mentored learning", "isn't affordable", "for most families."),
        ("Companies", "can't find skilled", "entry-level graduates."),
    ],
    "promise": "We find graduates who can learn but couldn't get hired with what college taught them. We make them industry-ready through intensive bootcamps, with no hefty fees and Pay After Placement.",
    "for_companies": "Industry-ready graduates with zero hiring cost.",
}

NAV = [
    {"label": "Tracks", "href": "/#tracks"},
    {"label": "Pay After Placement", "href": "/#pap"},
    {"label": "Internships", "href": "/#internship"},
    {"label": "Placements", "href": "/#placements"},
    {"label": "FAQ", "href": "/#faq"},
]

AUDIENCES = ["School Student", "College Student", "Graduate", "Working Professional"]

STATS = [
    {"prefix": "₹", "value": 0, "suffix": "", "label": "upfront tuition", "note": "pay after you're hired"},
    {"prefix": "", "value": 24, "suffix": " LPA", "label": "highest package", "note": "and climbing"},
    {"prefix": "", "value": 120, "suffix": "%", "label": "average salary hike", "note": "for career switchers"},
    {"prefix": "", "value": 50, "suffix": "+", "label": "hiring partners", "note": "regional & global"},
]

# Logos (cropped from karka.academy, recoloured for dark backgrounds) live in
# static/img/logos/<logo>.webp at 56px tall; `w` is the display width at 28px.
# Companies without a clean logo file fall back to a styled text wordmark.
PARTNERS = [
    {"name": "amazon", "logo": "amazon", "w": 93},
    {"name": "tcs", "logo": "tcs", "w": 45},
    {"name": "DigitKode"},
    {"name": "HCL", "logo": "hcl", "w": 127},
    {"name": "Maruti Suzuki"},
    {"name": "matrimony.com", "logo": "matrimony", "w": 180},
    {"name": "Neztora"},
    {"name": "NOVAC", "logo": "novac", "w": 104},
    {"name": "Arrow Thought"},
    {"name": "Capecom", "logo": "capecom", "w": 117},
    {"name": "SUHI"},
    {"name": "FLOW", "logo": "flow", "w": 103},
    {"name": "INDEX"},
    {"name": "SODISYS", "logo": "sodisys", "w": 106},
    {"name": "Sea Sense"},
]

# Real "Got Placed" posts from Instagram @karka.ai
PLACED = [
    {"name": "Subashini M", "role": "Software Developer", "company": "DigitKode"},
    {"name": "Abitha A", "role": "Software Developer", "company": "DigitKode"},
    {"name": "Safin Jefferson A", "role": "Node.js Developer", "company": "Neztora"},
    {"name": "V. Sabinesh", "role": "Data Analyst", "company": "Maruti Suzuki"},
    {"name": "Muthu Lekshmi", "role": "Python Developer cum Tester", "company": "Terralens Innovations"},
    {"name": "Meega", "role": "Software Developer", "company": "INDEX"},
    {"name": "Ashmiya", "role": "Research Programmer (Java)", "company": "SUHI"},
    {"name": "Grace Asha", "role": "Research Analyst", "company": "Arrow Thought"},
    {"name": "Saravana Kumar", "role": "Research Assistant", "company": "Sea Sense"},
    {"name": "Sabin", "role": "Graphic Designer", "company": "Tony Chapel"},
    {"name": "Sreedhar", "role": "Graphic Designer", "company": "JS Digital Desk"},
]

INTERN_ONBOARDED = {"name": "Shenbaga Janani A S", "company": "AgileTribers"}

TICKER = [
    "₹0 upfront",
    "Real client internships",
    "AI-first curriculum",
    "On-site mentors",
    "24 LPA highest package",
    "Mock interviews",
    "Job referrals",
]

WHY = [
    {
        "icon": "wallet",
        "title": "Pay after you get hired",
        "body": "Other institutes bill you upfront, job or no job. Here you start at ₹0 because we carry the risk. Fees begin only after you land a tech job.",
    },
    {
        "icon": "sparkles",
        "title": "AI-first, future-proof curriculum",
        "body": "Gen AI workflows, prompt engineering and AI automation are part of every track. You build software and interfaces the way modern teams do.",
    },
    {
        "icon": "rocket",
        "title": "Live internships, not paper certificates",
        "body": "Employers hire proof. You ship real client projects and graduate with a live, deployable portfolio plus an official internship certificate.",
    },
    {
        "icon": "users",
        "title": "On-site expert mentorship",
        "body": "Daily access to fully equipped labs and face-to-face mentors who track your progress and unblock your bugs in real time.",
    },
    {
        "icon": "network",
        "title": "Direct hiring pipelines",
        "body": "Skip the crowded job portals. Your portfolio goes straight to our hiring partners, local tech companies and startup ecosystems.",
    },
    {
        "icon": "grid",
        "title": "4-pillar job readiness",
        "body": "Core tech stack, AI speed, business communication and mock interviews. You leave as a complete professional, not just a coder.",
    },
]

PILLARS = [
    {
        "no": "01",
        "title": "Master the language of business",
        "items": ["Listening", "Speaking", "Reading", "Writing"],
        "tone": "blue",
        "icon": "message",
    },
    {
        "no": "02",
        "title": "Build scalable modern apps",
        "items": ["Web / Mobile", "Data Analytics", "UI/UX Design", "Digital Marketing"],
        "tone": "green",
        "icon": "laptop",
    },
    {
        "no": "03",
        "title": "AI skills",
        "items": ["Prompt Engineering", "AI Automation", "AI Tools", "LLMs"],
        "tone": "violet",
        "icon": "brain",
        "core": True,
    },
    {
        "no": "04",
        "title": "Interview skills",
        "items": ["ATS-friendly profile", "Mock interviews", "Group discussion", "Presentation skills"],
        "tone": "amber",
        "icon": "target",
    },
]

PAP_STEPS = [
    {
        "title": "Enroll & learn",
        "body": "Live sessions with real mentors, real-world projects and industry guidance. ₹0 to start.",
        "icon": "graduation",
    },
    {
        "title": "Get job ready",
        "body": "Resume, LinkedIn, portfolio and interview prep, done with you and not just handed to you.",
        "icon": "briefcase",
    },
    {
        "title": "Get paid, not billed",
        "body": "Focus on learning today. You share your success, and the fees, once you're placed.",
        "icon": "wallet",
    },
]

PAP_INCLUDED = [
    {"label": "1:1 mentorship", "icon": "trophy"},
    {"label": "Placement training", "icon": "check-circle"},
    {"label": "Resume & LinkedIn preparation", "icon": "file"},
    {"label": "Mock interviews", "icon": "users"},
    {"label": "Job referral support", "icon": "message"},
]

# ---------------------------------------------------------------------------
# Courses
# ---------------------------------------------------------------------------
# `featured` courses get a full detail page at /courses/<slug>.

TRACKS = [
    {
        "id": "fullstack",
        "name": "Fullstack",
        "tagline": "Master modern web ecosystems",
        "icon": "code",
        "hue": "violet",
        "popular": True,
        "courses": ["mern-fullstack", "react-java-fullstack", "react-python-fullstack"],
    },
    {
        "id": "genai",
        "name": "Gen AI",
        "tagline": "Lead the AI revolution",
        "icon": "bot",
        "hue": "blue",
        "courses": ["generative-ai-foundations", "generative-ai-mastery", "genai-llm-developer"],
    },
    {
        "id": "data",
        "name": "Data & ML",
        "tagline": "Master data intelligence",
        "icon": "database",
        "hue": "cyan",
        "courses": ["ai-data-science", "data-analytics-ai", "data-engineering"],
    },
    {
        "id": "design",
        "name": "Design",
        "tagline": "Create stunning UI/UX",
        "icon": "palette",
        "hue": "pink",
        "courses": ["ui-ux-design", "web-designing", "graphic-designing"],
    },
    {
        "id": "media",
        "name": "Digital Media",
        "tagline": "Visual storytelling & animation",
        "icon": "video",
        "hue": "rose",
        "courses": ["video-editing", "graphic-designing", "multimedia-animation"],
    },
    {
        "id": "marketing",
        "name": "Content & Marketing",
        "tagline": "Drive growth with strategy",
        "icon": "megaphone",
        "hue": "amber",
        "courses": ["digital-marketing", "seo-analyst", "storytelling-content-writing"],
    },
    {
        "id": "othertech",
        "name": "Other Tech",
        "tagline": "Advanced tech specialisations",
        "icon": "cloud",
        "hue": "blue",
        "courses": ["cloud-devops", "data-engineering", "data-analytics-ai"],
    },
    {
        "id": "nontech",
        "name": "Non-Tech",
        "tagline": "Essential business skills",
        "icon": "briefcase",
        "hue": "amber",
        "courses": ["hr-finance", "tally", "business-analyst"],
    },
]

COURSES: dict[str, dict] = {
    "mern-fullstack": {
        "name": "MERN Fullstack Development",
        "short": "MERN Fullstack",
        "featured": True,
        "badge": "Bootcamp",
        "duration": "6 months",
        "lessons": 48,
        "mode": "On-campus + Online",
        "enrollments": "800+",
        "rating": 4.8,
        "summary": "Master full-stack web development using MongoDB, Express, React and Node.js. Build scalable web apps from scratch, then ship them like a pro with DevOps, system design and production best practices.",
        "stack": ["MongoDB", "Express", "React", "Node.js", "Git", "Docker", "AI copilots"],
        "modules": [
            ("Web foundations", "HTML, modern CSS, responsive layouts and JavaScript fundamentals with AI pair-programming from day one."),
            ("React in depth", "Components, hooks, state, routing and performance. You build a real product UI, not to-do apps."),
            ("Node & Express APIs", "REST APIs, authentication, validation, file uploads and error handling."),
            ("MongoDB & data modelling", "Schemas, indexing, aggregation and integrating data into your apps."),
            ("DevOps & system design", "Git workflows, Docker, CI/CD, cloud deployment and how production systems scale."),
            ("Client internship + capstone", "Ship a live client project in a team and deploy a portfolio that recruiters can click."),
        ],
        "roles": ["Full Stack Developer", "Frontend Developer", "Node.js Developer"],
        "hue": "violet",
        "icon": "code",
    },
    "react-java-fullstack": {
        "name": "React + Java Full Stack Development",
        "short": "React + Java Fullstack",
        "featured": True,
        "duration": "6 months",
        "mode": "On-campus + Online",
        "rating": 4.8,
        "summary": "Enterprise-grade full stack: Java and Spring Boot on the backend and React on the front. It's the stack that service companies and product teams hire for.",
        "stack": ["Java", "Spring Boot", "React", "SQL", "REST", "Git"],
        "modules": [
            ("Core Java & OOP", "Java fundamentals, collections, exceptions and clean object-oriented design."),
            ("Spring Boot", "REST APIs, dependency injection, JPA/Hibernate, security and testing."),
            ("Databases & SQL", "Relational modelling, joins, transactions and query performance."),
            ("React frontend", "Component-driven UIs that talk to your Spring APIs."),
            ("Deployment", "Build, containerise and deploy full-stack apps to the cloud."),
            ("Client internship + capstone", "Team delivery on a real brief, with code reviews from mentors."),
        ],
        "roles": ["Java Full Stack Developer", "Backend Developer", "Software Engineer"],
        "hue": "violet",
        "icon": "layers",
    },
    "react-python-fullstack": {
        "name": "React + Python Full Stack Development",
        "short": "React + Python Fullstack",
        "featured": True,
        "duration": "6 months",
        "mode": "On-campus + Online",
        "rating": 4.8,
        "summary": "Python on the backend, React on the front, and AI built into the middle. It's the fastest route to building AI-powered products.",
        "stack": ["Python", "FastAPI / Django", "React", "SQL", "LLM APIs", "Git"],
        "modules": [
            ("Python for builders", "Python fundamentals, data structures and writing clean, testable code."),
            ("Backend APIs", "Build REST APIs with modern Python frameworks, auth and databases."),
            ("React frontend", "Responsive, accessible interfaces connected to your APIs."),
            ("AI integration", "Plug LLMs and AI automation into real product features."),
            ("Deployment", "Ship to the cloud with CI/CD and monitoring."),
            ("Client internship + capstone", "Deliver a real client project in a team."),
        ],
        "roles": ["Python Full Stack Developer", "Backend Developer", "AI App Developer"],
        "hue": "violet",
        "icon": "layers",
    },
    "generative-ai-foundations": {
        "name": "Generative AI Foundations",
        "short": "Gen AI Foundations",
        "featured": True,
        "duration": "3 months",
        "mode": "Online",
        "enrollments": "900+",
        "rating": 4.8,
        "summary": "Learn the basics of generative AI, prompt engineering and core AI concepts. It's the quickest way to start a tech career that's ready for AI.",
        "stack": ["ChatGPT / Claude / Gemini", "Prompt engineering", "AI automation", "No-code AI tools"],
        "modules": [
            ("How Gen AI works", "LLMs, tokens, embeddings and what models can and can't do, without the hype."),
            ("Prompt engineering", "Patterns, roles, chain-of-thought and evaluating outputs."),
            ("AI for productivity", "Automate research, writing, analysis and everyday workflows."),
            ("AI automation", "Connect tools and build simple agents that do real work."),
            ("Responsible AI", "Bias, privacy and safe use in the workplace."),
            ("Capstone", "Build and present an AI-powered solution to a real problem."),
        ],
        "roles": ["AI Associate", "Prompt Engineer", "AI Operations Analyst"],
        "hue": "blue",
        "icon": "bot",
    },
    "generative-ai-mastery": {"name": "Generative AI Mastery", "short": "Gen AI Mastery", "hue": "blue", "icon": "sparkles"},
    "genai-llm-developer": {"name": "Gen AI (LLM) Developer", "short": "LLM Developer", "hue": "blue", "icon": "bot"},
    "ai-data-science": {
        "name": "AI & Data Science",
        "short": "AI & Data Science",
        "featured": True,
        "duration": "6 months",
        "mode": "On-campus + Online",
        "enrollments": "650+",
        "rating": 4.8,
        "summary": "A complete study of AI and data science. Master the tools and machine learning models that drive the AI revolution, then deploy them.",
        "stack": ["Python", "Pandas", "SQL", "scikit-learn", "TensorFlow", "PyTorch"],
        "modules": [
            ("Python & statistics", "Python for data, probability and the statistics that actually matter."),
            ("Data wrangling & SQL", "Pandas, SQL and cleaning messy, real-world datasets."),
            ("Visualisation & storytelling", "Dashboards and charts that drive decisions."),
            ("Machine learning", "Regression, classification, clustering and model evaluation with scikit-learn."),
            ("Deep learning & Gen AI", "Neural networks with TensorFlow / PyTorch and working with LLMs."),
            ("Deployment + capstone", "Deploy a model behind an API and present your project."),
        ],
        "roles": ["Data Scientist", "ML Engineer", "Data Analyst"],
        "hue": "cyan",
        "icon": "database",
    },
    "data-analytics-ai": {"name": "Data Analytics with AI", "short": "Data Analytics with AI", "hue": "cyan", "icon": "chart"},
    "data-engineering": {"name": "Data Engineering", "short": "Data Engineering", "hue": "cyan", "icon": "database"},
    "ui-ux-design": {
        "name": "UI/UX Design",
        "short": "UI/UX Design",
        "featured": True,
        "duration": "4 months",
        "mode": "On-campus + Online",
        "enrollments": "450+",
        "rating": 4.8,
        "summary": "Master the art of designing intuitive, beautiful user interfaces and experiences using industry-standard tools, from first research to a hand-off developers love.",
        "stack": ["Figma", "Design systems", "Prototyping", "User research", "Accessibility", "AI design tools"],
        "modules": [
            ("Design thinking", "Research, personas, journeys and defining the right problem."),
            ("Visual design", "Type, colour, layout, grids and motion basics."),
            ("Figma pro", "Components, auto-layout, variables and interactive prototypes."),
            ("Design systems", "Tokens, component libraries and documentation."),
            ("Responsive & accessible UI", "Design for every screen and every user."),
            ("Client internship + case studies", "Real client work and a portfolio of case studies."),
        ],
        "roles": ["UI/UX Designer", "Product Designer", "Frontend Developer"],
        "hue": "pink",
        "icon": "palette",
    },
    "web-designing": {"name": "Web Designing", "short": "Web Designing", "hue": "pink", "icon": "globe"},
    "graphic-designing": {"name": "Graphic Designing", "short": "Graphic Designing", "hue": "pink", "icon": "palette"},
    "video-editing": {"name": "Video Editing", "short": "Video Editing", "hue": "rose", "icon": "video"},
    "multimedia-animation": {"name": "Multimedia & Animation", "short": "Multimedia & Animation", "hue": "rose", "icon": "image"},
    "digital-marketing": {"name": "Digital Marketing", "short": "Digital Marketing", "hue": "amber", "icon": "megaphone"},
    "seo-analyst": {"name": "SEO Analyst", "short": "SEO Analyst", "hue": "amber", "icon": "trending"},
    "storytelling-content-writing": {"name": "Storytelling & Content Writing", "short": "Storytelling & Content", "hue": "amber", "icon": "book"},
    "cloud-devops": {"name": "Cloud & DevOps", "short": "Cloud & DevOps", "hue": "blue", "icon": "cloud"},
    "hr-finance": {"name": "HR & Finance", "short": "HR & Finance", "hue": "amber", "icon": "users"},
    "tally": {"name": "Tally", "short": "Tally", "hue": "amber", "icon": "briefcase"},
    "business-analyst": {"name": "Business Analyst", "short": "Business Analyst", "hue": "amber", "icon": "clipboard"},
}

for _slug, _c in COURSES.items():
    _c["slug"] = _slug
    _c.setdefault("featured", False)

FEATURED = [c for c in COURSES.values() if c["featured"]]

PROGRAM_CHOICES = sorted({c["name"] for c in COURSES.values()}) + ["Not sure yet, help me choose"]

# Track finder: each answer adds weight to one or more tracks.
QUIZ = [
    {
        "q": "What sounds most fun?",
        "options": [
            {"label": "Building apps people use", "emoji": "🛠️", "w": {"fullstack": 3, "othertech": 1}},
            {"label": "Teaching machines to think", "emoji": "🤖", "w": {"genai": 3, "data": 1}},
            {"label": "Making things look stunning", "emoji": "🎨", "w": {"design": 3, "media": 1}},
            {"label": "Growing brands online", "emoji": "📈", "w": {"marketing": 3, "media": 1}},
        ],
    },
    {
        "q": "Pick your superpower",
        "options": [
            {"label": "Logic & problem solving", "emoji": "🧩", "w": {"fullstack": 2, "data": 1}},
            {"label": "Numbers & patterns", "emoji": "📊", "w": {"data": 3, "nontech": 1}},
            {"label": "Visual taste", "emoji": "✨", "w": {"design": 2, "media": 2}},
            {"label": "Words & people", "emoji": "💬", "w": {"marketing": 2, "nontech": 2}},
        ],
    },
    {
        "q": "Where are you right now?",
        "options": [
            {"label": "School student", "emoji": "🎒", "w": {"genai": 1, "design": 1}},
            {"label": "In college", "emoji": "🎓", "w": {"fullstack": 1, "data": 1}},
            {"label": "Graduated, job hunting", "emoji": "🚀", "w": {"fullstack": 1, "genai": 1}},
            {"label": "Working, want to switch", "emoji": "🔁", "w": {"genai": 1, "data": 1}},
        ],
    },
]

TRACK_PICK = {
    "fullstack": "mern-fullstack",
    "genai": "generative-ai-foundations",
    "data": "ai-data-science",
    "design": "ui-ux-design",
    "media": "video-editing",
    "marketing": "digital-marketing",
    "othertech": "cloud-devops",
    "nontech": "business-analyst",
}

INTERNSHIP_PERKS = [
    {"icon": "briefcase", "k": "Work on", "v": "real client projects"},
    {"icon": "layers", "k": "Build your", "v": "project portfolio"},
    {"icon": "users", "k": "Learn", "v": "team collaboration"},
    {"icon": "award", "k": "Receive an", "v": "internship certificate"},
]

INTERNSHIP_FLOW = [
    ("Brief", "Get a real client requirement and a team."),
    ("Sprint", "Build in weekly sprints with mentor code reviews."),
    ("Demo", "Present to the client, just like at a real job."),
    ("Ship", "Deploy it live, add it to your portfolio and get certified."),
]

# EXAMPLE: project types, not specific client records. Replace with real
# intern projects (client, stack, live link) when available.
PROJECTS = [
    {"title": "Restaurant ordering PWA", "stack": ["React", "Node", "MongoDB"], "kind": "app", "hue": "violet", "tag": "Fullstack"},
    {"title": "AI support chatbot", "stack": ["Python", "LLM", "FastAPI"], "kind": "chat", "hue": "blue", "tag": "Gen AI"},
    {"title": "Sales analytics dashboard", "stack": ["SQL", "Python", "Power BI"], "kind": "chart", "hue": "cyan", "tag": "Data"},
    {"title": "Clinic booking app redesign", "stack": ["Figma", "Design system"], "kind": "design", "hue": "pink", "tag": "UI/UX"},
    {"title": "Brand reel campaign", "stack": ["Premiere", "After Effects"], "kind": "video", "hue": "rose", "tag": "Media"},
    {"title": "Inventory management system", "stack": ["Java", "Spring Boot", "React"], "kind": "app", "hue": "violet", "tag": "Fullstack"},
]

STORIES = [
    {
        "name": "Priya",
        "track": "Karka learner",
        "quote": "Karka's hands-on approach completely changed my career path. The mentors are incredibly supportive and the curriculum is up-to-date with industry standards.",
        "rating": 5,
    },
    {
        "name": "Karthik",
        "track": "SQL & Data Analytics",
        "quote": "The transition from non-tech to tech was smooth thanks to Karka. The SQL and Data Analytics bootcamp was comprehensive and practical.",
        "rating": 5,
    },
    {
        "name": "Sneha",
        "track": "Java & Spring Boot",
        "quote": "The depth of knowledge in the advanced Java and Spring Boot modules is impressive. It's not just about coding; they teach you how to think like a software engineer.",
        "rating": 4,
    },
    {
        "name": "Arun",
        "track": "ReactJS",
        "quote": "I loved the ReactJS training! The live projects were challenging but very rewarding. A huge shoutout to the placement team.",
        "rating": 5,
    },
    {
        "name": "Divya",
        "track": "Karka learner",
        "quote": "Amazing support system. Even after placement, the mentors are available to help. Truly grateful for Karka.",
        "rating": 5,
        "placed": True,
    },
    {
        "name": "Vikram",
        "track": "Karka learner",
        "quote": "Hands down the best decision I made for my career. The project-based learning really helped me build confidence.",
        "rating": 5,
    },
    {
        "name": "Anitha",
        "track": "Karka learner",
        "quote": "It's a fantastic place to learn. The environment is positive and motivates you to keep learning. The technicians are very knowledgeable.",
        "rating": 4,
    },
]

# Video testimonials (karka.academy "Voices of Our Learners"). Files live in
# static/video/<slug>.mp4 (540x960 H.264, faststart) with a <slug>.webp poster.
VIDEO_STORIES = [
    {
        "slug": "gabriel", "name": "Gabriel Samraj", "role": "Frontend Developer",
        "quote": "Karka's UI/UX design course was a game-changer for me. The instructors are passionate and the curriculum is up-to-date with the latest design trends. I now feel confident in my ability to create stunning visuals that stand out.",
    },
    {
        "slug": "prabin", "name": "Prabin Raj", "role": "Full Stack Developer",
        "quote": "I learned to build scalable applications from scratch. The environment at Karka is incredibly supportive and pushed me to be a better developer every day.",
    },
    {
        "slug": "shiju", "name": "Shiju Mon", "role": "Graphic Designer",
        "quote": "Karka's graphic design course was a game-changer for me. The instructors are passionate and the curriculum is up-to-date with the latest design trends. I now feel confident in my ability to create stunning visuals that stand out.",
    },
    {
        "slug": "kishore", "name": "Kishore", "role": "UI/UX Designer",
        "quote": "Karka's UI/UX design course was a game-changer for me. The instructors are passionate and the curriculum is up-to-date with the latest design trends. I now feel confident in my ability to create stunning visuals that stand out.",
    },
    {
        "slug": "sridevi", "name": "Sridevi", "role": "UI/UX Designer",
        "quote": "Karka's UI/UX design course was a game-changer for me. The instructors are passionate and the curriculum is up-to-date with the latest design trends. I now feel confident in my ability to create stunning visuals that stand out.",
    },
]

COMBOS = [
    "UI/UX Design with AI",
    "Digital Marketing with AI",
    "Graphic Design & Video Editing with AI",
    "Fullstack + Agentic AI",
    "Fullstack + Mobile App Dev",
    "Fullstack + Cloud/DevOps",
    "Fullstack + Cybersecurity",
]

INFINI = {
    "url": "https://infini.karka.academy/",
    "prize": "₹1,00,000",
    "contests": [
        ("PaperPulse", "Idea presentation", "file"),
        ("TechRush", "Technical quiz", "zap"),
        ("Bug Hunt", "Debugging", "bug"),
        ("SiteSprint", "Website building", "globe"),
        ("Graphix", "Poster design", "palette"),
        ("VibeCut", "Video creation", "video"),
    ],
}

SPIKE_FEATURES = [
    ("AI-guided", "Learn with AI at your side", "bot"),
    ("Hands-on", "Practise as you learn", "code"),
    ("Progress", "Track your growth", "trending"),
    ("Mentor-backed", "Paired with Karka mentors", "users"),
]

FAQS = [
    {
        "q": "What is Pay After Placement?",
        "a": "We want you to focus entirely on learning without worrying about upfront costs. You start with ₹0 upfront tuition and pay your course fees only after you land a tech job with a guaranteed minimum salary. It's our way of saying we're in this together.",
    },
    {
        "q": "Is placement guaranteed?",
        "a": "You get 100% placement support: resume and LinkedIn preparation, mock interviews, placement training and direct referrals to our hiring partners. Because of Pay After Placement, our incentives match yours. We only get paid when you get hired.",
    },
    {
        "q": "Who are the mentors at Karka?",
        "a": "Industry practitioners who mentor you face-to-face in our Nagercoil labs every day. They track your progress, review your code and designs, and unblock you in real time, so you never lose momentum.",
    },
    {
        "q": "Do I need a background in coding or CSE?",
        "a": "No. Many of our learners come from non-CSE and non-tech backgrounds. Tracks start from fundamentals, and the 4-pillar system also builds communication and interview skills.",
    },
    {
        "q": "How long does the course take?",
        "a": "Most career programs run 6 to 8 months. Gen AI Foundations is 3 months and UI/UX Design is 4 months. You can learn on-campus in Nagercoil or online.",
    },
    {
        "q": "Will I get internship or project experience?",
        "a": "Yes. Every student works on real-time internship projects for real clients, guided by mentors. You graduate with a deployable portfolio and an official internship certificate.",
    },
]
