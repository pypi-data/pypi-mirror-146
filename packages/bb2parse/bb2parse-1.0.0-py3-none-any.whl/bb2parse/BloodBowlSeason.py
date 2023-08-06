from difflib import Match
from parse import parse
from BloodBowlMatch import Offense,Defense,Injuries,BloodBowlMatch
from ordered_set import OrderedSet
from collections import Counter


# For multiple games and multiple teams, all teans should play the same amount of games
class BloodBowlSeason:
    def __init__(self,*file):
        self.filelist = []
        for arg in file:
            self.filelist.append(arg)
        self.seasonmatchlist= []
        for item in self.filelist:
            self.seasonmatchlist.append(BloodBowlMatch(item))
        self.Teams= BloodBowlSeason.Teams(self.seasonmatchlist)
        self.teams = BloodBowlSeason.Teams.get_teams(self.Teams)
        # return iterable
        self.getTeams = [i for i in self.Teams.tmp.values()]
        self.seasonlength = self.getTeams[0].matches_played
        self.scoreboard = {i.name:i.total_record for i in self.getTeams}
        # Scoreboard of records
        
    class Teams:
        def __init__(self, MatchObjectList):
            # Set of team names #static
            self.teamlist = OrderedSet()
            for match in MatchObjectList:
                self.teamlist.add(match.HomeTeam.name)
                self.teamlist.add(match.AwayTeam.name)
            # dictionary of teams and list of their matches
            self.team_match_list = {k: [] for k in self.teamlist}
            for i in MatchObjectList:
                self.team_match_list[i.HomeTeam.name].append(i)
                self.team_match_list[i.AwayTeam.name].append(i)
            self.tmp = { k: {} for k in self.teamlist}
            for x in self.teamlist:
                self.tmp[x] = BloodBowlSeason.Teams.Team(x,self.team_match_list[x],self.teamlist)
        ## Total Home vs Away record 
        
                
        def get_teams(self):
            return self.teamlist
        def __repr__(self):
                return '<BloodBowlTeams Object>'
        
        
        class Team:
            def __init__(self,name,matches,teamlist):
                self.teamlist = teamlist
                self.matches = matches
                self.name = name
                self.matches_played = len(self.matches)
                if self.name == self.matches[0].HomeTeam.name:
                    self.coach = self.matches[0].HomeTeam.coach
                else:
                    self.coach = self.matches[0].AwayTeam.coach
                self.record = {'HomeRecord':{'W':0,'L':0 ,'D':0},'AwayRecord':{'W':0,'L':0,'D':0},'Breakdown':{k: {'W':0,'L':0,'D':0} for k in self.teamlist if k is not self.name}}
                for item in self.matches:
                    if item.match_outcome['winner'] == self.name:
                        if item.home == self.name:
                            self.record['HomeRecord']['W'] += 1
                            self.record['Breakdown'][item.away]['W'] += 1
                        else:
                            self.record['AwayRecord']['W'] += 1
                            self.record['Breakdown'][item.home]['W'] += 1
                    elif item.match_outcome['loser'] == self.name:
                        if item.home == self.name:
                            self.record['HomeRecord']['L'] += 1
                            self.record['Breakdown'][item.away]['L'] += 1
                        else:
                            self.record['AwayRecord']['L'] += 1
                            self.record['Breakdown'][item.home]['L'] += 1
                    else:
                        if item.home == self.name:
                            self.record['HomeRecord']['D'] += 1
                            self.record['Breakdown'][item.away]['D'] += 1
                        else:
                            self.record['AwayRecord']['D'] += 1
                            self.record['Breakdown'][item.home]['D'] += 1
                # self.total_record = dict(self.record['HomeRecord'].items() + self.record['AwayRecord'].items() + [(k,self.record['HomeRecord'][k] + self.record['AwayRecord'][k]) for k in set(self.record['AwayRecord']) & self.record['HomeRecord']])
                self.total_record = {x: self.record['HomeRecord'].get(x, 0) + self.record['AwayRecord'].get(x,0) for x in OrderedSet(self.record['HomeRecord']).union(self.record['AwayRecord'])}
            def get_total_kills(self):
                total_kills = 0
                for item in self.matches:
                    if item.home == self.name:
                        total_kills += item.HomeTeam.Defense.kills_inflicted
                    else:
                        total_kills += item.AwayTeam.Defense.kills_inflicted
                return total_kills
                    
            def get_total_touchdowns(self):
                total_td = 0
                for item in self.matches:
                    if item.home == self.name:
                        total_td += item.HomeTeam.touchdowns_scored
                    else:
                        total_td += item.AwayTeam.touchdowns_scored
                return total_td
            def get_total_running_yards(self):
                total_running_yards = 0
                for item in self.matches:
                    if item.home == self.name:
                        total_running_yards += item.HomeTeam.Offense.running_yards
                    else:
                        total_running_yards += item.AwayTeam.Offense.running_yards
                return total_running_yards
            def get_total_passing_yards(self):
                total_passing_yards = 0
                for item in self.matches:
                    if item.home == self.name:
                        total_passing_yards += item.HomeTeam.Offense.passing_yards
                    else:
                        total_passing_yards += item.AwayTeam.Offense.passing_yards
                return total_passing_yards
            def get_td_avg(self):
                x =self.get_total_touchdowns()
                return x / self.matches_played
            
            #roster
            def __repr__(self):
                return '<BloodBowlTeam Object>'
    
    def __repr__(self):
        return '<BloodBowlSeason Object>'



    
