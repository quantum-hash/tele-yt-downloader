#made with only default Notepad Windows 10 for fun

from pytube import YouTube

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
