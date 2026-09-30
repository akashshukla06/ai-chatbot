import pandas as pd


data = [

    {
        "question": "What is the full name of the college?",
        "answer": "The full name is ABES Engineering College, located in Ghaziabad, Uttar Pradesh.",
        "category": "General",
        "source": "ABES Official Website",
        "source_url": "https://www.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Where is ABES Engineering College located?",
        "answer": "ABES Engineering College is located at 19th KM Stone, NH-09, Ghaziabad, Uttar Pradesh, PIN 201009.",
        "category": "Contact",
        "source": "ABES Official Website",
        "source_url": "https://www.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "What is the phone number of ABES Engineering College?",
        "answer": "The official ABES website lists the college phone number as 01207135112.",
        "category": "Contact",
        "source": "ABES Official Website",
        "source_url": "https://www.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "What is the email address of ABES Engineering College?",
        "answer": "The official ABES website lists info@abes.ac.in as the college email address.",
        "category": "Contact",
        "source": "ABES Official Website",
        "source_url": "https://www.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "When was ABES Engineering College established?",
        "answer": "ABES was established in 2000.",
        "category": "General",
        "source": "ABES Official Admissions Website",
        "source_url": "https://admission.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Is ABES an autonomous college?",
        "answer": "The ABES official admissions website states that ABES is an autonomous college since 2025.",
        "category": "General",
        "source": "ABES Official Admissions Website",
        "source_url": "https://admission.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "What B.Tech courses are offered at ABES?",
        "answer": "ABES lists B.Tech programmes in Computer Science and Engineering, Computer Science and Engineering (Artificial Intelligence and Machine Learning), Computer Science and Engineering (Data Science), Electronics and Communication Engineering, Electrical and Computer Engineering, Mechanical Engineering, and working-professional programmes in CSE and ECE.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer Computer Science and Engineering?",
        "answer": "Yes. ABES lists Computer Science and Engineering as a B.Tech programme with an approved intake of 900 seats.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer CSE Artificial Intelligence and Machine Learning?",
        "answer": "Yes. ABES lists Computer Science and Engineering (Artificial Intelligence and Machine Learning) as a B.Tech programme with an approved intake of 360 seats.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer CSE Data Science?",
        "answer": "Yes. ABES lists Computer Science and Engineering (Data Science) as a B.Tech programme with an approved intake of 180 seats.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer Electronics and Communication Engineering?",
        "answer": "Yes. ABES lists Electronics and Communication Engineering as a B.Tech programme with an approved intake of 180 seats.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer Electrical and Computer Engineering?",
        "answer": "Yes. ABES lists Electrical and Computer Engineering as a B.Tech programme with an approved intake of 120 seats.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer Mechanical Engineering?",
        "answer": "Yes. ABES lists Mechanical Engineering as a B.Tech programme with an approved intake of 60 seats.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer MCA?",
        "answer": "Yes. ABES lists MCA with an approved intake of 180 seats.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer BCA?",
        "answer": "Yes. ABES lists BCA with an approved intake of 120 seats.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES offer M.Tech?",
        "answer": "Yes. ABES lists M.Tech in Computer Science and Engineering with an intake of 12 and M.Tech in Electronics and Communication Engineering with an intake of 6.",
        "category": "Academics",
        "source": "ABES Official Courses Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Where can I find the ABES academic calendar?",
        "answer": "ABES publishes academic calendars on its official Academic Calendar page. The page currently lists the 2026-27 Odd Semester calendar along with calendars from previous sessions.",
        "category": "Academic Calendar",
        "source": "ABES Official Academic Calendar",
        "source_url": "https://www.abes.ac.in/Academic-Calender.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Where can I find ABES notices and circulars?",
        "answer": "ABES publishes official circulars and notices on its Circulars/Notices page.",
        "category": "Notices",
        "source": "ABES Official Circulars",
        "source_url": "https://www.abes.ac.in/circulars.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Where can I find scholarship notifications at ABES?",
        "answer": "Scholarship-related notifications are published in the ABES official Circulars/Notices section. Current notices include Central Government and UP Government scholarship notifications.",
        "category": "Scholarship",
        "source": "ABES Official Circulars",
        "source_url": "https://www.abes.ac.in/circulars.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "What is ABC ID?",
        "answer": "ABES has published a notification regarding the creation of Academic Bank of Credits (ABC) IDs for newly admitted students and students from the previous session.",
        "category": "Student Services",
        "source": "ABES Official Circulars",
        "source_url": "https://www.abes.ac.in/circulars.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Does ABES have hostel facilities?",
        "answer": "Yes. ABES provides hostel accommodation for students and publishes hostel fee structures and accommodation terms.",
        "category": "Hostel",
        "source": "ABES Official Courses and Admissions Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "How is hostel room allotment done at ABES?",
        "answer": "ABES states that hostel room allotment is made on a first-come, first-served basis.",
        "category": "Hostel",
        "source": "ABES Official Courses and Admissions Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "What is the hostel security at ABES for 2026-27?",
        "answer": "For the 2026-27 session, ABES lists hostel security of ₹5,000. It is refundable and applicable one time while opting for hostel.",
        "category": "Hostel Fees",
        "source": "ABES Official Courses and Admissions Page",
        "source_url": "https://www.abes.ac.in/courses-offered.html",
        "last_verified": "2026-09-30"
    },

    {
        "question": "What is the highest placement package at ABES?",
        "answer": "The ABES official admissions website currently states a highest placement package of 60 LPA for placements 2025.",
        "category": "Placement",
        "source": "ABES Official Admissions Website",
        "source_url": "https://admission.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "How many placement offers did ABES have in 2025?",
        "answer": "The ABES official admissions website currently states 1692 placement offers for 2025.",
        "category": "Placement",
        "source": "ABES Official Admissions Website",
        "source_url": "https://admission.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "Where can I find ABES student forms?",
        "answer": "ABES provides student forms including Bonafide Certificate, No Dues, Duplicate Identity Card, Branch Change, Hostel Admission, Degree and Marksheet collection, Transfer Certificate, Character Certificate and other student applications.",
        "category": "Student Services",
        "source": "ABES Official Forms Page",
        "source_url": "https://www.abes.ac.in/footer-form.php",
        "last_verified": "2026-09-30"
    },

    {
        "question": "What is the ABES official address?",
        "answer": "19th KM Stone, NH-09, Ghaziabad, Uttar Pradesh, PIN 201009.",
        "category": "Contact",
        "source": "ABES Official Website",
        "source_url": "https://www.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "What is the latest ABES academic session?",
        "answer": "The current ABES admissions information is for the 2026-27 session.",
        "category": "Academic Session",
        "source": "ABES Official Admissions Website",
        "source_url": "https://admission.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

    {
        "question": "When does the ABES 2026-27 session commence?",
        "answer": "The ABES official admissions website currently states that class commencement for session 2026-27 is from 31 August 2026.",
        "category": "Academic Calendar",
        "source": "ABES Official Admissions Website",
        "source_url": "https://admission.abes.ac.in/",
        "last_verified": "2026-09-30"
    },

]


# Create DataFrame
df = pd.DataFrame(data)


# Save file
output_file = "dataset/processed/abes_knowledge.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)


print("ABES dataset created successfully!")
print("Total records:", len(df))
print("Saved to:", output_file)

print("\nColumns:")
print(df.columns.tolist())