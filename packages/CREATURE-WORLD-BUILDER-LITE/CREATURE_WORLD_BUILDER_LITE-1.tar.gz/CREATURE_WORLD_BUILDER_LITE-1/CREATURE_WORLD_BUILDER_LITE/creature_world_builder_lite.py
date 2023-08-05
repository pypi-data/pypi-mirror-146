"""
This file contains code for the game "Creature World Builder Lite".
Author: DigitalCreativeApkDev

The game "Creature World Builder Lite" is inspired by "Dragon City"
(https://play.google.com/store/apps/details?id=es.socialpoint.DragonCity&hl=en_NZ&gl=US) and "Monster Legends"
(https://play.google.com/store/apps/details?id=es.socialpoint.MonsterLegends&hl=en_NZ&gl=US).

Source of inspiration for the code in this file is as below.
https://github.com/NativeApkDev/LEGENDARY_CREATURE_CITY_BUILDER (by NativeApkDev, same account owner as
DigitalCreativeApkDev).
"""

# Game version: 1


# Importing necessary libraries


import sys
import uuid
import pickle
import copy
import random
from datetime import datetime, timedelta
import os
from functools import reduce

from mpmath import mp, mpf
from tabulate import tabulate

mp.pretty = True

# Creating static variables to be used throughout the game.


LETTERS: str = "abcdefghijklmnopqrstuvwxyz"
ELEMENT_CHART: list = [
    ["ATTACKING\nELEMENT", "TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
     "PURE",
     "LEGEND", "PRIMAL", "WIND"],
    ["DOUBLE\nDAMAGE", "ELECTRIC\nDARK", "NATURE\nICE", "FLAME\nWAR", "SEA\nLIGHT", "SEA\nMETAL", "NATURE\nWAR",
     "TERRA\nICE", "METAL\nLIGHT", "ELECTRIC\nDARK", "TERRA\nFLAME", "LEGEND", "PRIMAL", "PURE", "WIND"],
    ["HALF\nDAMAGE", "METAL\nWAR", "SEA\nWAR", "NATURE\nELECTRIC", "FLAME\nICE", "TERRA\nLIGHT", "FLAME\nMETAL",
     "ELECTRIC\nDARK", "TERRA", "NATURE", "SEA\nICE", "PRIMAL", "PURE", "LEGEND", "N/A"],
    ["NORMAL\nDAMAGE", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER",
     "OTHER",
     "OTHER", "OTHER", "OTHER"]
]


# Creating static functions to be used throughout the game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def tabulate_element_chart() -> str:
    return str(tabulate(ELEMENT_CHART, headers='firstrow', tablefmt='fancy_grid'))


def generate_random_name() -> str:
    res: str = ""  # initial value
    name_length: int = random.randint(5, 20)
    for i in range(name_length):
        res += LETTERS[random.randint(0, len(LETTERS) - 1)]

    return res.capitalize()


def generate_random_legendary_creature(element):
    # type: (str) -> LegendaryCreature
    name: str = generate_random_name()
    main_element: str = element
    rating: int = LegendaryCreature.MIN_RATING
    max_hp: mpf = mpf(random.randint(45000, 55000))
    max_magic_points: mpf = mpf(random.randint(45000, 55000))
    attack_power: mpf = mpf(random.randint(8500, 9500))
    defense: mpf = mpf(random.randint(8500, 9500))
    attack_speed: mpf = mpf(random.randint(100, 125))
    skills: list = [
        Skill("ATTACK SKILL #1", "Normal Attack Skill", "ATTACK",
              mpf("1e2") * random.randint(8, 14),
              DamageMultiplier(
                  random.randint(1, 3) * mpf("0.01"),
                  random.randint(1, 3) * mpf("0.01"),
                  mpf(3 + random.random() * 2),
                  mpf(random.random()),
                  mpf(3 + random.random() * 2),
                  mpf(random.random()),
                  random.randint(1, 3) * mpf("0.01"),
                  random.randint(1, 3) * mpf("0.01"),
                  mpf("0.5"),
                  mpf("0.25"),
                  mpf("0.05"),
                  mpf("0.05"),
                  mpf("0.05")
              ), mpf("0"), mpf("0"), mpf("0"), random.random() < 0.1),
        Skill("ATTACK SKILL #2", "Strong Attack Skill", "ATTACK",
              mpf("1e9") * random.randint(8, 14),
              DamageMultiplier(
                  random.randint(1, 3) * mpf("0.03"),
                  random.randint(1, 3) * mpf("0.03"),
                  mpf(9 + random.random() * 6),
                  mpf(2 * random.random()),
                  mpf(9 + random.random() * 6),
                  mpf(2 * random.random()),
                  random.randint(1, 3) * mpf("0.03"),
                  random.randint(1, 3) * mpf("0.03"),
                  mpf("1.5"),
                  mpf("0.75"),
                  mpf("0.1"),
                  mpf("0.1"),
                  mpf("0.1")
              ), mpf("0.1"), mpf("0.1"), mpf("0"), random.random() < 0.3),
        Skill("ATTACK SKILL #3", "Ultimate Attack Skill", "ATTACK",
              mpf("1e29") * random.randint(8, 14),
              DamageMultiplier(
                  random.randint(1, 3) * mpf("0.06"),
                  random.randint(1, 3) * mpf("0.06"),
                  mpf(27 + random.random() * 10),
                  mpf(6 * random.random()),
                  mpf(27 + random.random() * 10),
                  mpf(6 * random.random()),
                  random.randint(1, 3) * mpf("0.06"),
                  random.randint(1, 3) * mpf("0.06"),
                  mpf("4.5"),
                  mpf("2.25"),
                  mpf("0.3"),
                  mpf("0.3"),
                  mpf("0.3")
              ), mpf("0.25"), mpf("0.25"), mpf("0"), random.random() < 0.5),
        Skill("HEAL SKILL #1", "First Heal Skill", "HEAL",
              mpf("1e2") * random.randint(8, 14),
              DamageMultiplier(), mpf("0"), mpf("0"),
              mpf("1e2") * random.randint(18, 24), False),
        Skill("HEAL SKILL #2", "Better Heal Skill", "HEAL",
              mpf("1e9") * random.randint(8, 14),
              DamageMultiplier(), mpf("0"), mpf("0"),
              mpf("1e11") * random.randint(18, 24), False),
        Skill("HEAL SKILL #3", "Ultimate Heal Skill", "HEAL",
              mpf("1e29") * random.randint(8, 14),
              DamageMultiplier(), mpf("0"), mpf("0"),
              mpf("1e35") * random.randint(18, 24), False)
    ]

    awaken_bonus: AwakenBonus = AwakenBonus(mpf(random.randint(115, 135)), mpf(random.randint(115, 135)),
                                            mpf(random.randint(115, 135)), mpf(random.randint(115, 135)),
                                            mpf(random.randint(0, 15)),
                                            mpf(0.01 * random.randint(0, 15)), mpf(0.01 * random.randint(0, 15)),
                                            mpf(0.01 * random.randint(0, 15)), mpf(0.01 * random.randint(0, 15)))
    new_legendary_creature: LegendaryCreature = LegendaryCreature(name, main_element, rating, max_hp, max_magic_points,
                                                                  attack_power, defense, attack_speed, skills,
                                                                  awaken_bonus)
    return new_legendary_creature


def triangular(n: int) -> int:
    return int(n * (n - 1) / 2)


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(reduce(lambda x, y: mpf(x) * mpf(y) if is_number(x) and
                                                      is_number(y) else mpf(x) if is_number(x) and not is_number(
        y) else mpf(y) if is_number(y) and not is_number(x) else 1, a_list, 1))


def get_elemental_damage_multiplier(element1: str, element2: str) -> mpf:
    if element1 == "TERRA":
        return mpf("2") if element2 in ["ELECTRIC, DARK"] else mpf("0.5") if element2 in ["METAL", "WAR"] else mpf("1")
    elif element1 == "FLAME":
        return mpf("2") if element2 in ["NATURE", "ICE"] else mpf("0.5") if element2 in ["SEA", "WAR"] else mpf("1")
    elif element1 == "SEA":
        return mpf("2") if element2 in ["FLAME", "WAR"] else mpf("0.5") if element2 in ["NATURE", "ELECTRIC"] else \
            mpf("1")
    elif element1 == "NATURE":
        return mpf("2") if element2 in ["SEA", "LIGHT"] else mpf("0.5") if element2 in ["FLAME", "ICE"] else mpf("1")
    elif element1 == "ELECTRIC":
        return mpf("2") if element2 in ["SEA", "METAL"] else mpf("0.5") if element2 in ["TERRA", "LIGHT"] else mpf("1")
    elif element1 == "ICE":
        return mpf("2") if element2 in ["NATURE", "WAR"] else mpf("0.5") if element2 in ["FLAME", "METAL"] else mpf("1")
    elif element1 == "METAL":
        return mpf("2") if element2 in ["TERRA", "ICE"] else mpf("0.5") if element2 in ["ELECTRIC", "DARK"] else \
            mpf("1")
    elif element1 == "DARK":
        return mpf("2") if element2 in ["METAL", "LIGHT"] else mpf("0.5") if element2 == "TERRA" else mpf("1")
    elif element1 == "LIGHT":
        return mpf("2") if element2 in ["ELECTRIC", "DARK"] else mpf("0.5") if element2 == "NATURE" else mpf("1")
    elif element1 == "WAR":
        return mpf("2") if element2 in ["TERRA", "FLAME"] else mpf("0.5") if element2 in ["SEA", "ICE"] else mpf("1")
    elif element1 == "PURE":
        return mpf("2") if element2 == "LEGEND" else mpf("0.5") if element2 == "PRIMAL" else mpf("1")
    elif element1 == "LEGEND":
        return mpf("2") if element2 == "PRIMAL" else mpf("0.5") if element2 == "PURE" else mpf("1")
    elif element1 == "PRIMAL":
        return mpf("2") if element2 == "PURE" else mpf("0.5") if element2 == "LEGEND" else mpf("1")
    elif element1 == "WIND":
        return mpf("2") if element2 == "WIND" else mpf("1")
    else:
        return mpf("1")


def resistance_accuracy_rule(accuracy: mpf, resistance: mpf) -> mpf:
    if resistance - accuracy <= mpf("0.15"):
        return mpf("0.15")
    else:
        return resistance - accuracy


def load_game_data(file_name):
    # type: (str) -> Game
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (Game, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes to be used in the game.


###########################################
# BATTLE
###########################################


class Action:
    """
    This class contains attributes of an action which can be carried out during battles.
    """

    POSSIBLE_NAMES: list = ["NORMAL ATTACK", "NORMAL HEAL", "USE SKILL"]

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]

    def execute(self, user, target, skill_to_use=None):
        # type: (LegendaryCreature, LegendaryCreature, Skill or None) -> bool
        if self.name == "NORMAL ATTACK":
            if user == target:
                return False

            raw_damage: mpf = user.attack_power * (1 + user.attack_power_percentage_up / 100 -
                                                   user.attack_power_percentage_down / 100) * \
                              (1 + target.defense_percentage_up / 100 - target.defense_percentage_down / 100)
            damage_reduction_factor: mpf = mpf("1e8") / (mpf("1e8") + 3.5 * target.defense)
            damage: mpf = raw_damage * damage_reduction_factor
            target.curr_hp -= damage
            print(str(user.name) + " dealt " + str(damage) + " damage on " + str(target.name) + "!")
            return True

        elif self.name == "NORMAL HEAL":
            if user != target:
                return False

            heal_amount: mpf = 0.15 * user.max_hp
            user.curr_hp += heal_amount
            return True

        elif self.name == "USE SKILL":
            if isinstance(skill_to_use, Skill):
                if skill_to_use.skill_type == "ATTACK":
                    if user == target or user.corresponding_team == target.corresponding_team:
                        return False

                    # Deal damage on the target
                    damage: mpf = skill_to_use.damage_multiplier.calculate_raw_damage(user, target,
                                                                                      skill_to_use.does_ignore_enemies_defense)
                    target.curr_hp -= damage
                    print(str(user.name) + " dealt " + str(damage) + " damage on " + str(target.name) + "!")

                    # Reducing target's attack gauge
                    target.attack_gauge -= skill_to_use.enemies_attack_gauge_down
                    if target.attack_gauge <= target.MIN_ATTACK_GAUGE:
                        target.attack_gauge = target.MIN_ATTACK_GAUGE

                    print(str(target.name) + "'s attack gauge goes down by " +
                          str(skill_to_use.enemies_attack_gauge_down * 100) + "%!")
                else:
                    if user.corresponding_team != target.corresponding_team:
                        return False

                    # Increasing target' attack gauge and healing the target
                    target.attack_gauge += skill_to_use.allies_attack_gauge_up
                    target.curr_hp += skill_to_use.heal_amount_to_allies
                    if target.curr_hp >= target.max_hp:
                        target.curr_hp = target.max_hp

                    print(str(target.name) + " gained " + str(skill_to_use.allies_attack_gauge_up * 100) + "% attack "
                                                                                                           "gauge increase and " + str(
                        skill_to_use.heal_amount_to_allies) + " HP up!")

                return True
            return False

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Action
        return copy.deepcopy(self)


class Battle:
    """
    This class contains attributes of a battle in this game.
    """

    def __init__(self, team1, team2):
        # type: (Team, Team) -> None
        self.team1: Team = team1
        self.team2: Team = team2
        self.reward: Reward = Reward(mpf("10") ** sum(legendary_creature.rating for legendary_creature
                                                      in self.team2.get_legendary_creatures()),
                                     mpf("10") ** (sum(legendary_creature.rating for legendary_creature
                                                       in self.team2.get_legendary_creatures()) - 2),
                                     mpf("10") ** (sum(legendary_creature.rating for legendary_creature
                                                       in self.team2.get_legendary_creatures()) - 5),
                                     mpf("10") ** sum(legendary_creature.rating for legendary_creature
                                                      in self.team2.get_legendary_creatures()))
        self.whose_turn: LegendaryCreature or None = None
        self.winner: Team or None = None

    def get_someone_to_move(self):
        # type: () -> None
        """
        Getting a legendary creature to move and have its turn.
        :return: None
        """

        # Finding out which legendary creature moves
        full_attack_gauge_list: list = []  # initial value
        while len(full_attack_gauge_list) == 0:
            for legendary_creature in self.team1.get_legendary_creatures():
                if legendary_creature.attack_gauge >= legendary_creature.FULL_ATTACK_GAUGE and legendary_creature not \
                        in full_attack_gauge_list:
                    full_attack_gauge_list.append(legendary_creature)

            for legendary_creature in self.team2.get_legendary_creatures():
                if legendary_creature.attack_gauge >= legendary_creature.FULL_ATTACK_GAUGE and legendary_creature not \
                        in full_attack_gauge_list:
                    full_attack_gauge_list.append(legendary_creature)

            self.tick()

        max_attack_gauge: mpf = max(legendary_creature.attack_gauge for legendary_creature in full_attack_gauge_list)
        for legendary_creature in full_attack_gauge_list:
            if legendary_creature.attack_gauge == max_attack_gauge:
                self.whose_turn = legendary_creature

    def tick(self):
        # type: () -> None
        """
        The clock ticks when battles are carried out.
        :return: None
        """

        for legendary_creature in self.team1.get_legendary_creatures():
            legendary_creature.attack_gauge += legendary_creature.attack_speed * 0.07

        for legendary_creature in self.team2.get_legendary_creatures():
            legendary_creature.attack_gauge += legendary_creature.attack_speed * 0.07

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Battle
        return copy.deepcopy(self)


class Level:
    """
    This class contains attributes of a level for single player battles in this game.
    """

    LEVEL_NUMBER: int = 0

    def __init__(self, stages, reward):
        # type: (list, Reward) -> None
        Level.LEVEL_NUMBER += 1
        self.name: str = "LEVEL " + str(Level.LEVEL_NUMBER)
        self.__stages: list = stages
        self.is_cleared: bool = False
        self.clear_reward: Reward = reward

    def curr_stage(self, stage_number):
        # type: (int) -> Stage or None
        if stage_number < 0 or stage_number >= len(self.__stages):
            return None
        return self.__stages[stage_number]

    def next_stage(self, stage_number):
        # type: (int) -> Stage or None
        if stage_number < -1 or stage_number >= len(self.__stages) - 1:
            return None
        return self.__stages[stage_number + 1]

    def get_stages(self):
        # type: () -> list
        return self.__stages

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Level
        return copy.deepcopy(self)


class Stage:
    """
    This class contains attributes of a stage in a level in this game.
    """

    def __init__(self, enemies_list):
        # type: (list) -> None
        self.__enemies_list: list = enemies_list
        self.is_cleared: bool = False

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def get_enemies_list(self):
        # type: () -> list
        return self.__enemies_list

    def clone(self):
        # type: () -> Stage
        return copy.deepcopy(self)


###########################################
# BATTLE
###########################################


###########################################
# LEGENDARY CREATURE
###########################################


class AwakenBonus:
    """
    This class contains attributes of the bonus gained for awakening a legendary creature.
    """

    def __init__(self, max_hp_percentage_up, max_magic_points_percentage_up, attack_power_percentage_up,
                 defense_percentage_up, attack_speed_up, crit_rate_up, crit_damage_up, resistance_up,
                 accuracy_up):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.max_hp_percentage_up: mpf = max_hp_percentage_up
        self.max_magic_points_percentage_up: mpf = max_magic_points_percentage_up
        self.attack_power_percentage_up: mpf = attack_power_percentage_up
        self.defense_percentage_up: mpf = defense_percentage_up
        self.attack_speed_up: mpf = attack_speed_up
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_damage_up: mpf = crit_damage_up
        self.resistance_up: mpf = resistance_up
        self.accuracy_up: mpf = accuracy_up

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> AwakenBonus
        return copy.deepcopy(self)


