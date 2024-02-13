import requests
from ratio import divider

class Pika:

  def Profile(ign):
    req = requests.get(f'https://stats.pika-network.net/api/profile/{ign}')
    api = req.json()

    username = api['username']
    level = api['rank']['level']


    ranksjson = str(api['ranks'])
    ranklist = ['Champion', 'Titan', 'Elite', 'VIP']

    for ranks in ranklist:
      if ranks in ranksjson:
        pass
    rank = ranks


    if 'clan' in api:
      if api['clan'] is not None:
        gName = api['clan']['name']
        gTag = api['clan']['tag']
        gOwner = api['clan']['owner']['username']
        gLevel = api['clan']['leveling']['level']
        gMembers = len(api['clan']['members'])
      else:
        gName = None
        gTag = None
        gOwner = None
        gLevel = None
        gMembers = None


    dc_v = api['discord_verified']
    mail_v = api['email_verified']
    dc_boost = api['discord_boosting']

    return username, level, rank, gName, gTag, gOwner, gLevel, gMembers, dc_v, mail_v, dc_boost
  
  #
  
  def BWstats(ign='EpicPichu', interval='lifetime', mode='all_modes'):
    req = requests.get(f'https://stats.pika-network.net/api/profile/{ign}/leaderboard?type=BEDWARS&interval={interval}&mode={mode}')
    api = req.json()

    ###############################

    wina = api['Wins']['entries']
    if wina == None:
      winp, winv = '0', '0'
    else:
      winp, winv = str(wina[0]['place']), (wina[0]['value'])
    
    lossa = api['Losses']['entries']
    if lossa == None:
      lossp, lossv = '0', '0'
    else:
      lossp, lossv = str(lossa[0]['place']), lossa[0]['value']

    fka = api['Final kills']['entries']
    if fka == None:
      fkp, fkv = '0', '0'
    else:
      fkp, fkv = str(fka[0]['place']), fka[0]['value']

    fda = api['Final deaths']['entries']
    if fda == None:
      fdp, fdv = '0', '0'
    else:
      fdp, fdv = str(fda[0]['place']), fda[0]['value']

    ka = api['Kills']['entries']
    if ka == None:
      kp, kv = '0', '0'
    else:
      kp, kv = str(ka[0]['place']), ka[0]['value']

    da = api['Deaths']['entries']
    if da == None:
      dp, dv = '0', '0'
    else:
      dp, dv = str(da[0]['place']), da[0]['value']

    bba = api['Beds destroyed']['entries']
    if bba == None:
      bbp, bbv = '0', '0'
    else:
      bbp, bbv = str(bba[0]['place']), bba[0]['value']

#    bla = api['Beds lost']['entries']
#    if bla == None:
#      blp, blv = '0', '0'
#    else:
#      blp, blv = bla[0]['place'], bla[0]['value']

    arsa = api['Arrows shot']['entries']
    if arsa == None:
      arsp, arsv = '0', '0'
    else:
      arsp, arsv = str(arsa[0]['place']), arsa[0]['value']

    arha = api['Arrows hit']['entries']
    if arha == None:
      arhp, arhv = '0', '0'
    else:
      arhp, arhv = str(bba[0]['place']), bba[0]['value']

    hwsa = api['Highest winstreak reached']['entries']
    if hwsa == None:
      hwsp, hwsv = '0', '0'
    else:
      hwsp, hwsv = str(hwsa[0]['place']), hwsa[0]['value']

    gma = api['Games played']['entries']
    if gma == None:
      gmp, gmv = '0', '0'
    else:
      gmp, gmv = str(gma[0]['place']),  gma[0]['value']

    ##############################

    wlr = divider(winv, lossv)
    fkdr = divider(fkv, fdv)
    kdr = divider(kv, dv)
    ahr = divider(arsv, arhv)




    return winv, winp, lossv, lossp, wlr,  fkv, fkp, fdv, fdp, fkdr,   kv, kp, dv, dp, kdr,   bbv, bbp, arsv, arsp, ahr, hwsv, hwsp, gmv, gmp



# ily_pichu >//< #