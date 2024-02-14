import requests
from io import BytesIO

def model(ignin):
    precheck = requests.get('https://api.mojang.com/users/profiles/minecraft/'+ignin)
    if "Couldn't find any profile" in (str(precheck.json())):
        ign = 'Steve'
    else:
        ign = ignin

    url = ("https://starlightskins.lunareclipse.studio/skin-render/custom/"+ign+"/full?wideModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/pose1.obj&slimModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/pose1.obj&propModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/pose1prop.obj&propTexture=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/tnt.png&cameraPosition={%22x%22:%228.47%22,%22y%22:%2223.06%22,%22z%22:%22-30.87%22}&cameraFocalPoint={%22x%22:%224%22,%22y%22:%2219%22,%22z%22:%22-16.24%22}&cameraFOV=45&cameraWidth=374&cameraHeight=437")
    res = requests.get(url)
    if res.status_code == 200:
        im_bytes = BytesIO(res.content)
    return im_bytes

model('ily_pichu')