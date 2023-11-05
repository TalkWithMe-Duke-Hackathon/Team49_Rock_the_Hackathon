import requests
import base64
import azure.cognitiveservices.speech as speechsdk
import os
import csv
from flask import Flask, jsonify, render_template, request, make_response

app = Flask(__name__)

subscription_key = '0e7b29909ab741cfa1f9b05bfe012e71'
region = "eastus"
language = "en-US"
voice = "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)"

i = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gettoken", methods=["POST"])
def gettoken():
    fetch_token_url = 'https://%s.api.cognitive.microsoft.com/sts/v1.0/issueToken' %region
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = response.text
    return jsonify({"at":access_token})

@app.route("/ackaud", methods=["POST"])
def ackaud():
    global i
    f = request.files['audio_data']
    reftext = request.form.get("reftext")

    # a generator which reads audio data chunk by chunk
    def get_chunk(audio_source, chunk_size=1024):
        while True:
            chunk = audio_source.read(chunk_size)
            if not chunk:
                break
            yield chunk

    # build pronunciation assessment parameters
    referenceText = reftext
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\",\"EnableMiscue\":\"True\"}" % referenceText
    pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

    # build request
    url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=%s&usePipelineVersion=0" % (region, language)
    headers = { 'Accept': 'application/json;text/xml',
                'Connection': 'Keep-Alive',
                'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
                'Ocp-Apim-Subscription-Key': subscription_key,
                'Pronunciation-Assessment': pronAssessmentParams,
                'Transfer-Encoding': 'chunked',
                'Expect': '100-continue' }

    audioFile = f
    # send request with chunked data
    response = requests.post(url=url, data=get_chunk(audioFile), headers=headers)
    #getResponseTime = time.time()
    audioFile.close()

    # Parse the JSON data
    data_dict = response.json()

    # Check if "NBest" exists in the JSON response
    if "NBest" in data_dict:
        # Extract the values
        accuracy_score = data_dict["NBest"][0]["AccuracyScore"]
        fluency_score = data_dict["NBest"][0]["FluencyScore"]
        completeness_score = data_dict["NBest"][0]["CompletenessScore"]
        pron_score = data_dict["NBest"][0]["PronScore"]

        # Read the CSV file to find the last index
        last_index = None
        if os.path.exists('scores.csv'):
            with open('scores.csv', 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    last_index = int(row['Index'])

        # If the file is empty, initialize last_index to -1
        if last_index is None:
            last_index = -1

        # Increment the index for the next row
        i = last_index + 1

        # Write the new data to the CSV file
        with open('scores.csv', 'a', newline='') as csvfile:
            # print("I am HERE")
            fieldnames = ['Index', 'AccuracyScore', 'FluencyScore', 'CompletenessScore', 'PronScore']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Check if the file is empty and write the header if needed
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({'Index': i, 'AccuracyScore': accuracy_score, 'FluencyScore': fluency_score, 'CompletenessScore': completeness_score, 'PronScore': pron_score})

    else:
        print("The 'NBest' field does not exist in the JSON response.")

    return response.json()

@app.route("/gettts", methods=["POST"])
def gettts():
    reftext = request.form.get("reftext")
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice

    offsets=[]

    def wordbound(evt):
        offsets.append( evt.audio_offset / 10000)

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Subscribes to word boundary event
    # The unit of evt.audio_offset is tick (1 tick = 100 nanoseconds), divide it by 10,000 to convert to milliseconds.
    speech_synthesizer.synthesis_word_boundary.connect(wordbound)

    result = speech_synthesizer.speak_text_async(reftext).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        
        response = make_response(audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
        # response.headers['reftext'] = reftext
        response.headers['offsets'] = offsets
        return response
        
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return jsonify({"success":False})


@app.route("/getttsforword", methods=["POST"])
def getttsforword():
    word = request.form.get("word")

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_text_async(word).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        response = make_response(audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
        # response.headers['word'] = word
        return response
        
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return jsonify({"success":False})

if __name__ == "__main__":
        app.run(debug=True, port=int(os.environ.get("PORT", 8080)))
else:
        gunicorn_app = app