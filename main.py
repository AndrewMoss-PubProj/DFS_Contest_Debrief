import pandas as pd
import numpy as np
import datetime
import operator

def add_space(string):
    string_length = len(string) + 1  # will be adding 10 extra spaces
    string_revised = string.rjust(string_length)
    return string_revised

def get_stack_counts(teams):
    stacks = {}
    for item in set(teams):
        stacks[item] = teams.count(item)
    return sorted(stacks.items(), key=lambda item: item[1], reverse=True)


def process_lineup(row):
    print(row['Rank'])
    Lineup_row = []
    for player, position in zip(row['Lineup'], row['Lineup_Position']):
        position = position.strip()
        Player_info = Salaries[(Salaries['Name'] == player) & (np.isin(position,Salaries['Roster Position']))].\
            reset_index(drop=True)
        Lineup_row.extend([Player_info.loc[0, 'Name'], position,
                           Player_info.loc[0, 'Salary'], Player_info.loc[0, 'TeamAbbrev']])
    Lineup_row.extend([row['Points'], row['Rank']])
    Lineup_Dict[row['EntryName']] = Lineup_row
    return Lineup_Dict

def process_stacks(row):
    print(row['Rank'])
    row['Main_Stack'] = ''
    row['Secondary_Stack'] = ''
    row['Tertiary_Stack'] = ''
    row['Main_Stack_Length'] = ''
    row['Secondary_Stack_Length'] = ''
    row['Tertiary_Stack_Length'] = ''
    if row['Player_1_Position_Rostered'] == 'P' and row['Player_2_Position_Rostered'] == 'P':
        teams = row[['Player_3_Team', 'Player_4_Team', 'Player_5_Team', 'Player_6_Team', 'Player_7_Team',
                       'Player_8_Team', 'Player_9_Team', 'Player_10_Team']].tolist()
    elif row['Player_1_Position_Rostered'] == 'P' and row['Player_3_Position_Rostered'] == 'P':
        row[['Player_2_Team', 'Player_4_Team', 'Player_5_Team', 'Player_6_Team', 'Player_7_Team',
             'Player_8_Team', 'Player_9_Team', 'Player_10_Team']].tolist()
    elif row['Player_2_Position_Rostered'] == 'P' and row['Player_3_Position_Rostered'] == 'P':
        row[['Player_1_Team', 'Player_4_Team', 'Player_5_Team', 'Player_6_Team', 'Player_7_Team',
             'Player_8_Team', 'Player_9_Team', 'Player_10_Team']].tolist()
    teams = get_stack_counts(teams)
    row['Main_Stack'] = teams[0][0]
    row['Main_Stack_Length'] = teams[0][1]
    if teams[1][1] > 1:
        row['Secondary_Stack'] = teams[1][0]
        try:
            if teams[2][1] > 1:
                row['Tertiary_Stack'] = teams[2][0]
        except:
            'Only 2 Teams used'
    if row['Secondary_Stack'] != '':
        row['Secondary_Stack_Length'] = teams[1][1]
    if row['Tertiary_Stack'] != '':
        row['Tertiary_Stack_Length'] = teams[2][1]
    return row



DateString = input('Do you want to enter a datestring (Press enter to use today\'s date, otherwise use YYYY_MM_DD)')
if DateString == '':
    DateString = str(datetime.datetime.utcnow().year) + '_' + \
             str(datetime.datetime.utcnow().month) + '_' + \
             str(datetime.datetime.utcnow().day)
print('\n' + DateString)
Slate = input('What Slate are you trying to analyze')
Date_Slate = DateString + '_' + Slate

Lineup = pd.read_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\Lineup_Construction_Research\\Lineups\\' + Date_Slate +
                     '.csv')
Salaries = pd.read_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\Lineup_Construction_Research\\Salaries\\Salaries_' +
                       Date_Slate + '.csv',skiprows=7,
                                   usecols=["Name", "Name + ID", "Salary", "Roster Position", "TeamAbbrev",
                                            "Game Info"])
