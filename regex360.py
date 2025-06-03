import re

departments = {
    "Bilgisayar ve Öğretim Teknolojileri Eğitimi" : "Computer Education and Educational Technology",
    "Eğitim Bilimleri" : "Educational Sciences",
    "Temel Eğitim" : "Primary education",
    "Matematik ve Fen Bilimleri Eğitimi" : "Mathematics and Science Education",
    "Yabancı Diller Eğitimi" : "Foreign Language Education",
    "Batı Dilleri ve Edebiyatları" : "Western Languages and Literatures",
    "Çeviribilimi" : "Translation and Interpreting Studies",
    "Dilbilimi" : "Linguistics",
    "Felsefe" : "Philosophy",
    "Fizik" : "Physics",
    "Kimya" : "Chemistry",
    "Matematik" : "Mathematics",
    "Moleküler Biyoloji ve Genetik" : "Molecular Biology and Genetics",
    "Psikoloji" :"Psychology",
    "Sosyoloji" :"Sociology",
    "Tarih" : "History",
    "Türk Dili ve Edebiyatı" :"Turkish Language and Literature",
    "İktisat" : "Economics",
    "İşletme" : "Management",
    "Siyaset Bilimi ve Uluslararası İlişkiler" : "Political Science and International Relations",
    "Bilgisayar Mühendisliği" :"Computer Engineering",
    "Elektrik-Elektronik Mühendisliği" : "Electrical and Electronic Engineering",
    "Endüstri Mühendisliği" : "Industrial Engineering",
    "İnşaat Mühendisliği" : "Civil Engineering",
    "Kimya Mühendisliği" : "Chemical Engineering",
    "Makina Mühendisliği" : "Mechanical Engineering",
    "Turizm İşletmeciliği" : "Tourism Administration",
    "Uluslararası Ticaret" : "International Trade",
    "Yönetim Bilişim Sistemleri" : "Management Information Systems"
}

def translate_class(turkish_class):
    turkish_class = turkish_class.lower()
    mapping = {
        "1. sınıf": "1st year",
        "birinci sınıf": "1st year",
        "2. sınıf": "2nd year",
        "ikinci sınıf": "2nd year",
        "3. sınıf": "3rd year",
        "üçüncü sınıf": "3rd year",
        "4. sınıf": "4th year",
        "dördüncü sınıf": "4th year",
        "son sınıf": "final year"
    }
    return mapping.get(turkish_class, "")

def analyzing_info(user_input):

    course_code_match = re.findall(r'\b[A-Z]+\.?[0-9]+[A-Z]?\b', user_input)
    course_code = course_code_match[0] if course_code_match else ""

    student_class_match = re.findall(r'\b(\d\. sınıf|birinci sınıf|ikinci sınıf|üçüncü sınıf|dördüncü sınıf|son sınıf)\b', user_input.lower())
    student_class = student_class_match[0] if student_class_match else ""

    words = user_input.split()
    potential_majors = []
    for i in range(len(words)):
        for j in range(1, 6):
            phrase = ' '.join(words[i:i+j])
            if phrase in departments:
                potential_majors.append(phrase)
    major_turkish = potential_majors[0] if potential_majors else ""

    user_input_without_major = user_input.replace(major_turkish, '') if major_turkish else user_input
    names = re.findall(r'\b([A-ZÇÖİŞÜĞ][a-zığüşöç]+(?: [A-ZÇÖİŞÜĞ][a-zığüşöç]+)+)', user_input_without_major)
    student_name = names[0] if len(names) >= 1 else ""
    instructor_name = names[1] if len(names) >= 2 else ""

    tone_match = re.search(r'\b([a-zA-ZçöşüğıĞÜŞİÖÇ]+)\s+(tonda|şekilde|consent)\b', user_input.lower())
    consent_tone = tone_match.group(1) if tone_match else ""

    if consent_tone.lower() == "ingilizce":
        translated_class = translate_class(student_class)
        translated_major = departments.get(major_turkish, "")
        combined_major = f"{translated_class} {translated_major}".strip()
    else:
        combined_major = f"{student_class} {major_turkish}".strip()

    return course_code, combined_major, student_name, instructor_name, consent_tone

