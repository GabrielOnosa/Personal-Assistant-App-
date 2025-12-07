import speech_recognition as sr

def transcribe_from_microphone(timeout = 5, phrase_time_limit = 15):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout= timeout, phrase_time_limit= phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""
        
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""
    
if __name__ == "__main__":
    text = transcribe_from_microphone()
    print("Transcribed Text:", text)