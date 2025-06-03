import nltk
import random
import numpy as np
import re

def generate_consent(course_code, combined_major, student_name, instructor_name, consent_tone, start_context=("]", ","), max_length=300):
    if consent_tone == "interested" or consent_tone == "ilgili":
        with open('interested_tr.txt', 'r', encoding='utf-8') as f:
            tone_raw = f.read()
    elif consent_tone == "praise" or consent_tone == "övgülü":
        with open('praise_tr.txt', 'r', encoding='utf-8') as f:
            tone_raw = f.read()
    elif consent_tone == "begging" or consent_tone == "yalvaran":
        with open('begging_tr.txt', 'r', encoding='utf-8') as f:
            tone_raw = f.read()
    elif consent_tone == "english" or consent_tone == "ingilizce":
        with open('tone_eng.txt', 'r', encoding='utf-8') as f:
            tone_raw = f.read()
    nltk.download('punkt_tab')
    tone_sents = nltk.sent_tokenize(tone_raw)
    tone_sents_tokenized = [nltk.word_tokenize(s) for s in tone_sents]

    tone_corpus = []
    for sentence in tone_sents_tokenized:
        tone_corpus += ["<s>"] + sentence + ["</s>"]
    tone_corpus = [i.lower() for i in tone_corpus]

    tone_trigrams = [(tone_corpus[i], tone_corpus[i+1], tone_corpus[i+2]) for i in range(len(tone_corpus)-2)]
    trigram_freqs = nltk.FreqDist(tone_trigrams)
    trigram_cfd = nltk.ConditionalFreqDist(((w1, w2), w3) for (w1, w2, w3) in tone_trigrams)
    trigram_probs = nltk.ConditionalProbDist(trigram_cfd, nltk.MLEProbDist)

    context = start_context
    current_words = list(context)
    generated_words = []
    counter = 0
    dative = ["ilgiliyim", "ilgi", "gerçekten"]
    accusative = ["sizden"]

    for i in range(max_length):
        context = tuple(current_words[-2:])
        if context not in trigram_probs:
            break
        probable_words = list(trigram_probs[context].samples())
        word_probabilities = [trigram_probs[context].prob(word) for word in probable_words]
        word_probabilities = np.array(word_probabilities)
        word_probabilities = word_probabilities / word_probabilities.sum()
        next_word = np.random.choice(probable_words, p=word_probabilities)
        if counter < 3:
            if next_word == "</s>":
                counter += 1
        else:
            break
        current_words.append(next_word)
        generated_words.append(next_word)

    if consent_tone == "english" or consent_tone == "ingilizce":
        for i in range(len(generated_words)-2):
            if generated_words[i] == "[" and generated_words[i+1] == "coursecontent" and generated_words[i+2] == "]":
                generated_words[i] = "the"
                generated_words[i+1] = "course"
                generated_words[i+2] = "content"
    else:
        for i in range(len(generated_words)-2):
            if generated_words[i] == "[" and generated_words[i+1] == "coursecontent" and generated_words[i+2] == "]":
                generated_words[i] = "bu"
                generated_words[i+1] = "dersin"
                generated_words[i+2] = "konusu"

    i = 0
    while i < len(generated_words) - 1:
        if generated_words[i] == "konusu" and generated_words[i + 1] in ["konusuna", "konusunda"]:
            del generated_words[i]
            continue
        i += 1

    for i in range(len(generated_words)-1):
        if generated_words[i] == "konusu" and generated_words[i+1] in dative:
            generated_words[i] = "konusuna"
        if generated_words[i] == "konusu" and generated_words[i+1] in accusative:
            generated_words[i] = "konusunu"
    final_message=" ".join(generated_words)
    final_message=re.sub("\[ greetings \]","",final_message)
    final_message=re.sub("\[ regards \]","",final_message)
    final_message=re.sub("\[Instructor Name\]","",final_message)
    final_message=re.sub("\[InstructorName\]","",final_message)
    final_message=re.sub("\[instructor name\]","",final_message)
    final_message=re.sub("\[ instructorname \]","",final_message)
    all_chars_before=list(final_message)
    all_chars_before[0]=all_chars_before[0].upper()
    final_message="".join(all_chars_before)
    final_message=f"[Greetings],\n {final_message} \n [Regards]"
    if consent_tone=="english" or consent_tone=="ingilizce":
      with open("eng_greetings.txt", "r", encoding="utf-8") as f:
        greetings = f.read().splitlines()
      with open("eng_regards.txt", "r", encoding="utf-8") as f:
        regards = f.read().splitlines()
    else:
      with open("tr_greetings.txt", "r", encoding="utf-8") as f:
        greetings = f.read().splitlines()
      with open("tr_regards.txt", "r", encoding="utf-8") as f:
        regards = f.read().splitlines()
    greeting_final=random.choice(greetings)
    regard_final=random.choice(regards)
    final_message=re.sub("\[Greetings\]",greeting_final,final_message)
    final_message=re.sub("\[Regards\]",regard_final,final_message)
    final_message=re.sub("<s>","",final_message)
    final_message=re.sub("\[Instructor Name\]",instructor_name,final_message)
    final_message=re.sub("\[InstructorName\]",instructor_name,final_message)
    final_message=re.sub("\[instructor name\]",instructor_name,final_message)
    final_message=re.sub("\[ instructorname \]",instructor_name,final_message)
    final_message=re.sub("\[ currentcoursecode \]",course_code,final_message)
    final_message=re.sub("\[ currenycoursecode \]",course_code,final_message)
    final_message=re.sub("\[ major \]",combined_major,final_message)
    final_message=re.sub("\[ studentname \]",student_name,final_message)
    final_message=re.sub("</s>","",final_message)
    final_message=re.sub(r"[ ]+,","",final_message)
    final_message=re.sub(r"[ ]{2,}","",final_message)
    final_message=re.sub(r" +"," ",final_message)
    final_message=re.sub(r" +\.",". ",final_message)
    final_message=re.sub(r" +"," ",final_message)
    final_message=re.sub(" ’ ","’",final_message)
    all_chars=list(final_message)
    for i in range(len(all_chars)-2):
      if all_chars[i]==".":
        all_chars[i+2]=all_chars[i+2].upper()
    all_chars[0]=all_chars[0].upper()
    final_message="".join(all_chars)
    return final_message