class LegendaryCreature:
    """
    This class contains attributes of a legendary creature in this game.
    """

    MIN_RATING: int = 1
    MAX_RATING: int = 6
    MIN_CRIT_RATE: mpf = mpf("0.15")
    MIN_CRIT_DAMAGE: mpf = mpf("1.5")
    MIN_RESISTANCE: mpf = mpf("0.15")
    MAX_RESISTANCE: mpf = mpf("1")
    MIN_ACCURACY: mpf = mpf("0")
    MAX_ACCURACY: mpf = mpf("1")
    MIN_ATTACK_GAUGE: mpf = mpf("0")
    FULL_ATTACK_GAUGE: mpf = mpf("1")
    MIN_CRIT_RESIST: mpf = mpf("0")
    MAX_CRIT_RESIST: mpf = mpf("1")
    POTENTIAL_ELEMENTS: list = ["TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
                                "PURE", "LEGEND", "PRIMAL", "WIND", "BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM",
                                "SOUL"]

    def __init__(self, name, main_element, rating, max_hp, max_magic_points, attack_power, defense, attack_speed,
                 skills, awaken_bonus):
        # type: (str, str, int, mpf, mpf, mpf, mpf, mpf, list, AwakenBonus) -> None
        self.legendary_creature_id: str = str(uuid.uuid1())  # generating random legendary creature ID
        self.name: str = name
        self.__elements: list = [main_element if main_element in self.POTENTIAL_ELEMENTS else
                                 self.POTENTIAL_ELEMENTS[0]]  # a list of elements the legendary creature has. The main
        # (i.e., first) element will be the element considered as the defending element of this legendary creature.
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else self.MIN_RATING
        self.level: int = 1
        self.max_level: int = 10 * triangular(self.rating) if self.rating < self.MAX_RATING else float('inf')
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.exp_per_second: mpf = mpf("0")
        self.player_gold_per_second: mpf = mpf(int(max_hp / 500))
        self.curr_hp: mpf = max_hp
        self.max_hp: mpf = max_hp
        self.curr_magic_points: mpf = max_magic_points
        self.max_magic_points: mpf = max_magic_points
        self.attack_power: mpf = attack_power
        self.defense: mpf = defense
        self.attack_speed: mpf = attack_speed
        self.crit_rate: mpf = self.MIN_CRIT_RATE
        self.crit_damage: mpf = self.MIN_CRIT_DAMAGE
        self.resistance: mpf = self.MIN_RESISTANCE
        self.accuracy: mpf = self.MIN_ACCURACY
        self.crit_resist: mpf = self.MIN_CRIT_RESIST
        self.__skills: list = skills
        self.awaken_bonus: AwakenBonus = awaken_bonus
        self.__runes: dict = {}  # initial value
        self.has_awakened: bool = False
        self.attack_gauge: mpf = self.MIN_ATTACK_GAUGE
        self.placed_in_training_area: bool = False
        self.placed_in_habitat: bool = False
        self.corresponding_team: Team = Team()

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def awaken(self):
        # type: () -> bool
        if not self.has_awakened:
            self.name = "AWAKENED " + str(self.name)
            self.max_hp *= 1 + self.awaken_bonus.max_hp_percentage_up / 100
            self.max_magic_points *= 1 + self.awaken_bonus.max_magic_points_percentage_up / 100
            self.attack_power *= 1 + self.awaken_bonus.attack_power_percentage_up / 100
            self.defense *= 1 + self.awaken_bonus.defense_percentage_up / 100
            self.attack_speed += self.awaken_bonus.attack_speed_up
            self.crit_rate += self.awaken_bonus.crit_rate_up
            self.crit_damage += self.awaken_bonus.crit_damage_up
            self.resistance += self.awaken_bonus.resistance_up
            if self.resistance > self.MAX_RESISTANCE:
                self.resistance = self.MAX_RESISTANCE

            self.accuracy += self.awaken_bonus.accuracy_up
            if self.accuracy > self.MAX_ACCURACY:
                self.accuracy = self.MAX_ACCURACY

            self.restore()
            self.has_awakened = True
            return True
        return False

    def evolve(self):
        # type: () -> bool
        if self.level == self.max_level and self.rating < self.MAX_RATING and self.exp >= self.required_exp:
            self.rating += 1
            self.level = 1
            self.max_level = 10 * triangular(self.rating) if self.rating < self.MAX_RATING else float('inf')
            self.exp = mpf("0")
            self.required_exp = mpf("1e6")
            temp_runes: dict = self.__runes
            for slot_number in self.__runes.keys():
                self.remove_rune(slot_number)

            self.attack_power *= triangular(self.level) + 1
            self.max_hp *= triangular(self.level) + 1
            self.max_magic_points *= triangular(self.level) + 1
            self.defense *= triangular(self.level) + 1
            self.attack_speed += 3
            for rune in temp_runes.values():
                self.place_rune(rune)

            self.restore()
            return True
        return False

    def place_rune(self, rune):
        # type: (Rune) -> bool
        if rune.already_placed:
            return False

        if rune.slot_number in self.__runes.keys():
            self.remove_rune(rune.slot_number)

        self.__runes[rune.slot_number] = rune
        self.max_hp *= 1 + (rune.stat_increase.max_hp_percentage_up / 100)
        self.max_hp += rune.stat_increase.max_hp_up
        self.max_magic_points *= 1 + (rune.stat_increase.max_magic_points_percentage_up / 100)
        self.max_magic_points += rune.stat_increase.max_magic_points_up
        self.attack_power *= 1 + (rune.stat_increase.attack_percentage_up / 100)
        self.attack_power += rune.stat_increase.attack_up
        self.defense *= 1 + (rune.stat_increase.defense_percentage_up / 100)
        self.defense += rune.stat_increase.defense_up
        self.attack_speed += rune.stat_increase.attack_speed_up
        self.crit_rate += rune.stat_increase.crit_rate_up
        self.crit_damage += rune.stat_increase.crit_damage_up
        self.resistance += rune.stat_increase.resistance_up
        if self.resistance >= self.MAX_RESISTANCE:
            self.resistance = self.MAX_RESISTANCE

        self.accuracy += rune.stat_increase.accuracy_up
        if self.accuracy >= self.MAX_ACCURACY:
            self.accuracy = self.MAX_ACCURACY

        self.crit_resist += rune.stat_increase.crit_resist_up
        if self.crit_resist >= self.MAX_CRIT_RESIST:
            self.crit_resist = self.MAX_CRIT_RESIST

        self.restore()
        rune.already_placed = True
        return True

    def remove_rune(self, slot_number):
        # type: (int) -> bool
        if slot_number in self.__runes.keys():
            # Remove the rune at slot number 'slot_number'
            current_rune: Rune = self.__runes[slot_number]
            self.max_hp -= current_rune.stat_increase.max_hp_up
            self.max_hp /= 1 + (current_rune.stat_increase.max_hp_percentage_up / 100)
            self.max_magic_points -= current_rune.stat_increase.max_magic_points_up
            self.max_magic_points /= 1 + (current_rune.stat_increase.max_magic_points_percentage_up / 100)
            self.attack_power -= current_rune.stat_increase.attack_up
            self.attack_power /= 1 + (current_rune.stat_increase.attack_percentage_up / 100)
            self.defense -= current_rune.stat_increase.defense_up
            self.defense /= 1 + (current_rune.stat_increase.defense_percentage_up / 100)
            self.attack_speed -= current_rune.stat_increase.attack_speed_up
            self.crit_rate -= current_rune.stat_increase.crit_rate_up
            if self.crit_rate <= self.MIN_CRIT_RATE:
                self.crit_rate = self.MIN_CRIT_RATE

            self.crit_damage -= current_rune.stat_increase.crit_damage_up
            if self.crit_damage <= self.MIN_CRIT_DAMAGE:
                self.crit_damage = self.MIN_CRIT_DAMAGE

            self.resistance -= current_rune.stat_increase.resistance_up
            if self.resistance <= self.MIN_RESISTANCE:
                self.resistance = self.MIN_RESISTANCE

            self.accuracy -= current_rune.stat_increase.accuracy_up
            if self.accuracy <= self.MIN_ACCURACY:
                self.accuracy = self.MIN_ACCURACY

            self.crit_resist -= current_rune.stat_increase.crit_resist_up
            if self.crit_resist <= self.MIN_CRIT_RESIST:
                self.crit_resist = self.MIN_CRIT_RESIST

            self.restore()
            self.__runes.pop(current_rune.slot_number)
            current_rune.already_placed = False
            return True
        return False

    def level_up_rune(self, slot_number):
        # type: (int) -> bool
        if slot_number not in self.__runes.keys():
            return False

        current_rune: Rune = self.__runes[slot_number]
        self.remove_rune(slot_number)
        success: bool = current_rune.level_up()
        self.place_rune(current_rune)
        return success

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp and self.level < self.max_level:
            self.level += 1
            self.required_exp *= mpf("10") ** self.level
            temp_runes: dict = self.__runes
            for slot_number in self.__runes.keys():
                self.remove_rune(slot_number)

            self.attack_power *= triangular(self.level)
            self.max_hp *= triangular(self.level)
            self.player_gold_per_second *= triangular(self.level)
            self.max_magic_points *= triangular(self.level)
            self.defense *= triangular(self.level)
            self.attack_speed += 2
            for rune in temp_runes.values():
                self.place_rune(rune)

            self.restore()

    def restore(self):
        # type: () -> None
        self.curr_hp = self.max_hp
        self.curr_magic_points = self.max_magic_points

    def recover_magic_points(self):
        # type: () -> None
        self.curr_magic_points += self.max_magic_points / 12
        if self.curr_magic_points >= self.max_magic_points:
            self.curr_magic_points = self.max_magic_points

    def get_is_alive(self):
        # type: () -> bool
        return self.curr_hp > 0

    def get_elements(self):
        # type: () -> list
        return self.__elements

    def set_elements(self, elements):
        # type: (list) -> None
        self.__elements = elements

    def add_element(self, element):
        # type: (str) -> bool
        if element in self.__elements:
            return False
        self.__elements.append(element)
        return True

    def remove_element(self, element):
        # type: (str) -> bool
        if element in self.__elements:
            self.__elements.remove(element)
            return True
        return False

    def get_skills(self):
        # type: () -> list
        return self.__skills

    def get_runes(self):
        # type: () -> dict
        return self.__runes

    def have_turn(self, other, skill_to_use, action_name):
        # type: (LegendaryCreature, Skill or None, str) -> bool
        if action_name == "NORMAL ATTACK":
            self.normal_attack(other)
        elif action_name == "NORMAL HEAL":
            self.normal_heal(other)
        elif action_name == "USE SKILL" and isinstance(skill_to_use, Skill):
            self.use_skill(other, skill_to_use)
        else:
            return False

        return True

    def normal_attack(self, other):
        # type: (LegendaryCreature) -> None
        action: Action = Action("NORMAL ATTACK")
        action.execute(self, other)

    def normal_heal(self, other):
        # type: (LegendaryCreature) -> None
        action: Action = Action("NORMAL HEAL")
        action.execute(self, other)

    def use_skill(self, other, skill_to_use):
        # type: (LegendaryCreature, Skill) -> bool
        if skill_to_use not in self.__skills:
            return False

        if self.curr_magic_points < skill_to_use.magic_points_cost:
            return False

        action: Action = Action("USE SKILL")
        action.execute(self, other, skill_to_use)
        self.curr_magic_points -= skill_to_use.magic_points_cost
        return True

    def clone(self):
        # type: () -> LegendaryCreature
        return copy.deepcopy(self)


class Skill:
    """
    This class contains attributes of a skill legendary creatures have.
    """

    POTENTIAL_SKILL_TYPES: list = ["ATTACK", "HEAL"]

    def __init__(self, name, description, skill_type, magic_points_cost, damage_multiplier, allies_attack_gauge_up,
                 enemies_attack_gauge_down, heal_amount_to_allies, does_ignore_enemies_defense):
        # type: (str, str, str, mpf, DamageMultiplier, mpf, mpf, mpf, bool) -> None
        self.name: str = name
        self.description: str = description
        self.skill_type: str = skill_type if skill_type in self.POTENTIAL_SKILL_TYPES else self.POTENTIAL_SKILL_TYPES[0]
        self.magic_points_cost: mpf = magic_points_cost
        self.level: int = 1
        self.damage_multiplier: DamageMultiplier = damage_multiplier if self.skill_type == "ATTACK" else \
            DamageMultiplier()
        self.allies_attack_gauge_up: mpf = allies_attack_gauge_up
        self.enemies_attack_gauge_down: mpf = enemies_attack_gauge_down
        self.heal_amount_to_allies: mpf = heal_amount_to_allies if self.skill_type == "HEAL" else mpf("0")
        self.does_ignore_enemies_defense: bool = does_ignore_enemies_defense

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def level_up(self):
        # type: () -> None
        self.level += 1
        if self.skill_type == "HEAL":
            self.heal_amount_to_allies *= mpf("10") ** triangular(self.level)
        else:
            self.damage_multiplier.multiplier_to_self_max_hp *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_enemy_max_hp *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_self_attack_power *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_enemy_attack_power *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_self_defense *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_enemy_defense *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_self_max_magic_points *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_enemy_max_magic_points *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_self_attack_speed *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_enemy_attack_speed *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_self_current_hp_percentage *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_self_hp_percentage_loss *= mpf("1.25") * self.level
            self.damage_multiplier.multiplier_to_enemy_current_hp_percentage *= mpf("1.25") * self.level

    def clone(self):
        # type: () -> Skill
        return copy.deepcopy(self)


class DamageMultiplier:
    """
    This class contains attributes of the damage multiplier of a skill.
    """

    def __init__(self, multiplier_to_self_max_hp=mpf("0"), multiplier_to_enemy_max_hp=mpf("0"),
                 multiplier_to_self_attack_power=mpf("0"), multiplier_to_enemy_attack_power=mpf("0"),
                 multiplier_to_self_defense=mpf("0"), multiplier_to_enemy_defense=mpf("0"),
                 multiplier_to_self_max_magic_points=mpf("0"), multiplier_to_enemy_max_magic_points=mpf("0"),
                 multiplier_to_self_attack_speed=mpf("0"), multiplier_to_enemy_attack_speed=mpf("0"),
                 multiplier_to_self_current_hp_percentage=mpf("0"), multiplier_to_self_hp_percentage_loss=mpf("0"),
                 multiplier_to_enemy_current_hp_percentage=mpf("0")):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.multiplier_to_self_max_hp: mpf = multiplier_to_self_max_hp
        self.multiplier_to_enemy_max_hp: mpf = multiplier_to_enemy_max_hp
        self.multiplier_to_self_attack_power: mpf = multiplier_to_self_attack_power
        self.multiplier_to_enemy_attack_power: mpf = multiplier_to_enemy_attack_power
        self.multiplier_to_self_defense: mpf = multiplier_to_self_defense
        self.multiplier_to_enemy_defense: mpf = multiplier_to_enemy_defense
        self.multiplier_to_self_max_magic_points: mpf = multiplier_to_self_max_magic_points
        self.multiplier_to_enemy_max_magic_points: mpf = multiplier_to_enemy_max_magic_points
        self.multiplier_to_self_attack_speed: mpf = multiplier_to_self_attack_speed
        self.multiplier_to_enemy_attack_speed: mpf = multiplier_to_enemy_attack_speed
        self.multiplier_to_self_current_hp_percentage: mpf = multiplier_to_self_current_hp_percentage
        self.multiplier_to_self_hp_percentage_loss: mpf = multiplier_to_self_hp_percentage_loss
        self.multiplier_to_enemy_current_hp_percentage: mpf = multiplier_to_enemy_current_hp_percentage

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def calculate_raw_damage_without_enemy_defense(self, user, target):
        # type: (LegendaryCreature, LegendaryCreature) -> mpf
        self_current_hp_percentage: mpf = (user.curr_hp / user.max_hp) * 100
        self_hp_percentage_loss: mpf = 100 - self_current_hp_percentage
        target_current_hp_percentage: mpf = (target.curr_hp / target.max_hp) * 100
        return user.max_hp * self.multiplier_to_self_max_hp + target.max_hp * self.multiplier_to_enemy_max_hp + \
               user.attack_power * (self.multiplier_to_self_attack_speed * user.attack_speed +
                                    self.multiplier_to_self_attack_power) + target.attack_power * \
               (self.multiplier_to_enemy_attack_speed * target.attack_speed + self.multiplier_to_enemy_attack_power) + \
               user.defense * self.multiplier_to_self_defense + target.defense * self.multiplier_to_enemy_defense + \
               user.max_magic_points * self.multiplier_to_self_max_magic_points + \
               target.max_magic_points * self.multiplier_to_enemy_max_magic_points * \
               (1 + self_current_hp_percentage * self.multiplier_to_self_current_hp_percentage) * \
               (1 + self_hp_percentage_loss * self.multiplier_to_self_hp_percentage_loss) * \
               (1 + target_current_hp_percentage * self.multiplier_to_enemy_current_hp_percentage)

    def calculate_raw_damage(self, user, target, does_ignore_defense=False):
        # type: (LegendaryCreature, LegendaryCreature, bool) -> mpf
        damage_reduction_factor: mpf = mpf("1") if does_ignore_defense else mpf("1e8") / (mpf("1e8") +
                                                                                          3.5 * target.defense)
        raw_damage: mpf = self.calculate_raw_damage_without_enemy_defense(user, target)

        # Checking for damage multiplier by element
        damage_multiplier_by_element: mpf = mpf("0")  # initial value
        for element in user.get_elements():
            curr_multiplier: mpf = get_elemental_damage_multiplier(element, target.get_elements()[0])
            if curr_multiplier > damage_multiplier_by_element:
                damage_multiplier_by_element = curr_multiplier

        # Checking for critical hits
        crit_chance: mpf = user.crit_rate - target.crit_resist
        is_crit: bool = random.random() < crit_chance
        return raw_damage * damage_reduction_factor * damage_multiplier_by_element \
            if not is_crit else raw_damage * user.crit_damage * damage_reduction_factor * damage_multiplier_by_element

    def clone(self):
        # type: () -> DamageMultiplier
        return copy.deepcopy(self)


