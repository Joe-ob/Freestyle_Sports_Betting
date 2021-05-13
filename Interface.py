##Base Code
import json
import requests
# An api key is emailed to you when you sign up to a plan
api_key = "46a70b05e16c5bdb663037f8eb80a31b"
# First get a list of in-season sports
sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
    'api_key': api_key
})
sports_json = json.loads(sports_response.text)
if not sports_json['success']:
    print(
        'There was a problem with the sports request:',
        sports_json['msg']
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



#sport_selection = 'baseball_mlb'                                                      
odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': api_key,                                                         #This should be in a .env file as instructed in the ReadMe file
    'sport': sport_selection,                                                         #This should definitely be a user input
    'region': 'us', # uk | us | eu | au                                         #I think we assume US
    'mkt': 'spreads', # h2h | spreads | totals           
    'dateFormat': 'iso'                      #This might be a user input
})
odds_json = json.loads(odds_response.text)
if not odds_json['success']:
    print(
        'There was a problem with the odds request:',
        odds_json['msg']
    )
else:
    # odds_json['data'] contains a list of live and 
    #   upcoming events and odds for different bookmakers.
    # Events are ordered by start time (live events are first)
    print()
    print("Good")
        #'Successfully got {} events'.format(len(odds_json['data'])),
        #'Here\'s the first event:'
    
    game_odds = (odds_json['data'][3])
    #print(game_odds)
    # Check your usage
    print()
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])
    


###Figuring out how to search by team
#team_selection = input("Please enter the name of the team you would like to search for: ")

for item in odds_json['data']:
    for teams_in_game in item['teams']:
        print(teams_in_game)
    for site in item["sites"]:
        for option in site:
            print(option['site_nice'])
    print("-----")
    print("-----")
    print("-----")




####User Input for the Zip Code (with Data Validation) to verify Legal Betting in each State
#zip_code = input("Please input your Zip Code: ")
#try:
#  if (len(zip_code)) != 5: 
#    raise ValueError()
#  elif zip_code.isnumeric() == False:
#    raise ValueError()
#except ValueError:
#  print("Error: Please Enter a valid 5 digit, numeric zip code")
#  exit()