from random import choice, randrange, shuffle


class Ability(object):
    def __init__(self, name: str, max_damage: int):
        self.name = name
        self.max_damage = max_damage

    def attack(self) -> int:
        return randrange(self.max_damage + 1)


class Armor(object):
    def __init__(self, name: str, max_block: int):
        self.name = name
        self.max_block = max_block

    def block(self):
        return randrange(self.max_block + 1)


class Weapon(Ability):
    def attack(self):
        return randrange(self.max_damage // 2, self.max_damage)


class Hero(object):
    def __init__(self, name: str, starting_health=100):
        self.name = name
        self.starting_health = starting_health
        self.current_health = starting_health
        self.deaths = 0
        self.kills = 0
        self.abilities = []
        self.armors = []

    def __str__(self):
        return self.name

    def add_kill(self):
        self.kills += 1

    def add_deaths(self):
        self.deaths += 1

    def add_ability(self, ability: Ability) -> None:
        self.abilities.append(ability)

    def add_armor(self, armor: Armor) -> None:
        self.armors.append(armor)

    def attack(self) -> int:
        return sum(ability.attack() for ability in self.abilities)

    def defend(self, damage: int) -> int:
        return damage - sum(armor.block() for armor in self.armors)

    def take_damage(self, incoming_damage: int) -> None:
        self.current_health -= self.defend(incoming_damage)

    def is_alive(self) -> bool:
        return self.current_health > 0

    def fight(self, opponent: "Hero") -> None:
        if len(self.abilities) == len(opponent.abilities) == 0:
            print("Draw")
            return
        # guarantee that the first attack is random
        player1, player2 = shuffle([self, opponent])
        while player1.is_alive() and player2.is_alive():
            player2.take_damage(player1.attack())
            if not (player1.is_alive() and player2.is_alive()):
                break
            player1.take_damage(player2.attack())
        player1.kills += player1.is_alive()
        player1.deaths += player1.is_alive() ^ 1
        player2.kills += player2.is_alive()
        player2.deaths += player2.is_alive() ^ 1
        print(f"{(player1.name if player1.is_alive() else player2.name)} won")

    def revive(self):
        self.current_health = self.starting_health

    def add_weapon(self, weapon: Weapon):
        self.abilities.append(weapon)


class Team(object):
    def __init__(self, name: str):
        self.name = name

        # order doesn't matter so let's use a data structure
        # with constant del/add
        self.heroes = []
        self.living_heroes = 0

    def team_has_lost(self):
        return self.living_heroes <= 0

    def add_hero(self, hero: Hero):
        # self.heroes[hero.name] = hero
        self.heroes.append(hero)
        self.living_heroes += hero.is_alive()

    def remove_hero(self, name: str):
        # if name not in self.members:
        #     return 0
        # del self.members[name]
        for i, hero in enumerate(self.heroes):
            if hero.name == name:
                self.living_heroes -= 1
                del self.heroes[i]
                return
        return 0

    def view_all_heroes(self):
        for hero in self.heroes:
            print(hero)

    def attack(self, other_team: "Team"):
        if not len(self.heroes):
            raise Exception("Our team has no heroes :{")
        if not len(other_team.heroes):
            raise Exception("Other team has no heroes ;{")
        while not self.team_has_lost() and not other_team.team_has_lost():
            choice(self.heroes).fight(choice(other_team.heroes))

    def revive_heroes(self, health=100):
        for hero in self.heroes:
            hero.revive()
        self.living_heroes = len(self.heroes)

    def stats(self):
        for hero in self.heroes:
            print(f"{hero} - deaths: {hero.deaths} kills: {hero.kills}")


class Arena(object):
    def __init__(self):
        self.team_one = None
        self.team_two = None

    @staticmethod
    def create_ability():
        return Ability(input("Name: "), input("max damage: "))

    @staticmethod
    def create_weapon():
        return Weapon(input("Name: "), input("max damage: "))

    @staticmethod
    def create_armor():
        return Armor(input("Name: "), input("max block:"))

    @staticmethod
    def create_hero():
        hero = Hero(input("Name: "))
        while input("Add armor (y/n)?") != "n":
            hero.add_armor(Arena.create_armor())
        while input("Add ability (y/n)?") != "n":
            hero.add_ability(Arena.create_ability())
        while input("Add weapon (y/n)?") != "n":
            hero.add_weapon(Arena.create_weapon())
        return hero

    @staticmethod
    def create_team():
        team = Team(input("Team name: "))
        for member in range(int(input("# of heroes: "))):
            team.add_hero(Arena.create_hero())
        return team

    @staticmethod
    def avg_kills_per_death(team):
        return sum(hero.kills for hero in team) / sum(hero.deaths for hero in team)

    def create_team_one(self):
        self.team_one = Arena.create_team()

    def create_team_two(self):
        self.team_two = Arena.create_team()

    def team_battle(self):
        self.team_one.attack(self.team_two)

    def show_stats(self):
        print(f"The winner is {'team one' if self.team_one.team_has_lost() else 'team two'}")

        print(f"Team one average kill/death: {Arena.avg_kills_per_death(self.team_one)}")
        print(f"Team two average kill/death: {Arena.avg_kills_per_death(self.team_two)}")

if __name__ == "__main__":
    game_is_running = True

    # Instantiate Game Arena
    arena = Arena()

    #Build Teams
    arena.create_team_one()
    arena.create_team_two()

    while game_is_running:

        arena.team_battle()
        arena.show_stats()
        play_again = input("Play Again? Y or N: ")

        #Check for Player Input
        if play_again.lower() == "n":
            game_is_running = False

        else:
            #Revive heroes to play again
            arena.team_one.revive_heroes()
            arena.team_two.revive_heroes()
