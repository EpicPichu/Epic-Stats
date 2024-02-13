def divider(v1, v2):

    n1, n2 = int(v1), int(v2)
    if n1 != 0 and n2 != 0:
      out = n1/n2
    elif n1 != 0 and n2 == 0: 
      out = n1
    elif n1 == 0 and n2 != 0:
      out = 0
    elif n1 ==0 and n2 == 0:
       out = 0

    pp = round(out, 2)
    ratio = f"{pp:.2f}"

    return ratio

# ily_pichu >//< #