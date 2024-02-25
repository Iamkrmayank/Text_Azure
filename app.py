import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import io
import wave

# Function to synthesize speech and save audio
def synthesize_and_save_audio(text, file_path):
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data

        with wave.open(file_path, 'wb') as wave_file:
            wave_file.setnchannels(1)  # Mono audio
            wave_file.setsampwidth(2)   # 16-bit audio
            wave_file.setframerate(16000)  # Sample rate, you can adjust this based on the speech synthesis settings
            wave_file.writeframes(audio_data)

        st.success("Audio saved to: {}".format(file_path))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        st.error("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            st.error("Error details: {}".format(cancellation_details.error_details))

# Streamlit app
st.title("Speech Synthesis with Azure Cognitive Services")

# Input text
text_input = st.text_area("Enter text for speech synthesis:")

# Button to generate and play audio
if st.button("Generate and Play Audio"):
    if text_input:
        # Save audio to a temporary in-memory file
        temp_file = io.BytesIO()
        synthesize_and_save_audio(text_input, temp_file)
        
        # Play the generated audio
        st.audio(temp_file.getvalue(), format="audio/wav")

# Explanation
st.markdown("""
### Instructions:
1. Enter the text you want to synthesize in the text area.
2. Click the "Generate and Play Audio" button to generate and play the audio.
""")
