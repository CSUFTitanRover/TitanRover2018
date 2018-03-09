from datetime import datetime, date

d = str(date.today())
epo = datetime(int(d[0:4]), int(d[5:7]), int(d[8:11]), 8, 0, 0)

def ep():
  x = round((datetime.utcnow()- epo).total_seconds(), 3)
  #print('epo:', epo)
  #print(x)
  return x
