#made with default Notepad Windows 10 for fun

#import connection_checker
#connection_checker.check(url = "https://www.amazon.com", frequency = [240,300])

import telebot, ffmpeg, time, os, requests
from pytube import YouTube
from telebot import types

def streams(ink, only_audio=False): #ink : link of the video
		global video
		if only_audio == True:
			comp2 = {}

			youtube = YouTube(ink)
			video = youtube.streams.filter(only_audio=True)
			for i in list(enumerate(video)):
				#print(dir(i[1]))
				valu_e = int(i[1].filesize)/1024/1024
				if valu_e > 1000 :
					valu_e = str(round(valu_e/1024, 2))+ " GB"
				else:
					valu_e = str(round(valu_e, 1))+ " MB"
				#print(valu_e)
				ext = i[1].subtype
				itag = i[1].itag
				
				if (ext == "webm") or (ext == "mp4"):
					bits = int(i[1].bitrate)
					if ext in comp2:
						if bits > comp2[ext][1]:
							comp2[ext] = [itag, bits, i[1].audio_codec, valu_e]
					else:
						comp2[ext] = [itag, bits, i[1].audio_codec, valu_e]
			return comp2

		if only_audio == False:
			comp = [[],{}]
			comp2 = {}

			youtube = YouTube(ink)
			video = youtube.streams
			for i in list(enumerate(video)):
				#print(dir(i[1]))
				valu_e = int(i[1].filesize)/1024/1024
				if valu_e > 1000 :
					valu_e = str(round(valu_e/1024, 2))+ " GB"
				else:
					valu_e = str(round(valu_e, 1))+ " MB"
				#print(valu_e)
				ext = i[1].subtype
				itag = i[1].itag
				if i[1].type == "video" and (ext == "webm" or ext == "mp4"):
					pixel = int(i[1].resolution[:-1])
		
					comp[0].append(pixel)
				
					if pixel in comp[1]:
						if (i[1].is_progressive == True) and (ext == "mp4"):
							comp[1][pixel] = [itag, i[1].resolution, ext, i[1].is_progressive, i[1].video_codec, valu_e]
					else:
						comp[1][pixel] = [itag, i[1].resolution, ext, i[1].is_progressive, i[1].video_codec, valu_e]
				if i[1].type == "audio" and (ext == "webm" or ext == "mp4"):
		
					bits = int(i[1].bitrate)
					if ext in comp2:
						if bits > comp2[ext][1]:
							comp2[ext] = [itag, bits, i[1].audio_codec, valu_e]
					else:
						comp2[ext] = [itag, bits, i[1].audio_codec, valu_e]
			comp[0] = sorted(list(set(comp[0])))
			return comp, comp2

#------------------------------------------------------------------------------------------------------------

TOKENN = "XXXXXXXXXXTelegramXXXXXTokenXXXXXXXXXX"

bottele = telebot.TeleBot(TOKENN)

@bottele.message_handler(commands=['start'])
def send_welcome(message):
	print("Started")
	print(message.text)
	bottele.reply_to(message, "Hey, bot is starting... ")
	time.sleep(1)
	bottele.send_message(message.chat.id, "[FULL VID] Send link of the video like this : /downloadmp4 videolink\n[AUDIO ONLY] Send link of the video like this : /downloadmp3 videolink")


@bottele.message_handler(commands=['downloadmp4'])
def downlmp4(message):
	mess= str(message.text)
	print(mess)
	
	link = mess.split()[1]


	#def convertto (file, extension):
	#	if extension == 'mp4':
		
	#	if extension == 'mp3':
	#def merge (file1, file2):
		
	#def downmp4 (link, res): #video.get_by_itag(22) #.download()
	
	vidX, audX = streams(link)
	
	markup = types.InlineKeyboardMarkup()
	recommended = []
	#print(vidX)
	for vod in vidX[0]:
		if vidX[1][vod][3] == True:
			recommended.append(str(vidX[1][vod][1]))
		ytext = str(vod)+'p'+' ==> '+str(vidX[1][vod][-1])
		markup.add(types.InlineKeyboardButton(text=ytext, callback_data=str(vidX[1][vod][0])))
	#print(recommended)
	bottele.send_message(chat_id=message.chat.id, text="choose video resolution", reply_markup=markup)
	bottele.send_message(chat_id=message.chat.id, text=str(max(recommended))+" is recommended.")