###########################################
# LEGENDARY CREATURE
###########################################


###########################################
# TEAM
###########################################


class Team:
    """
    This class contains attributes of a team brought to battles.
    """

    MAX_LEGENDARY_CREATURES: int = 5

    def __init__(self, legendary_creatures=None):
        # type: (list) -> None
        if legendary_creatures is None:
            legendary_creatures = []
        self.__legendary_creatures: list = legendary_creatures if len(legendary_creatures) <= \
                                                                  self.MAX_LEGENDARY_CREATURES else []

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def get_legendary_creatures(self):
        # type: () -> list
        return self.__legendary_creatures

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures) < self.MAX_LEGENDARY_CREATURES:
            self.__legendary_creatures.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures:
            self.__legendary_creatures.remove(legendary_creature)
            return True
        return False

    def recover_all(self):
        # type: () -> None
        for legendary_creature in self.get_legendary_creatures():
            legendary_creature.restore()

    def all_died(self):
        # type: () -> bool
        for legendary_creature in self.__legendary_creatures:
            if legendary_creature.get_is_alive():
                return False
        return True

    def clone(self):
        # type: () -> Team
        return copy.deepcopy(self)


###########################################
# TEAM
###########################################


###########################################
# ITEM
###########################################


class Item:
    """
    This class contains attributes of an item in this game.
    """

    def __init__(self, name, description, gold_cost, gem_cost):
        # type: (str, str, mpf, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.gold_cost: mpf = gold_cost
        self.gem_cost: mpf = gem_cost
        self.sell_gold_gain: mpf = gold_cost / 5
        self.sell_gem_gain: mpf = gem_cost / 5

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Item
        return copy.deepcopy(self)


class Rune(Item):
    """
    This class contains attributes of a rune used to strengthen legendary creatures.
    """

    MIN_SLOT_NUMBER: int = 1
    MAX_SLOT_NUMBER: int = 6
    MIN_RATING: int = 1
    MAX_RATING: int = 6

    def __init__(self, name, description, gold_cost, gem_cost, rating, slot_number, stat_increase):
        # type: (str, str, mpf, mpf, int, int, StatIncrease) -> None
        Item.__init__(self, name, description, gold_cost, gem_cost)
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else self.MIN_RATING
        self.slot_number: int = slot_number if self.MIN_SLOT_NUMBER <= slot_number <= self.MAX_SLOT_NUMBER else \
            self.MIN_SLOT_NUMBER
        self.stat_increase: StatIncrease = stat_increase
        self.level: int = 1
        self.level_up_gold_cost: mpf = gold_cost
        self.level_up_success_rate: mpf = mpf("1")
        self.already_placed: bool = False  # initial value

    def level_up(self):
        # type: () -> bool
        # Check whether levelling up is successful or not
        if random.random() > self.level_up_success_rate:
            return False

        # Increase the level of the rune
        self.level += 1

        # Update the cost and success rate of levelling up the rune
        self.level_up_gold_cost *= mpf("10") ** (self.level + self.rating)
        self.level_up_success_rate *= mpf("0.95")

        # Increase stat increase of the rune
        self.stat_increase.max_hp_up += mpf("10") ** (6 * self.rating + self.level)
        self.stat_increase.max_hp_percentage_up += self.rating
        self.stat_increase.max_magic_points_up += mpf("10") ** (6 * self.rating + self.level)
        self.stat_increase.max_magic_points_percentage_up += self.rating
        self.stat_increase.attack_up += mpf("10") ** (5 * self.rating + 1)
        self.stat_increase.attack_percentage_up += self.rating
        self.stat_increase.defense_up += mpf("10") ** (5 * self.rating + 1)
        self.stat_increase.defense_percentage_up += self.rating
        self.stat_increase.attack_speed_up += 2 * self.rating
        self.stat_increase.crit_rate_up += 0.01 * self.rating
        self.stat_increase.crit_damage_up += 0.05 * self.rating
        self.stat_increase.resistance_up += 0.01 * self.rating
        self.stat_increase.accuracy_up += 0.01 * self.rating
        self.stat_increase.crit_resist_up += 0.01 * self.rating
        return True


class StatIncrease:
    """
    This class contains attributes of increase in stats in a rune.
    """

    def __init__(self, max_hp_up=mpf("0"), max_hp_percentage_up=mpf("0"), max_magic_points_up=mpf("0"),
                 max_magic_points_percentage_up=mpf("0"), attack_up=mpf("0"), attack_percentage_up=mpf("0"),
                 defense_up=mpf("0"), defense_percentage_up=mpf("0"), attack_speed_up=mpf("0"), crit_rate_up=mpf("0"),
                 crit_damage_up=mpf("0"), resistance_up=mpf("0"), accuracy_up=mpf("0"), crit_resist_up=mpf("0")):
        # type: (mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf, mpf) -> None
        self.max_hp_up: mpf = max_hp_up
        self.max_hp_percentage_up: mpf = max_hp_percentage_up
        self.max_magic_points_up: mpf = max_magic_points_up
        self.max_magic_points_percentage_up: mpf = max_magic_points_percentage_up
        self.attack_up: mpf = attack_up
        self.attack_percentage_up: mpf = attack_percentage_up
        self.defense_up: mpf = defense_up
        self.defense_percentage_up: mpf = defense_percentage_up
        self.attack_speed_up: mpf = attack_speed_up
        self.crit_rate_up: mpf = crit_rate_up
        self.crit_damage_up: mpf = crit_damage_up
        self.resistance_up: mpf = resistance_up
        self.accuracy_up: mpf = accuracy_up
        self.crit_resist_up: mpf = crit_resist_up

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> StatIncrease
        return copy.deepcopy(self)


class AwakenShard(Item):
    """
    This class contains attributes of a shard used to awaken a legendary creature.
    """

    def __init__(self, gold_cost, gem_cost, legendary_creature_element):
        # type: (mpf, mpf, str) -> None
        Item.__init__(self, str(legendary_creature_element).upper() + " AWAKEN SHARD", "A shard used to awaken a " +
                      str(legendary_creature_element) + " legendary creature.", gold_cost, gem_cost)
        self.legendary_creature_element: str = legendary_creature_element  # the element of the legendary creature
        # to be awakened


class Egg(Item):
    """
    This class contains attributes of an egg which can be hatched to produce legendary creatures.
    """

    POTENTIAL_ELEMENTS: list = ["TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
                                "PURE", "LEGEND", "PRIMAL", "WIND", "BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM",
                                "SOUL"]

    def __init__(self, gold_cost, gem_cost, element):
        # type: (mpf, mpf, str) -> None
        Item.__init__(self, str(element if element in self.POTENTIAL_ELEMENTS else self.POTENTIAL_ELEMENTS[0]).upper() +
                      " EGG", "An egg which can be hatched for legendary creatures to come out.",
                      gold_cost, gem_cost)
        self.hatch_time: datetime or None = None  # initial value
        self.element: str = element if element in self.POTENTIAL_ELEMENTS else self.POTENTIAL_ELEMENTS[0]
        self.already_placed: bool = False


class LevelUpShard(Item):
    """
    This class contains attributes of a level up shard to immediately level up a legendary creature.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Item.__init__(self, "LEVEL UP SHARD", "A shard used to immediately increase the level of a legendary creature.",
                      gold_cost, gem_cost)


class SkillLevelUpShard(Item):
    """
    This class contains attributes of a skill level up shard to level up a legendary creatures's skill.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Item.__init__(self, "SKILL LEVEL UP SHARD", "A shard used to immediately increase the level of a "
                                                    "legendary creature's skill.", gold_cost, gem_cost)


class EXPShard(Item):
    """
    This class contains attributes of an EXP shard to increase the EXP of a legendary creature.
    """

    def __init__(self, gold_cost, gem_cost, exp_granted):
        # type: (mpf, mpf, mpf) -> None
        Item.__init__(self, "EXP SHARD", "A shard used to increase the EXP of a legendary creature.", gold_cost,
                      gem_cost)
        self.exp_granted: mpf = exp_granted


###########################################
# ITEM
###########################################


###########################################
# BUILDING
###########################################


class CreatureWorld:
    """
    This class contains attributes of a creature world.
    """

    def __init__(self):
        # type: () -> None
        self.__sections: list = [Section()]  # initial value
        self.section_build_gold_cost: mpf = mpf("1e8")

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def add_section(self):
        # type: () -> None
        self.section_build_gold_cost *= mpf("10") ** (triangular(len(self.__sections)))
        self.__sections.append(Section())

    def get_sections(self):
        # type: () -> list
        return self.__sections

    def clone(self):
        # type: () -> CreatureWorld
        return copy.deepcopy(self)


class Section:
    """
    This class contains attributes of a section in a creature world.
    """

    SECTION_WIDTH: int = 10
    SECTION_HEIGHT: int = 10

    def __init__(self):
        # type: () -> None
        self.__tiles: list = []  # initial value
        for i in range(self.SECTION_WIDTH):
            new = []  # initial value
            for k in range(self.SECTION_HEIGHT):
                # Ensuring that obstacles are not placed at the edges of the section
                place_obstacle: bool = random.random() <= 0.3
                if place_obstacle and not self.is_edge(i, k):
                    new.append(SectionTile(Obstacle()))
                else:
                    new.append(SectionTile())

            self.__tiles.append(new)

    def is_edge(self, x, y):
        # type: (int, int) -> bool
        return (x == 0 and y == 0) or (x == 0 and y == self.SECTION_HEIGHT - 1) or \
               (x == self.SECTION_WIDTH - 1 and y == 0) or (x == self.SECTION_WIDTH - 1
                                                            and y == self.SECTION_HEIGHT - 1)

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def get_tile_at(self, x, y):
        # type: (int, int) -> SectionTile or None
        if x < 0 or x >= self.SECTION_WIDTH or y < 0 or y >= self.SECTION_HEIGHT:
            return None
        return self.__tiles[y][x]

    def __str__(self):
        # type: () -> str
        return str(tabulate(self.__tiles, headers='firstrow', tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> Section
        return copy.deepcopy(self)


class SectionTile:
    """
    This class contains attributes of a tile in a section.
    """

    def __init__(self, building=None):
        # type: (Building or None) -> None
        self.building: Building or None = building

    def __str__(self):
        # type: () -> str
        if isinstance(self.building, Building):
            return "SectionTile(" + str(self.building.name) + ")"
        return "SectionTile(GRASS)"

    def clone(self):
        # type: () -> SectionTile
        return copy.deepcopy(self)


class Building:
    """
    This class contains attributes of a building which can be built on a section tile.
    """

    def __init__(self, name, description, gold_cost, gem_cost):
        # type: (str, str, mpf, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.gold_cost: mpf = gold_cost
        self.gem_cost: mpf = gem_cost
        self.sell_gold_gain: mpf = gold_cost / 5
        self.sell_gem_gain: mpf = gem_cost / 5
        self.upgrade_gold_cost: mpf = gold_cost
        self.upgrade_gem_cost: mpf = gem_cost
        self.level: int = 1

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def level_up(self):
        # type: () -> None
        pass

    def clone(self):
        # type: () -> Building
        return copy.deepcopy(self)


class Habitat(Building):
    """
    This class contains attributes of a habitat where legendary creatures live.
    """

    POTENTIAL_ELEMENTS: list = ["TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
                                "PURE", "LEGEND", "PRIMAL", "WIND", "BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM",
                                "SOUL"]
    MAX_LEGENDARY_CREATURES: int = 10

    def __init__(self, gold_cost, gem_cost, element, player_gold_per_second_increase):
        # type: (mpf, mpf, str, mpf) -> None
        Building.__init__(self, str(element if element in self.POTENTIAL_ELEMENTS else
                                    self.POTENTIAL_ELEMENTS[0]).upper() +
                          " HABITAT", "A habitat for " + str(element) +
                          " legendary creatures.", gold_cost, gem_cost)
        self.element: str = element if element in self.POTENTIAL_ELEMENTS else self.POTENTIAL_ELEMENTS[0]
        self.player_gold_per_second_increase: mpf = player_gold_per_second_increase
        self.__legendary_creatures_placed: list = []  # initial value

    def get_legendary_creatures_placed(self):
        # type: () -> list
        return self.__legendary_creatures_placed

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures_placed) < self.MAX_LEGENDARY_CREATURES:
            self.__legendary_creatures_placed.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures_placed:
            self.__legendary_creatures_placed.remove(legendary_creature)
            return True
        return False

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.player_gold_per_second_increase *= mpf("10") ** (self.level / 2)
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class Obstacle(Building):
    """
    This class contains attributes of an obstacle to be removed by the player.
    """

    def __init__(self):
        # type: () -> None
        Building.__init__(self, "OBSTACLE", "A removable obstacle.", mpf("0"), mpf("0"))
        self.remove_gold_gain: mpf = mpf("10") ** random.randint(5, 10)
        self.remove_gem_gain: mpf = mpf("10") ** random.randint(2, 6)


class FusionCenter(Building):
    """
    This class contains attributes of a fusion center used to fuse legendary creatures.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "FUSION CENTER", "A building used to fuse legendary creatures into a stronger one.",
                          gold_cost, gem_cost)
        self.upgrade_gold_cost = mpf("0")
        self.upgrade_gem_cost = mpf("0")


class TrainingArea(Building):
    """
    This class contains attributes of a training area used to automatically increase the EXP of legendary creatures.
    """

    MAX_LEGENDARY_CREATURES: int = 5

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "TRAINING AREA", "A training area to increase the EXP of legendary creatures.",
                          gold_cost, gem_cost)
        self.legendary_creature_exp_per_second: mpf = self.gold_cost / mpf("1e5")
        self.__legendary_creatures_placed: list = []  # initial value

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.legendary_creature_exp_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level

    def get_legendary_creatures_placed(self):
        # type: () -> list
        return self.__legendary_creatures_placed

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures_placed) < self.MAX_LEGENDARY_CREATURES:
            self.__legendary_creatures_placed.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures_placed:
            self.__legendary_creatures_placed.remove(legendary_creature)
            return True
        return False


class Tree(Building):
    """
    This class contains attributes of a tree used for decoration.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "TREE", "A tree.", gold_cost, gem_cost)


class Hatchery(Building):
    """
    This class contains attributes of a hatchery used to hatch legendary creatures.
    """

    MAX_EGGS: int = 5

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "HATCHERY", "A hatchery to hatch eggs and gain new legendary creatures.",
                          gold_cost, gem_cost)
        self.__eggs_placed: list = []  # initial value
        self.upgrade_gold_cost = mpf("0")
        self.upgrade_gem_cost = mpf("0")

    def get_eggs_placed(self):
        # type: () -> list
        return self.__eggs_placed

    def add_egg(self, egg):
        # type: (Egg) -> bool
        if len(self.__eggs_placed) < self.MAX_EGGS:
            self.__eggs_placed.append(egg)
            return True
        return False

    def remove_egg(self, egg):
        # type: (Egg) -> bool
        if egg in self.__eggs_placed:
            self.__eggs_placed.remove(egg)
            return True
        return False


class FoodFarm(Building):
    """
    This class contains attributes of a food farm producing food.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "FOOD FARM", "A farm producing food.", gold_cost, gem_cost)
        self.food_per_second: mpf = self.gold_cost / mpf("1e5")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.food_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class GoldMine(Building):
    """
    This class contains attributes of a gold mine producing gold.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "GOLD MINE", "A mine producing gold.", gold_cost, gem_cost)
        self.gold_per_second: mpf = self.gold_cost / mpf("1e5")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.gold_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class GemMine(Building):
    """
    This class contains attributes of a gem mine producing gems.
    """

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "GEM MINE", "A mine producing gems.", gold_cost, gem_cost)
        self.gem_per_second: mpf = self.gold_cost / mpf("1e7")

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.gem_per_second *= mpf("10") ** self.level
        self.upgrade_gold_cost *= mpf("10") ** self.level
        self.upgrade_gem_cost *= mpf("10") ** self.level


class PowerUpCircle(Building):
    """
    This class contains attributes of a power-up circle used to power-up and evolve legendary creatures.
    """

    MAX_MATERIAL_LEGENDARY_CREATURES: int = 5

    def __init__(self, gold_cost, gem_cost):
        # type: (mpf, mpf) -> None
        Building.__init__(self, "POWER UP CIRCLE", "A building used to power up and evolve legendary creatures.",
                          gold_cost, gem_cost)
        self.legendary_creature_to_power_up: LegendaryCreature or None = None
        self.__material_legendary_creatures: list = []  # initial value
        self.upgrade_gold_cost = mpf("0")
        self.upgrade_gem_cost = mpf("0")

    def execute_power_up(self):
        # type: () -> LegendaryCreature or None
        if isinstance(self.legendary_creature_to_power_up, LegendaryCreature):
            curr_legendary_creature: LegendaryCreature = self.legendary_creature_to_power_up
            for legendary_creature in self.__material_legendary_creatures:
                curr_legendary_creature.exp += legendary_creature.rating * legendary_creature.exp
                curr_legendary_creature.level_up()

            self.deselect_legendary_creature_to_power_up()
            self.set_material_legendary_creatures([])
            return curr_legendary_creature
        return None

    def execute_evolution(self):
        # type: () -> LegendaryCreature or None
        if isinstance(self.legendary_creature_to_power_up, LegendaryCreature):
            curr_legendary_creature: LegendaryCreature = self.legendary_creature_to_power_up

            # Evolve the legendary creature if there are sufficient material legendary creatures of the
            # same or higher rating as the legendary creature to be evolved
            num_materials: int = sum(1 for legendary_creature in self.__material_legendary_creatures if
                                     legendary_creature.rating >= curr_legendary_creature.rating)
            if len(self.__material_legendary_creatures) == curr_legendary_creature.rating - 1 and \
                    num_materials == curr_legendary_creature.rating - 1:
                curr_legendary_creature.evolve()

            self.deselect_legendary_creature_to_power_up()
            self.set_material_legendary_creatures([])
            return curr_legendary_creature
        return None

    def get_material_legendary_creatures(self):
        # type: () -> list
        return self.__material_legendary_creatures

    def set_material_legendary_creatures(self, material_legendary_creatures):
        # type: (list) -> None
        self.__material_legendary_creatures = material_legendary_creatures

    def select_legendary_creature_to_power_up(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if self.legendary_creature_to_power_up is None:
            self.legendary_creature_to_power_up = legendary_creature
            return True
        return False

    def deselect_legendary_creature_to_power_up(self):
        # type: () -> bool
        if isinstance(self.legendary_creature_to_power_up, LegendaryCreature):
            self.legendary_creature_to_power_up = None
            return True
        return False

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__material_legendary_creatures) < self.MAX_MATERIAL_LEGENDARY_CREATURES:
            self.__material_legendary_creatures.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__material_legendary_creatures:
            self.__material_legendary_creatures.remove(legendary_creature)
            return True
        return False


