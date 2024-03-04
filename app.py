import os
import azure.cognitiveservices.speech as speechsdk
import streamlit as st

# Retrieve Azure Speech key and region from environment variables
azure_speech_key = os.environ.get("AZURE_SPEECH_KEY")
azure_service_region = os.environ.get("AZURE_SERVICE_REGION")

if not azure_speech_key or not azure_service_region:
    st.error("Please set the AZURE_SPEECH_KEY and AZURE_SERVICE_REGION environment variables.")
    st.stop()

# Speech configuration
speech_config = speechsdk.SpeechConfig(subscription=azure_speech_key, region=azure_service_region)
speech_config.speech_synthesis_voice_name = "en-IN-PrabhatNeural"

# Text to be synthesized
text = "Hi, this is Prabhat"

# Speech synthesizer
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Synthesize speech
result = speech_synthesizer.speak_text_async(text).get()

# Display the result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    st.success("Speech synthesized successfully!")
    
    # Get the audio data
    audio_data = result.audio_data

    # Save the audio data to a WAV file (optional)
    file_path = "synthesized_speech.wav"
    with open(file_path, "wb") as file:
        file.write(audio_data)

    st.audio(audio_data, format="audio/wav")
    st.info("Synthesized speech saved to: {}".format(file_path))

elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    st.error("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        st.error("Error details: {}".format(cancellation_details.error_details))
