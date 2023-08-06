import xml.etree.ElementTree as ET
from parse import parse


#For only one 
class BloodBowlMatch:
    def __init__(self,file):
        self.gamefile = file
        self.stats = parse(file)
        self.HomeTeam = BloodBowlMatch.HomeTeam(self.stats)
        self.AwayTeam = BloodBowlMatch.AwayTeam(self.stats)
        self.home = self.HomeTeam.name
        self.away = self.AwayTeam.name
        ## Match Outcome attribute ({Winning team}, 'W' vs {Losing Team}, 'L') or Draw
        self.match_outcome = self.outcome()
    
    def outcome(self):
        if int(self.AwayTeam.touchdowns_scored) > int(self.HomeTeam.touchdowns_scored):
            return {'winner': self.AwayTeam.name , 'loser':self.HomeTeam.name}
        elif int(self.AwayTeam.touchdowns_scored) < int(self.HomeTeam.touchdowns_scored):
            return {'winner': self.HomeTeam.name , 'loser':self.AwayTeam.name}
        else:
            return {'winner': None, 'loser':None, 'Draw': True}
    class HomeTeam:
        def __init__(self,x):
            self.Offense = Offense(x['Home'],'Home')
            self.Defense = Defense(x['Home'],'Home')
            self.Injuries = Injuries(x['Home'],'Home')
            self.name = x['Home']['TeamHomeName']
            self.coach = x['Home']['CoachHomeName']
            self.touchdowns_scored = self.Offense.touchdowns
            return

          
    class AwayTeam:
        def __init__(self,x):
            self.Offense = Offense(x['Away'],'Away')
            self.Defense = Defense(x['Away'],'Away')
            self.Injuries = Injuries(x['Away'],'Away')
            self.name = x['Away']['TeamAwayName']
            self.coach = x['Away']['CoachAwayName']
            self.touchdowns_scored = self.Offense.touchdowns
            return       
                
    def __repr__(self):
        return '<BloodBowlMatch Object>'
    
    
class Offense:
    def __init__(self,x,y):
        self.interceptions = x['Offense'][f'{y}SustainedInterceptions']
        self.touchdowns = int(x['Offense'][f'{y}InflictedTouchdowns'])
        self.running_yards = int(x['Offense'][f'{y}InflictedMetersRunning'])
        self.passing_yards = int(x['Offense'][f'{y}InflictedMetersPassing'])
        self.passes = x['Offense'][f'{y}InflictedPasses']
        self.catches = x['Offense'][f'{y}InflictedCatches']
        self.possession = x['Offense'][f'{y}PossessionBall']
        self.occupation_own = x['Offense'][f'{y}OccupationOwn']
        self.defense = Defense(x,y)
        return
    def __repr__(self):
        return '<Offense Object>'
    def get_pass_completion(self):
        return f'{self.catches/self.passes}%'
    def get_pass_intercept_ratio(self):
        return f'{self.defense.interceptions/float(self.passes)}%'
    
    
class Defense:
    def __init__(self,x,y):
        self.casualties_inflicted = x['Defense'][f'{y}InflictedCasualties']
        self.interceptions = x['Defense'][f'{y}InflictedInterceptions']
        self.ko_inflicted = x['Defense'][f'{y}InflictedKO']
        self.injuries_inflicted = x['Defense'][f'{y}InflictedInjuries']
        self.kills_inflicted = x['Defense'][f'{y}InflictedDead']
        self.expulsions = x['Defense'][f'{y}SustainedExpulsions']
        self.occupation_their = x['Defense'][f'{y}OccupationTheir']
        
        self.injuries = Injuries(x,y)
        return
    def __repr__(self):
        return '<Defense Object>'
    def get_ratio_injuries(self):
        return f'{float(self.injuries_inflicted)} injuries inflicted : {float(self.injuries.injuries_sustained)} injuries sustained'
    def get_ratio_casualties(self):
        return f'{float(self.casualties_inflicted)} casualties inflicted : {float(self.injuries.casualties_sustained)} casualties sustained'
    def get_ratio_kills(self):
        return f'{float(self.kills_inflicted)} kills inflicted : {float(self.injuries.deaths_sustained)} deaths sustained'
    
    
class Injuries:
    def __init__(self,x,y):
        self.deaths_sustained = x['Injuries'][f'{y}SustainedDead']
        self.ko_sustained = x['Injuries'][f'{y}SustainedKO']
        self.casualties_sustained = x['Injuries'][f'{y}SustainedCasualties']
        self.injuries_sustained = x['Injuries'][f'{y}SustainedInjuries']
    def __repr__(self):
        return '<Injuries Object>'

# tree = ET.parse('Coach.xml')
# root = tree.getroot()
# for item in root.find('./ReplayStep/RulesEventGameFinished/MatchResult/Row'):
#     print(item.tag)
# x = BloodBowlMatch('Coach.xml')
# print(type(x.HomeTeam.touchdowns_scored))
