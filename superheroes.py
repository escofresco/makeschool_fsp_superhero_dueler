from random import choice, randrange, shuffle

class Ability(object):
    def __init__(self, name: str, max_damage: int):
        self.name = name
        self.max_damage = max_damage

    def attack(self) -> int:
        return randrange(self.max_damage+1)

class Armor(object):
    def __init__(self, name: str, max_block: int):
        self.name = name
        self.max_block = max_block

    def block(self):
        return randrange(self.max_block+1)

class Weapon(Ability):
    def attack(self):
        return randrange(self.max_damage//2, self.max_damage)

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

    def take_damage(self, damage: int) -> None:
        self.current_health -= self.defend(damage)

    def is_alive(self) -> bool:
        return self.current_health > 0

    def fight(self, opponent: 'Hero') -> None:
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
        player1.kills += player1.is_alive() ^ 0
        player1.deaths += player1.is_alive() ^ 1
        player2.kills += player2.is_alive() ^ 0
        player2.deaths += player2.is_alive() ^ 1
        print(f"{(player1.name if player1.is_alive() else player2.name)} won")

    def revive(self):
        self.current_health = self.starting_health

class Team(object):
    def __init__(self, name: str):
        self.name = name

        # order doesn't matter so let's use a data structure
        # with constant del/add
        self.heroes = []

    def add_hero(self, hero: Hero):
        #self.heroes[hero.name] = hero
        self.heroes.append(hero)

    def remove_hero(self, name: str):
        # if name not in self.members:
        #     return 0
        # del self.members[name]
        for i, hero in enumerate(self.heroes):
            if hero.name == name:
                del self.heroes[i]
                return
        return 0

    def view_all_heroes(self):
        for hero in self.heroes:
            print(hero)

    def attack(self, other_team: 'Team'):
        if not len(self.heroes):
            raise Exception('Our team has no heroes :{')
        if not len(other_team.heroes):
            raise Exception('Other team has no heroes ;{')
        choice(self.heroes).fight(choice(other_team.heroes))

    def revive_heroes(self, health=100):
        for hero in self.heroes:
            hero.revive()

    def stats(self):
        pass
