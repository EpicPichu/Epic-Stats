import sys, os

if len(sys.argv) > 4:
  print("Usage: ep-bw username interval mode")
  sys.exit(1)

dir = os.path.dirname(os.path.abspath(__file__))



def Stats(ign):
  from stats import Pika

  #Profile function
  pr = Pika.Profile(ign)
  
  #Invalid player handler
  if pr == 'Invalid player!':
    return 'Invalid player!'
  


  #Start executing
  from PIL import Image, ImageDraw, ImageFont

  ref = Image.open(dir+'/2.png')
  stat = Image.new("RGBA", (1366, 768), (0,0,0,0))
  draw = ImageDraw.Draw(stat)
  hfont = ImageFont.truetype(dir+"/assets/Mojangles.ttf", 110)
  bfont = ImageFont.truetype(dir+"/assets/Mojangles.ttf", 50)
  mfont = ImageFont.truetype(dir+"/assets/Mojangles.ttf", 40)
  sfont = ImageFont.truetype(dir+"/assets/Mojangles.ttf", 28)
  draw.fontmode = '1'

  #Stats function 
  args = sys.argv[2:]
  st = Pika.BWstats(pr[0], *args)

  #Alignment

  def alignC(posx, text, font=mfont):
    width = draw.textlength(text, font=font)
    newx = float(posx) - (float(width) / 2)
    return int(newx)

  def alignR(posx, text, font=sfont):
    width = draw.textlength(text, font=font)
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



  lvl= int(pr[1])
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



  #######################################################################################################


  #Profile ->

  #Username
  draw.text((alignC(238, pr[0], mfont), 55), pr[0], fill=rankc, font=mfont)

  #Player model
  import playermodel
  model = Image.open(playermodel.model(pr[0]))
  stat.paste(model, (51, 110), model)

  #Guild stats
  if pr[4] == None:
    #Guild text
    draw.text((alignC(238, 'NO GUILD'), 552), 'NO GUILD', fill='yellow', font=mfont)
  elif pr[4] is not None: 
    #Guild text
    draw.text((alignC(238, 'GUILD'), 552), 'GUILD', fill='aqua', font=mfont)
    #Guild Name+Tag
    draw.text((alignC(238, f'{pr[3]} ({pr[4]})'), 597), f'{pr[3]} ({pr[4]})', fill='white', font=mfont)
    #Guild Level+Members
    draw.text((alignC(238, f'Level {pr[5]} | {pr[6]} Members'), 642), f'Level {pr[5]} | {pr[6]} Members', fill='white', font=mfont)
    #Guild owner
    draw.text((alignC(238, f'By: {pr[7]}'), 687), f'By: {pr[7]}', fill='white', font=mfont)
  #



  #Stats ->
  
  #0 Title
  draw.text((490, 40), "BedWars Stats", fill='white', font=hfont)
  #1 Text Positive
  draw.text((488, 172), "Wins", fill='white', font=mfont)
  draw.text((488, 280), "F-Kills", fill='white', font=mfont)
  draw.text((488, 388), "Kills", fill='white', font=mfont)
  draw.text((488, 496), "B-Break", fill='white', font=mfont)
  draw.text((488, 604), "Hs Ws", fill='white', font=mfont)
  #2 Text Negative
  draw.text((844, 172), "Loss", fill='white', font=mfont)
  draw.text((844, 280), "F-Death", fill='white', font=mfont)
  draw.text((844, 388), "Deaths", fill='white', font=mfont)
  draw.text((844, 496), "Arrows", fill='white', font=mfont)
  draw.text((844, 604), "Games", fill='white', font=mfont)
  #4 Text Ratio
  draw.text((1201, 172), "WLR", fill='white', font=mfont)
  draw.text((1189, 280), "FDKR", fill='white', font=mfont)
  draw.text((1201, 388), "KDR", fill='white', font=mfont)
  draw.text((1201, 496), "AHR", fill='white', font=mfont)
  draw.text((1201, 604), "LVL", fill='white', font=mfont)
  x1, x2 = 834, 1170
  #4 Position Positive
  draw.text((alignR(x1, f'(#{st[1]})'), 179), f'(#{st[1]})', fill="aqua", font=sfont)
  draw.text((alignR(x1, f'(#{st[6]})'), 287), f'(#{st[6]})', fill="aqua", font=sfont)
  draw.text((alignR(x1, f'(#{st[11]})'), 394), f'(#{st[11]})', fill="aqua", font=sfont)
  draw.text((alignR(x1, f'(#{st[16]})'), 502), f'(#{st[16]})', fill="aqua", font=sfont)
  draw.text((alignR(x1, f'(#{st[21]})'), 612), f'(#{st[21]})', fill="aqua", font=sfont)
  #5 Position Negative
  draw.text((alignR(x2, f'(#{st[3]})'), 179), f'(#{st[3]})', fill="aqua", font=sfont)
  draw.text((alignR(x2, f'(#{st[8]})'), 287), f'(#{st[8]})', fill="aqua", font=sfont)
  draw.text((alignR(x2, f'(#{st[13]})'), 394), f'(#{st[13]})', fill="aqua", font=sfont)
  draw.text((alignR(x2, f'(#{st[18]})'), 502), f'(#{st[18]})', fill="aqua", font=sfont)
  draw.text((alignR(x2, f'(#{st[23]})'), 612), f'(#{st[23]})', fill="aqua", font=sfont)
  # Stats Ratio
  draw.text((alignC(1236, st[4], bfont), 213), st[4], fill=rc(st[4]), font=bfont)
  draw.text((alignC(1236, st[9], bfont), 321), st[9], fill=rc(st[9]), font=bfont)
  draw.text((alignC(1236, st[14], bfont), 429), st[14], fill=rc(st[14]), font=bfont)
  draw.text((alignC(1236, st[19], bfont), 537), st[19], fill=rc(st[19]), font=bfont)
  draw.text((alignC(1236, pr[1], bfont), 645), pr[1], fill=lvlc, font=bfont)
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
  ref.save(dir+"/output.png")
  return 'Success'





print(Stats(sys.argv[1]))





# ily_pichu >//< #