###########################################
# BUILDING
###########################################


###########################################
# GENERAL
###########################################


class ItemShop:
    """
    This class contains attributes of an item shop to buy items.
    """

    def __init__(self, items_sold):
        # type: (list) -> None
        self.name: str = "ITEM SHOP"
        self.__items_sold: list = items_sold

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def get_items_sold(self):
        # type: () -> list
        return self.__items_sold

    def clone(self):
        # type: () -> ItemShop
        return copy.deepcopy(self)


class BuildingShop:
    """
    This class contains attributes of a building shop to buy buildings.
    """

    def __init__(self, buildings_sold):
        # type: (list) -> None
        self.name: str = "BUILDING SHOP"
        self.__buildings_sold: list = buildings_sold

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def get_buildings_sold(self):
        # type: () -> list
        return self.__buildings_sold

    def clone(self):
        # type: () -> BuildingShop
        return copy.deepcopy(self)


class Player:
    """
    This class contains attributes of the player in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.player_id: str = str(uuid.uuid1())
        self.name: str = name
        self.level: int = 1
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.exp_per_second: mpf = mpf("0")
        self.gold: mpf = mpf("5e6")
        self.gold_per_second: mpf = mpf("0")
        self.gems: mpf = mpf("100")
        self.gems_per_second: mpf = mpf("0")
        self.food: mpf = mpf("0")
        self.food_per_second: mpf = mpf("0")
        self.battle_team: Team = Team()
        self.item_inventory: ItemInventory = ItemInventory()
        self.legendary_creature_inventory: LegendaryCreatureInventory = LegendaryCreatureInventory()
        self.creature_world: CreatureWorld = CreatureWorld()
        self.__unlocked_levels: list = []  # initial value
        self.add_unlocked_level()  # ensuring that the player has unlocked at least one level

    def place_egg_in_hatchery(self, egg, hatchery):
        # type: (Egg, Hatchery) -> bool
        if egg not in self.item_inventory.get_items():
            return False

        hatchery_exists: bool = False
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if curr_tile.building == hatchery:
                        hatchery_exists = True
                        break

        if not hatchery_exists:
            return False

        if hatchery.add_egg(egg):
            # Make the egg hatch in 5 minutes
            egg.hatch_time = datetime.now() + timedelta(minutes=5)
            egg.already_placed = True
            return True
        return False

    def hatch_eggs_in_hatcheries(self):
        # type: () -> None
        """
        This function automatically hatches all eggs in the hatcheries
        :return: None
        """
        hatcheries: list = []  # initial value
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if isinstance(curr_tile.building, Hatchery):
                        hatcheries.append(curr_tile.building)

        for hatchery in hatcheries:
            assert isinstance(hatchery, Hatchery), "Not a hatchery! Invalid instance in 'hatcheries' list!"
            for egg in hatchery.get_eggs_placed():
                if egg.hatch_time is not None:
                    if datetime.now() >= egg.hatch_time:
                        # Initialise a random legendary creature
                        hatchery.remove_egg(egg)
                        self.remove_item_from_inventory(egg)
                        new_legendary_creature: LegendaryCreature = generate_random_legendary_creature(egg.element)
                        self.add_legendary_creature(new_legendary_creature)

    def claim_reward(self, reward):
        # type: (Reward) -> None
        self.exp += reward.player_reward_exp
        self.level_up()
        self.gold += reward.player_reward_gold
        self.gems += reward.player_reward_gems
        for legendary_creature in self.battle_team.get_legendary_creatures():
            legendary_creature.exp += reward.legendary_creature_reward_exp
            legendary_creature.level_up()

        self.battle_team.recover_all()
        for item in reward.get_player_reward_items():
            self.add_item_to_inventory(item)

    def feed_legendary_creature(self, legendary_creature, food):
        # type: (LegendaryCreature, mpf) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        if food > self.food:
            return False

        legendary_creature.exp += food
        legendary_creature.level_up()
        return True

    def fuse_legendary_creatures(self, legendary_creature1, legendary_creature2, fusion_center):
        # type: (LegendaryCreature, LegendaryCreature, FusionCenter) -> bool
        if legendary_creature1 not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature2 not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        if legendary_creature1 in self.battle_team.get_legendary_creatures() or \
                legendary_creature2 in self.battle_team.get_legendary_creatures():
            return False

        if legendary_creature1.placed_in_training_area or legendary_creature1.placed_in_habitat or \
                legendary_creature2.placed_in_training_area or legendary_creature2.placed_in_habitat:
            return False

        fusion_center_exists: bool = False
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if curr_tile.building == fusion_center:
                        fusion_center_exists = True
                        break

        if not fusion_center_exists:
            return False

        # Fuse both legendary creatures into a new one
        name: str = generate_random_name()
        main_element: str = legendary_creature1.get_elements()[0]
        elements: list = [element for element in legendary_creature1.get_elements()] + \
                         [element for element in legendary_creature2.get_elements()]
        rating: int = 1
        max_hp: mpf = legendary_creature1.max_hp + legendary_creature2.max_hp
        max_magic_points: mpf = legendary_creature1.max_magic_points + legendary_creature2.max_magic_points
        attack_power: mpf = legendary_creature1.attack_power + legendary_creature2.attack_power
        defense: mpf = legendary_creature1.defense + legendary_creature2.defense
        attack_speed: mpf = max(legendary_creature1.attack_speed, legendary_creature2.attack_speed)
        skills: list = [skill for skill in legendary_creature1.get_skills()] + \
                       [skill for skill in legendary_creature2.get_skills()]
        awaken_bonus: AwakenBonus = legendary_creature1.awaken_bonus
        new_legendary_creature: LegendaryCreature = LegendaryCreature(name, main_element, rating, max_hp,
                                                                      max_magic_points, attack_power, defense,
                                                                      attack_speed, skills, awaken_bonus)
        new_legendary_creature.set_elements(elements)
        self.remove_legendary_creature(legendary_creature1)
        self.remove_legendary_creature(legendary_creature2)
        self.add_legendary_creature(new_legendary_creature)
        return True

    def give_item_to_legendary_creature(self, item, legendary_creature):
        # type: (Item, LegendaryCreature) -> bool
        if item not in self.item_inventory.get_items():
            return False

        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        if isinstance(item, EXPShard):
            legendary_creature.exp += item.exp_granted
            legendary_creature.level_up()
            self.remove_item_from_inventory(item)
            return True
        elif isinstance(item, LevelUpShard):
            legendary_creature.exp = legendary_creature.required_exp
            legendary_creature.level_up()
            self.remove_item_from_inventory(item)
            return True
        elif isinstance(item, SkillLevelUpShard):
            skill_index: int = random.randint(0, len(legendary_creature.get_skills()) - 1)
            curr_skill: Skill = legendary_creature.get_skills()[skill_index]
            curr_skill.level_up()
            self.remove_item_from_inventory(item)
            return True
        elif isinstance(item, AwakenShard):
            if item.legendary_creature_element in legendary_creature.get_elements():
                legendary_creature.awaken()
                self.remove_item_from_inventory(item)
                return True
            return False
        return False

    def power_up_legendary_creature(self, legendary_creature_to_power_up, material_legendary_creatures,
                                    power_up_circle):
        # type: (LegendaryCreature, list, PowerUpCircle) -> bool
        if len(material_legendary_creatures) < 0 or len(material_legendary_creatures) > \
                power_up_circle.MAX_MATERIAL_LEGENDARY_CREATURES:
            return False

        if legendary_creature_to_power_up not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        power_up_circle_exists: bool = False
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if curr_tile.building == power_up_circle:
                        power_up_circle_exists = True
                        break

        if not power_up_circle_exists:
            return False

        power_up_circle.deselect_legendary_creature_to_power_up()
        power_up_circle.select_legendary_creature_to_power_up(legendary_creature_to_power_up)
        power_up_circle.set_material_legendary_creatures(material_legendary_creatures)
        legendary_creature_to_power_up = power_up_circle.execute_power_up()
        assert isinstance(legendary_creature_to_power_up, LegendaryCreature), "Legendary creature power-up failed!"
        for legendary_creature in material_legendary_creatures:
            self.remove_legendary_creature(legendary_creature)

        return True

    def evolve_legendary_creature(self, legendary_creature_to_evolve, material_legendary_creatures,
                                  power_up_circle):
        # type: (LegendaryCreature, list, PowerUpCircle) -> bool
        if len(material_legendary_creatures) < 0 or len(material_legendary_creatures) > \
                power_up_circle.MAX_MATERIAL_LEGENDARY_CREATURES:
            return False

        if legendary_creature_to_evolve not in self.legendary_creature_inventory.get_legendary_creatures():
            return False

        power_up_circle_exists: bool = False
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if curr_tile.building == power_up_circle:
                        power_up_circle_exists = True
                        break

        if not power_up_circle_exists:
            return False

        power_up_circle.deselect_legendary_creature_to_power_up()
        power_up_circle.select_legendary_creature_to_power_up(legendary_creature_to_evolve)
        power_up_circle.set_material_legendary_creatures(material_legendary_creatures)
        legendary_creature_to_evolve = power_up_circle.execute_evolution()
        assert isinstance(legendary_creature_to_evolve, LegendaryCreature), "Legendary creature evolution failed!"
        for legendary_creature in material_legendary_creatures:
            self.remove_legendary_creature(legendary_creature)

        return True

    def add_legendary_creature_to_habitat(self, legendary_creature, habitat):
        # type: (LegendaryCreature, Habitat) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_training_area:
            return False

        habitat_exists: bool = False
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if curr_tile.building == habitat:
                        habitat_exists = True
                        break

        if not habitat_exists:
            return False

        if habitat.add_legendary_creature(legendary_creature) and habitat.element in legendary_creature.get_elements():
            legendary_creature.player_gold_per_second += habitat.player_gold_per_second_increase
            self.gold_per_second += habitat.player_gold_per_second_increase
            legendary_creature.placed_in_habitat = True
            return True
        return False

    def remove_legendary_creature_from_habitat(self, legendary_creature, habitat):
        # type: (LegendaryCreature, Habitat) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_training_area:
            return False

        habitat_exists: bool = False
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if curr_tile.building == habitat:
                        habitat_exists = True
                        break

        if not habitat_exists:
            return False

        if habitat.remove_legendary_creature(legendary_creature):
            legendary_creature.player_gold_per_second -= habitat.player_gold_per_second_increase
            self.gold_per_second -= habitat.player_gold_per_second_increase
            legendary_creature.placed_in_habitat = False
            return True
        return False

    def add_legendary_creature_to_training_area(self, legendary_creature, training_area):
        # type: (LegendaryCreature, TrainingArea) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_habitat:
            return False

        training_area_exists: bool = False
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if curr_tile.building == training_area:
                        training_area_exists = True
                        break

        if not training_area_exists:
            return False

        if training_area.add_legendary_creature(legendary_creature):
            legendary_creature.exp_per_second += training_area.legendary_creature_exp_per_second
            legendary_creature.placed_in_training_area = True
            return True
        return False

    def remove_legendary_creature_from_training_area(self, legendary_creature, training_area):
        # type: (LegendaryCreature, TrainingArea) -> bool
        if legendary_creature not in self.legendary_creature_inventory.get_legendary_creatures() or \
                legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_habitat:
            return False

        training_area_exists: bool = False
        for section in self.creature_world.get_sections():
            for y in range(section.SECTION_HEIGHT):
                for x in range(section.SECTION_WIDTH):
                    curr_tile: SectionTile = section.get_tile_at(x, y)
                    if curr_tile.building == training_area:
                        training_area_exists = True
                        break

        if not training_area_exists:
            return False

        if training_area.remove_legendary_creature(legendary_creature):
            legendary_creature.exp_per_second -= training_area.legendary_creature_exp_per_second
            legendary_creature.placed_in_training_area = False
            return True
        return False

    def add_section_to_creature_world(self):
        # type: () -> bool
        if self.gold >= self.creature_world.section_build_gold_cost:
            self.gold -= self.creature_world.section_build_gold_cost
            self.creature_world.add_section()
            return True
        return False

    def level_up_building_at_section_tile(self, section_index, tile_x, tile_y):
        # type: (int, int, int) -> bool
        if section_index < 0 or section_index >= len(self.creature_world.get_sections()):
            return False

        corresponding_section: Section = self.creature_world.get_sections()[section_index]
        if isinstance(corresponding_section.get_tile_at(tile_x, tile_y), SectionTile):
            curr_tile: SectionTile = corresponding_section.get_tile_at(tile_x, tile_y)
            if isinstance(curr_tile.building, Building):
                curr_building: Building = curr_tile.building
                if self.gold < curr_building.upgrade_gold_cost or self.gems < curr_building.upgrade_gem_cost:
                    return False

                self.gold -= curr_building.upgrade_gold_cost
                self.gems -= curr_building.upgrade_gem_cost

                if isinstance(curr_building, FoodFarm):
                    initial_food_per_second: mpf = curr_building.food_per_second
                    curr_building.level_up()
                    self.food_per_second += (curr_building.food_per_second - initial_food_per_second)
                elif isinstance(curr_building, GoldMine):
                    initial_gold_per_second: mpf = curr_building.gold_per_second
                    curr_building.level_up()
                    self.gold_per_second += (curr_building.gold_per_second - initial_gold_per_second)
                elif isinstance(curr_building, GemMine):
                    initial_gems_per_second: mpf = curr_building.gem_per_second
                    curr_building.level_up()
                    self.gems_per_second += (curr_building.gem_per_second - initial_gems_per_second)
                elif isinstance(curr_building, Habitat):
                    initial_gold_per_second: mpf = curr_building.player_gold_per_second_increase
                    curr_building.level_up()
                    for legendary_creature in curr_building.get_legendary_creatures_placed():
                        legendary_creature.player_gold_per_second += (curr_building.player_gold_per_second_increase -
                                                                      initial_gold_per_second)
                        self.gold_per_second += (curr_building.player_gold_per_second_increase -
                                                 initial_gold_per_second)

                else:
                    curr_building.level_up()
                return True

            return False
        return False

    def build_at_section_tile(self, section_index, tile_x, tile_y, building):
        # type: (int, int, int, Building) -> bool
        if section_index < 0 or section_index >= len(self.creature_world.get_sections()):
            return False

        corresponding_section: Section = self.creature_world.get_sections()[section_index]
        if isinstance(corresponding_section.get_tile_at(tile_x, tile_y), SectionTile):
            curr_tile: SectionTile = corresponding_section.get_tile_at(tile_x, tile_y)
            if curr_tile.building is not None:
                return False

            if self.gold < building.gold_cost or self.gems < building.gem_cost:
                return False

            self.gold -= building.gold_cost
            self.gems -= building.gem_cost

            if isinstance(building, FoodFarm):
                self.food_per_second += building.food_per_second
            elif isinstance(building, GoldMine):
                self.gold_per_second += building.gold_per_second
            elif isinstance(building, GemMine):
                self.gems_per_second += building.gem_per_second
            elif isinstance(building, Obstacle):
                # Cannot build obstacle
                return False

            curr_tile.building = building
            return True
        return False

    def remove_building_from_section_tile(self, section_index, tile_x, tile_y):
        # type: (int, int, int) -> bool
        if section_index < 0 or section_index >= len(self.creature_world.get_sections()):
            return False

        corresponding_section: Section = self.creature_world.get_sections()[section_index]
        if isinstance(corresponding_section.get_tile_at(tile_x, tile_y), SectionTile):
            curr_tile: SectionTile = corresponding_section.get_tile_at(tile_x, tile_y)
            if isinstance(curr_tile.building, Building):
                curr_building: Building = curr_tile.building
                self.gold += curr_building.sell_gold_gain
                self.gems += curr_building.sell_gem_gain

                if isinstance(curr_building, FoodFarm):
                    self.food_per_second -= curr_building.food_per_second
                elif isinstance(curr_building, GoldMine):
                    self.gold_per_second -= curr_building.gold_per_second
                elif isinstance(curr_building, GemMine):
                    self.gems_per_second -= curr_building.gem_per_second
                elif isinstance(curr_building, Obstacle):
                    self.gold += curr_building.remove_gold_gain
                    self.gems += curr_building.remove_gem_gain

                curr_tile.building = None
                return True
            return False
        return False

    def place_rune_on_legendary_creature(self, legendary_creature, rune):
        # type: (LegendaryCreature, Rune) -> bool
        if legendary_creature in self.legendary_creature_inventory.get_legendary_creatures() and rune in \
                self.item_inventory.get_items():
            legendary_creature.place_rune(rune)
            return True
        return False

    def remove_rune_from_legendary_creature(self, legendary_creature, slot_number):
        # type: (LegendaryCreature, int) -> bool
        if legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
            if slot_number in legendary_creature.get_runes().keys():
                legendary_creature.remove_rune(slot_number)
                return True
            return False
        return False

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp:
            self.level += 1
            self.required_exp *= mpf("10") ** self.level

    def purchase_item(self, item):
        # type: (Item) -> bool
        if self.gold >= item.gold_cost and self.gems >= item.gem_cost:
            self.gold -= item.gold_cost
            self.gems -= item.gem_cost
            self.add_item_to_inventory(item)
            return True
        return False

    def sell_item(self, item):
        # type: (Item) -> bool
        if item in self.item_inventory.get_items():
            if isinstance(item, Rune):
                if item.already_placed:
                    return False

            self.remove_item_from_inventory(item)
            self.gold += item.sell_gold_gain
            self.gems += item.sell_gem_gain
            return True
        return False

    def level_up_rune(self, rune):
        # type: (Rune) -> bool
        if rune in self.item_inventory.get_items():
            if self.gold >= rune.level_up_gold_cost:
                self.gold -= rune.level_up_gold_cost
                return rune.level_up()
            return False
        else:
            # Check whether a legendary creature has the rune 'rune' or not
            for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                if rune in legendary_creature.get_runes().values():
                    if self.gold >= rune.level_up_gold_cost:
                        self.gold -= rune.level_up_gold_cost
                        return legendary_creature.level_up_rune(rune.slot_number)
                    return False
            return False

    def add_item_to_inventory(self, item):
        # type: (Item) -> None
        self.item_inventory.add_item(item)

    def remove_item_from_inventory(self, item):
        # type: (Item) -> bool
        if isinstance(item, Rune):
            for legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
                if item in legendary_creature.get_runes().values():
                    return False

        return self.item_inventory.remove_item(item)

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> None
        self.gold_per_second += legendary_creature.player_gold_per_second
        self.legendary_creature_inventory.add_legendary_creature(legendary_creature)

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.battle_team.get_legendary_creatures() or \
                legendary_creature.placed_in_training_area or legendary_creature.placed_in_habitat:
            return False
        if self.legendary_creature_inventory.remove_legendary_creature(legendary_creature):
            self.gold_per_second -= legendary_creature.player_gold_per_second
            return True

    def add_legendary_creature_to_team(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
            if self.battle_team.add_legendary_creature(legendary_creature):
                legendary_creature.corresponding_team = self.battle_team
                return True
            return False
        return False

    def remove_legendary_creature_from_team(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.legendary_creature_inventory.get_legendary_creatures():
            legendary_creature.corresponding_team = Team()
            return self.battle_team.remove_legendary_creature(legendary_creature)
        return False

    def get_unlocked_levels(self):
        # type: () -> list
        return self.__unlocked_levels

    def add_unlocked_level(self):
        # type: () -> None
        new_level_number: int = Level.LEVEL_NUMBER + 1
        level_stages: list = []  # initial value
        for i in range(5):
            level_stages.append(Stage([generate_random_legendary_creature(
                Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
            ),
                generate_random_legendary_creature(
                    Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
                ),
                generate_random_legendary_creature(
                    Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
                ),
                generate_random_legendary_creature(
                    Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
                ),
                generate_random_legendary_creature(
                    Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]
                )]))

        level_ups: int = 5 * (new_level_number - 1)
        for stage in level_stages:
            for legendary_creature in stage.get_enemies_list():
                for k in range(level_ups):
                    legendary_creature.exp = legendary_creature.required_exp
                    legendary_creature.level_up()
                    if legendary_creature.level == legendary_creature.max_level:
                        legendary_creature.evolve()

        new_level: Level = Level(level_stages, Reward(
            mpf("10") ** (5 * new_level_number),
            mpf("10") ** (5 * new_level_number),
            mpf(5 * new_level_number),
            mpf("10") ** (5 * new_level_number),
            [Egg(mpf("1e6"), mpf("10"),
                 Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)]),
             AwakenShard(mpf("1e6"), mpf("10"),
                         Egg.POTENTIAL_ELEMENTS[random.randint(0, len(Egg.POTENTIAL_ELEMENTS) - 1)])]
        ))
        self.__unlocked_levels.append(new_level)

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class ItemInventory:
    """
    This class contains attributes of an inventory containing items.
    """

    def __init__(self):
        # type: () -> None
        self.__items: list = []  # initial value

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def get_items(self):
        # type: () -> list
        return self.__items

    def add_item(self, item):
        # type: (Item) -> None
        self.__items.append(item)

    def remove_item(self, item):
        # type: (Item) -> bool
        if item in self.__items:
            self.__items.remove(item)
            return True
        return False

    def clone(self):
        # type: () -> ItemInventory
        return copy.deepcopy(self)


class LegendaryCreatureInventory:
    """
    This class contains attributes of an inventory containing legendary creatures.
    """

    def __init__(self):
        # type: () -> None
        self.__legendary_creatures: list = []  # initial value

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def get_legendary_creatures(self):
        # type: () -> list
        return self.__legendary_creatures

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> None
        self.__legendary_creatures.append(legendary_creature)

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures:
            self.__legendary_creatures.remove(legendary_creature)
            return True
        return False

    def clone(self):
        # type: () -> LegendaryCreatureInventory
        return copy.deepcopy(self)


class Reward:
    """
    This class contains attributes of a reward gained for doing something in the game.
    """

    def __init__(self, player_reward_exp=mpf("0"), player_reward_gold=mpf("0"), player_reward_gems=mpf("0"),
                 legendary_creature_reward_exp=mpf("0"), player_reward_items=None):
        # type: (mpf, mpf, mpf, mpf, list) -> None
        if player_reward_items is None:
            player_reward_items = []

        self.player_reward_exp: mpf = player_reward_exp
        self.player_reward_gold: mpf = player_reward_gold
        self.player_reward_gems: mpf = player_reward_gems
        self.legendary_creature_reward_exp: mpf = legendary_creature_reward_exp
        self.__player_reward_items: list = player_reward_items

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def get_player_reward_items(self):
        # type: () -> list
        return self.__player_reward_items

    def clone(self):
        # type: () -> Reward
        return copy.deepcopy(self)


class Game:
    """
    This class contains attributes of saved game data.
    """

    def __init__(self, player_data, item_shop, building_shop):
        # type: (Player, ItemShop, BuildingShop) -> None
        self.player_data: Player = player_data
        self.item_shop: ItemShop = item_shop
        self.building_shop: BuildingShop = building_shop

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Game
        return copy.deepcopy(self)


###########################################
# GENERAL
###########################################


# Creating main function used to run the game.


def main() -> int:
    """
    This main function is used to run the game.
    :return: an integer
    """

    print("Welcome to 'Creature World Builder Lite' by 'DigitalCreativeApkDev'.")
    print("In this game, you will build your own creature world to raise legendary creatures to be brought ")
    print("for battles.")
    print("Below is the element chart in 'Creature World Builder Lite'.\n")
    print(str(tabulate_element_chart()) + "\n")
    print("The following elements do not have any elemental strengths nor weaknesses.")
    print("This is because they are ancient world elements. In this case, these elements will always ")
    print("be dealt with normal damage.\n")
    ancient_world_elements: list = ["BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM", "SOUL"]
    for i in range(0, len(ancient_world_elements)):
        print(str(i + 1) + ". " + str(ancient_world_elements[i]))

    # Initialising variables to be used in the saved game data
    runes: list = []  # initial value
    for rating in range(Rune.MIN_RATING, Rune.MAX_RATING + 1):
        for slot_number in range(Rune.MIN_SLOT_NUMBER, Rune.MAX_SLOT_NUMBER + 1):
            name: str = str(rating) + "-STAR RUNE - SLOT " + str(slot_number)
            description: str = "Rune of rating " + str(rating) + " at slot " + \
                               str(slot_number)
            gold_cost: mpf = mpf("10") ** (6 + 5 * (rating - 1))
            gem_cost: mpf = 0 if rating == 1 else 10 * triangular(rating)
            stat_increase: StatIncrease = StatIncrease(mpf("10") ** (6 * rating), mpf(2 * rating),
                                                       mpf("10") ** (6 * rating), mpf(2 * rating),
                                                       mpf("10") ** (5 * rating), mpf(2 * rating),
                                                       mpf("10") ** (5 * rating), mpf(2 * rating),
                                                       mpf(2 * rating), mpf(0.01 * rating), mpf(0.05 * rating),
                                                       mpf(0.01 * rating), mpf(0.01 * rating), mpf(0.01 * rating))
            new_rune: Rune = Rune(name, description, gold_cost, gem_cost, rating, slot_number, stat_increase)
            runes.append(new_rune)

    eggs: list = []  # initial value
    for element in Egg.POTENTIAL_ELEMENTS:
        new_egg: Egg = Egg(mpf("8e5"), mpf("8"), element)
        eggs.append(new_egg)

    awaken_shards: list = []  # initial value
    for element in Egg.POTENTIAL_ELEMENTS:
        new_awaken_shard: AwakenShard = AwakenShard(mpf("1e6"), mpf("10"), element)
        awaken_shards.append(new_awaken_shard)

    items: list = [rune for rune in runes] + [egg for egg in eggs] + \
                  [awaken_shard for awaken_shard in awaken_shards]
    items = items + [EXPShard(mpf("1e6"), mpf("10"), mpf("1e5")),
                     LevelUpShard(mpf("1e6"), mpf("10")),
                     SkillLevelUpShard(mpf("1e6"), mpf("10"))]

    item_shop: ItemShop = ItemShop(items)

    habitats: list = []  # initial value
    for element in Egg.POTENTIAL_ELEMENTS:
        new_habitat: Habitat = Habitat(mpf("1e5"), mpf("1"), element, mpf("1e3"))
        habitats.append(new_habitat)

    building_shop: BuildingShop = BuildingShop(
        [habitat for habitat in habitats] + [
            Hatchery(mpf("1e5"), mpf("1")),
            TrainingArea(mpf("1e8"), mpf("1000")),
            Tree(mpf("1e4"), mpf("0")),
            FoodFarm(mpf("1e6"), mpf("10")),
            GoldMine(mpf("1e6"), mpf("10")),
            GemMine(mpf("1e6"), mpf("10")),
            PowerUpCircle(mpf("1e5"), mpf("1")),
            FusionCenter(mpf("1e8"), mpf("1000"))
        ]
    )

    # Initialising variable for the saved game data
    # Asking the user to enter his/her name to check whether saved game data exists or not
    player_name: str = input("Please enter your name: ")
    file_name: str = "SAVED CREATURE WORLD BUILDER LITE GAME DATA - " + str(player_name).upper()

    new_game: Game
    try:
        new_game = load_game_data(file_name)

        # Clearing up the command line window
        clear()

        print("Current game progress:\n", str(new_game))
    except FileNotFoundError:
        # Clearing up the command line window
        clear()

        print("Sorry! No saved game data with player name '" + str(player_name) + "' is available!")
        name: str = input("Please enter your name: ")
        player_data: Player = Player(name)
        new_game = Game(player_data, item_shop, building_shop)

    # Getting the current date and time
    old_now: datetime = datetime.now()
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_playing: str = input("Do you want to continue playing 'Creature World Builder Lite'? ")
    while continue_playing == "Y":
        # Updating the old time
        new_now: datetime = datetime.now()
        time_difference = new_now - old_now
        seconds: int = time_difference.seconds
        old_now = new_now

        # Increase player's EXP, gold, and gems
        new_game.player_data.exp += new_game.player_data.exp_per_second * seconds
        new_game.player_data.level_up()
        new_game.player_data.gold += new_game.player_data.gold_per_second * seconds
        new_game.player_data.gems += new_game.player_data.gems_per_second * seconds

        # Increase the exp of all legendary creatures owned by the player
        for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
            legendary_creature.exp += legendary_creature.exp_per_second * seconds
            legendary_creature.level_up()

        # Hatching all eggs in hatcheries
        new_game.player_data.hatch_eggs_in_hatcheries()

        # Asking the player what he/she wants to do in the game.
        allowed: list = ["PLAY ADVENTURE MODE", "MANAGE CREATURE WORLD", "MANAGE BATTLE TEAM",
                         "MANAGE LEGENDARY CREATURE INVENTORY", "MANAGE ITEM INVENTORY", "FUSE LEGENDARY CREATURES",
                         "PLACE EGG", "FEED LEGENDARY CREATURE", "GIVE ITEM", "POWER UP LEGENDARY CREATURE",
                         "EVOLVE LEGENDARY CREATURE", "MANAGE HABITAT", "MANAGE TRAINING AREA", "PLACE RUNE",
                         "REMOVE RUNE", "BUY ITEM", "VIEW STATS"]
        print("Enter 'PLAY ADVENTURE MODE' to play in adventure mode.")
        print("Enter 'MANAGE CREATURE WORLD' to manage your creature world.")
        print("Enter 'MANAGE BATTLE TEAM' to manage your battle team.")
        print("Enter 'MANAGE LEGENDARY CREATURE INVENTORY' to manage your legendary creature inventory.")
        print("Enter 'MANAGE ITEM INVENTORY' to manage your item inventory.")
        print("Enter 'FUSE LEGENDARY CREATURES' to fuse legendary creatures using a fusion center.")
        print("Enter 'PLACE EGG' to place an egg in the hatchery to get it hatched.")
        print("Enter 'FEED LEGENDARY CREATURE' to feed a legendary creature and increase its EXP.")
        print("Enter 'GIVE ITEM' to give an item to a legendary creature.")
        print("Enter 'POWER UP LEGENDARY CREATURE' to power up legendary creatures.")
        print("Enter 'EVOLVE LEGENDARY CREATURE' to evolve legendary creatures.")
        print("Enter 'MANAGE HABITAT' to manage your habitat.")
        print("Enter 'MANAGE TRAINING AREA' to manage your training area.")
        print("Enter 'PLACE RUNE' to place a rune on a legendary creature.")
        print("Enter 'REMOVE RUNE' to remove a rune from a legendary creature.")
        print("Enter 'BUY ITEM' to purchase an item from the item shop.")
        print("Enter 'VIEW STATS' to view your stats.")
        print("Enter anything else to save game data and quit the game.")
        action: str = input("What do you want to do? ")
        if action not in allowed:
            continue_playing = "N"
            break
        else:
            if action == "VIEW STATS":
                # Clearing the command line window
                clear()

                # Display player's stats
                print(new_game.player_data)
            elif action == "BUY ITEM":
                # Clearing the command line window
                clear()

                # Show a list of items which the player can buy
                item_list: list = new_game.item_shop.get_items_sold()
                print("Below is a list of items you can buy.\n")
                curr_item_index: int = 1  # initial value
                for item in item_list:
                    print("ITEM #" + str(curr_item_index))
                    print(str(item) + "\n")
                    curr_item_index += 1

                item_index: int = int(input("Please enter the index of the item you want to buy (1 - " +
                                            str(len(item_list)) + "): "))
                while item_index < 1 or item_index > len(item_list):
                    item_index: int = int(input("Sorry, invalid input! Please enter the index of the item you want "
                                                "to buy (1 - " + str(len(item_list)) + "): "))

                item_to_buy: Item = item_list[item_index - 1]
                if new_game.player_data.purchase_item(item_to_buy):
                    print("You have successfully bought " + str(item_to_buy.name))
                else:
                    print("Sorry, you have insufficient gold and/or gems!")

            elif action == "REMOVE RUNE":
                # Clearing up the command line window
                clear()

                # Allow the player to remove a rune if there are legendary creatures in the legendary creature
                # inventory.
                if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                    print("Below is a list of legendary creatures you have.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    legendary_creature_index: int = int(input("Please enter the index of the legendary creature "
                                                              "you want to remove a rune from (1 - " +
                                                              str(len(new_game.player_data.legendary_creature_inventory.
                                                                      get_legendary_creatures())) + "): "))
                    while legendary_creature_index < 1 or legendary_creature_index > \
                            len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                        legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                             "legendary creature you want to remove a rune from "
                                                             "(1 - " +
                                                             str(len(new_game.player_data.legendary_creature_inventory.
                                                                     get_legendary_creatures())) + "): "))

                    chosen_legendary_creature: LegendaryCreature = \
                        new_game.player_data.legendary_creature_inventory.get_legendary_creatures() \
                            [legendary_creature_index - 1]
                    print(str(chosen_legendary_creature.name) + " has runes placed in slots as below.")
                    for i in chosen_legendary_creature.get_runes().keys():
                        print("SLOT NUMBER #" + str(i))

                    slot_number: int = int(input("Please enter the slot number of the rune you want to remove "
                                                 "(1 - 6): "))
                    while slot_number < 1 or slot_number > 6:
                        slot_number = int(
                            input("Sorry, invalid input! Please enter the slot number of the rune you want to "
                                  "remove (1 - 6): "))

                    chosen_legendary_creature.remove_rune(slot_number)

            elif action == "PLACE RUNE":
                # Clearing up the command line window
                clear()

                # Allow the player to place a rune if there are legendary creatures in the legendary creature
                # inventory.
                if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                    print("Below is a list of legendary creatures you have.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    legendary_creature_index: int = int(input("Please enter the index of the legendary creature "
                                                              "you want to place a rune on (1 - " +
                                                              str(len(new_game.player_data.legendary_creature_inventory.
                                                                      get_legendary_creatures())) + "): "))
                    while legendary_creature_index < 1 or legendary_creature_index > \
                            len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                        legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                             "legendary creature you want to place a rune on "
                                                             "(1 - " +
                                                             str(len(new_game.player_data.legendary_creature_inventory.
                                                                     get_legendary_creatures())) + "): "))

                    chosen_legendary_creature: LegendaryCreature = \
                        new_game.player_data.legendary_creature_inventory.get_legendary_creatures() \
                            [legendary_creature_index - 1]

                    # Getting a list of runes which can be placed to the legendary creature
                    runes: list = []  # initial value
                    for item in new_game.player_data.item_inventory.get_items():
                        if isinstance(item, Rune):
                            if not item.already_placed:
                                runes.append(item)

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    place_rune: str = input(
                        "Do you want to place a rune to " + str(chosen_legendary_creature.name) + "? ")
                    if place_rune == "Y":
                        if len(runes) > 0:
                            print("Below is a list of runes you have.\n")
                            curr_rune_index: int = 1  # initial value
                            for rune in runes:
                                print("RUNE #" + str(curr_rune_index))
                                print(str(rune) + "\n")
                                curr_rune_index += 1

                            rune_index: int = int(input("Please enter the index of the rune you want to place to "
                                                        "this legendary creature (1 - " + str(len(runes)) + "): "))
                            while rune_index < 1 or rune_index > len(runes):
                                rune_index = int(input(
                                    "Sorry, invalid input! Please enter the index of the rune you want to place to "
                                    "this legendary creature (1 - " + str(len(runes)) + "): "))

                            chosen_rune: Rune = runes[rune_index - 1]
                            chosen_legendary_creature.place_rune(chosen_rune)

            elif action == "MANAGE TRAINING AREA":
                # Clearing up the command line window
                clear()

                # Getting a list of training areas in the player's creature world
                training_areas: list = []  # initial value
                for section in new_game.player_data.creature_world.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: SectionTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, TrainingArea):
                                training_areas.append(curr_tile.building)

                # If there are training areas, ask the player which training area he/she wants to manage.
                if len(training_areas) > 0:
                    print("Below is a list of training areas that you have.\n")
                    curr_training_area_index: int = 1  # initial value
                    for training_area in training_areas:
                        print("TRAINING AREA #" + str(curr_training_area_index))
                        print(str(training_area) + "\n")
                        curr_training_area_index += 1

                    training_area_index: int = int(input("Please enter the index of the training area you want to "
                                                         "manage (1 - " + str(len(training_areas)) + "): "))
                    while training_area_index < 1 or training_area_index > len(training_areas):
                        training_area_index = int(input("Sorry, invalid input! Please enter the index of the training "
                                                        "area "
                                                        "you want to manage (1 - " + str(len(training_areas)) + "): "))

                    chosen_training_area: TrainingArea = training_areas[training_area_index - 1]

                    # Checking whether a legendary creature can be added to the chosen training area or not.
                    if len(chosen_training_area.get_legendary_creatures_placed()) < \
                            chosen_training_area.MAX_LEGENDARY_CREATURES:
                        # Printing a list of legendary creatures the player can add to the training area
                        available_legendary_creatures: list = []  # initial value
                        for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                            if legendary_creature not in new_game.player_data.battle_team.get_legendary_creatures() and \
                                    not legendary_creature.placed_in_training_area and not \
                                    legendary_creature.placed_in_habitat:
                                available_legendary_creatures.append(legendary_creature)

                        if len(available_legendary_creatures) > 0:
                            print("Enter 'Y' for yes.")
                            print("Enter anything else for no.")
                            add_legendary_creature: str = input("Do you want to add a legendary creature to the "
                                                                "training area? ")
                            if add_legendary_creature == "Y":
                                print(
                                    "Below is a list of legendary creatures which you can add to the training area.\n")
                                curr_legendary_creature_index: int = 1  # initial value
                                for legendary_creature in available_legendary_creatures:
                                    print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                    print(str(legendary_creature) + "\n")
                                    curr_legendary_creature_index += 1

                                legendary_creature_index: int = int(
                                    input("Please enter the index of the legendary creature "
                                          "you want to add to the training area (1 - " +
                                          str(len(available_legendary_creatures)) + "): "))
                                while legendary_creature_index < 1 or legendary_creature_index > \
                                        len(available_legendary_creatures):
                                    legendary_creature_index = int(
                                        input("Sorry, invalid input! Please enter the index of the "
                                              "legendary creature you want to add to the training "
                                              "area (1 - " +
                                              str(len(available_legendary_creatures)) + "): "))

                                legendary_creature_to_add: LegendaryCreature = \
                                    available_legendary_creatures[legendary_creature_index - 1]
                                new_game.player_data.add_legendary_creature_to_training_area(legendary_creature_to_add,
                                                                                             chosen_training_area)

                    # Checking whether a legendary creature can be removed from the chosen training area or not.
                    if len(chosen_training_area.get_legendary_creatures_placed()) > 0:
                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        remove_legendary_creature: str = input("Do you want to remove a legendary creature from the "
                                                               "training area? ")
                        if remove_legendary_creature == "Y":
                            # Printing a list of legendary creatures in the chosen training area
                            curr_legendary_creature_index: int = 1
                            for legendary_creature in chosen_training_area.get_legendary_creatures_placed():
                                print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                print(str(legendary_creature) + "\n")
                                curr_legendary_creature_index += 1

                            legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                      "creature "
                                                                      "you want to remove from the training area (1 - " +
                                                                      str(len(chosen_training_area.
                                                                              get_legendary_creatures_placed())) + "): "))
                            while legendary_creature_index < 1 or legendary_creature_index > \
                                    len(chosen_training_area.get_legendary_creatures_placed()):
                                legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of "
                                                                     "the "
                                                                     "legendary creature "
                                                                     "you want to remove from the training area (1 - " +
                                                                     str(len(chosen_training_area.
                                                                             get_legendary_creatures_placed())) + "): "))

                            legendary_creature_to_remove: LegendaryCreature = \
                                chosen_training_area.get_legendary_creatures_placed()[legendary_creature_index - 1]
                            new_game.player_data.remove_legendary_creature_from_training_area \
                                (legendary_creature_to_remove, chosen_training_area)

            elif action == "MANAGE HABITAT":
                # Clearing up the command line window
                clear()

                # Getting a list of habitats in the player's creature world
                habitats: list = []  # initial value
                for section in new_game.player_data.creature_world.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: SectionTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, Habitat):
                                habitats.append(curr_tile.building)

                # If there are habitats, ask the player which training area he/she wants to manage.
                if len(habitats) > 0:
                    print("Below is a list of habitats that you have.\n")
                    curr_habitat_index: int = 1
                    for habitat in habitats:
                        print("HABITAT #" + str(curr_habitat_index))
                        print(str(habitat) + "\n")
                        curr_habitat_index += 1

                    chosen_habitat_index: int = int(input("Please enter the index of the habitat you want "
                                                          "to manage (1 - " + str(len(habitats)) + "): "))
                    while chosen_habitat_index < 1 or chosen_habitat_index > len(habitats):
                        chosen_habitat_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                         "habitat you want "
                                                         "to manage (1 - " + str(len(habitats)) + "): "))

                    chosen_habitat: Habitat = habitats[chosen_habitat_index - 1]

                    # Checking whether legendary creatures can be added to the chosen habitat or not.
                    if len(chosen_habitat.get_legendary_creatures_placed()) < chosen_habitat.MAX_LEGENDARY_CREATURES:
                        # Printing a list of legendary creatures the player can add to the habitat
                        available_legendary_creatures: list = []  # initial value
                        for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                            if legendary_creature not in new_game.player_data.battle_team.get_legendary_creatures() and \
                                    not legendary_creature.placed_in_training_area and not \
                                    legendary_creature.placed_in_habitat and chosen_habitat.element in \
                                    legendary_creature.get_elements():
                                available_legendary_creatures.append(legendary_creature)

                        if len(available_legendary_creatures) > 0:
                            print("Enter 'Y' for yes.")
                            print("Enter anything else for no.")
                            add_legendary_creature: str = input("Do you want to add a legendary creature to the "
                                                                "habitat? ")
                            if add_legendary_creature == "Y":
                                print("Below is a list of legendary creatures which you can add to the habitat.\n")
                                curr_legendary_creature_index: int = 1  # initial value
                                for legendary_creature in available_legendary_creatures:
                                    print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                    print(str(legendary_creature) + "\n")
                                    curr_legendary_creature_index += 1

                                legendary_creature_index: int = int(input("Please enter the index of the "
                                                                          "legendary creature you want to "
                                                                          "add to the habitat (1 - " +
                                                                          str(len(available_legendary_creatures)) +
                                                                          "): "))
                                while legendary_creature_index < 1 or legendary_creature_index > \
                                        len(available_legendary_creatures):
                                    legendary_creature_index = int(input("Sorry, invalid input! "
                                                                         "Please enter the index of the "
                                                                         "legendary creature you want to "
                                                                         "add to the habitat (1 - " +
                                                                         str(len(available_legendary_creatures)) +
                                                                         "): "))

                                legendary_creature_to_add: LegendaryCreature = \
                                    available_legendary_creatures[legendary_creature_index - 1]
                                new_game.player_data.add_legendary_creature_to_habitat(legendary_creature_to_add,
                                                                                       chosen_habitat)

                    # Checking whether a legendary creature can be removed from the chosen habitat or not.
                    if len(chosen_habitat.get_legendary_creatures_placed()) > 0:
                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        remove_legendary_creature: str = input("Do you want to remove a legendary creature from the "
                                                               "habitat? ")
                        if remove_legendary_creature == "Y":
                            # Printing a list of legendary creatures in the chosen habitat
                            curr_legendary_creature_index: int = 1
                            for legendary_creature in chosen_habitat.get_legendary_creatures_placed():
                                print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                print(str(legendary_creature) + "\n")
                                curr_legendary_creature_index += 1

                            legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                      "creature "
                                                                      "you want to remove from the habitat (1 - " +
                                                                      str(len(chosen_habitat.
                                                                              get_legendary_creatures_placed())) + "): "))
                            while legendary_creature_index < 1 or legendary_creature_index > \
                                    len(chosen_habitat.get_legendary_creatures_placed()):
                                legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of "
                                                                     "the "
                                                                     "legendary creature "
                                                                     "you want to remove from the habitat (1 - " +
                                                                     str(len(chosen_habitat.
                                                                             get_legendary_creatures_placed())) + "): "))

                            legendary_creature_to_remove: LegendaryCreature = \
                                chosen_habitat.get_legendary_creatures_placed()[legendary_creature_index - 1]
                            new_game.player_data.remove_legendary_creature_from_habitat \
                                (legendary_creature_to_remove, chosen_habitat)

            elif action == "EVOLVE LEGENDARY CREATURE":
                # Clearing up the command line window
                clear()

                # Getting a list of power-up circles in the player's creature world
                power_up_circles: list = []  # initial value
                for section in new_game.player_data.creature_world.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: SectionTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, PowerUpCircle):
                                power_up_circles.append(curr_tile.building)

                # If there are power up circles, ask the player which power-up circle he/she wants to use
                if len(power_up_circles) > 0:
                    print("Below is a list of power up circles that you have.\n")
                    curr_power_up_circle_index: int = 1  # initial value
                    for power_up_circle in power_up_circles:
                        print("POWER UP CIRCLE #" + str(curr_power_up_circle_index))
                        print(str(power_up_circle) + "\n")
                        curr_power_up_circle_index += 1

                    power_up_circle_index: int = int(input("Please enter the index of the power-up circle you want to "
                                                           "use (1 - " + str(len(power_up_circles)) + "): "))
                    while power_up_circle_index < 1 or power_up_circle_index > len(power_up_circles):
                        power_up_circle_index = int(
                            input("Sorry, invalid input! Please enter the index of the power-up circle you want to "
                                  "use (1 - " + str(len(power_up_circles)) + "): "))

                    chosen_power_up_circle: PowerUpCircle = power_up_circles[power_up_circle_index - 1]

                    # Ask the player to choose the legendary creature to be evolved and the materials used if
                    # possible
                    if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                        # Printing all the legendary creatures the player has.
                        for legendary_creature in \
                                new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                            print(str(legendary_creature) + "\n")

                        # Ask the player to choose the legendary creature to be evolved
                        to_be_evolved_index: int = int(input("Please enter the index of the legendary creature "
                                                             "you want to evolve (1 - " +
                                                             str(len(new_game.
                                                                     player_data.legendary_creature_inventory
                                                                     .get_legendary_creatures())) +
                                                             "): "))
                        while to_be_evolved_index < 1 or to_be_evolved_index > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                            to_be_evolved_index = int(
                                input("Sorry, invalid input! Please enter the index of the legendary creature "
                                      "you want to evolve (1 - " +
                                      str(len(new_game.
                                              player_data.legendary_creature_inventory.get_legendary_creatures())) +
                                      "): "))

                        to_be_evolved: LegendaryCreature = new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures()[to_be_evolved_index - 1]

                        materials_to_use: list = []
                        num_materials: int = int(input("How many material legendary creatures do you want to place "
                                                       "(0-" +
                                                       str(min(5,
                                                               len(new_game.player_data.legendary_creature_inventory.
                                                                   get_legendary_creatures()))) +
                                                       "): "))

                        while num_materials < 0 or num_materials > 5 or num_materials > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) - 1:
                            num_materials = int(input("Sorry, invalid input! How many material legendary creatures do "
                                                      "you want to place "
                                                      "(0-" +
                                                      str(min(5,
                                                              len(new_game.player_data.legendary_creature_inventory.
                                                                  get_legendary_creatures()))) +
                                                      "): "))

                        legendary_creature_options: list = new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures()
                        legendary_creature_options.remove(to_be_evolved)
                        for i in range(num_materials):
                            print("Below is a list of legendary creatures you can choose as a material.\n")
                            curr_legendary_creature_index: int = 1  # initial value
                            for legendary_creature in legendary_creature_options:
                                print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                print(str(legendary_creature) + "\n")
                                curr_legendary_creature_index += 1

                            chosen_legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                             "creature you want to use as a material "
                                                                             "(1 - " +
                                                                             str(len(legendary_creature_options)) +
                                                                             ": "))
                            while chosen_legendary_creature_index < 1 or chosen_legendary_creature_index > \
                                    len(legendary_creature_options):
                                chosen_legendary_creature_index = int(
                                    input("Sorry, invalid input! Please enter the index of the legendary "
                                          "creature you want to use as a material "
                                          "(1 - " +
                                          str(len(legendary_creature_options)) +
                                          ": "))

                            chosen_material: LegendaryCreature = legendary_creature_options \
                                [chosen_legendary_creature_index - 1]
                            materials_to_use.append(chosen_material)
                            legendary_creature_options.remove(chosen_material)

                        new_game.player_data.evolve_legendary_creature(to_be_evolved, materials_to_use,
                                                                       chosen_power_up_circle)

            elif action == "POWER UP LEGENDARY CREATURE":
                # Clearing up the command line window
                clear()

                # Getting a list of power-up circles in the player's creature world
                power_up_circles: list = []  # initial value
                for section in new_game.player_data.creature_world.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: SectionTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, PowerUpCircle):
                                power_up_circles.append(curr_tile.building)

                # If there are power up circles, ask the player which power-up circle he/she wants to use
                if len(power_up_circles) > 0:
                    print("Below is a list of power up circles that you have.")
                    curr_power_up_circle_index: int = 1  # initial value
                    for power_up_circle in power_up_circles:
                        print("POWER UP CIRCLE #" + str(curr_power_up_circle_index))
                        print(str(power_up_circle) + "\n")
                        curr_power_up_circle_index += 1

                    power_up_circle_index: int = int(input("Please enter the index of the power-up circle you want to "
                                                           "use (1 - " + str(len(power_up_circles)) + "): "))
                    while power_up_circle_index < 1 or power_up_circle_index > len(power_up_circles):
                        power_up_circle_index = int(
                            input("Sorry, invalid input! Please enter the index of the power-up circle you want to "
                                  "use (1 - " + str(len(power_up_circles)) + "): "))

                    chosen_power_up_circle: PowerUpCircle = power_up_circles[power_up_circle_index - 1]

                    # Ask the player to choose the legendary creature to be powered up and the materials used if
                    # possible
                    if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                        # Printing all the legendary creatures the player has.
                        curr_legendary_creature_index: int = 1  # initial value
                        for legendary_creature in \
                                new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                            print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                            print(str(legendary_creature) + "\n")
                            curr_legendary_creature_index += 1

                        # Ask the player to choose the legendary creature to be powered up
                        to_be_powered_up_index: int = int(input("Please enter the index of the legendary creature "
                                                                "you want to power-up (1 - " +
                                                                str(len(new_game.
                                                                        player_data.legendary_creature_inventory
                                                                        .get_legendary_creatures())) +
                                                                "): "))
                        while to_be_powered_up_index < 1 or to_be_powered_up_index > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                            to_be_powered_up_index = int(
                                input("Sorry, invalid input! Please enter the index of the legendary creature "
                                      "you want to power-up (1 - " +
                                      str(len(new_game.
                                              player_data.legendary_creature_inventory.get_legendary_creatures())) +
                                      "): "))

                        to_be_powered_up: LegendaryCreature = new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures()[to_be_powered_up_index - 1]

                        materials_to_use: list = []
                        num_materials: int = int(input("How many material legendary creatures do you want to place "
                                                       "(0-" +
                                                       str(min(5,
                                                               len(new_game.player_data.legendary_creature_inventory.
                                                                   get_legendary_creatures()))) +
                                                       "): "))

                        while num_materials < 0 or num_materials > 5 or num_materials > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) - 1:
                            num_materials = int(input("Sorry, invalid input! How many material legendary creatures do "
                                                      "you want to place "
                                                      "(0-" +
                                                      str(min(5,
                                                              len(new_game.player_data.legendary_creature_inventory.
                                                                  get_legendary_creatures()))) +
                                                      "): "))

                        legendary_creature_options: list = new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures()
                        legendary_creature_options.remove(to_be_powered_up)
                        for i in range(num_materials):
                            print("Below is a list of legendary creatures you can choose as a material.\n")
                            curr_legendary_creature_index: int = 1  # initial value
                            for legendary_creature in legendary_creature_options:
                                print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                                print(str(legendary_creature) + "\n")
                                curr_legendary_creature_index += 1

                            chosen_legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                             "creature you want to use as a material "
                                                                             "(1 - " +
                                                                             str(len(legendary_creature_options)) +
                                                                             ": "))
                            while chosen_legendary_creature_index < 1 or chosen_legendary_creature_index > \
                                    len(legendary_creature_options):
                                chosen_legendary_creature_index = int(
                                    input("Sorry, invalid input! Please enter the index of the legendary "
                                          "creature you want to use as a material "
                                          "(1 - " +
                                          str(len(legendary_creature_options)) +
                                          ": "))

                            chosen_material: LegendaryCreature = legendary_creature_options \
                                [chosen_legendary_creature_index - 1]
                            materials_to_use.append(chosen_material)
                            legendary_creature_options.remove(chosen_material)

                        new_game.player_data.power_up_legendary_creature(to_be_powered_up, materials_to_use,
                                                                         chosen_power_up_circle)

            elif action == "GIVE ITEM":
                # Clearing up the command line window
                clear()

                # Getting a list of items which are neither runes nor eggs in the player's item inventory
                neither_rune_nor_egg_items: list = [item for item in new_game.player_data.item_inventory.get_items()
                                                    if not isinstance(item, Rune) and not isinstance(item, Egg)]

                # If items which are neither runes nor eggs exist and there are legendary creatures in the
                # legendary creature inventory, ask the player to choose which item is to be given to a
                # legendary creature.
                if len(neither_rune_nor_egg_items) > 0 and \
                        len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                    print("Below is a list of items which are neither runes nor eggs that you have.\n")
                    curr_item_index: int = 1  # initial value
                    for item in neither_rune_nor_egg_items:
                        print("ITEM #" + str(curr_item_index))
                        print(str(item) + "\n")
                        curr_item_index += 1

                    item_index: int = int(input("Please enter the index of the item you want to give (1 - " +
                                                str(len(neither_rune_nor_egg_items)) + "): "))
                    while item_index < 1 or item_index > len(neither_rune_nor_egg_items):
                        item_index = int(input("Sorry, invalid input! Please enter the index of the item you want to "
                                               "give (1 - " +
                                               str(len(neither_rune_nor_egg_items)) + "): "))

                    item_to_give: Item = neither_rune_nor_egg_items[item_index - 1]
                    print("Below is a list of legendary creatures you have.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    legendary_creature_index: int = int(input("Please enter the index of the legendary creature you "
                                                              "want to give the item to (1 - " +
                                                              str(len(new_game.player_data.legendary_creature_inventory.
                                                                      get_legendary_creatures())) + "): "))
                    while legendary_creature_index < 1 or legendary_creature_index > len(
                            new_game.player_data.legendary_creature_inventory.
                                    get_legendary_creatures()):
                        legendary_creature_index = int(
                            input("Sorry, invalid input! Please enter the index of the legendary creature you "
                                  "want to give the item to (1 - " +
                                  str(len(new_game.player_data.legendary_creature_inventory.
                                          get_legendary_creatures())) + "): "))

                    chosen_legendary_creature: LegendaryCreature = new_game.player_data.legendary_creature_inventory. \
                        get_legendary_creatures()[legendary_creature_index - 1]

                    # Give the item to the chosen legendary creature
                    if new_game.player_data.give_item_to_legendary_creature(item_to_give, chosen_legendary_creature):
                        print("You have successfully given " + str(item_to_give.name) + " to " +
                              str(chosen_legendary_creature.name) + ".")
                    else:
                        print("Sorry! Item " + str(item_to_give.name) + " cannot be given to " +
                              str(chosen_legendary_creature.name) + ".")

            elif action == "FEED LEGENDARY CREATURE":
                # Clearing up the command line window
                clear()

                # Printing a list of legendary creatures the player can feed.
                print("Below is a list of legendary creatures you can feed.\n")
                curr_legendary_creature_index: int = 1  # initial value
                for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                    print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                    print(str(legendary_creature) + "\n")
                    curr_legendary_creature_index += 1

                legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                          "creature you want to feed (1 - " +
                                                          str(len(new_game.player_data.legendary_creature_inventory.
                                                                  get_legendary_creatures())) + "): "))
                while legendary_creature_index < 1 or legendary_creature_index > \
                        len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                    legendary_creature_index = int(
                        input("Sorry, invalid input! Please enter the index of the legendary "
                              "creature you want to feed (1 - " +
                              str(len(new_game.player_data.legendary_creature_inventory.
                                      get_legendary_creatures())) + "): "))

                chosen_legendary_creature: LegendaryCreature = new_game.player_data.legendary_creature_inventory. \
                    get_legendary_creatures()[legendary_creature_index - 1]
                food: mpf = mpf(input("Please enter the amount of food you want to feed (0 - " +
                                      str(new_game.player_data.food) + "): "))
                while food < 0 or food > new_game.player_data.food:
                    food: mpf = mpf(input("Sorry, invalid input! Please enter the amount of food "
                                          "you want to feed (0 - " +
                                          str(new_game.player_data.food) + "): "))

                new_game.player_data.feed_legendary_creature(chosen_legendary_creature, food)
                print("You have successfully fed " + str(food) + " food to " + str(chosen_legendary_creature.name) +
                      "!")

            elif action == "PLACE EGG":
                # Clearing up the command line window
                clear()

                # Getting a list of hatcheries the player has.
                hatcheries: list = []  # initial value
                for section in new_game.player_data.creature_world.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: SectionTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, Hatchery):
                                hatcheries.append(curr_tile.building)

                # Getting a list of eggs the player can place.
                eggs: list = []  # initial value
                for item in new_game.player_data.item_inventory.get_items():
                    if isinstance(item, Egg):
                        if not item.already_placed:
                            eggs.append(item)

                # If there are hatcheries and eggs, ask the player to choose which egg to be placed at which hatchery
                if len(hatcheries) > 0 and len(eggs) > 0:
                    print("Below is a list of hatcheries you have.\n")
                    curr_hatchery_index: int = 1
                    for hatchery in hatcheries:
                        print("HATCHERY #" + str(curr_hatchery_index))
                        print(str(hatchery) + "\n")
                        curr_hatchery_index += 1

                    hatchery_index: int = int(input("Please enter the index of the hatchery "
                                                    "you want to place an egg at (1 - " +
                                                    str(len(hatcheries)) + "): "))
                    while hatchery_index < 1 or hatchery_index > len(hatcheries):
                        hatchery_index = int(input("Sorry, invalid input! Please enter the index of the hatchery "
                                                   "you want to place an egg at (1 - " +
                                                   str(len(hatcheries)) + "): "))

                    chosen_hatchery: Hatchery = hatcheries[hatchery_index - 1]

                    print("Below is a list of eggs you can place.\n")
                    curr_egg_index: int = 1
                    for egg in eggs:
                        print("EGG #" + str(curr_egg_index))
                        print(str(egg) + "\n")
                        curr_egg_index += 1

                    egg_index: int = int(input("Please enter the index of the egg you want to place (1 - " +
                                               str(len(eggs)) + "): "))
                    while egg_index < 1 or egg_index > len(eggs):
                        egg_index = int(input("Sorry, invalid input! Please enter the index of the egg "
                                              "you want to place (1 - " +
                                              str(len(eggs)) + "): "))

                    chosen_egg: Egg = eggs[egg_index - 1]
                    if new_game.player_data.place_egg_in_hatchery(chosen_egg, chosen_hatchery):
                        print("You have successfully placed " + str(chosen_egg.name) + " at " +
                              str(chosen_hatchery.name) + "!")
                    else:
                        print("Sorry! You cannot place an egg in " + str(chosen_hatchery.name) + "!")

            elif action == "FUSE LEGENDARY CREATURES":
                # Clearing up the command line window
                clear()

                # Getting a list of fusion centers in the player's creature world
                fusion_centers: list = []  # initial value
                for section in new_game.player_data.creature_world.get_sections():
                    for x in range(section.SECTION_WIDTH):
                        for y in range(section.SECTION_HEIGHT):
                            curr_tile: SectionTile = section.get_tile_at(x, y)
                            if isinstance(curr_tile.building, FusionCenter):
                                fusion_centers.append(curr_tile.building)

                potential_material_legendary_creatures: list = [legendary_creature for legendary_creature in
                                                                new_game.player_data.legendary_creature_inventory.
                                                                    get_legendary_creatures() if legendary_creature not
                                                                in new_game.player_data.battle_team.
                                                                    get_legendary_creatures() and
                                                                not legendary_creature.placed_in_training_area and
                                                                not legendary_creature.placed_in_habitat]
                # If there are fusion centers and at least two legendary creatures which can be used as materials,
                # ask the user to choose which fusion center to use.
                if len(fusion_centers) > 0 and len(potential_material_legendary_creatures) >= 2:
                    print("Below is a list of fusion centers that you have.\n")
                    curr_fusion_center_index: int = 1  # initial value
                    for fusion_center in fusion_centers:
                        print("FUSION CENTER #" + str(curr_fusion_center_index))
                        print(str(fusion_center) + "\n")
                        curr_fusion_center_index += 1

                    fusion_center_index: int = int(input("Please enter the index of the fusion center you want "
                                                         "to use (1 - " + str(len(fusion_centers)) + "): "))
                    while fusion_center_index < 1 or fusion_center_index > len(fusion_centers):
                        fusion_center_index: int = int(input("Please enter the index of the fusion center you want "
                                                             "to use (1 - " + str(len(fusion_centers)) + "): "))

                    chosen_fusion_center: FusionCenter = fusion_centers[fusion_center_index - 1]

                    print("Below is a list of legendary creatures you can use as materials.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in potential_material_legendary_creatures:
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    chosen_indices: list = []  # initial value
                    for i in range(2):
                        legendary_creature_index: int = int(input("Please enter the index of the "
                                                                  "legendary creature you want to use (1 - " +
                                                                  str(len(potential_material_legendary_creatures))))
                        while legendary_creature_index < 1 or legendary_creature_index > \
                                len(potential_material_legendary_creatures) or legendary_creature_index in chosen_indices:
                            legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                                 "legendary creature you want to use (1 - " +
                                                                 str(len(potential_material_legendary_creatures))))

                        chosen_indices.append(legendary_creature_index)

                    first_index: int = chosen_indices[0] - 1
                    second_index: int = chosen_indices[0] - 1
                    first_legendary_creature: LegendaryCreature = potential_material_legendary_creatures[first_index]
                    second_legendary_creature: LegendaryCreature = potential_material_legendary_creatures[second_index]
                    new_game.player_data.fuse_legendary_creatures(first_legendary_creature,
                                                                  second_legendary_creature, chosen_fusion_center)

            elif action == "MANAGE ITEM INVENTORY":
                # Clearing up the command line window
                clear()
                if len(new_game.player_data.item_inventory.get_items()) > 0:
                    print("Below is a list of items in your item inventory.\n")
                    curr_item_index: int = 1
                    for item in new_game.player_data.item_inventory.get_items():
                        print("ITEM #" + str(curr_item_index))
                        print(str(item) + "\n")
                        curr_item_index += 1

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    sell_item: str = input("Do you want to sell an item? ")
                    if sell_item == "Y":
                        item_index: int = int(input("Please enter the index of the item you want to sell (1 - " +
                                                    str(len(new_game.player_data.item_inventory.get_items())) + "): "))
                        while item_index < 1 or item_index > len(new_game.player_data.item_inventory.get_items()):
                            item_index = int(input("Sorry, invalid input! Please enter the index of the item you "
                                                   "want to sell (1 - " +
                                                   str(len(new_game.player_data.item_inventory.get_items())) + "): "))

                        to_be_sold: Item = new_game.player_data.item_inventory.get_items()[item_index - 1]
                        if new_game.player_data.sell_item(to_be_sold):
                            print("Congratulations! You have earned " + str(to_be_sold.sell_gold_gain) + " gold and " +
                                  str(to_be_sold.sell_gem_gain) + " gems for selling " + str(to_be_sold.name) + "!")
                        else:
                            print("Sorry! " + str(to_be_sold.name) + " cannot be sold!")

                    runes: list = []  # initial value
                    for item in new_game.player_data.item_inventory.get_items():
                        if isinstance(item, Rune):
                            runes.append(item)

                    # Ask the player which rune to level up if there are runes in the item inventory
                    if len(runes) > 0:
                        print("Below is a list of runes you have.\n")
                        curr_rune_index: int = 1  # initial value
                        for rune in runes:
                            print("RUNE #" + str(curr_rune_index))
                            print(str(rune) + "\n")
                            curr_rune_index += 1

                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        level_up_rune: str = input("Do you want to level up a rune? ")
                        if level_up_rune == "Y":
                            rune_index: int = int(input("Please enter the index of the rune you want to level "
                                                        "up (1 - " + str(len(runes)) + "): "))
                            while rune_index < 1 or rune_index > len(runes):
                                rune_index = int(input("Sorry, invalid input! Please enter the index of the rune you "
                                                       "want to level "
                                                       "up (1 - " + str(len(runes)) + "): "))

                            chosen_rune: Rune = runes[rune_index - 1]
                            new_game.player_data.level_up_rune(chosen_rune)

            elif action == "MANAGE LEGENDARY CREATURE INVENTORY":
                # Clearing up the command line window
                clear()
                if len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()) > 0:
                    print("Below is a list of legendary creatures in your legendary creature inventory.\n")
                    curr_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory. \
                            get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(curr_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        curr_legendary_creature_index += 1

                    legendary_creature_index: int = int(input("Please enter the index of the legendary creature "
                                                              "you want to remove (1 - " +
                                                              str(len(new_game.player_data.
                                                                      legendary_creature_inventory.
                                                                      get_legendary_creatures())) + "): "))
                    while legendary_creature_index < 1 or legendary_creature_index > \
                            len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                        legendary_creature_index = int(input("Sorry, invalid input! Please enter the "
                                                             "index of the legendary creature "
                                                             "you want to remove (1 - " +
                                                             str(len(new_game.player_data.
                                                                     legendary_creature_inventory.
                                                                     get_legendary_creatures())) + "): "))

                    to_be_removed: LegendaryCreature = \
                        new_game.player_data.legendary_creature_inventory.get_legendary_creatures() \
                            [legendary_creature_index - 1]
                    new_game.player_data.remove_legendary_creature(to_be_removed)

            elif action == "MANAGE BATTLE TEAM":
                # Clearing up the command line window
                clear()
                if len(new_game.player_data.battle_team.get_legendary_creatures()) > 0:
                    print("Below is a list of legendary creatures in your battle team.\n")
                    current_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.battle_team.get_legendary_creatures():
                        print("LEGENDARY CREATURE #" + str(current_legendary_creature_index))
                        print(str(legendary_creature) + "\n")
                        current_legendary_creature_index += 1

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    remove_legendary_creature: str = input("Do you want to remove a legendary creature from "
                                                           "your team? ")
                    if remove_legendary_creature == "Y":
                        legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                  "creature you want to remove from "
                                                                  "your battle team (1 - " +
                                                                  str(len(new_game.player_data.
                                                                          battle_team.get_legendary_creatures())) +
                                                                  "): "))
                        while legendary_creature_index < 1 or legendary_creature_index > \
                                len(new_game.player_data.battle_team.get_legendary_creatures()):
                            legendary_creature_index = int(input("Sorry, invalid input! Please enter the index of the "
                                                                 "legendary "
                                                                 "creature you want to remove from "
                                                                 "your battle team (1 - " +
                                                                 str(len(new_game.player_data.
                                                                         battle_team.get_legendary_creatures())) +
                                                                 "): "))

                        to_be_removed: LegendaryCreature = new_game.player_data.battle_team.get_legendary_creatures() \
                            [legendary_creature_index - 1]
                        new_game.player_data.remove_legendary_creature_from_team(to_be_removed)

                if len(new_game.player_data.battle_team.get_legendary_creatures()) < Team.MAX_LEGENDARY_CREATURES:
                    print("Below is a list of legendary creatures you have.\n")
                    current_legendary_creature_index: int = 1  # initial value
                    for legendary_creature in new_game.player_data.legendary_creature_inventory.get_legendary_creatures():
                        if not legendary_creature.placed_in_habitat and \
                                not legendary_creature.placed_in_training_area and \
                                legendary_creature.legendary_creature_id not in [creature.legendary_creature_id for creature in
                                                                                 new_game.player_data.battle_team.get_legendary_creatures()]:
                            print("LEGENDARY CREATURE #" + str(current_legendary_creature_index))
                            print(str(legendary_creature) + "\n")
                            current_legendary_creature_index += 1

                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    add_legendary_creature: str = input("Do you want to add a legendary creature to your team? ")
                    if add_legendary_creature == "Y":
                        legendary_creature_index: int = int(input("Please enter the index of the legendary "
                                                                  "creature you want to add to your "
                                                                  "battle team (1 - " +
                                                                  str(len(new_game.player_data.
                                                                          legendary_creature_inventory.
                                                                          get_legendary_creatures())) + "): "))
                        while legendary_creature_index < 1 or legendary_creature_index > \
                                len(new_game.player_data.legendary_creature_inventory.get_legendary_creatures()):
                            legendary_creature_index = int(input("Sorry, invalid input! Please enter the index "
                                                                 "of the legendary "
                                                                 "creature you want to add to your "
                                                                 "battle team (1 - " +
                                                                 str(len(new_game.player_data.
                                                                         legendary_creature_inventory.
                                                                         get_legendary_creatures())) + "): "))

                        to_be_added: LegendaryCreature = \
                            new_game.player_data.legendary_creature_inventory.get_legendary_creatures() \
                                [legendary_creature_index - 1]
                        new_game.player_data.add_legendary_creature_to_team(to_be_added)

            elif action == "MANAGE CREATURE WORLD":
                # Clearing up the command line window
                clear()

                # Asking whether the player wants to add a new section to the player's creature world or not
                print("Enter 'Y' for yes.")
                print("Enter anything else for no.")
                add_section: str = input("Do you want to add a new section to your creature world for " +
                                         str(new_game.player_data.creature_world.section_build_gold_cost) + " gold? ")
                if add_section == "Y":
                    new_game.player_data.add_section_to_creature_world()

                # Showing the sections in the player's creature world
                if len(new_game.player_data.creature_world.get_sections()) > 0:
                    section_count: int = 1
                    for section in new_game.player_data.creature_world.get_sections():
                        print("----------SECTION #" + str(section_count) + "----------")
                        print(str(section) + "\n")
                        section_count += 1

                    chosen_section_index: int = int(input("Enter the index of the section you want to manage (1 - " +
                                                          str(len(
                                                              new_game.player_data.creature_world.get_sections())) + "): "))
                    while chosen_section_index < 1 or chosen_section_index > \
                            len(new_game.player_data.creature_world.get_sections()):
                        chosen_section_index = int(input("Sorry, invalid input! Enter the index of the section "
                                                         "you want to manage (1 - " +
                                                         str(len(
                                                             new_game.player_data.creature_world.get_sections())) + "): "))

                    chosen_section: Section = new_game.player_data.creature_world.get_sections()[
                        chosen_section_index - 1]
                    print("Enter 'LEVEL UP BUILDING' to level up a building at an section tile.")
                    print("Enter 'BUILD BUILDING' to build at an section tile.")
                    print("Enter 'REMOVE BUILDING' to remove a building from an section tile.")
                    valid_sub_actions: list = ["LEVEL UP BUILDING", "BUILD BUILDING", "REMOVE BUILDING"]
                    sub_action: str = input("What do you want to do? ")
                    while sub_action not in valid_sub_actions:
                        print("Enter 'LEVEL UP BUILDING' to level up a building at an section tile.")
                        print("Enter 'BUILD BUILDING' to build at an section tile.")
                        print("Enter 'REMOVE BUILDING' to remove a building from an section tile.")
                        sub_action = input("Sorry, invalid input! What do you want to do? ")

                    if sub_action == "LEVEL UP BUILDING":
                        tile_x: int = int(input("Please enter x-coordinates of the building to be levelled up: "))
                        tile_y: int = int(input("Please enter y-coordinates of the building to be levelled up: "))
                        if new_game.player_data.level_up_building_at_section_tile(chosen_section_index - 1, tile_x,
                                                                                  tile_y):
                            print("You have successfully levelled up " +
                                  str(chosen_section.get_tile_at(tile_x, tile_y).building.name) + "!")
                        else:
                            print("Building level up failed!")
                    elif sub_action == "BUILD BUILDING":
                        tile_x: int = int(input("Please enter x-coordinates of the tile to build at: "))
                        tile_y: int = int(input("Please enter y-coordinates of the tile to build at: "))
                        if isinstance(chosen_section.get_tile_at(tile_x, tile_y), SectionTile):
                            curr_tile: SectionTile = chosen_section.get_tile_at(tile_x, tile_y)
                            if curr_tile.building is None:
                                print("Below is a list of buildings you can build on the tile.")
                                building_count: int = 1
                                for building in building_shop.get_buildings_sold():
                                    print("BUILDING #" + str(building_count))
                                    print(str(building) + "\n")
                                    building_count += 1

                                building_index: int = int(input("Please enter the index of the building you "
                                                                "want to build (1 - " +
                                                                str(len(building_shop.get_buildings_sold())) + "): "))
                                while building_index < 1 or building_index > len(building_shop.get_buildings_sold()):
                                    building_index = int(input("Sorry, invalid input! Please enter the index of "
                                                               "the building you "
                                                               "want to build (1 - " +
                                                               str(len(building_shop.get_buildings_sold())) + "): "))

                                to_build: Building = building_shop.get_buildings_sold()[building_index - 1]
                                if new_game.player_data.build_at_section_tile(chosen_section_index - 1, tile_x, tile_y,
                                                                              to_build):
                                    print("You have successfully built " + str(to_build.name) + "!")
                                else:
                                    print("Sorry, you cannot build " + str(to_build.name) + "!")
                            else:
                                print("Sorry, you cannot build here!")
                        else:
                            print("Sorry, you cannot build here!")
                    elif sub_action == "REMOVE BUILDING":
                        tile_x: int = int(input("Please enter x-coordinates of the tile to remove building from: "))
                        tile_y: int = int(input("Please enter y-coordinates of the tile to remove building from: "))
                        if new_game.player_data.remove_building_from_section_tile(chosen_section_index - 1, tile_x,
                                                                                  tile_y):
                            print("You have successfully removed a building!")
                        else:
                            print("You failed to remove a building!")

            elif action == "PLAY ADVENTURE MODE":
                # Clearing up the command line window
                clear()

                # Getting a list of levels for the player to choose from.
                print("Below is a list of levels you can choose from.\n")
                curr_level_index: int = 1  # initial value
                for level in new_game.player_data.get_unlocked_levels():
                    print("LEVEL #" + str(curr_level_index))
                    print(str(level) + "\n")
                    curr_level_index += 1

                level_index: int = int(input("Please enter the index of the level "
                                             "you want to battle in (1 - " +
                                             str(len(new_game.player_data.get_unlocked_levels())) + "): "))
                while level_index < 1 or level_index > len(new_game.player_data.get_unlocked_levels()):
                    level_index = int(input("Sorry, invalid input! Please enter the index of the level "
                                            "you want to battle in (1 - " +
                                            str(len(new_game.player_data.get_unlocked_levels())) + "): "))

                chosen_level: Level = new_game.player_data.get_unlocked_levels()[level_index - 1]

                # Start the battle and battle until all stages are cleared
                curr_stage_number: int = 0
                current_stage: Stage = chosen_level.curr_stage(curr_stage_number)
                while chosen_level.next_stage(curr_stage_number) is not None and \
                        not new_game.player_data.battle_team.all_died():
                    # Clearing up the command line window
                    clear()

                    # Show the current stage
                    print("--------------------STAGE #" + str(curr_stage_number + 1) + "--------------------")
                    curr_battle: Battle = Battle(new_game.player_data.battle_team,
                                                 Team(current_stage.get_enemies_list()))
                    while curr_battle.winner is None:
                        # Printing out the stats of legendary creatures in both teams
                        print("Below are the stats of all legendary creatures in player's team.\n")
                        for legendary_creature in curr_battle.team1.get_legendary_creatures():
                            print(str(legendary_creature) + "\n")

                        print("Below are the stats of all legendary creatures in enemy's team.\n")
                        for legendary_creature in curr_battle.team2.get_legendary_creatures():
                            print(str(legendary_creature) + "\n")

                        # Make a legendary creature move
                        curr_battle.get_someone_to_move()
                        assert isinstance(curr_battle.whose_turn, LegendaryCreature), "Cannot proceed with battle!"

                        # Checking which legendary creature moves
                        if curr_battle.whose_turn in curr_battle.team1.get_legendary_creatures():
                            moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                            # Asking the player what he/she wants to do
                            print("Enter 'NORMAL ATTACK' for normal attack.")
                            print("Enter 'NORMAL HEAL' for normal heal.")
                            print("Enter anything else to use a skill (only applicable if you have usable skills).")
                            usable_skills: list = [skill for skill in curr_battle.whose_turn.get_skills()
                                                   if curr_battle.whose_turn.curr_magic_points >=
                                                   skill.magic_points_cost and isinstance(skill, Skill)]
                            possible_actions: list = ["NORMAL ATTACK", "NORMAL HEAL"]
                            trainer_battle_action: str = input("What do you want to do? ")
                            while len(usable_skills) == 0 and trainer_battle_action not in possible_actions:
                                print("Enter 'NORMAL ATTACK' for normal attack.")
                                print("Enter 'NORMAL HEAL' for normal heal.")
                                trainer_battle_action = input("Sorry, invalid input! What do you want to do? ")

                            if trainer_battle_action not in possible_actions:
                                # Use skill
                                trainer_battle_action = "USE SKILL"

                                # Show a list of skills the player can use
                                print("Below is a list of skills you can use.\n")
                                curr_skill_index: int = 1  # initial value
                                for skill in usable_skills:
                                    print("SKILL #" + str(curr_skill_index))
                                    print(str(skill) + "\n")
                                    curr_skill_index += 1

                                skill_index: int = int(input("Please enter the index of the skill "
                                                             "you want to use (1 - " +
                                                             str(len(usable_skills)) + "): "))
                                while skill_index < 1 or skill_index > len(usable_skills):
                                    skill_index = int(input("Sorry, invalid input! Please enter the "
                                                            "index of the skill "
                                                            "you want to use (1 - " +
                                                            str(len(usable_skills)) + "): "))

                                skill_to_use: Skill = usable_skills[skill_index - 1]
                                if skill_to_use.skill_type == "ATTACK":
                                    # Asking the user to select a target
                                    print("Below is a list of enemies you can attack.")
                                    enemy_index: int = 1  # initial value
                                    for enemy in curr_battle.team2.get_legendary_creatures():
                                        if enemy.get_is_alive():
                                            print("ENEMY #" + str(enemy_index))
                                            print(str(enemy) + "\n")
                                            enemy_index += 1

                                    chosen_enemy_index: int = int(input("Please enter the index of the "
                                                                        "enemy you want to attack (1 - " +
                                                                        str(len(curr_battle.
                                                                                team2.get_legendary_creatures())) +
                                                                        "): "))
                                    while chosen_enemy_index < 1 or chosen_enemy_index > len(curr_battle.
                                                                                team2.get_legendary_creatures()):
                                        chosen_enemy_index = int(input("Sorry, invalid input! "
                                                                       "Please enter the index of the "
                                                                       "enemy you want to attack (1 - " +
                                                                       str(len(curr_battle.
                                                                               team2.get_legendary_creatures())) +
                                                                       "): "))

                                    chosen_enemy_target: LegendaryCreature = curr_battle.team2. \
                                        get_legendary_creatures()[chosen_enemy_index - 1]
                                    curr_battle.whose_turn.have_turn(chosen_enemy_target, skill_to_use,
                                                                     trainer_battle_action)

                                elif skill_to_use.skill_type == "HEAL":
                                    # Asking the user to select who to heal
                                    print("Below is a list of allies you can heal.")
                                    ally_index: int = 1  # initial value
                                    for ally in curr_battle.team1.get_legendary_creatures():
                                        if ally.get_is_alive():
                                            print("ALLY #" + str(ally_index))
                                            print(str(ally) + "\n")
                                            ally_index += 1

                                    chosen_ally_index: int = int(input("Please enter the index of the "
                                                                       "ally you want to heal (1 - " +
                                                                       str(len(curr_battle.
                                                                               team1.get_legendary_creatures())) +
                                                                       "): "))
                                    while chosen_ally_index < 1 or chosen_ally_index > len(curr_battle.
                                                                            team1.get_legendary_creatures()):
                                        chosen_ally_index = int(input("Sorry, invalid input! "
                                                                      "Please enter the index of the "
                                                                      "ally you want to heal (1 - " +
                                                                      str(len(curr_battle.
                                                                              team1.get_legendary_creatures())) +
                                                                      "): "))

                                    chosen_ally_target: LegendaryCreature = curr_battle.team1. \
                                        get_legendary_creatures()[chosen_ally_index - 1]
                                    curr_battle.whose_turn.have_turn(chosen_ally_target, skill_to_use,
                                                                     trainer_battle_action)

                            elif trainer_battle_action == "NORMAL ATTACK":
                                # Asking the user to select a target
                                print("Below is a list of enemies you can attack.")
                                enemy_index: int = 1  # initial value
                                for enemy in curr_battle.team2.get_legendary_creatures():
                                    if enemy.get_is_alive():
                                        print("ENEMY #" + str(enemy_index))
                                        print(str(enemy) + "\n")
                                        enemy_index += 1

                                chosen_enemy_index: int = int(input("Please enter the index of the "
                                                                    "enemy you want to attack (1 - " +
                                                                    str(len(curr_battle.
                                                                            team2.get_legendary_creatures())) +
                                                                    "): "))
                                while chosen_enemy_index < 1 or chosen_enemy_index > len(curr_battle.
                                                                            team2.get_legendary_creatures()):
                                    chosen_enemy_index = int(input("Sorry, invalid input! "
                                                                   "Please enter the index of the "
                                                                   "enemy you want to attack (1 - " +
                                                                   str(len(curr_battle.
                                                                           team2.get_legendary_creatures())) +
                                                                   "): "))

                                chosen_enemy_target: LegendaryCreature = curr_battle.team2. \
                                    get_legendary_creatures()[chosen_enemy_index - 1]
                                curr_battle.whose_turn.have_turn(chosen_enemy_target, None, trainer_battle_action)

                            elif trainer_battle_action == "NORMAL HEAL":
                                # Asking the user to select who to heal
                                print("Below is a list of allies you can heal.")
                                ally_index: int = 1  # initial value
                                for ally in curr_battle.team1.get_legendary_creatures():
                                    if ally.get_is_alive():
                                        print("ALLY #" + str(ally_index))
                                        print(str(ally) + "\n")
                                        ally_index += 1

                                chosen_ally_index: int = int(input("Please enter the index of the "
                                                                   "ally you want to heal (1 - " +
                                                                   str(len(curr_battle.
                                                                           team1.get_legendary_creatures())) +
                                                                   "): "))
                                while chosen_ally_index < 1 or chosen_ally_index > len(curr_battle.
                                                                                    team1.get_legendary_creatures()):
                                    chosen_ally_index = int(input("Sorry, invalid input! "
                                                                  "Please enter the index of the "
                                                                  "ally you want to heal (1 - " +
                                                                  str(len(curr_battle.
                                                                          team1.get_legendary_creatures())) +
                                                                  "): "))

                                chosen_ally_target: LegendaryCreature = curr_battle.team1. \
                                    get_legendary_creatures()[chosen_ally_index - 1]
                                curr_battle.whose_turn.have_turn(chosen_ally_target, None,
                                                                 trainer_battle_action)
                            else:
                                pass

                            # Recovering magic points
                            curr_battle.whose_turn.recover_magic_points()
                            curr_battle.get_someone_to_move()

                        elif curr_battle.whose_turn in curr_battle.team2.get_legendary_creatures():
                            curr_moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                            chance: float = random.random()
                            trainer_battle_action: str = "NORMAL ATTACK" if chance <= 1 / 3 else \
                                "NORMAL HEAL" if 1 / 3 < chance <= 2 / 3 else "USE SKILL"
                            usable_skills: list = [skill for skill in curr_battle.whose_turn.get_skills()
                                                   if curr_battle.whose_turn.curr_magic_points >=
                                                   skill.magic_points_cost and isinstance(skill, Skill)]

                            # If there are no usable skills and 'trainer_battle_action' is set to "USE SKILL",
                            # change the value of 'trainer_battle_action'
                            if len(usable_skills) == 0:
                                trainer_battle_action = "NORMAL ATTACK" if random.random() < 0.5 else "NORMAL HEAL"

                            if trainer_battle_action == "NORMAL ATTACK":
                                # A normal attack occurs
                                moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                                target: LegendaryCreature = curr_battle.team1.get_legendary_creatures() \
                                    [random.randint(0, len(curr_battle.team1.get_legendary_creatures()) - 1)]
                                while not target.get_is_alive():
                                    target = curr_battle.team1.get_legendary_creatures() \
                                        [random.randint(0, len(curr_battle.team1.get_legendary_creatures()) - 1)]

                                moving_legendary_creature.have_turn(target, None, trainer_battle_action)
                            elif trainer_battle_action == "NORMAL HEAL":
                                # A normal heal occurs
                                moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                                target: LegendaryCreature = curr_battle.team2.get_legendary_creatures() \
                                    [random.randint(0, len(curr_battle.team2.get_legendary_creatures()) - 1)]
                                while not target.get_is_alive():
                                    target = curr_battle.team2.get_legendary_creatures() \
                                        [random.randint(0, len(curr_battle.team2.get_legendary_creatures()) - 1)]

                                moving_legendary_creature.have_turn(target, None, trainer_battle_action)
                            elif trainer_battle_action == "USE SKILL":
                                # A skill is used
                                moving_legendary_creature: LegendaryCreature = curr_battle.whose_turn
                                skill_to_use: Skill = usable_skills[random.randint(0, len(usable_skills) - 1)]
                                if skill_to_use.skill_type == "ATTACK":
                                    target: LegendaryCreature = curr_battle.team1.get_legendary_creatures() \
                                        [random.randint(0, len(curr_battle.team1.get_legendary_creatures()) - 1)]
                                    while not target.get_is_alive():
                                        target = curr_battle.team1.get_legendary_creatures() \
                                            [random.randint(0, len(curr_battle.team1.get_legendary_creatures()) - 1)]

                                    moving_legendary_creature.have_turn(target, skill_to_use, trainer_battle_action)
                                else:
                                    target: LegendaryCreature = curr_battle.team2.get_legendary_creatures() \
                                        [random.randint(0, len(curr_battle.team2.get_legendary_creatures()) - 1)]
                                    while not target.get_is_alive():
                                        target = curr_battle.team2.get_legendary_creatures() \
                                            [random.randint(0, len(curr_battle.team2.get_legendary_creatures()) - 1)]

                                    moving_legendary_creature.have_turn(target, skill_to_use, trainer_battle_action)
                            else:
                                pass

                            # Recovering magic points
                            curr_battle.whose_turn.recover_magic_points()
                            curr_battle.get_someone_to_move()

                        # Recovering magic points
                        curr_battle.whose_turn.recover_magic_points()

                    if curr_battle.winner == curr_battle.team1:
                        print("Congratulations! You won the battle!")
                        new_game.player_data.claim_reward(curr_battle.reward)
                        current_stage.is_cleared = True

                        # Checking whether the next stage is None or not. If yes, the player has cleared the level
                        if chosen_level.next_stage(curr_stage_number) is None:
                            new_game.player_data.claim_reward(chosen_level.clear_reward)
                            chosen_level.is_cleared = True
                            new_game.player_data.add_unlocked_level()
                        else:
                            # Move on to the next stage
                            current_stage = chosen_level.next_stage(curr_stage_number)
                            curr_stage_number += 1
                    elif curr_battle.winner == curr_battle.team2:
                        print("You lost the battle! Please come back stronger!")

                    # Restore all legendary creatures
                    curr_battle.team1.recover_all()
                    curr_battle.team2.recover_all()

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing = input("Do you want to continue playing 'Creature World Builder Lite'? ")

    # Saving game data and quitting the game.
    save_game_data(new_game, file_name)
    return 0


if __name__ == '__main__':
    main()
