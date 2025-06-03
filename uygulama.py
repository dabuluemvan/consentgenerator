import streamlit as st
from regex360 import analyzing_info
from gerisi360 import generate_consent
st.title="Consent Message Generator"
user_input=input("O istediğin dersi almak üzeresin ama önce consentini oluşturmak için birkaç bilgiye ihtiyacımız var: \nLütfen ismini, bölümünü, almak istediğin dersi ve hocasını belirt. Ardından consentinin tonunu veya dilini seç. (yalvaran, ilgili, övgülü ya da ingilizce) Gerisi bizde! \n")
if st.button("Generate Consent Message"):
    course_code, combined_major, student_name, instructor_name, consent_tone = analyzing_info(user_input)
    if not all([course_code, combined_major, student_name, instructor_name, consent_tone]):
        st.error("Bazı bilgiler eksik tespit edildi. Lütfen metni daha açık yaz.")
    else:
        final_message = generate_consent(
            trigram_probs=None,
            start_context=("coursecontent", "]")
        )
        st.subheader("Generated Consent Message")
        st.write(final_message)
