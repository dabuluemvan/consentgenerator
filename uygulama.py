import streamlit as st
from regex360 import analyzing_info
from generator360 import generate_consent

st.title("Consent Message Generator")

user_input = st.text_area("İsmini, bölümünü, ders kodunu, hocanı ve tonunu içeren bir metin yaz:")

if st.button("Generate Consent Message"):
    course_code, combined_major, student_name, instructor_name, consent_tone = analyzing_info(user_input)

    if not all([course_code, combined_major, student_name, instructor_name, consent_tone]):
        st.error("Bazı bilgiler eksik tespit edildi. Lütfen metni daha açık yaz.")
    else:
        final_message = generate_consent(
            course_code=course_code,
            combined_major=combined_major,
            student_name=student_name,
            instructor_name=instructor_name,
            consent_tone=consent_tone,
            start_context=("coursecontent", "]")
        )
        st.subheader("Generated Consent Message")
        st.write(final_message)
