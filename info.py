import json
import requests

listPlayers = []
listConstructors = []

def getFromAPI():
  listPlayers.clear()
  listConstructors.clear()
  response = requests.get("https://fantasy-api.formula1.com/partner_games/f1/players")
  jsonData = json.loads(response.text)['players']
  
  for item in jsonData:
    player = {"name":None, "surname":None, "price":None,"sentiment":None, "ppm":None, "position":None}
    player['name'] = item['first_name']
    player['surname'] = item['last_name']
    player['price'] = item['price']
    
    if player['surname'] == "":
      listConstructors.append(player)
    else: 
      listPlayers.append(player)

    ob = item['current_price_change_info']['probability_price_up_percentage']
    ob1 = item['current_price_change_info']['probability_price_down_percentage']
    if ob < ob1:
      player['sentiment'] = ob1
      player['position']="-"
    else:
      player['sentiment'] = ob
      player['position']="+"
    
    player['ppm'] = (item['season_score']/10.)/item['price']
    player['ppm'] = int(player['ppm']*1000)/1000.
  
  return 


def sentimentSort(e):
  return e['sentiment']

def pointsSort(e):
  return e['ppm']

def get_sentiment():
  getFromAPI()

  listUpPlayers = []
  listDownPlayers = []
  listUpConstructors = []
  listDownConstructors = []

  for item in listPlayers:
    if item['position'] == "+":
      listUpPlayers.append(item)
    else:
      listDownPlayers.append(item)
    
  for item in listConstructors:
    if item['position'] == "+":
      listUpConstructors.append(item)
    else:
      listDownConstructors.append(item)

  listUpPlayers.sort(reverse=True,key=sentimentSort)
  listDownPlayers.sort(key=sentimentSort)
  listUpConstructors.sort(reverse=True,key=sentimentSort)
  listDownConstructors.sort(key=sentimentSort)
  sent="\n```"
  
  sent+="\n"
  sent+="┌─────────────────────┬───────┬──────┐"
  sent+="\n"
  sent+="│         Name        │ Price │ Sent │"
  sent+="\n"
  sent+="├─────────────────────┼───────┼──────┤"
  sent+="\n"
  for item in listUpPlayers:
    
    full=item['name']+" "+item['surname']
    while(len(full) < 20): full+=" "
    sent+="│ "
    sent+=full
    sent+="│  "
    if len(str(item['price'])) < 4: sent+=" "
    sent+=str(item['price'])

    sent+=" │ "
    if len(str(item['sentiment'])) < 2: sent+=" "
    sent+=str(item['sentiment'])
    sent+=" %"
    sent+=" │"
    sent+="\n"
    
  sent+="├─────────────────────┼───────┼──────┤"
  sent+="\n"
  for item in listDownPlayers:
    full=item['name']+" "+item['surname']
    while(len(full) < 20): full+=" "
    sent+="│ "
    sent+=full
    sent+="│  "
    if len(str(item['price'])) < 4: sent+=" "
    sent+=str(item['price'])
    sent+=" │"
    sent+="-"
    if len(str(item['sentiment'])) < 2: sent+=" "
    sent+=str(item['sentiment'])
    sent+=" %"
    sent+=" │"
    sent+="\n"  
  
  sent+="└─────────────────────┴───────┴──────┘"

  sent+="\n"
  sent+="┌─────────────────────────────────────────┬───────┬──────┐"
  sent+="\n"
  sent+="│               Constructor               │ Price │ Sent │"
  sent+="\n"
  sent+="├─────────────────────────────────────────┼───────┼──────┤"
  sent+="\n"

  for item in listUpConstructors:
    full=item['name']+" "+item['surname']
    while(len(full) < 40): full+=" "
    sent+="│ "
    sent+=full
    sent+="│  "
    if len(str(item['price'])) < 4: sent+=" "
    sent+=str(item['price'])
    sent+=" │ "
    
    if len(str(item['sentiment'])) < 2: sent+=" "
    sent+=str(item['sentiment'])
    sent+=" %"
    sent+=" │"
    sent+="\n"  

  sent+="├─────────────────────────────────────────┼───────┼──────┤"
  sent+="\n"
  for item in listDownConstructors:
    full=item['name']+" "+item['surname']
    while(len(full) < 40): full+=" "
    sent+="│ "
    sent+=full
    sent+="│  "
    if len(str(item['price'])) < 4: sent+=" "
    sent+=str(item['price'])
    sent+=" │"
    sent+="-"
    if len(str(item['sentiment'])) < 2: sent+=" "
    sent+=str(item['sentiment'])
    sent+=" %"
    sent+=" │"
    sent+="\n" 
  sent+="└─────────────────────────────────────────┴───────┴──────┘"
  sent+="```"
  return(sent)
  

def get_PPM():
  getFromAPI()
    
  listPlayers.sort(reverse=True,key=pointsSort)
  listConstructors.sort(reverse=True,key=pointsSort)
  result="\n```"
  
  result+="\n"
  result+="┌─────────────────────┬───────┬───────┐"
  result+="\n"
  result+="│         Name        │ Price │  PPM  │"
  result+="\n"
  result+="├─────────────────────┼───────┼───────┤"
  result+="\n"
  for item in listPlayers:
    
    full=item['name']+" "+item['surname']
    while(len(full) < 20): full+=" "
    result+="│ "
    result+=full
    result+="│  "
    if len(str(item['price'])) < 4: result+=" "
    result+=str(item['price'])

    result+=" │ "
    
    result+=str(item['ppm'])
    if len(str(item['ppm'])) < 5: result+=" "
    if len(str(item['ppm'])) < 4: result+=" "
    result+=" │"
    result+="\n"
    
  
  result+="└─────────────────────┴───────┴───────┘"

  result+="\n"
  result+="┌─────────────────────────────────────────┬───────┬───────┐"
  result+="\n"
  result+="│               Constructor               │ Price │  PPM  │"
  result+="\n"
  result+="├─────────────────────────────────────────┼───────┼───────┤"
  result+="\n"

  for item in listConstructors:
    full=item['name']+" "+item['surname']
    while(len(full) < 40): full+=" "
    result+="│ "
    result+=full
    result+="│  "
    if len(str(item['price'])) < 4: result+=" "
    result+=str(item['price'])
    result+=" │ "
    
    result+=str(item['ppm'])
    if len(str(item['ppm'])) < 5: result+=" "
    result+=" │"
    result+="\n"  

  result+="└─────────────────────────────────────────┴───────┴───────┘"
  result+="```"
  return(result)