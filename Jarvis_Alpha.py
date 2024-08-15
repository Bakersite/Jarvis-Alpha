import speech_recognition as sr
from hugchat import hugchat
from hugchat.login import Login
from gtts import gTTS
from pydub import AudioSegment

# speaking
def speak(text):
	tts = gTTS(text=text, lang='en')
	tts.save("response.mp3")

	# 轉換為 16 位 PCM 格式的 WAV 文件
	audio = AudioSegment.from_mp3("response.mp3")
	audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
	audio.export("response.wav", format='wav')


# initialize the recognizer
r = sr.Recognizer()

# log in
email = ""
passwd = ""
sign = Login(email, passwd)
cookies = sign.login()

# activate bot
jarvis = hugchat.ChatBot(cookies=cookies.get_dict())

# generate response
while(True):
	try:
		# use the microphone as the source for input
		with sr.Microphone() as source:
			print("Adjusting for ambient noise, please wait...")
			r.adjust_for_ambient_noise(source)
			print("Say something!")
			audio = r.listen(source)
		
		try:
			message = r.recognize_google(audio)
			print("ME: ", r.recognize_google(audio))
		except sr.UnknownValueError:
			print("Google Web Speech could not understand the audio")
		except sr.Request as e:
			print("Could not request results form Google Web service")
		
		# generate the response
		response = jarvis.chat(message)
		speak(str(response))
		print("Jarvis: ", response)
	except KeyboardInterrupt:
		print("Exiting...")
		break
