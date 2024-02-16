from PIL import Image, ImageDraw, ImageFont
from stats import Pika
import playermodel, sys

ign = sys.argv[1]

ref = Image.open('2.png')
stat = Image.new("RGBA", (1366, 768), (0,0,0,0))
draw = ImageDraw.Draw(stat)
draw.fontmode = '1'

hfont = ImageFont.truetype("assets/Mojangles.ttf", 110)
bfont = ImageFont.truetype("assets/Mojangles.ttf", 50)
mfont = ImageFont.truetype("assets/Mojangles.ttf", 40)
sfont = ImageFont.truetype("assets/Mojangles.ttf", 28)

pr = Pika.Profile(ign)
st = Pika.BWstats(pr[0])

def alignC(posx, text):
  width = draw.textlength(text, font=mfont)
  newx = float(posx) - (float(width) / 2)
  return int(newx)

def alignR(posx, text):
  width = draw.textlength(text, font=mfont)
  newx = float(posx) - float(width)
  return int(newx)



#Color handling

def rc(rat):
  if float(rat) < float(1):
    ratc = 'red'
  elif float(rat) > float(1):
    ratc = 'lime'
  else:
    ratc = 'white'
  return ratc


lvl = int(pr[1])

if 0 < lvl < 5:
  lvlc = 'gray'

elif 5<=lvl<10 or 40<=lvl<45:
  lvlc = 'lime'
elif 10<=lvl<15 or 45<=lvl<50:
  lvlc = 'aqua'
elif 15<=lvl<20 or 50<=lvl<60:
  lvlc = 'pink'
elif 20<=lvl<25 or  60<=lvl<75:
  lvlc = 'orange'
elif 25<=lvl<30 or 75<=lvl<100:
  lvlc = 'yellow'
elif 30<=lvl<35 or lvl==100:
  lvlc = 'red'

elif 35 <= lvl < 40:
  lvlc = 'white'



if lvl >= 35:
  lvlb = True
else:
  lvlb = False




rank = pr[2]

if rank == 'Champion':
  rankc = (170,0,0)
elif rank == 'Titan':
  rankc = (255,170,0)
elif rank == 'Elite':
  rankc = (85,255,255)
elif rank == 'VIP':
  rankc = (85,255,85)
else:
  rankc = (170,170,170)



#Profile
#Username
draw.text((alignC(238, pr[0]), 55), pr[0], fill=rankc, font=mfont)

model = Image.open(playermodel.model(pr[0]))
stat.paste(model, (51, 110), model)











#Stats
#0 Title
draw.text((490, 40), "BedWars Stats", fill=(255, 255, 255), font=hfont)
#1 Positive
draw.text((488, 172), "Wins", fill=(255, 255, 255), font=mfont)
draw.text((488, 280), "F-Kills", fill=(255, 255, 255), font=mfont)
draw.text((488, 388), "Kills", fill=(255, 255, 255), font=mfont)
draw.text((488, 496), "B-Break", fill=(255, 255, 255), font=mfont)
draw.text((488, 604), "Hs Ws", fill=(255, 255, 255), font=mfont)
#2 Negative
draw.text((844, 172), "Loss", fill=(255, 255, 255), font=mfont)
draw.text((844, 280), "F-Death", fill=(255, 255, 255), font=mfont)
draw.text((844, 388), "Deaths", fill=(255, 255, 255), font=mfont)
draw.text((844, 496), "Arrows", fill=(255, 255, 255), font=mfont)
draw.text((844, 604), "Games", fill=(255, 255, 255), font=mfont)
#4 Ratio
draw.text((1201, 172), "WLR", fill=(255, 255, 255), font=mfont)
draw.text((1189, 280), "FDKR", fill=(255, 255, 255), font=mfont)
draw.text((1201, 388), "KDR", fill=(255, 255, 255), font=mfont)
draw.text((1201, 496), "AHR", fill=(255, 255, 255), font=mfont)
draw.text((1201, 604), "LVL", fill=(255, 255, 255), font=mfont)
#4 Position Positive
draw.text((572, 179), f'(#{st[1]})', fill="aqua", font=sfont)
draw.text((628, 287), f'(#{st[6]})', fill="aqua", font=sfont)
draw.text((577, 395), f'(#{st[11]})', fill="aqua", font=sfont)
draw.text((660, 503), f'(#{st[16]})', fill="aqua", font=sfont)
draw.text((610, 611), f'(#{st[21]})', fill="aqua", font=sfont)
#5 Position Negative
draw.text((944, 179), f'(#{st[3]})', fill="aqua", font=sfont)
draw.text((1008, 287), f'(#{st[8]})', fill="aqua", font=sfont)
draw.text((984, 395), f'(#{st[13]})', fill="aqua", font=sfont)
draw.text((992, 503), f'(#{st[18]})', fill="aqua", font=sfont)
draw.text((968, 611), f'(#{st[23]})', fill="aqua", font=sfont)
# Stats Ratio
draw.text((alignC(1227, st[4]), 213), st[4], fill=rc(st[4]), font=bfont)
draw.text((alignC(1227, st[9]), 321), st[9], fill=rc(st[9]), font=bfont)
draw.text((alignC(1227, st[14]), 429), st[14], fill=rc(st[14]), font=bfont)
draw.text((alignC(1227, st[19]), 537), st[19], fill=rc(st[19]), font=bfont)
draw.text((alignC(1227, pr[1]), 645), pr[1], fill=lvlc, font=bfont)
#Stats Positive
draw.text((495, 214), st[0], fill="lime", font=bfont)
draw.text((495, 322), st[5], fill="lime", font=bfont)
draw.text((495, 429), st[10], fill="lime", font=bfont)
draw.text((495, 537), st[15], fill="lime", font=bfont)
draw.text((495, 647), st[20], fill="lime", font=bfont)
#stats Negative
draw.text((852, 214), st[2], fill="lime", font=bfont)
draw.text((852, 322), st[7], fill="lime", font=bfont)
draw.text((852, 429), st[12], fill="lime", font=bfont)
draw.text((852, 537), st[17], fill="lime", font=bfont)
draw.text((852, 647), st[22], fill="lime", font=bfont)








ref.paste(stat, (0, 0), stat)

ref.save("output.png")

# ily_pichu >//< #