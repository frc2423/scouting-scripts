#Radar plots for scouting in FIRST Deep Space.
#Karl Twelker, Team 2423, March 2019.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def radarPlot(series, label = None):
    '''
    Makes a radar plot (spiderweb plot) for a pandas series.
    Adapted from code I found on stackexchange.
    '''
    categories=series.index
    #print(categories)
    N = len(categories)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values=series.values.flatten().tolist()
    values += values[:1]  #Makes it a list instead of a float
    #print(values)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=12)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([2.5, 5, 7.5], ["2.5", "5", "7.5"], color="grey", size=12)
    plt.ylim(0,7.5)

    # Plot data
    plt.plot(angles, values, linewidth=1, linestyle='solid', label = label)

    # Fill area
    plt.fill(angles, values, alpha=0.1)

    return plt
    #plt.show()

def plotAllianceSpiderWeb(teams, filename = None, plotTotal = False):
    '''
    Plots the combined spider webs for an alliance of teams.
    Useful for visualizing alliance strengths and weaknesses.
    plotTotal = True includes the sum of all teams
    '''
    plt.figure(figsize = (10, 10))
    if plotTotal:
        radarPlot(df.loc[teams][['TotalRocket', 'TotalShip', 'TotalHatch', 'TotalCargo', 'EndgameLevelClimbed']].sum(), label = 'Total')
    for team in teams:
        radarPlot(df.loc[team][['TotalRocket', 'TotalShip', 'TotalHatch', 'TotalCargo', 'EndgameLevelClimbed']], label = team)
    plt.legend()
    if filename:
        plt.savefig(filename)
    plt.show()

grid = False
#Example data from the green alliance from the 2019 Reading competition
df = pd.read_csv('NE-MAREA-green.csv')
#This file is a table of the mean scores for each team.
df.set_index('TeamScouted', inplace = True)

#Sum the four main scoring components
df['TotalRocket'] = (df['AutoBottomRocketCargo'] + df['AutoMiddleRocketCargo'] + df['AutoTopRocketCargo'] +
                     df['AutoBottomRocketPanels'] + df['AutoMiddleRocketPanels'] + df['AutoTopRocketPanels'] +
                     df['TeleopBottomRocketCargo'] + df['TeleopMiddleRocketCargo'] + df['TeleopTopRocketCargo'] +
                     df['TeleopBottomRocketPanels'] + df['TeleopMiddleRocketPanels'] + df['TeleopTopRocketPanels'])

df['TotalShip'] = (df['TeleopShipPanels'] + df['TeleopShipCargo'] +
                   df['AutoShipPanels'] + df['AutoShipCargo'])

df['TotalHatch'] = (df['TeleopShipPanels'] + df['AutoBottomRocketPanels'] + df['AutoMiddleRocketPanels'] + df['AutoTopRocketPanels'] +
                df['AutoShipPanels'] + df['TeleopBottomRocketPanels'] + df['TeleopMiddleRocketPanels'] + df['TeleopTopRocketPanels'])

df['TotalCargo'] = (df['TeleopShipCargo'] + df['AutoBottomRocketCargo'] + df['AutoMiddleRocketCargo'] + df['AutoTopRocketCargo'] +
                df['AutoShipCargo'] + df['TeleopBottomRocketCargo'] + df['TeleopMiddleRocketCargo'] + df['TeleopTopRocketCargo'])

#Generate a new dataframe with rankings for each category in the ranking field
rankingFields = ['TotalHatch', 'TotalCargo', 'TotalRocket', 'TotalShip', 'EndgameLevelClimbed']
d = {}
for field in rankingFields:
    d[field + 'Rank'] = df[field].sort_values(ascending = False).index
rankingDF = pd.DataFrame(d, dtype=np.int)

print(rankingDF)

grid = False

if grid:
    plt.figure(figsize = (16, 10))
for i, team in enumerate(df.index):
    if not grid:
        plt.figure()
    if grid:
        plt.subplot(8, 5, i + 1)
    plt.title('Team ' + str(int(team)))
    barChartFields = ['TotalHatch', 'TotalCargo', 'TotalRocket', 'TotalShip']
    data = df.loc[team][barChartFields].values
    plt.barh(range(len(barChartFields)), data)
    plt.yticks(range(len(barChartFields)), barChartFields)
    maxTotal = np.nanmax(df[barChartFields].values)
    plt.xlim([0, maxTotal + 2])

    plt.text(maxTotal - 1.25, len(barChartFields) - 0.75, 'Category Ranking')
    for i, field in enumerate(barChartFields):
        rankInField = df[field].rank(ascending = False)[team]
        plt.text(maxTotal, i, str(rankInField))

    if not grid:
        plt.show()
    break
if grid:
    plt.show()

print(df.loc[2423])

for team in df.index:
    plt.figure(figsize = (8, 8))
    radarPlot(df.loc[team][['TotalRocket', 'TotalShip', 'TotalHatch', 'TotalCargo', 'EndgameLevelClimbed']], label = team)
    plt.legend()
    plt.show()
    break

plotAllianceSpiderWeb([2423, 3958, 95])
