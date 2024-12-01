from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

test = Image.open('assets/images/image_bw_foreground.png')
draw1 = ImageDraw.Draw(test)
draw1.fontmode = '1'

hfont = ImageFont.truetype("assets/Mojangles.ttf", 110)
bfont = ImageFont.truetype("assets/Mojangles.ttf", 50)
mfont = ImageFont.truetype("assets/Mojangles.ttf", 40)
sfont = ImageFont.truetype("assets/Mojangles.ttf", 28)

def alignC(posx, text, font=mfont):
    width = draw1.textlength(text, font=font)
    newx = float(posx) - (float(width) / 2)
    return int(newx)

def alignR(posx, text, font=sfont):
    width = draw1.textlength(text, font=font)
    newx = float(posx) - float(width)
    return int(newx)

def bwimg(
        
    ign,
    ign_c,
    gt,
    g_c,
    gnametag,
    glvlmember,
    gowner,
    seen,
    seen_c,

    playermodel,

    interval,
    int_c,
    mode,
    mode_c,

    v_c,

    vwins,
    vfkills,
    vkills,
    vbbreak,
    vhws,

    vloss,
    vfdeaths,
    vdeaths,
    varrows,
    vgames,

    p_c,

    pwins,
    pfkills,
    pkills,
    pbbreak,
    phws,

    ploss,
    pfdeaths,
    pdeaths,
    parrows,
    pgames,


    wlr,
    wlr_c,
    fkdr,
    fkdr_c,
    kdr,
    kdr_c,
    ahr,
    ahr_c,
    lvl,
    lvl_c

):
    
    bg = Image.open('assets/images/2.png')
    image = Image.open('assets/images/image_bw_foreground.png')
    draw = ImageDraw.Draw(image)
    draw.fontmode = '1'
    
    # Profile
    
    draw.text((alignC(238, ign, mfont), 55), ign, fill=ign_c, font=mfont) # username
    
    if playermodel:
        model = Image.open(BytesIO(playermodel))
    else: model = Image.open('assets/default.png')
    image.paste(model, (51, 110), model)


    draw.text((alignC(238, gt), 552), gt, fill=g_c, font=mfont) #Guild text
    draw.text((alignC(238, gnametag), 597), gnametag, fill='white', font=mfont) #Guild Name+Tag
    draw.text((alignC(238, glvlmember, font=sfont), 638), glvlmember, fill='white', font=sfont) #Guild Level+Members
    draw.text((alignC(238, gowner, font=sfont), 670), gowner, fill='white', font=sfont) #Guild owner

    draw.text((alignC(238, seen, font=sfont), 700), seen, fill=seen_c, font=sfont) # seen

    draw.text((alignR(822, interval, font=mfont), 125), interval, fill=int_c, font=mfont) # interval
    draw.text((862, 125), mode, fill=mode_c, font=mfont) # mode

    # Stats
    x1, x2 = 834, 1170

    draw.text((alignR(x1, pwins), 179), pwins, fill=p_c, font=sfont) #wins position
    draw.text((alignR(x1, pfkills), 287), pfkills, fill=p_c, font=sfont) # fkills position
    draw.text((alignR(x1, pkills), 394), pkills, fill=p_c, font=sfont) # kills position
    draw.text((alignR(x1, pbbreak), 502), pbbreak, fill=p_c, font=sfont) # bed break position
    draw.text((alignR(x1, phws), 612), phws, fill=p_c, font=sfont) # highest ws position

    draw.text((alignR(x2, ploss), 179), ploss, fill=p_c, font=sfont) # losses position
    draw.text((alignR(x2, pfdeaths), 287), pfdeaths, fill=p_c, font=sfont) # f deaths position
    draw.text((alignR(x2, pdeaths), 394), pdeaths, fill=p_c, font=sfont) # deaths position
    draw.text((alignR(x2, parrows), 502), parrows, fill=p_c, font=sfont) # arrows shot posision
    draw.text((alignR(x2, pgames), 612), pgames, fill=p_c, font=sfont) # total games posision

    draw.text((alignC(1236, wlr, bfont), 213), wlr, fill=wlr_c, font=bfont) # wlr
    draw.text((alignC(1236, fkdr, bfont), 321), fkdr, fill=fkdr_c, font=bfont) # fkdr
    draw.text((alignC(1236, kdr, bfont), 429), kdr, fill=kdr_c, font=bfont) # kdr
    draw.text((alignC(1236, ahr, bfont), 537), ahr, fill=ahr_c, font=bfont) # ahr
    draw.text((alignC(1236, lvl, bfont), 645), lvl, fill=lvl_c, font=bfont) # level

    draw.text((495, 214), vwins, fill=v_c, font=bfont) # wins
    draw.text((495, 322), vfkills, fill=v_c, font=bfont) # final kills
    draw.text((495, 429), vkills, fill=v_c, font=bfont) # kills
    draw.text((495, 537), vbbreak, fill=v_c, font=bfont) # bed breaks
    draw.text((495, 647), vhws, fill=v_c, font=bfont) # highest ws

    draw.text((852, 214), vloss, fill=v_c, font=bfont) # losses
    draw.text((852, 322), vfdeaths, fill=v_c, font=bfont) # final deaths 
    draw.text((852, 429), vdeaths, fill=v_c, font=bfont) # deaths
    draw.text((852, 537), varrows, fill=v_c, font=bfont) # arrows shot
    draw.text((852, 647), vgames, fill=v_c, font=bfont) # total games played
    
    bg.paste(image, (0, 0), image)

    output = BytesIO()
    bg.save(output, 'PNG')
    output.seek(0)
    return output