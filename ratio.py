def divider(v1=0, v2=0):

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

  if pp < float(10):
    ratio = f"{pp:.2f}"
  elif float(100) > pp >= float(10):
    ratio = f"{pp:.1f}"
  elif pp >= float(100):
    ratio = int(pp)

  return ratio



# ily_pichu >//< #