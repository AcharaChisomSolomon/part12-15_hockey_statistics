import json


class Player:
    def __init__(self, player: dict) -> None:
        self.name = player['name']
        self.nationality = player['nationality']
        self.assists = player['assists']
        self.goals = player['goals']
        self.penalties = player['penalties']
        self.team = player['team']
        self.games = player['games']

    def __str__(self) -> str:
        return f"{self.name:<21}{self.team:4} {self.goals:2} + {self.assists:2} = {self.goals + self.assists:3}"


class PlayerManager:
    def __init__(self) -> None:
        self.__players = []

    def load_players(self, filename: str):
        with open(filename) as file:
            data = file.read()

        players = json.loads(data)

        for player in players:
            self.__players.append(Player(player))

        return len(players)

    def get_player_data(self, name: str):
        for player in self.__players:
            if name == player.name:
                return player
            
        return None
    
    def get_teams(self):
        return sorted(list(set(map(lambda player: player.team, self.__players))))
    
    def get_countries(self):
        return sorted(list(set(map(lambda player: player.nationality, self.__players))))
    
    def __by_points(self, player: Player):
        return player.assists + player.goals
    
    def get_players_in_team(self, team_name: str):
        players = list(filter(lambda player: player.team == team_name, self.__players))
        return sorted(players, key=self.__by_points, reverse=True)
    
    def get_players_in_country(self, country_name):
        players = list(filter(lambda player: player.nationality == country_name, self.__players))
        return sorted(players, key=self.__by_points, reverse=True)
    
    def __by_points_then_goals(self, player: Player):
        return (player.assists + player.goals, player.goals)
    
    def __by_goals_then_games(self, player: Player):
        return (player.goals, -player.games)
    
    def get_players_with_most_points(self, amount: int):
        players = sorted(self.__players, key=self.__by_points_then_goals, reverse=True)
        return players[:amount]
    
    def get_players_with_most_goal(self, amount: int):
        players = sorted(self.__players, key=self.__by_goals_then_games, reverse=True)
        return players[:amount]
    

class Application:
    def __init__(self) -> None:
        self.__player_manager = PlayerManager()

    def __help(self):
        print('commands:')
        print('0 quit')
        print('1 search for player')
        print('2 teams')
        print('3 countries')
        print('4 players in team')
        print('5 players from country')
        print('6 most points')
        print('7 most goals')

    def __get_player(self):
        name = input('name: ')
        print()

        print(self.__player_manager.get_player_data(name))

    def __get_teams(self):
        teams = self.__player_manager.get_teams()
        for team in teams:
            print(team)

    def __get_countries(self):
        countries = self.__player_manager.get_countries()
        for country in countries:
            print(country)

    def __get_players_in_team(self):
        team = input('team: ')
        print()

        players = self.__player_manager.get_players_in_team(team)
        for player in players:
            print(player)

    def __get_players_in_country(self):
        country = input('country: ')
        print()

        players = self.__player_manager.get_players_in_country(country)
        for player in players:
            print(player)

    def __get_players_with_most_points(self):
        amount = int(input('how many: '))
        print()

        players = self.__player_manager.get_players_with_most_points(amount)
        for player in players:
            print(player)

    def __get_players_with_most_goals(self):
        amount = int(input('how many: '))
        print()

        players = self.__player_manager.get_players_with_most_goal(amount)
        for player in players:
            print(player)

    def execute(self):
        filename = input('file name: ')
        num_of_players = self.__player_manager.load_players(filename)
        print(f"read the data of {num_of_players} players")
        print()

        self.__help()

        while True:
            print()
            cmd = input('command: ')

            if cmd == '0':
                break
            elif cmd == '1':
                self.__get_player()
            elif cmd == '2':
                self.__get_teams()
            elif cmd == '3':
                self.__get_countries()
            elif cmd == '4':
                self.__get_players_in_team()
            elif cmd == '5':
                self.__get_players_in_country()
            elif cmd == '6':
                self.__get_players_with_most_points()
            elif cmd == '7':
                self.__get_players_with_most_goals()


Application().execute()