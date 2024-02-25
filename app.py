import os
import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import io
import wave
from pydub import AudioSegment

# Load API keys from environment variables
speech_key = os.getenv("8ada5b541bcb4f5ebbcb0d80eb332903")
service_region = os.getenv("eastus")

# Check if API keys are set
if not speech_key or not service_region:
    st.error("Please set your Azure Cognitive Services API keys in the environment variables.")
    st.stop()

# Creates an instance of a speech config with specified subscription key and service region.
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name = "en-IN-PrabhatNeural"

# Function to synthesize speech and save audio as MP3
def synthesize_and_save_audio(text, file_path):
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data

        # Convert WAV audio data to MP3
        audio_segment = AudioSegment(
            audio_data.tobytes(),
            frame_rate=16000,
            sample_width=2,
            channels=1
        )

        # Save audio as MP3
        audio_segment.export(file_path, format="mp3")

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
        st.audio(temp_file.getvalue(), format="audio/mp3")

# Explanation
st.markdown("""
### Instructions:
1. Enter the text you want to synthesize in the text area.
2. Click the "Generate and Play Audio" button to generate and play the audio.
""")
