from random import randrange, shuffle

class Ability(object):
    def __init__(self, name: str, max_damage: int):
        self.name = name
        self.max_damage

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

class Team(object):
    def __init__(self, name: str):
        self.name = name

        # order doesn't matter so let's use a data structure
        # with constant del/add
        self.members = {}

    def add_hero(self, hero: Hero):
        self.members[hero.name] = hero

    def remove_hero(self, name: str):
        if name in self.members:
            del self.members[name]

    def view_all(self):
        for hero in self.members:
            print(hero)

class Hero(object):
    def __init__(self, name: str, starting_health=100):
        self.name = name
        self.starting_health = self.current_health = starting_health
        self.abilities = []
        self.armors = []

    def __str__(self):
        return self.name

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

    def fight(self, opponent: Hero) -> None:
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
        print(f"{
              player1.name if player1.is_alive() else player2.name
        } won")
