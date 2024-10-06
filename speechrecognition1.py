import os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import cohere  # Import the Cohere library

# Initialize the Cohere API
cohere_client = cohere.Client('ZuDC2r6ZPbcv5gPno4vyDCVbLTq5on2RLJQ8ip0o')  # Replace with your Cohere API key

def speak_text(text):
    print(f"Converting to speech: {text}")  # Debugging line
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        filename = "response.mp3"
        tts.save(filename)
        print(f"Saved audio file: {filename}")  # Debugging line
        
        # Check if the file was created
        if os.path.exists(filename):
            print(f"File {filename} created successfully.")  # Debugging line
            
            # Play the audio file
            playsound(filename)

            os.remove(filename)  # Remove the file after playing it
            print("Speech output successful!")  # Debugging line
        else:
            print(f"File {filename} was not created.")  # Debugging line
    except Exception as e:
        print(f"Error in Text-to-Speech: {e}")  # Debugging line

def get_cohere_response(prompt):
    try:
        # Send recognized text to Cohere for text generation
        response = cohere_client.generate(
            model='command-xlarge-nightly',  # Specify the model
            prompt=prompt,
            max_tokens=150,  # Limit the token count for responses
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error during Cohere API call: {e}")
        return "Sorry, I could not generate a response."

def main():
    print("Speech-to-Speech LLM Bot is ready. Start speaking...")
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            recognized_text = recognizer.recognize_google(audio)
            print(f"Recognized: {recognized_text}")
            
            # Get the response from Cohere's model
            cohere_response = get_cohere_response(recognized_text)
            print(f"Cohere Response: {cohere_response}")

            # Convert the response to speech
            speak_text(cohere_response)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error during speech recognition or text generation: {e}")

if __name__ == "__main__":
    main()
