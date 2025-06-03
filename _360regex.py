import re

departments = {
    "Bilgisayar ve ��retim Teknolojileri E�itimi" : "Computer Education and Educational Technology",
    "E�itim Bilimleri" : "Educational Sciences",
    "Temel E�itim" : "Primary education",
    "Matematik ve Fen Bilimleri E�itimi" : "Mathematics and Science Education",
    "Yabanc� Diller E�itimi" : "Foreign Language Education",
    "Bat� Dilleri ve Edebiyatlar�" : "Western Languages and Literatures",
    "�eviribilimi" : "Translation and Interpreting Studies",
    "Dilbilimi" : "Linguistics",
    "Felsefe" : "Philosophy",
    "Fizik" : "Physics",
    "Kimya" : "Chemistry",
    "Matematik" : "Mathematics",
    "Molek�ler Biyoloji ve Genetik" : "Molecular Biology and Genetics",
    "Psikoloji" :"Psychology",
    "Sosyoloji" :"Sociology",
    "Tarih" : "History",
    "T�rk Dili ve Edebiyat�" :"Turkish Language and Literature",
    "�ktisat" : "Economics",
    "��letme" : "Management",
    "Siyaset Bilimi ve Uluslararas� �li�kiler" : "Political Science and International Relations",
    "Bilgisayar M�hendisli�i" :"Computer Engineering",
    "Elektrik-Elektronik M�hendisli�i" : "Electrical and Electronic Engineering",
    "End�stri M�hendisli�i" : "Industrial Engineering",
    "�n�aat M�hendisli�i" : "Civil Engineering",
    "Kimya M�hendisli�i" : "Chemical Engineering",
    "Makina M�hendisli�i" : "Mechanical Engineering",
    "Turizm ��letmecili�i" : "Tourism Administration",
    "Uluslararas� Ticaret" : "International Trade",
    "Y�netim Bili�im Sistemleri" : "Management Information Systems"
}

def translate_class(turkish_class):
    turkish_class = turkish_class.lower()
    mapping = {
        "1. s�n�f": "1st year",
        "birinci s�n�f": "1st year",
        "2. s�n�f": "2nd year",
        "ikinci s�n�f": "2nd year",
        "3. s�n�f": "3rd year",
        "���nc� s�n�f": "3rd year",
        "4. s�n�f": "4th year",
        "d�rd�nc� s�n�f": "4th year",
        "son s�n�f": "final year"
    }
    return mapping.get(turkish_class, "")

def analyzing_info(user_input):

    course_code_match = re.findall(r'\b[A-Z]+\.?[0-9]+[A-Z]?\b', user_input)
    course_code = course_code_match[0] if course_code_match else ""

    student_class_match = re.findall(r'\b(\d\. s�n�f|birinci s�n�f|ikinci s�n�f|���nc� s�n�f|d�rd�nc� s�n�f|son s�n�f)\b', user_input.lower())
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
    names = re.findall(r'\b([A-Z������][a-z������]+(?: [A-Z������][a-z������]+)+)', user_input_without_major)
    student_name = names[0] if len(names) >= 1 else ""
    instructor_name = names[1] if len(names) >= 2 else ""

    tone_match = re.search(r'\b([a-zA-Z������������]+)\s+(tonda|�ekilde|consent)\b', user_input.lower())
    consent_tone = tone_match.group(1) if tone_match else ""

    if consent_tone.lower() == "ingilizce":
        translated_class = translate_class(student_class)
        translated_major = departments.get(major_turkish, "")
        combined_major = f"{translated_class} {translated_major}".strip()
    else:
        combined_major = f"{student_class} {major_turkish}".strip()

    return course_code, combined_major, student_name, instructor_name, consent_tone

looking_for = ["Lesson Code", "Major", "Student Name", "Instructor Name", "Consent Tone"]

while True:
    user_input = input("O istedi�in dersi almak �zeresin ama �nce consentini olu�turmak i�in birka� bilgiye ihtiyac�m�z var: \nL�tfen ismini, b�l�m�n�, almak istedi�in dersi ve hocas�n� belirt. Ard�ndan consentinin tonunu veya dilini se�. (yalvaran, ilgili, �vg�l� ya da ingilizce)�Gerisi�bizde! \n")
    course_code, combined_major, student_name, instructor_name, consent_tone = analyzing_info(user_input)

    values = [course_code, combined_major, student_name, instructor_name, consent_tone]

    missing = [looking_for[i] for i, v in enumerate(values) if not v]

    if missing:
        print("Eksik bilgiler: ", ', '.join(missing))
        print("L�tfen eksik bilgileri de kullanarak yeni bir prompt giriniz.")
        continue

    print("Course Code:", course_code)
    print("Combined Major:", combined_major)
    print("Student Name:", student_name)
    print("Instructor Name:", instructor_name)
    print("Consent Tone:", consent_tone)
    break

