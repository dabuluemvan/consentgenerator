import re

departments = {
    "Bilgisayar ve Öðretim Teknolojileri Eðitimi" : "Computer Education and Educational Technology",
    "Eðitim Bilimleri" : "Educational Sciences",
    "Temel Eðitim" : "Primary education",
    "Matematik ve Fen Bilimleri Eðitimi" : "Mathematics and Science Education",
    "Yabancý Diller Eðitimi" : "Foreign Language Education",
    "Batý Dilleri ve Edebiyatlarý" : "Western Languages and Literatures",
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
    "Türk Dili ve Edebiyatý" :"Turkish Language and Literature",
    "Ýktisat" : "Economics",
    "Ýþletme" : "Management",
    "Siyaset Bilimi ve Uluslararasý Ýliþkiler" : "Political Science and International Relations",
    "Bilgisayar Mühendisliði" :"Computer Engineering",
    "Elektrik-Elektronik Mühendisliði" : "Electrical and Electronic Engineering",
    "Endüstri Mühendisliði" : "Industrial Engineering",
    "Ýnþaat Mühendisliði" : "Civil Engineering",
    "Kimya Mühendisliði" : "Chemical Engineering",
    "Makina Mühendisliði" : "Mechanical Engineering",
    "Turizm Ýþletmeciliði" : "Tourism Administration",
    "Uluslararasý Ticaret" : "International Trade",
    "Yönetim Biliþim Sistemleri" : "Management Information Systems"
}

def translate_class(turkish_class):
    turkish_class = turkish_class.lower()
    mapping = {
        "1. sýnýf": "1st year",
        "birinci sýnýf": "1st year",
        "2. sýnýf": "2nd year",
        "ikinci sýnýf": "2nd year",
        "3. sýnýf": "3rd year",
        "üçüncü sýnýf": "3rd year",
        "4. sýnýf": "4th year",
        "dördüncü sýnýf": "4th year",
        "son sýnýf": "final year"
    }
    return mapping.get(turkish_class, "")

def analyzing_info(user_input):

    course_code_match = re.findall(r'\b[A-Z]+\.?[0-9]+[A-Z]?\b', user_input)
    course_code = course_code_match[0] if course_code_match else ""

    student_class_match = re.findall(r'\b(\d\. sýnýf|birinci sýnýf|ikinci sýnýf|üçüncü sýnýf|dördüncü sýnýf|son sýnýf)\b', user_input.lower())
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
    names = re.findall(r'\b([A-ZÇÖÝÞÜÐ][a-zýðüþöç]+(?: [A-ZÇÖÝÞÜÐ][a-zýðüþöç]+)+)', user_input_without_major)
    student_name = names[0] if len(names) >= 1 else ""
    instructor_name = names[1] if len(names) >= 2 else ""

    tone_match = re.search(r'\b([a-zA-ZçöþüðýÐÜÞÝÖÇ]+)\s+(tonda|þekilde|consent)\b', user_input.lower())
    consent_tone = tone_match.group(1) if tone_match else ""

    if consent_tone.lower() == "ingilizce":
        translated_class = translate_class(student_class)
        translated_major = departments.get(major_turkish, "")
        combined_major = f"{translated_class} {translated_major}".strip()
    else:
        combined_major = f"{student_class} {major_turkish}".strip()

    return course_code, combined_major, student_name, instructor_name, consent_tone