Salaries['Game Info'] = Salaries['Game Info'].str.replace(r'[^a-zA-Z,@]', '').str[0:-4]
Salaries['Game Info'] = Salaries['Game Info'].str.split('@')
Salaries['Game Info'] = np.where(Salaries['Game Info'].str[0] == Salaries['TeamAbbrev'],
                                 Salaries['Game Info'].str[1], Salaries['Game Info'].str[0])
Salaries = Salaries.rename(columns={'Game Info': 'Opp'})
Lineup = Lineup[Lineup['Lineup'].isnull() == False]

Lineup['Lineup'] = Lineup['Lineup'].apply(lambda x: add_space(x))
Lineup['Lineup'] = Lineup['Lineup'].str.replace('á', 'a')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('é', 'e')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('í', 'i')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('ó', 'o')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('ú', 'u')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('ñ', 'n')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('Á', 'A')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('É', 'E')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('Í', 'I')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('Ó', 'O')
Lineup['Lineup'] = Lineup['Lineup'].str.replace('Ú', 'U')

Lineup['Lineup_Position'] = Lineup['Lineup'].str.findall(r'\s+[P+|C+|1+B+|2+B+|3+B+|S+S+|O+F+]+\s')
Lineup['Lineup'] = Lineup['Lineup'].str.split(r'\s+[P+|C+|1B+|2B+|3B+|SS+|OF]+\s+').str[1:]

Lineup_Dict = {}

Lineup.apply(lambda x: process_lineup(x), axis=1)


colnames = ['Player_1_Name', 'Player_1_Position_Rostered', 'Player_1_Salary', 'Player_1_Team',
            'Player_2_Name', 'Player_2_Position_Rostered', 'Player_2_Salary', 'Player_2_Team',
            'Player_3_Name', 'Player_3_Position_Rostered', 'Player_3_Salary', 'Player_3_Team',
            'Player_4_Name', 'Player_4_Position_Rostered', 'Player_4_Salary', 'Player_4_Team',
            'Player_5_Name', 'Player_5_Position_Rostered', 'Player_5_Salary', 'Player_5_Team',
            'Player_6_Name', 'Player_6_Position_Rostered', 'Player_6_Salary', 'Player_6_Team',
            'Player_7_Name', 'Player_7_Position_Rostered', 'Player_7_Salary', 'Player_7_Team',
            'Player_8_Name', 'Player_8_Position_Rostered', 'Player_8_Salary', 'Player_8_Team',
            'Player_9_Name', 'Player_9_Position_Rostered', 'Player_9_Salary', 'Player_9_Team',
            'Player_10_Name', 'Player_10_Position_Rostered', 'Player_10_Salary', 'Player_10_Team', 'Points', 'Rank']
Lineups = pd.DataFrame.from_dict(Lineup_Dict, orient='index', columns=colnames)
Lineups = Lineups[['Rank', 'Points', 'Player_1_Name', 'Player_2_Name', 'Player_3_Name',
                   'Player_4_Name', 'Player_5_Name', 'Player_6_Name', 'Player_7_Name',
                   'Player_8_Name', 'Player_9_Name', 'Player_10_Name',
                   'Player_1_Position_Rostered', 'Player_2_Position_Rostered', 'Player_3_Position_Rostered',
                   'Player_4_Position_Rostered', 'Player_5_Position_Rostered', 'Player_6_Position_Rostered',
                   'Player_7_Position_Rostered', 'Player_8_Position_Rostered', 'Player_9_Position_Rostered',
                   'Player_10_Position_Rostered', 'Player_1_Salary', 'Player_2_Salary', 'Player_3_Salary',
                   'Player_4_Salary', 'Player_5_Salary', 'Player_6_Salary', 'Player_7_Salary',
                   'Player_8_Salary', 'Player_9_Salary', 'Player_10_Salary', 'Player_1_Team', 'Player_2_Team',
                   'Player_3_Team', 'Player_4_Team', 'Player_5_Team', 'Player_6_Team', 'Player_7_Team',
                   'Player_8_Team', 'Player_9_Team', 'Player_10_Team']]
Lineups = Lineups.apply(lambda x: process_stacks(x), axis=1)
Lineups.to_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\Lineup_Construction_Research\\Results\\' + Date_Slate +'.csv')





