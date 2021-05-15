##Base Code
import json
import requests
from datetime import datetime, timedelta
import time 
import pytz


# An api key is emailed to you when you sign up to a plan
api_key = '46a70b05e16c5bdb663037f8eb80a31b'
# First get a list of in-season sports

sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
    'api_key': api_key
})
sports_json = json.loads(sports_response.text)
if not sports_json['success']:
    print(
        'There was a problem with the sports request, please try again',
        #sports_json['msg']
    )
#else:
#    print()
#    print(
#        'Successfully got {} sports'.format(len(sports_json['data'])),
#        'Here\'s the first sport:'
#    )
#    print(sports_json['data'][3])
# To get odds for a sepcific sport, use the sport key from the last request
#   or set sport to "upcoming" to see live and upcoming across all sports

###User Input for the Zip Code (with Data Validation) to verify Legal Betting in each State
zip_code = input("Please input your Zip Code: ")
try:
  if (len(zip_code)) != 5: 
    raise ValueError()
  elif zip_code.isnumeric() == False:
    raise ValueError()
except ValueError:
  print("Error: Please Enter a valid 5 digit, numeric zip code")
  exit()


#Use Will's code to say if you live in a certain state, say online betting is illegal


###User Input for Sport Selection
sport = input("Please select your Sport (baseball, football, hockey, or basketball): ")
valid_options = ['baseball', 'football', 'hockey', 'basketball']
is_valid = sport not in valid_options
try:
  if is_valid == True: 
    raise ValueError()
except ValueError:
    print("Please enter a valid sport")
    exit()

## Can probably do this cleaner but its not raising an error if I don't make a new variable
sport_selection = sport
if sport_selection == 'baseball':
  sport_selection = 'baseball_mlb'
elif sport_selection == 'football':
  sport_selection = 'americanfootball_nfl'
elif sport_selection == 'hockey':
  sport_selection = 'icehockey_nhl'
elif sport_selection == 'basketball':
  sport_selection = 'basketball_nba'

                                                   
odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': api_key,                                                         
    'sport': sport_selection,                                                        
    'region': 'us', # uk | us | eu | au                                         
    'mkt': 'spreads', # h2h | spreads | totals           
    'dateFormat': 'unix'                      
})
odds_json = json.loads(odds_response.text)
if not odds_json['success']:
    print(
        'There was a problem with the odds request, please try again',
        #odds_json['msg']
    )
else:
    print("--------------------")
    print("Disclaimer: This app is not for gambling, it only compares odds from different gambling websites to give you the best information. you must go to the websites displayed to place your bet.")
    print("--------------------")
    print("Understanding the Odds: These odds show your potential winnings on different websites. If you bet one dollar on the team on the left or right, and they win, you will recieve the corresponding winnings in return. If your team loses, you recieve nothing. Good Luck Betting!")
    print("--------------------")


    a = []
    teams = []
    home_team = []
    away_team = []
    if odds_json['success'] == True:
      Team_name = input("Enter the name of the team you are looking for. If you want to search for all teams in this sport, type 'Go': ").split()
      print("---------------")
      for item in Team_name:
        name_cap = item.capitalize()
        teams.append(name_cap)
      #print(teams)
      for item in odds_json['data']:
          #print(item.keys())
          commence_datetime = item['commence_time']
          ts = int(commence_datetime)
          dt_utc = datetime.utcfromtimestamp(ts)
          dt_diff = timedelta(hours=4)
          dt_est = dt_utc - dt_diff
          game_start_date = dt_est.date()
          game_start_time = dt_est.time()
          home = item['teams'][0].split()
          away = item['teams'][1].split()
          for word in home:
            home_team.append(word)
          for word in away:
            away_team.append(word)
          if 'Go' in teams:
            a.append(item['teams'])
            print(f"For the game between {item['teams']} that starts at {game_start_time} on {game_start_date},")
            for site in item["sites"]:
              print(f"The odds on  {site['site_nice']} are {site['odds']['spreads']['odds']}")
          check = all(item in home_team for item in teams) or all(item in away_team for item in teams)
          if check is True:
            a.append(item['teams'])
            print(f"For the game between {item['teams']} that starts at {game_start_time} on {game_start_date},")
            for site in item["sites"]:
              print(f"The odds on  {site['site_nice']} are {site['odds']['spreads']['odds']}")
            home_team.clear()
            away_team.clear()
          if check is False:
            pass
            home_team.clear()
            away_team.clear()

      if not a:
          print("We could not find the team you were looking for, here are all of the upcoming games")
          print("---------------")
          for item in odds_json['data']:
              commence_datetime = item['commence_time']
              ts = int(commence_datetime)
              dt_utc = datetime.utcfromtimestamp(ts)
              dt_diff = timedelta(hours=4)
              dt_est = dt_utc - dt_diff
              game_start_date = dt_est.date()
              game_start_time = dt_est.time()
              print(f"For the game between {item['teams']} that starts at {game_start_time} on {game_start_date},")
              for site in item["sites"]:
                print(f"The odds on  {site['site_nice']} are {site['odds']['spreads']['odds']}")
      else:
          print(f"It appears there are no {sport_selection} games today, make sure this sport is in season or try another sport.")

    game_odds = (odds_json['data'][3])

    # Check your usage
    print()
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])
    











