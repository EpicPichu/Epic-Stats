from PIL import Image, ImageDraw, ImageFont
from stats import Pika
import playermodel

ref = Image.open('2.png')
stat = Image.new("RGBA", (1366, 768), (0,0,0,0))
draw = ImageDraw.Draw(stat)
draw.fontmode = '1'


ign = input('Ign: ')
pr = Pika.Profile(ign)
st = Pika.BWstats(pr[0])


hfont = ImageFont.truetype("assets/Mojangles.ttf", 110)
bfont = ImageFont.truetype("assets/Mojangles.ttf", 50)
mfont = ImageFont.truetype("assets/Mojangles.ttf", 40)
sfont = ImageFont.truetype("assets/Mojangles.ttf", 28)

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
draw.text((1201, 604), "- -", fill=(255, 255, 255), font=mfont)
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
draw.text((1188, 213), st[4], fill=(255, 255, 255), font=bfont)
draw.text((1189, 321), st[9], fill=(255, 255, 255), font=bfont)
draw.text((1189, 429), st[14], fill=(255, 255, 255), font=bfont)
draw.text((1189, 537), st[19], fill=(255, 255, 255), font=bfont)
draw.text((1189, 645), "- -", fill=(255, 255, 255), font=bfont)
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




def alignC(posx):
    width = draw.textlength(pr[0], font=mfont)
    newx = float(posx) - (float(width) / 2)
    return int(newx)

def alignR(posx):
    width = draw.textlength(pr[0], font=mfont)
    newx = float(posx) - float(width)
    return int(newx)




#Profile

if pr[2] == 'Champion':
  rankc = 'red'
elif pr[2] == 'Titan':
  rankc = 'yellow'
elif pr[2] == 'Elite':
  rankc = 'aqua'
elif pr[2] == 'VIP':
  rankc = 'lime'
else: rankc = 'white'

#Username
draw.text((alignC(238), 55), pr[0], fill=rankc, font=mfont)

model = Image.open(playermodel.model(pr[0]))
stat.paste(model, (51, 110), model)





ref.paste(stat, (0, 0), stat)

ref.save("output.png")

# ily_pichu >//< #