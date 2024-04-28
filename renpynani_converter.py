import os, pathlib, glob,re
from itertools import islice

def find_string(txt, str1):
  return txt.find(str1, txt.find(str1)+1)
#---
directory = str(pathlib.Path(__file__).parent.resolve())
os.chdir(directory)
for file in glob.glob("*.rpy"):
	filename=directory+"\\"+file
	head= open(filename,'r', encoding="utf8").readlines()

	mypage=[]

	for i in head:
		if not i.isspace():
			i=i.strip()

			if i.startswith("#"): #COMMENTS
				i=i.replace("#",";")

			elif i.startswith("label "): #LABELS
				i=i.replace("label ","#")
				i=i.replace(":","")

			elif i =="$ renpy.pause ()":
				i=""

			elif i.startswith("$ renpy.pause "): #RENPY PAUSE
				i=i.replace("$ renpy.pause","@wait ")
				for x in ["(",")"]:
					i=i.replace(x,"")

			elif i.startswith("$ renpy.")or i.startswith("call") or i.startswith("glitch")or i.startswith("queue")or i.startswith("show text"): #RENPY OTHER
				i=""

			elif i.startswith("$") or  i.startswith("default") or  i.startswith("define"): #VARIABLES
				i=i.replace("$","@set ");i=i.replace("default","@set ");i=i.replace("define","@set ")
				i="=".join([a.strip() for a in i.split("=")])
				i="+=".join([a.strip() for a in i.split("+=")])
				i="-=".join([a.strip() for a in i.split("-=")])
				i=i.replace("True","true")
				i=i.replace("False","false")


			elif i.startswith("scene"): #BACKGROUNDS
				i=i.replace("scene","@back")
				for x in ["at","with",":"]:
					i=i.split(x, 1)[0]

			elif i.startswith("show item"): #ITEM CG SHOW
				i=i.replace("show item","@char item.obj- pos:50,30 \n")
				i=re.sub("cg","@char item.obj>",i)
				for i in ["with",":"]:
					i=i.split(x, 1)[0]

			elif i.startswith("hide item"): #ITEM CG HIDE
				i="@hide item time:.5"

			elif i.startswith("play sound"): #SOUND EFFECTS
				i=i.replace("play sound","@sfx")
				i=i.replace("loop","loop:true")
				i=i.replace("volume","volume:")
				i=i.replace("volume ","volume:")
				i=i.replace("volume: ","volume:")
				i=re.sub("\"","",i)
				for x in [".mp3","fadein"]:
					i=i.split(x, 1)[0]
				for x in [")","("]:
					i=i.replace(x,"")
				i=re.sub('<[^>]+>', '', i)

			elif i.startswith("play music"): #MUSIC
				i=i.replace("play music","@bgm")
				for x in [")","("]:
					i=i.replace(x," ")
				i=re.sub("\"","",i)
				for x in [".mp3","fadein","loop"]:
					i=i.split(x, 1)[0]
				i=re.sub('<[^>]+>', '', i)
				

			elif i.startswith("stop sound"): #SOUND EFFECTS
				i="@stopSfx fade:1.0"

			elif i.startswith("stop music"): #MUSIC
				i="@stopBgm fade:1.0"

			elif i.startswith("narrator \""): #NARRATOR
				i=i.replace("narrator \"","")
				i=i.replace("{","<")
				i=i.replace("}",">")
				i=re.sub("\"","",i)
				for x in ["\"","<wave>","<sc>","<glitch>"]:
					i=re.sub(x,"",i)
				i=i.replace("[player]","{player.name}")

			elif i.startswith("\""): #CHOICE
				i=i.replace("\"","@choice \"")
				i=i[:-10]+"\""
				i=i.replace("[player]","{player.name}")

			elif len(i.split("\"", 1))==2: #CHARACTERS
				h=i.split("\"", 1)
				i= h[0].strip()+":"+" "+h[1]
				i=i.replace("{","<")
				i=i.replace("}",">")
				for x in ["\"","<wave>","<sc>","<glitch>"]:
					i=re.sub(x,"",i)
				i=i.replace("[player]","{player.name}")
					


			elif  i.startswith("show black"): #SHOW BLACK
				i="@back black"
				
			elif  i.startswith("show"): #SHOW SPRITE
				i=i.replace("show","@char")
				y=find_string(i, " ")
				i = i[:y] + "." + i[y+1:]
				y=find_string(i, " ")
				i=i[:y+1]

			elif  i.startswith("hide"): #SHOW SPRITE
				i=i.replace("hide","@hide")
				y=find_string(i, " ")
				i=i[:y+1]
			elif i.startswith("jump"): #JUMP
				i=i.replace("jump ","@goto .")

			elif i.startswith("if"): #IF
				i=i.replace("if ","@if")
				i="==".join([a.strip() for a in i.split("==")])
				i="!=".join([a.strip() for a in i.split("!=")])
				i=">".join([a.strip() for a in i.split(">")])
				i="<".join([a.strip() for a in i.split("<")])
				i=">=".join([a.strip() for a in i.split(">=")])
				i="<=".join([a.strip() for a in i.split("<=")])
			elif i.startswith("elif"): #IF
				i=i.replace("elif ","@elseif")
				i="==".join([a.strip() for a in i.split("==")])
				i="!=".join([a.strip() for a in i.split("!=")])
				i=">".join([a.strip() for a in i.split(">")])
				i="<".join([a.strip() for a in i.split("<")])
				i=">=".join([a.strip() for a in i.split(">=")])
				i="<=".join([a.strip() for a in i.split("<=")])
			
			elif i.startswith("else"): #else
				i=i.replace("else ","@else .")
				i=i+"\n@endif"
			else:
				i=";"+ i
			mypage.append(i)

	#print(mypage)
	myfile=file[:-4]+".nani"
	with open(myfile, "w") as fp:
         for item in mypage:
            fp.write("%s\n" % item)