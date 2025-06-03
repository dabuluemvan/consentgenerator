import streamlit as st
from regex360 import analyzing_info
from gerisi360 import generate_consent

st.title("Consent Message Generator")

user_input = st.text_area("O istediğin dersi almak üzeresin ama önce consentini oluşturmak için birkaç bilgiye ihtiyacımız var: \nLütfen ismini, bölümünü, almak istediğin dersi ve hocasını belirt. Ardından consentinin tonunu veya dilini seç. (yalvaran, ilgili, övgülü ya da ingilizce) Gerisi bizde! \n")

if st.button("Generate Consent Message"):
    course_code, combined_major, student_name, instructor_name, consent_tone = analyzing_info(user_input)

    st.write(f"**Course Code:** {course_code}")
    st.write(f"**Major:** {combined_major}")
    st.write(f"**Student Name:** {student_name}")
    st.write(f"**Instructor Name:** {instructor_name}")
    st.write(f"**Consent Tone:** {consent_tone}")

    missing_fields = []
    if not course_code:
        missing_fields.append("Course Code")
    if not combined_major:
        missing_fields.append("Major")
    if not student_name:
        missing_fields.append("Student Name")
    if not instructor_name:
        missing_fields.append("Instructor Name")
    if not consent_tone:
        missing_fields.append("Consent Tone")

    if missing_fields:
        st.error(f"Eksik bilgiler tespit edildi: {', '.join(missing_fields)}. Lütfen metni daha açık yaz.")
    else:
        final_message = generate_consent(
            course_code=course_code,
            combined_major=combined_major,
            student_name=student_name,
            instructor_name=instructor_name,
            consent_tone=consent_tone,
            start_context=("]", ",")
        )
        st.subheader("Generated Consent Message")
        st.write(final_message)
