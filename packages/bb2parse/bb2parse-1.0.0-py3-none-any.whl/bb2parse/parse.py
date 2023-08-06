import xml.etree.ElementTree as ET

def parse(file):
    teams = ['Home','Away']
    objs = ['Offense','Defense','Injuries']
    offense_n = ['PossessionBall','OccupationOwn','SustainedInterceptions','InflictedTouchdowns','InflictedMetersRunning','InflictedMetersPassing','InflictedPasses','InflictedCatches']
    defense_n = ['OccupationTheir','InflictedCasualties','InflictedInterceptions','InflictedKO','InflictedInjuries','InflictedDead','SustainedExpulsions']
    injuries_n = ['SustainedDead','SustainedKO','SustainedCasualties','SustainedInjuries']
    values = []
    stats = {name:{key:{} for key in objs} for name in teams}
    for x in stats:
        stats[x][f'Team{x}Name'] = None
        stats[x][f'Coach{x}Name'] = None
        it = iter(values)
        stats[x]['Offense'] = {f'{x}{k}': next(it, 0) for k in offense_n}
        stats[x]['Defense']= {f'{x}{k}': next(it,0) for k in defense_n}
        stats[x]['Injuries'] = {f'{x}{k}': next(it, 0) for k in injuries_n}
        

    tree = ET.parse(file)
    root = tree.getroot()
    for item in root.find('./ReplayStep/RulesEventGameFinished/MatchResult/Row'):
        if item.tag in stats['Away'].keys():
            stats['Away'][item.tag] = item.text
        elif item.tag in stats['Away']['Offense'].keys():
            stats['Away']['Offense'][item.tag] = item.text
        elif item.tag in stats['Away']['Defense'].keys():
            stats['Away']['Defense'][item.tag] = item.text
        elif item.tag in stats['Away']['Injuries'].keys():
            stats['Away']['Injuries'][item.tag] = item.text
        elif item.tag in stats['Home'].keys():
            stats['Home'][item.tag] = item.text
        elif item.tag in stats['Home']['Offense'].keys():
            stats['Home']['Offense'][item.tag] = item.text
        elif item.tag in stats['Home']['Defense'].keys():
            stats['Home']['Defense'][item.tag] = item.text
        elif item.tag in stats['Home']['Injuries'].keys():
            stats['Home']['Injuries'][item.tag] = item.text
        else:
            pass
    return stats