@bottele.message_handler(commands=['downloadmp3'])
def downlmp3(message):
	mess= str(message.text)
	print(mess)

	link = mess.split()[1]
	
	audX = streams(link, only_audio=True)
	time.sleep(1)
	markup = types.InlineKeyboardMarkup()
	#print(audX)
	for vod in audX:
		ytext = str(audX[vod][1])[:-3]+'kbps'+' ==> '+str(audX[vod][-1])
		markup.add(types.InlineKeyboardButton(text=ytext, callback_data=str(audX[vod][0])))

	bottele.send_message(chat_id=message.chat.id, text="choose audio", reply_markup=markup)


@bottele.callback_query_handler(func=lambda call: True)
def longname(call):
	global video
	print(call.data)
	tmp = video.get_by_itag(call.data)
	x = tmp.download("folder")
	#print('this is X',x)
	if tmp.is_progressive == False and tmp.type == "video":
		dd = video.filter().get_audio_only()
		y = dd.download("audiofolder")
		#MERGE-
		i1 = ffmpeg.input(x)
		i2 = ffmpeg.input(y)
		merged  = ffmpeg.concat(i1, i2, v=1, a=1) 
		#name = x.split('\\')[-1:][0].rsplit('.', 1)[0]
		name, tens = os.path.splitext(os.path.basename(x))
		output  = ffmpeg.output(merged, name+".mp4")
		output.run(overwrite_output=True)
		print("Finished converting {}".format(output))
		# sendVideo
		with open(name+".mp4", 'rb') as vidfile:
			#if os.path.getsize(name+".mp4") > 52428800 :
			try:
				bottele.send_video(call.message.chat.id, vidfile)
			except:

				files = {'file': (name+".mp4", vidfile),}
				response = requests.post('https://api.anonfiles.com/upload', files=files)
				#print(response.json())
				bottele.send_message(call.message.chat.id, response.json()['data']['file']['url']['short'])

	elif tmp.subtype == "webm" and tmp.type == "video":
		#CONVERT-WEBM-TO-MP4
		i1 = ffmpeg.input(x)
		name = x.split('\\')[-1:][0].rsplit('.', 1)[0]
		output  = ffmpeg.output(i1, name+".mp4")
		output.run(overwrite_output=True)
		print("Finished converting {}".format(output))
		# sendVideo
		with open(name+".mp4", 'rb') as vidfile:
			#if os.path.getsize(name+".mp4") > 52428800 :
			try:
				bottele.send_video(call.message.chat.id, vidfile)
			except:

				files = {'file': (name+".mp4", vidfile),}
				response = requests.post('https://api.anonfiles.com/upload', files=files)
				#print(response.json())
				bottele.send_message(call.message.chat.id, response.json()['data']['file']['url']['short'])

	elif tmp.type == "audio":
		#CONVERT-MP4:WEBM-TO-MP3
		i1 = ffmpeg.input(x)
		#name = x.split('\\')[-1:][0].rsplit('.', 1)[0]
		name, tens = os.path.splitext(os.path.basename(x))
		print(name)
		output  = ffmpeg.output(i1, name+".mp3") #os.path.join(os.path.dirname(os.path.dirname(x)), "filetosend", name+".mp3")
		output.run(overwrite_output=True)
		print("Finished converting {}".format(output))
		# sendAudio
		with open(name+".mp3", 'rb') as audiofile:
			#if os.path.getsize(name+".mp3") > 52428800 :
			try:
				bottele.send_audio(call.message.chat.id, audiofile)
			except:

				files = {'file': (name+".mp3", audiofile),}
				response = requests.post('https://api.anonfiles.com/upload', files=files)
				#print(response.json())
				bottele.send_message(call.message.chat.id, response.json()['data']['file']['url']['short'])

	elif tmp.is_progressive == True and tmp.subtype == "mp4":
		with open(x, 'rb') as vidfile:
			#if os.path.getsize(x) > 52428800 :
			try:
				bottele.send_video(call.message.chat.id, vidfile)
			except:

				files = {'file': (x, vidfile),}
				response = requests.post('https://api.anonfiles.com/upload', files=files)
				print(response.json())
				bottele.send_message(call.message.chat.id, response.json()['data']['file']['url']['short'])	

	else:
		pass
	for trash in [x, name+".mp4", name+".mp3"]:
		try:
			os.remove(trash)
		except FileNotFoundError:
			print(trash, 'not deleted')

	video = None
	try:
		os.remove(y)
	except FileNotFoundError: #UnboundLocalError:
		print(y, 'not deleted (passing)')



bottele.infinity_polling()


