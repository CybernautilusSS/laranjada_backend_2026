"""
- Menu principal
- Criação de personagem
- 3 classes
- Combate por turnos
- Grupo de aliados
- Inimigos variados
- Chefes
- Habilidades
- Efeitos de status
- Inventário
- Equipamentos
- Loja
- Ouro
- XP e níveis
- Missões
- Exploração
- Salvamento em JSON
- Carregamento de jogo
"""

import json
import os
import random
import time


# ============================================================
# CONFIGURAÇÕES
# ============================================================

SAVE_FILE = "save_rpg.json"
VERSION = "1.0"

WIDTH = 70


# ============================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPressione ENTER para continuar...")


def line(char="=", size=WIDTH):
    print(char * size)


def title(text):
    clear()
    line()
    print(text.center(WIDTH))
    line()


def ask_int(prompt, minimum, maximum):
    while True:
        try:
            value = int(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Digite um número entre {minimum} e {maximum}.")
        except ValueError:
            print("Digite um número válido.")


def ask_yes_no(prompt):
    while True:
        value = input(prompt + " [s/n]: ").strip().lower()
        if value in ("s", "sim"):
            return True
        if value in ("n", "nao", "não"):
            return False
        print("Digite s ou n.")


def chance(percent):
    return random.randint(1, 100) <= percent


# ============================================================
# CLASSE DE STATUS
# ============================================================

class StatusEffect:
    def __init__(self, name, turns, power=0):
        self.name = name
        self.turns = turns
        self.power = power

    def tick(self):
        self.turns -= 1

    def expired(self):
        return self.turns <= 0

    def to_dict(self):
        return {
            "name": self.name,
            "turns": self.turns,
            "power": self.power,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["turns"], data["power"])


# ============================================================
# CLASSE BASE DE PERSONAGEM
# ============================================================

class Character:
    def __init__(
        self,
        name,
        level,
        max_hp,
        max_mp,
        attack,
        defense,
        magic,
        speed,
    ):
        self.name = name
        self.level = level
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.speed = speed

        self.xp = 0
        self.xp_next = 100
        self.critical = 5

        self.statuses = []
        self.defending = False
        self.alive = True

    def is_alive(self):
        return self.hp > 0

    def receive_damage(self, amount):
        amount = max(1, int(amount))

        if self.defending:
            amount = max(1, amount // 2)

        self.hp -= amount

        if self.hp <= 0:
            self.hp = 0
            self.alive = False

        return amount

    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def restore_mp(self, amount):
        old_mp = self.mp
        self.mp = min(self.max_mp, self.mp + amount)
        return self.mp - old_mp

    def basic_attack(self, target):
        base = random.randint(
            max(1, self.attack - 4),
            self.attack + 7,
        )

        critical = chance(self.critical)

        if critical:
            base *= 2

        damage = max(1, base - target.defense)

        return target.receive_damage(damage), critical

    def add_status(self, status):
        for current in self.statuses:
            if current.name == status.name:
                current.turns = max(current.turns, status.turns)
                current.power = max(current.power, status.power)
                return
        self.statuses.append(status)

    def has_status(self, name):
        return any(
            status.name == name and status.turns > 0
            for status in self.statuses
        )

    def process_statuses(self):
        messages = []

        for status in list(self.statuses):
            if status.name == "Queimando":
                damage = self.receive_damage(status.power)
                messages.append(
                    f"{self.name} sofreu {damage} de dano de queimadura."
                )

            elif status.name == "Regeneração":
                healed = self.heal(status.power)
                messages.append(
                    f"{self.name} recuperou {healed} HP."
                )

            status.tick()

            if status.expired():
                self.statuses.remove(status)
                messages.append(
                    f"O efeito {status.name} terminou em {self.name}."
                )

        return messages

    def gain_xp(self, amount):
        self.xp += amount
        levels = 0

        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level_up()
            levels += 1

        return levels

    def level_up(self):
        self.level += 1
        self.max_hp += 18
        self.max_mp += 8
        self.attack += 4
        self.defense += 2
        self.magic += 3
        self.speed += 1
        self.critical = min(35, self.critical + 1)

        self.xp_next = int(self.xp_next * 1.25)

        self.hp = self.max_hp
        self.mp = self.max_mp
        self.alive = True

    def reset_battle(self):
        self.defending = False

    def status_text(self):
        if not self.statuses:
            return "Nenhum"

        return ", ".join(
            f"{s.name}({s.turns})"
            for s in self.statuses
        )

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "max_mp": self.max_mp,
            "mp": self.mp,
            "attack": self.attack,
            "defense": self.defense,
            "magic": self.magic,
            "speed": self.speed,
            "xp": self.xp,
            "xp_next": self.xp_next,
            "critical": self.critical,
            "statuses": [s.to_dict() for s in self.statuses],
        }


# ============================================================
# CLASSES DO JOGADOR
# ============================================================

class Warrior(Character):
    def __init__(self, name):
        super().__init__(
            name,
            1,
            170,
            40,
            25,
            14,
            5,
            8,
        )
        self.class_name = "Guerreiro"
        self.critical = 8

    def skills(self):
        return [
            "Golpe Poderoso",
            "Investida",
            "Provocar",
            "Fúria",
        ]

    def use_skill(self, name, target, party):
        if name == "Golpe Poderoso":
            return self.power_strike(target)

        if name == "Investida":
            return self.charge(target)

        if name == "Provocar":
            return self.taunt(target)

        if name == "Fúria":
            return self.fury()

        return "Habilidade inválida."

    def power_strike(self, target):
        cost = 8

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        raw = self.attack + random.randint(14, 25)
        damage = target.receive_damage(
            max(1, raw - target.defense)
        )

        return f"Golpe Poderoso causou {damage} de dano."

    def charge(self, target):
        cost = 12

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        raw = self.attack + self.speed + random.randint(12, 22)
        damage = target.receive_damage(
            max(1, raw - target.defense)
        )

        return f"Investida causou {damage} de dano."

    def taunt(self, target):
        cost = 5

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        target.attack = max(1, target.attack - 5)
        target.add_status(
            StatusEffect("Provocado", 2, 0)
        )

        return "O inimigo foi provocado e perdeu ataque."

    def fury(self):
        cost = 15

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        self.add_status(
            StatusEffect("Fúria", 3, 8)
        )

        self.attack += 8

        return "O Guerreiro entrou em Fúria!"


class Mage(Character):
    def __init__(self, name):
        super().__init__(
            name,
            1,
            100,
            110,
            10,
            7,
            30,
            9,
        )
        self.class_name = "Mago"
        self.critical = 6

    def skills(self):
        return [
            "Bola de Fogo",
            "Raio Arcano",
            "Cura",
            "Cura em Grupo",
            "Barreira",
        ]

    def use_skill(self, name, target, party):
        if name == "Bola de Fogo":
            return self.fireball(target)

        if name == "Raio Arcano":
            return self.arcane_bolt(target)

        if name == "Cura":
            return self.heal_target(party)

        if name == "Cura em Grupo":
            return self.group_heal(party)

        if name == "Barreira":
            return self.barrier()

        return "Habilidade inválida."

    def fireball(self, target):
        cost = 14

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        raw = self.magic * 2 + random.randint(18, 30)

        damage = target.receive_damage(
            max(1, raw - target.defense // 2)
        )

        target.add_status(
            StatusEffect("Queimando", 3, 8)
        )

        return f"Bola de Fogo causou {damage} de dano."

    def arcane_bolt(self, target):
        cost = 20

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        raw = self.magic * 2 + random.randint(20, 35)

        damage = target.receive_damage(raw)

        return f"Raio Arcano causou {damage} de dano."

    def heal_target(self, party):
        cost = 16

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        target = min(
            (
                member
                for member in party
                if member.is_alive()
            ),
            key=lambda member: member.hp / member.max_hp,
            default=self,
        )

        amount = target.heal(
            45 + self.magic
        )

        return f"{target.name} recuperou {amount} HP."

    def group_heal(self, party):
        cost = 28

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        total = 0

        for member in party:
            if member.is_alive():
                total += member.heal(
                    20 + self.magic // 2
                )

        return f"Cura em Grupo restaurou {total} HP."

    def barrier(self):
        cost = 18

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        self.add_status(
            StatusEffect("Barreira", 3, 0)
        )

        self.defending = True

        return "O Mago criou uma Barreira."


class Archer(Character):
    def __init__(self, name):
        super().__init__(
            name,
            1,
            120,
            65,
            22,
            9,
            12,
            17,
        )
        self.class_name = "Arqueiro"
        self.critical = 14

    def skills(self):
        return [
            "Tiro Preciso",
            "Flecha Dupla",
            "Chuva de Flechas",
            "Evasão",
        ]

    def use_skill(self, name, target, party):
        if name == "Tiro Preciso":
            return self.precise_shot(target)

        if name == "Flecha Dupla":
            return self.double_arrow(target)

        if name == "Chuva de Flechas":
            return self.arrow_rain(target)

        if name == "Evasão":
            return self.evasion()

        return "Habilidade inválida."

    def precise_shot(self, target):
        cost = 8

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        raw = self.attack + random.randint(18, 30)

        damage = target.receive_damage(
            max(1, raw - target.defense // 2)
        )

        return f"Tiro Preciso causou {damage} de dano."

    def double_arrow(self, target):
        cost = 13

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        total = 0

        for _ in range(2):
            raw = self.attack // 2 + random.randint(8, 15)
            total += target.receive_damage(
                max(1, raw - target.defense)
            )

        return f"Flecha Dupla causou {total} de dano."

    def arrow_rain(self, target):
        cost = 24

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        raw = self.attack + random.randint(25, 40)

        damage = target.receive_damage(
            max(1, raw - target.defense // 2)
        )

        return f"Chuva de Flechas causou {damage} de dano."

    def evasion(self):
        cost = 10

        if self.mp < cost:
            return "MP insuficiente."

        self.mp -= cost

        self.add_status(
            StatusEffect("Evasão", 3, 0)
        )

        return "O Arqueiro aumentou sua evasão."


# ============================================================
# INIMIGOS
# ============================================================

class Enemy(Character):
    def __init__(
        self,
        name,
        kind,
        level,
        hp,
        mp,
        attack,
        defense,
        magic,
        speed,
        xp_reward,
        gold_reward,
        boss=False,
    ):
        super().__init__(
            name,
            level,
            hp,
            mp,
            attack,
            defense,
            magic,
            speed,
        )

        self.kind = kind
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.boss = boss

    def choose_action(self, party):
        alive = [
            member
            for member in party
            if member.is_alive()
        ]

        if not alive:
            return None

        target = random.choice(alive)

        if self.boss and chance(25):
            return "magic", target

        if chance(15):
            return "heavy", target

        return "attack", target

    def attack_target(self, target):
        raw = random.randint(
            max(1, self.attack - 4),
            self.attack + 7,
        )

        if self.boss and chance(10):
            raw += self.magic

        damage = max(
            1,
            raw - target.defense
        )

        if target.has_status("Evasão") and chance(35):
            return 0

        return target.receive_damage(damage)


# ============================================================
# FÁBRICA DE INIMIGOS
# ============================================================

def create_enemy(kind, level=1):
    scale = max(0, level - 1)

    if kind == "Slime":
        return Enemy(
            "Slime",
            "Monstro",
            level,
            55 + scale * 10,
            5,
            10 + scale * 2,
            3 + scale,
            2,
            5,
            25 + scale * 5,
            12 + scale * 2,
        )

    if kind == "Goblin":
        return Enemy(
            "Goblin",
            "Humanoide",
            level,
            70 + scale * 14,
            15,
            14 + scale * 3,
            5 + scale,
            3,
            10 + scale,
            40 + scale * 8,
            18 + scale * 3,
        )

    if kind == "Lobo":
        return Enemy(
            "Lobo Sombrio",
            "Fera",
            level,
            80 + scale * 16,
            10,
            18 + scale * 3,
            6 + scale,
            2,
            16 + scale,
            48 + scale * 10,
            24 + scale * 4,
        )

    if kind == "Orc":
        return Enemy(
            "Orc",
            "Humanoide",
            level,
            145 + scale * 20,
            25,
            24 + scale * 4,
            10 + scale * 2,
            5,
            7,
            90 + scale * 15,
            45 + scale * 6,
        )

    if kind == "Necromante":
        return Enemy(
            "Necromante",
            "Mago",
            level,
            125 + scale * 18,
            100,
            14 + scale * 2,
            7 + scale,
            28 + scale * 4,
            10,
            125 + scale * 18,
            65 + scale * 8,
        )

    if kind == "Golem":
        return Enemy(
            "Golem de Pedra",
            "Constructo",
            level,
            280 + scale * 35,
            30,
            31 + scale * 4,
            19 + scale * 3,
            8,
            3,
            200 + scale * 25,
            95 + scale * 10,
        )

    if kind == "Dragao":
        return Enemy(
            "Dragão Ancião",
            "Dragão",
            level,
            750 + scale * 80,
            200,
            60 + scale * 7,
            26 + scale * 3,
            45 + scale * 5,
            15,
            1400 + scale * 120,
            700 + scale * 60,
            True,
        )

    return create_enemy("Slime", level)


# ============================================================
# ITENS
# ============================================================

class Item:
    def __init__(self, name, item_type, value, quantity=0):
        self.name = name
        self.item_type = item_type
        self.value = value
        self.quantity = quantity

    def to_dict(self):
        return {
            "name": self.name,
            "item_type": self.item_type,
            "value": self.value,
            "quantity": self.quantity,
        }


def default_items():
    return {
        "Poção": 3,
        "Éter": 2,
        "Poção Grande": 1,
        "Antídoto": 2,
        "Elixir": 0,
    }


# ============================================================
# EQUIPAMENTOS
# ============================================================

class Equipment:
    def __init__(
        self,
        name,
        slot,
        attack=0,
        defense=0,
        magic=0,
        speed=0,
        price=0,
    ):
        self.name = name
        self.slot = slot
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.speed = speed
        self.price = price

    def to_dict(self):
        return {
            "name": self.name,
            "slot": self.slot,
            "attack": self.attack,
            "defense": self.defense,
            "magic": self.magic,
            "speed": self.speed,
            "price": self.price,
        }


WEAPONS = [
    Equipment(
        "Espada de Ferro",
        "weapon",
        attack=5,
        price=100,
    ),
    Equipment(
        "Espada Reforçada",
        "weapon",
        attack=12,
        price=220,
    ),
    Equipment(
        "Lâmina Real",
        "weapon",
        attack=22,
        magic=3,
        price=500,
    ),
    Equipment(
        "Cajado Arcano",
        "weapon",
        attack=3,
        magic=18,
        price=450,
    ),
    Equipment(
        "Arco Élfico",
        "weapon",
        attack=16,
        speed=5,
        price=420,
    ),
]


ARMORS = [
    Equipment(
        "Armadura de Couro",
        "armor",
        defense=4,
        price=100,
    ),
    Equipment(
        "Armadura Reforçada",
        "armor",
        defense=10,
        price=230,
    ),
    Equipment(
        "Armadura Real",
        "armor",
        defense=20,
        price=550,
    ),
]


# ============================================================
# MISSÕES
# ============================================================

class Quest:
    def __init__(
        self,
        name,
        description,
        target,
        required,
        reward_gold,
        reward_xp,
    ):
        self.name = name
        self.description = description
        self.target = target
        self.required = required
        self.progress = 0
        self.reward_gold = reward_gold
        self.reward_xp = reward_xp
        self.completed = False
        self.claimed = False

    def advance(self, target, amount=1):
        if self.completed:
            return

        if target == self.target:
            self.progress += amount

            if self.progress >= self.required:
                self.progress = self.required
                self.completed = True

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "target": self.target,
            "required": self.required,
            "progress": self.progress,
            "reward_gold": self.reward_gold,
            "reward_xp": self.reward_xp,
            "completed": self.completed,
            "claimed": self.claimed,
        }

    @classmethod
    def from_dict(cls, data):
        quest = cls(
            data["name"],
            data["description"],
            data["target"],
            data["required"],
            data["reward_gold"],
            data["reward_xp"],
        )

        quest.progress = data["progress"]
        quest.completed = data["completed"]
        quest.claimed = data["claimed"]

        return quest


# ============================================================
# GERENCIADOR DO JOGO
# ============================================================

class Game:
    def __init__(self):
        self.player = None
        self.party = []
        self.enemies = []

        self.gold = 150
        self.day = 1
        self.location = "Vila de Aurora"

        self.inventory = default_items()

        self.equipment = {
            "weapon": None,
            "armor": None,
        }

        self.quests = [
            Quest(
                "Caçador de Goblins",
                "Derrote 5 Goblins.",
                "Goblin",
                5,
                100,
                80,
            ),
            Quest(
                "Ameaça Sombria",
                "Derrote 3 Lobos Sombrios.",
                "Lobo",
                3,
                120,
                100,
            ),
            Quest(
                "O Gigante",
                "Derrote um Golem.",
                "Golem",
                1,
                250,
                220,
            ),
        ]

        self.victories = 0
        self.defeats = 0
        self.battle_number = 0

    def create_player(self):
        title("CRIAÇÃO DE PERSONAGEM")

        name = input("Nome do personagem: ").strip()

        if not name:
            name = "Aren"

        print("\nEscolha uma classe:")
        print("1 - Guerreiro")
        print("2 - Mago")
        print("3 - Arqueiro")

        choice = ask_int("Classe: ", 1, 3)

        if choice == 1:
            self.player = Warrior(name)

        elif choice == 2:
            self.player = Mage(name)

        else:
            self.player = Archer(name)

        self.party = [self.player]

        print(
            f"\n{name} começou sua aventura como "
            f"{self.player.class_name}!"
        )

        pause()

    def add_ally(self, ally):
        self.party.append(ally)

    def heal_party(self):
        for member in self.party:
            member.hp = member.max_hp
            member.mp = member.max_mp
            member.alive = True
            member.statuses.clear()

    def show_party(self):
        title("GRUPO")

        for i, member in enumerate(self.party, 1):
            print(
                f"{i}. {member.name} "
                f"[{member.class_name}] "
                f"Nv.{member.level}"
            )

            print(
                f"   HP {member.hp}/{member.max_hp} "
                f"| MP {member.mp}/{member.max_mp}"
            )

            print(
                f"   ATQ {member.attack} "
                f"| DEF {member.defense} "
                f"| MAG {member.magic} "
                f"| SPD {member.speed}"
            )

            print(
                f"   XP {member.xp}/{member.xp_next}"
            )

            print(
                f"   Status: {member.status_text()}"
            )

            line("-", 55)

        pause()

    def show_inventory(self):
        title("INVENTÁRIO")

        for name, quantity in self.inventory.items():
            print(f"{name}: {quantity}")

        print(f"\nOuro: {self.gold}")

        pause()

    def show_equipment(self):
        title("EQUIPAMENTOS")

        weapon = self.equipment.get("weapon")
        armor = self.equipment.get("armor")

        print(
            "Arma:",
            weapon.name if weapon else "Nenhuma"
        )

        print(
            "Armadura:",
            armor.name if armor else "Nenhuma"
        )

        pause()

    def equip(self, equipment):
        slot = equipment.slot
        old = self.equipment.get(slot)

        if old:
            self.remove_equipment_stats(old)

        self.equipment[slot] = equipment
        self.apply_equipment_stats(equipment)

        print(f"{equipment.name} equipado.")

    def apply_equipment_stats(self, equipment):
        self.player.attack += equipment.attack
        self.player.defense += equipment.defense
        self.player.magic += equipment.magic
        self.player.speed += equipment.speed

    def remove_equipment_stats(self, equipment):
        self.player.attack -= equipment.attack
        self.player.defense -= equipment.defense
        self.player.magic -= equipment.magic
        self.player.speed -= equipment.speed

    def use_item(self):
        title("USAR ITEM")

        available = [
            name
            for name, quantity in self.inventory.items()
            if quantity > 0
        ]

        if not available:
            print("Você não possui itens.")
            pause()
            return

        for i, name in enumerate(available, 1):
            print(f"{i} - {name}")

        print("0 - Voltar")

        choice = ask_int(
            "Escolha: ",
            0,
            len(available),
        )

        if choice == 0:
            return

        item = available[choice - 1]

        if item == "Poção":
            healed = self.player.heal(50)
            self.inventory[item] -= 1
            print(
                f"{self.player.name} recuperou "
                f"{healed} HP."
            )

        elif item == "Poção Grande":
            healed = self.player.heal(120)
            self.inventory[item] -= 1
            print(
                f"{self.player.name} recuperou "
                f"{healed} HP."
            )

        elif item == "Éter":
            restored = self.player.restore_mp(60)
            self.inventory[item] -= 1
            print(
                f"{self.player.name} recuperou "
                f"{restored} MP."
            )

        elif item == "Antídoto":
            if self.player.statuses:
                self.player.statuses.clear()
                self.inventory[item] -= 1
                print("Todos os efeitos negativos foram removidos.")
            else:
                print("Nenhum efeito negativo.")

        elif item == "Elixir":
            self.player.hp = self.player.max_hp
            self.player.mp = self.player.max_mp
            self.inventory[item] -= 1
            print("HP e MP restaurados.")

        pause()

    # --------------------------------------------------------
    # EXPLORAÇÃO
    # --------------------------------------------------------

    def explore(self, region):
        self.location = region
        self.day += 1

        title(f"EXPLORANDO: {region}")

        roll = random.randint(1, 100)

        if region == "Floresta":
            if roll <= 35:
                enemies = [
                    create_enemy(
                        "Goblin",
                        self.player.level,
                    )
                ]

            elif roll <= 65:
                enemies = [
                    create_enemy(
                        "Lobo",
                        self.player.level,
                    ),
                    create_enemy(
                        "Goblin",
                        max(1, self.player.level - 1),
                    ),
                ]

            elif roll <= 85:
                enemies = [
                    create_enemy(
                        "Slime",
                        self.player.level,
                    ),
                    create_enemy(
                        "Lobo",
                        self.player.level,
                    ),
                ]

            else:
                self.random_treasure()
                return

        elif region == "Montanha":
            if roll <= 40:
                enemies = [
                    create_enemy(
                        "Orc",
                        self.player.level,
                    )
                ]

            elif roll <= 75:
                enemies = [
                    create_enemy(
                        "Orc",
                        self.player.level,
                    ),
                    create_enemy(
                        "Lobo",
                        self.player.level,
                    ),
                ]

            elif roll <= 90:
                enemies = [
                    create_enemy(
                        "Golem",
                        self.player.level + 1,
                    )
                ]

            else:
                self.random_treasure()
                return

        elif region == "Caverna":
            if roll <= 35:
                enemies = [
                    create_enemy(
                        "Necromante",
                        self.player.level,
                    )
                ]

            elif roll <= 70:
                enemies = [
                    create_enemy(
                        "Golem",
                        self.player.level,
                    ),
                    create_enemy(
                        "Necromante",
                        self.player.level,
                    ),
                ]

            elif roll <= 92:
                enemies = [
                    create_enemy(
                        "Golem",
                        self.player.level + 1,
                    )
                ]

            else:
                enemies = [
                    create_enemy(
                        "Dragao",
                        self.player.level + 2,
                    )
                ]

        else:
            enemies = [
                create_enemy(
                    "Slime",
                    self.player.level,
                )
            ]

        self.start_battle(enemies)
        self.battle_loop()

    def random_treasure(self):
        print("Você encontrou um baú!")

        reward = random.randint(30, 100)
        self.gold += reward

        print(
            f"Você encontrou {reward} moedas de ouro."
        )

        if chance(50):
            item = random.choice(
                [
                    "Poção",
                    "Éter",
                    "Antídoto",
                ]
            )

            self.inventory[item] += 1

            print(
                f"Também encontrou 1x {item}."
            )

        pause()

    # --------------------------------------------------------
    # COMBATE
    # --------------------------------------------------------

    def start_battle(self, enemies):
        self.enemies = enemies
        self.battle_number += 1

        for member in self.party:
            member.reset_battle()

        for enemy in self.enemies:
            enemy.reset_battle()

        print(
            f"\nBATALHA #{self.battle_number}"
        )

        pause()

    def alive_party(self):
        return [
            member
            for member in self.party
            if member.is_alive()
        ]

    def alive_enemies(self):
        return [
            enemy
            for enemy in self.enemies
            if enemy.is_alive()
        ]

    def battle_loop(self):
        while (
            self.alive_party()
            and self.alive_enemies()
        ):
            self.player_turn()
            if not self.alive_enemies():
                break

            self.enemy_turn()

        if self.alive_party():
            self.victory()
        else:
            self.defeat()

    def display_battle(self):
        clear()
        line()
        print(
            f"BATALHA #{self.battle_number}".center(WIDTH)
        )
        line()

        print("SEU GRUPO")
        line("-", 30)

        for member in self.party:
            state = "VIVO" if member.is_alive() else "CAÍDO"

            print(
                f"{member.name} "
                f"[{member.class_name}] "
                f"Nv.{member.level} - {state}"
            )

            print(
                f" HP {member.hp}/{member.max_hp}"
                f" | MP {member.mp}/{member.max_mp}"
            )

        print("\nINIMIGOS")
        line("-", 30)

        for i, enemy in enumerate(
            self.enemies,
            1,
        ):
            state = "VIVO" if enemy.is_alive() else "DERROTADO"

            print(
                f"{i}. {enemy.name} "
                f"Nv.{enemy.level} - {state}"
            )

            print(
                f" HP {enemy.hp}/{enemy.max_hp}"
            )

        line()

    def choose_enemy(self):
        alive = self.alive_enemies()

        if not alive:
            return None

        for i, enemy in enumerate(alive, 1):
            print(
                f"{i} - {enemy.name} "
                f"HP {enemy.hp}/{enemy.max_hp}"
            )

        choice = ask_int(
            "Escolha o alvo: ",
            1,
            len(alive),
        )

        return alive[choice - 1]

    def choose_member(self):
        alive = self.alive_party()

        if not alive:
            return None

        for i, member in enumerate(alive, 1):
            print(
                f"{i} - {member.name} "
                f"HP {member.hp}/{member.max_hp}"
            )

        choice = ask_int(
            "Escolha o personagem: ",
            1,
            len(alive),
        )

        return alive[choice - 1]

    def player_turn(self):
        for member in self.alive_party():
            if not self.alive_enemies():
                return

            member.defending = False

            messages = member.process_statuses()

            for message in messages:
                print(message)

            if not member.is_alive():
                continue

            self.display_battle()

            print(
                f"\nTurno de {member.name}"
            )

            print("1 - Ataque básico")
            print("2 - Habilidade")
            print("3 - Defender")
            print("4 - Usar item")

            action = ask_int(
                "Ação: ",
                1,
                4,
            )

            if action == 1:
                target = self.choose_enemy()

                if target:
                    damage, critical = member.basic_attack(
                        target
                    )

                    if damage == 0:
                        print(
                            f"{member.name} errou!"
                        )

                    elif critical:
                        print(
                            f"CRÍTICO! "
                            f"{member.name} causou "
                            f"{damage} de dano!"
                        )

                    else:
                        print(
                            f"{member.name} causou "
                            f"{damage} de dano."
                        )

            elif action == 2:
                self.skill_menu(member)

            elif action == 3:
                member.defending = True

                print(
                    f"{member.name} está defendendo."
                )

            elif action == 4:
                self.battle_item(member)

            pause()

    def skill_menu(self, member):
        title(
            f"HABILIDADES - {member.name}"
        )

        skills = member.skills()

        for i, skill in enumerate(skills, 1):
            print(f"{i} - {skill}")

        print("0 - Cancelar")

        choice = ask_int(
            "Escolha: ",
            0,
            len(skills),
        )

        if choice == 0:
            return

        skill_name = skills[choice - 1]

        target = None

        if skill_name not in (
            "Cura",
            "Cura em Grupo",
            "Barreira",
            "Evasão",
            "Fúria",
        ):
            target = self.choose_enemy()

        result = member.use_skill(
            skill_name,
            target,
            self.party,
        )

        print(result)

    def battle_item(self, member):
        print("\nItens:")
        print("1 - Poção")
        print("2 - Poção Grande")
        print("3 - Éter")
        print("4 - Antídoto")
        print("5 - Elixir")
        print("0 - Cancelar")

        choice = ask_int(
            "Escolha: ",
            0,
            5,
        )

        if choice == 0:
            return

        names = {
            1: "Poção",
            2: "Poção Grande",
            3: "Éter",
            4: "Antídoto",
            5: "Elixir",
        }

        item = names[choice]

        if self.inventory[item] <= 0:
            print("Você não possui esse item.")
            return

        if item == "Poção":
            amount = member.heal(50)
            print(
                f"{member.name} recuperou "
                f"{amount} HP."
            )

        elif item == "Poção Grande":
            amount = member.heal(120)
            print(
                f"{member.name} recuperou "
                f"{amount} HP."
            )

        elif item == "Éter":
            amount = member.restore_mp(60)
            print(
                f"{member.name} recuperou "
                f"{amount} MP."
            )

        elif item == "Antídoto":
            member.statuses.clear()
            print(
                f"Efeitos de {member.name} removidos."
            )

        elif item == "Elixir":
            member.hp = member.max_hp
            member.mp = member.max_mp
            print(
                f"{member.name} foi completamente restaurado."
            )

        self.inventory[item] -= 1

    def enemy_turn(self):
        print("\n--- TURNO DOS INIMIGOS ---")

        for enemy in self.alive_enemies():
            messages = enemy.process_statuses()

            for message in messages:
                print(message)

            if not enemy.is_alive():
                continue

            action, target = enemy.choose_action(
                self.party
            )

            if action == "magic":
                raw = (
                    enemy.magic
                    + random.randint(15, 35)
                )

                damage = target.receive_damage(
                    max(
                        1,
                        raw - target.defense // 2,
                    )
                )

                print(
                    f"{enemy.name} lançou magia "
                    f"e causou {damage} de dano."
                )

            elif action == "heavy":
                raw = (
                    enemy.attack
                    + random.randint(12, 25)
                )

                damage = target.receive_damage(
                    max(
                        1,
                        raw - target.defense,
                    )
                )

                print(
                    f"{enemy.name} usou ataque pesado "
                    f"e causou {damage} de dano."
                )

            else:
                damage = enemy.attack_target(
                    target
                )

                if damage == 0:
                    print(
                        f"{enemy.name} errou o ataque."
                    )

                else:
                    print(
                        f"{enemy.name} atacou "
                        f"{target.name} e causou "
                        f"{damage} de dano."
                    )

            if not self.alive_party():
                break

        pause()

    def victory(self):
        title("VITÓRIA!")

        total_xp = sum(
            enemy.xp_reward
            for enemy in self.enemies
        )

        total_gold = sum(
            enemy.gold_reward
            for enemy in self.enemies
        )

        self.gold += total_gold

        print(
            f"Você recebeu {total_xp} XP."
        )

        print(
            f"Você recebeu {total_gold} ouro."
        )

        for member in self.party:
            if member.is_alive():
                levels = member.gain_xp(
                    total_xp
                )

                if levels:
                    print(
                        f"{member.name} subiu "
                        f"{levels} nível(is)!"
                    )

        for enemy in self.enemies:
            self.update_quests(enemy)

        self.victories += 1

        if any(
            enemy.boss
            for enemy in self.enemies
        ):
            print(
                "\nVocê derrotou um CHEFE!"
            )

        if chance(30):
            item = random.choice(
                [
                    "Poção",
                    "Éter",
                    "Poção Grande",
                    "Antídoto",
                ]
            )

            self.inventory[item] += 1

            print(
                f"Você encontrou 1x {item}."
            )

        pause()

    def defeat(self):
        title("DERROTA")

        self.defeats += 1

        print(
            "Seu grupo foi derrotado."
        )

        print(
            "Você acordou na Vila de Aurora."
        )

        self.gold = max(
            0,
            self.gold - 30,
        )

        self.heal_party()

        pause()

    # --------------------------------------------------------
    # QUESTS
    # --------------------------------------------------------

    def update_quests(self, enemy):
        for quest in self.quests:
            quest.advance(
                enemy.kind
            )

    def quest_menu(self):
        title("MISSÕES")

        for quest in self.quests:
            state = "CONCLUÍDA" if quest.completed else "EM ANDAMENTO"

            print(
                f"{quest.name} - {state}"
            )

            print(
                quest.description
            )

            print(
                f"Progresso: "
                f"{quest.progress}/{quest.required}"
            )

            if (
                quest.completed
                and not quest.claimed
            ):
                print(
                    "Recompensa disponível!"
                )

            line("-", 55)

        claimable = [
            quest
            for quest in self.quests
            if quest.completed
            and not quest.claimed
        ]

        if claimable:
            print(
                "Existem recompensas para receber."
            )

            if ask_yes_no(
                "Receber recompensas agora?"
            ):
                for quest in claimable:
                    self.gold += quest.reward_gold

                    self.player.gain_xp(
                        quest.reward_xp
                    )

                    quest.claimed = True

                    print(
                        f"{quest.name}: "
                        f"+{quest.reward_gold} ouro "
                        f"+{quest.reward_xp} XP"
                    )

        pause()

    # --------------------------------------------------------
    # LOJA
    # --------------------------------------------------------

    def shop(self):
        while True:
            title("LOJA DE AURORA")

            print(
                f"Ouro: {self.gold}\n"
            )

            print("1 - Poção ................. 30")
            print("2 - Poção Grande .......... 80")
            print("3 - Éter .................. 40")
            print("4 - Antídoto .............. 25")
            print("5 - Elixir ................ 250")
            print("6 - Espada Reforçada ...... 220")
            print("7 - Lâmina Real ........... 500")
            print("8 - Cajado Arcano ......... 450")
            print("9 - Arco Élfico ........... 420")
            print("10 - Armadura Reforçada .. 230")
            print("11 - Armadura Real ........ 550")
            print("0 - Voltar")

            choice = ask_int(
                "Escolha: ",
                0,
                11,
            )

            if choice == 0:
                return

            if choice <= 5:
                items = {
                    1: ("Poção", 30),
                    2: ("Poção Grande", 80),
                    3: ("Éter", 40),
                    4: ("Antídoto", 25),
                    5: ("Elixir", 250),
                }

                name, price = items[choice]

                if self.gold < price:
                    print("Ouro insuficiente.")
                else:
                    self.gold -= price
                    self.inventory[name] += 1
                    print(
                        f"Você comprou 1x {name}."
                    )

                pause()
                continue

            equipment = None

            if choice == 6:
                equipment = WEAPONS[1]

            elif choice == 7:
                equipment = WEAPONS[2]

            elif choice == 8:
                equipment = WEAPONS[3]

            elif choice == 9:
                equipment = WEAPONS[4]

            elif choice == 10:
                equipment = ARMORS[1]

            elif choice == 11:
                equipment = ARMORS[2]

            if equipment:
                if self.gold < equipment.price:
                    print("Ouro insuficiente.")
                else:
                    self.gold -= equipment.price
                    self.equip(equipment)

                pause()

    # --------------------------------------------------------
    # DESCANSO
    # --------------------------------------------------------

    def rest(self):
        title("POUSADA")

        price = 25

        print(
            f"Uma noite custa {price} ouro."
        )

        if self.gold < price:
            print("Você não possui ouro suficiente.")
            pause()
            return

        if ask_yes_no("Deseja descansar?"):
            self.gold -= price
            self.heal_party()
            self.day += 1

            print(
                "Seu grupo foi completamente restaurado."
            )

        pause()

    # --------------------------------------------------------
    # STATUS DO PERSONAGEM
    # --------------------------------------------------------

    def character_screen(self):
        title("PERSONAGEM")

        p = self.player

        print(
            f"Nome: {p.name}"
        )

        print(
            f"Classe: {p.class_name}"
        )

        print(
            f"Nível: {p.level}"
        )

        print(
            f"HP: {p.hp}/{p.max_hp}"
        )

        print(
            f"MP: {p.mp}/{p.max_mp}"
        )

        print(
            f"Ataque: {p.attack}"
        )

        print(
            f"Defesa: {p.defense}"
        )

        print(
            f"Magia: {p.magic}"
        )

        print(
            f"Velocidade: {p.speed}"
        )

        print(
            f"Crítico: {p.critical}%"
        )

        print(
            f"XP: {p.xp}/{p.xp_next}"
        )

        print(
            f"Ouro: {self.gold}"
        )

        pause()

    # --------------------------------------------------------
    # SAVE / LOAD
    # --------------------------------------------------------

    def save(self):
        data = {
            "version": VERSION,
            "gold": self.gold,
            "day": self.day,
            "location": self.location,
            "inventory": self.inventory,
            "victories": self.victories,
            "defeats": self.defeats,
            "battle_number": self.battle_number,
            "player": self.player.to_dict(),
            "quests": [
                quest.to_dict()
                for quest in self.quests
            ],
        }

        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

        print(
            "\nJogo salvo com sucesso."
        )

        pause()

    def load(self):
        if not os.path.exists(SAVE_FILE):
            print(
                "Nenhum save encontrado."
            )
            pause()
            return False

        try:
            with open(
                SAVE_FILE,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            self.gold = data["gold"]
            self.day = data["day"]
            self.location = data["location"]
            self.inventory = data["inventory"]
            self.victories = data["victories"]
            self.defeats = data["defeats"]
            self.battle_number = data["battle_number"]

            player_data = data["player"]

            class_map = {
                "Guerreiro": Warrior,
                "Mago": Mage,
                "Arqueiro": Archer,
            }

            class_name = player_data.get(
                "class_name",
                "Guerreiro",
            )

            # Identifica a classe pela estrutura salva.
            if player_data["max_hp"] >= 150:
                player = Warrior(
                    player_data["name"]
                )
            elif player_data["max_mp"] >= 90:
                player = Mage(
                    player_data["name"]
                )
            else:
                player = Archer(
                    player_data["name"]
                )

            player.level = player_data["level"]
            player.max_hp = player_data["max_hp"]
            player.hp = player_data["hp"]
            player.max_mp = player_data["max_mp"]
            player.mp = player_data["mp"]
            player.attack = player_data["attack"]
            player.defense = player_data["defense"]
            player.magic = player_data["magic"]
            player.speed = player_data["speed"]
            player.xp = player_data["xp"]
            player.xp_next = player_data["xp_next"]
            player.critical = player_data["critical"]

            player.statuses = [
                StatusEffect.from_dict(status)
                for status in player_data.get(
                    "statuses",
                    [],
                )
            ]

            self.player = player
            self.party = [player]

            self.quests = [
                Quest.from_dict(q)
                for q in data["quests"]
            ]

            print(
                "Save carregado com sucesso."
            )

            pause()

            return True

        except (
            OSError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ) as error:
            print(
                "Erro ao carregar o save:",
                error,
            )

            pause()

            return False

    # --------------------------------------------------------
    # MENU PRINCIPAL
    # --------------------------------------------------------

    def main_menu(self):
        while True:
            title("RPG DE TURNO - PYTHON")

            print(
                "1 - Novo jogo"
            )

            print(
                "2 - Carregar jogo"
            )

            print(
                "3 - Sair"
            )

            choice = ask_int(
                "Escolha: ",
                1,
                3,
            )

            if choice == 1:
                self.create_player()
                self.game_loop()
                return

            if choice == 2:
                if self.load():
                    self.game_loop()
                    return

            if choice == 3:
                print(
                    "Até a próxima!"
                )
                return

    # --------------------------------------------------------
    # LOOP DO JOGO
    # --------------------------------------------------------

    def game_loop(self):
        while True:
            title(
                f"VILA DE AURORA - DIA {self.day}"
            )

            print(
                f"Herói: {self.player.name}"
            )

            print(
                f"Classe: {self.player.class_name}"
            )

            print(
                f"Nível: {self.player.level}"
            )

            print(
                f"Ouro: {self.gold}"
            )

            print()

            print(
                "1 - Explorar Floresta"
            )

            print(
                "2 - Explorar Montanha"
            )

            print(
                "3 - Explorar Caverna"
            )

            print(
                "4 - Loja"
            )

            print(
                "5 - Pousada"
            )

            print(
                "6 - Personagem"
            )

            print(
                "7 - Grupo"
            )

            print(
                "8 - Inventário"
            )

            print(
                "9 - Equipamentos"
            )

            print(
                "10 - Missões"
            )

            print(
                "11 - Usar item"
            )

            print(
                "12 - Salvar"
            )

            print(
                "13 - Sair"
            )

            choice = ask_int(
                "Escolha: ",
                1,
                13,
            )

            if choice == 1:
                self.explore("Floresta")

            elif choice == 2:
                self.explore("Montanha")

            elif choice == 3:
                self.explore("Caverna")

            elif choice == 4:
                self.shop()

            elif choice == 5:
                self.rest()

            elif choice == 6:
                self.character_screen()

            elif choice == 7:
                self.show_party()

            elif choice == 8:
                self.show_inventory()

            elif choice == 9:
                self.show_equipment()

            elif choice == 10:
                self.quest_menu()

            elif choice == 11:
                self.use_item()

            elif choice == 12:
                self.save()

            elif choice == 13:
                if ask_yes_no(
                    "Deseja salvar antes de sair?"
                ):
                    self.save()

                print(
                    "Obrigado por jogar!"
                )

                break


# ============================================================
# INÍCIO DO PROGRAMA
# ============================================================

def main():
    game = Game()
    game.main_menu()


if __name__ == "__main__":
    main()

# NOTA DE EXPANSÃO 001
# O sistema usa orientação a objetos para organizar personagens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 002
# Cada classe possui atributos iniciais próprios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 003
# O Guerreiro possui mais HP e defesa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 004
# O Mago possui mais MP e magia.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 005
# O Arqueiro possui mais velocidade e crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 006
# Habilidades consomem MP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 007
# Ataques básicos podem causar crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 008
# Defender reduz o dano recebido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 009
# Efeitos de status são processados no início do turno.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 010
# Queimadura causa dano periódico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 011
# Regeneração recupera HP periodicamente.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 012
# Evasão pode fazer ataques errarem.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 013
# Provocar reduz o ataque do alvo.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 014
# Fúria aumenta temporariamente a força do Guerreiro.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 015
# Barreira permite ao Mago reduzir dano.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 016
# A experiência permite evolução de nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 017
# O custo de XP aumenta a cada nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 018
# A loja permite comprar consumíveis.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 019
# Equipamentos alteram atributos do jogador.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 020
# O inventário guarda quantidades de itens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 021
# Missões acompanham progresso de inimigos derrotados.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 022
# Vitórias concedem ouro e XP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 023
# Chefes possuem recompensas maiores.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 024
# A exploração gera encontros aleatórios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 025
# A floresta possui inimigos de nível inicial.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 026
# A montanha possui inimigos mais resistentes.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 027
# A caverna possui chance de gerar o chefe.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 028
# O sistema possui salvamento em JSON.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 029
# O arquivo de save é criado na pasta do programa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 030
# O carregamento restaura os principais atributos.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 031
# O projeto não exige bibliotecas externas.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 032
# O código foi pensado para ser expandido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 033
# O sistema usa orientação a objetos para organizar personagens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 034
# Cada classe possui atributos iniciais próprios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 035
# O Guerreiro possui mais HP e defesa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 036
# O Mago possui mais MP e magia.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 037
# O Arqueiro possui mais velocidade e crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 038
# Habilidades consomem MP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 039
# Ataques básicos podem causar crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 040
# Defender reduz o dano recebido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 041
# Efeitos de status são processados no início do turno.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 042
# Queimadura causa dano periódico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 043
# Regeneração recupera HP periodicamente.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 044
# Evasão pode fazer ataques errarem.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 045
# Provocar reduz o ataque do alvo.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 046
# Fúria aumenta temporariamente a força do Guerreiro.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 047
# Barreira permite ao Mago reduzir dano.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 048
# A experiência permite evolução de nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 049
# O custo de XP aumenta a cada nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 050
# A loja permite comprar consumíveis.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 051
# Equipamentos alteram atributos do jogador.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 052
# O inventário guarda quantidades de itens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 053
# Missões acompanham progresso de inimigos derrotados.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 054
# Vitórias concedem ouro e XP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 055
# Chefes possuem recompensas maiores.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 056
# A exploração gera encontros aleatórios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 057
# A floresta possui inimigos de nível inicial.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 058
# A montanha possui inimigos mais resistentes.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 059
# A caverna possui chance de gerar o chefe.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 060
# O sistema possui salvamento em JSON.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 061
# O arquivo de save é criado na pasta do programa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 062
# O carregamento restaura os principais atributos.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 063
# O projeto não exige bibliotecas externas.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 064
# O código foi pensado para ser expandido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 065
# O sistema usa orientação a objetos para organizar personagens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 066
# Cada classe possui atributos iniciais próprios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 067
# O Guerreiro possui mais HP e defesa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 068
# O Mago possui mais MP e magia.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 069
# O Arqueiro possui mais velocidade e crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 070
# Habilidades consomem MP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 071
# Ataques básicos podem causar crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 072
# Defender reduz o dano recebido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 073
# Efeitos de status são processados no início do turno.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 074
# Queimadura causa dano periódico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 075
# Regeneração recupera HP periodicamente.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 076
# Evasão pode fazer ataques errarem.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 077
# Provocar reduz o ataque do alvo.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 078
# Fúria aumenta temporariamente a força do Guerreiro.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 079
# Barreira permite ao Mago reduzir dano.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 080
# A experiência permite evolução de nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 081
# O custo de XP aumenta a cada nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 082
# A loja permite comprar consumíveis.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 083
# Equipamentos alteram atributos do jogador.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 084
# O inventário guarda quantidades de itens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 085
# Missões acompanham progresso de inimigos derrotados.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 086
# Vitórias concedem ouro e XP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 087
# Chefes possuem recompensas maiores.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 088
# A exploração gera encontros aleatórios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 089
# A floresta possui inimigos de nível inicial.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 090
# A montanha possui inimigos mais resistentes.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 091
# A caverna possui chance de gerar o chefe.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 092
# O sistema possui salvamento em JSON.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 093
# O arquivo de save é criado na pasta do programa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 094
# O carregamento restaura os principais atributos.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 095
# O projeto não exige bibliotecas externas.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 096
# O código foi pensado para ser expandido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 097
# O sistema usa orientação a objetos para organizar personagens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 098
# Cada classe possui atributos iniciais próprios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 099
# O Guerreiro possui mais HP e defesa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 100
# O Mago possui mais MP e magia.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 101
# O Arqueiro possui mais velocidade e crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 102
# Habilidades consomem MP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 103
# Ataques básicos podem causar crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 104
# Defender reduz o dano recebido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 105
# Efeitos de status são processados no início do turno.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 106
# Queimadura causa dano periódico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 107
# Regeneração recupera HP periodicamente.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 108
# Evasão pode fazer ataques errarem.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 109
# Provocar reduz o ataque do alvo.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 110
# Fúria aumenta temporariamente a força do Guerreiro.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 111
# Barreira permite ao Mago reduzir dano.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 112
# A experiência permite evolução de nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 113
# O custo de XP aumenta a cada nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 114
# A loja permite comprar consumíveis.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 115
# Equipamentos alteram atributos do jogador.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 116
# O inventário guarda quantidades de itens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 117
# Missões acompanham progresso de inimigos derrotados.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 118
# Vitórias concedem ouro e XP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 119
# Chefes possuem recompensas maiores.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 120
# A exploração gera encontros aleatórios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 121
# A floresta possui inimigos de nível inicial.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 122
# A montanha possui inimigos mais resistentes.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 123
# A caverna possui chance de gerar o chefe.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 124
# O sistema possui salvamento em JSON.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 125
# O arquivo de save é criado na pasta do programa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 126
# O carregamento restaura os principais atributos.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 127
# O projeto não exige bibliotecas externas.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 128
# O código foi pensado para ser expandido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 129
# O sistema usa orientação a objetos para organizar personagens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 130
# Cada classe possui atributos iniciais próprios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 131
# O Guerreiro possui mais HP e defesa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 132
# O Mago possui mais MP e magia.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 133
# O Arqueiro possui mais velocidade e crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 134
# Habilidades consomem MP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 135
# Ataques básicos podem causar crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 136
# Defender reduz o dano recebido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 137
# Efeitos de status são processados no início do turno.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 138
# Queimadura causa dano periódico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 139
# Regeneração recupera HP periodicamente.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 140
# Evasão pode fazer ataques errarem.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 141
# Provocar reduz o ataque do alvo.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 142
# Fúria aumenta temporariamente a força do Guerreiro.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 143
# Barreira permite ao Mago reduzir dano.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 144
# A experiência permite evolução de nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 145
# O custo de XP aumenta a cada nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 146
# A loja permite comprar consumíveis.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 147
# Equipamentos alteram atributos do jogador.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 148
# O inventário guarda quantidades de itens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 149
# Missões acompanham progresso de inimigos derrotados.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 150
# Vitórias concedem ouro e XP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 151
# Chefes possuem recompensas maiores.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 152
# A exploração gera encontros aleatórios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 153
# A floresta possui inimigos de nível inicial.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 154
# A montanha possui inimigos mais resistentes.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 155
# A caverna possui chance de gerar o chefe.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 156
# O sistema possui salvamento em JSON.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 157
# O arquivo de save é criado na pasta do programa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 158
# O carregamento restaura os principais atributos.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 159
# O projeto não exige bibliotecas externas.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 160
# O código foi pensado para ser expandido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 161
# O sistema usa orientação a objetos para organizar personagens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 162
# Cada classe possui atributos iniciais próprios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 163
# O Guerreiro possui mais HP e defesa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 164
# O Mago possui mais MP e magia.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 165
# O Arqueiro possui mais velocidade e crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 166
# Habilidades consomem MP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 167
# Ataques básicos podem causar crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 168
# Defender reduz o dano recebido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 169
# Efeitos de status são processados no início do turno.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 170
# Queimadura causa dano periódico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 171
# Regeneração recupera HP periodicamente.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 172
# Evasão pode fazer ataques errarem.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 173
# Provocar reduz o ataque do alvo.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 174
# Fúria aumenta temporariamente a força do Guerreiro.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 175
# Barreira permite ao Mago reduzir dano.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 176
# A experiência permite evolução de nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 177
# O custo de XP aumenta a cada nível.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 178
# A loja permite comprar consumíveis.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 179
# Equipamentos alteram atributos do jogador.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 180
# O inventário guarda quantidades de itens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 181
# Missões acompanham progresso de inimigos derrotados.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 182
# Vitórias concedem ouro e XP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 183
# Chefes possuem recompensas maiores.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 184
# A exploração gera encontros aleatórios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 185
# A floresta possui inimigos de nível inicial.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 186
# A montanha possui inimigos mais resistentes.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 187
# A caverna possui chance de gerar o chefe.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 188
# O sistema possui salvamento em JSON.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 189
# O arquivo de save é criado na pasta do programa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 190
# O carregamento restaura os principais atributos.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 191
# O projeto não exige bibliotecas externas.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 192
# O código foi pensado para ser expandido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 193
# O sistema usa orientação a objetos para organizar personagens.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 194
# Cada classe possui atributos iniciais próprios.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 195
# O Guerreiro possui mais HP e defesa.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 196
# O Mago possui mais MP e magia.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 197
# O Arqueiro possui mais velocidade e crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 198
# Habilidades consomem MP.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 199
# Ataques básicos podem causar crítico.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.

# NOTA DE EXPANSÃO 200
# Defender reduz o dano recebido.
# Você pode substituir estas notas por novos sistemas,
# como árvores de habilidades, NPCs, mapas, crafting,
# armas raras, classes adicionais ou novas quests.