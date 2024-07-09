import random
import textwrap

class Room:
    def __init__(self, name, description, exits=None):
        self.name = name
        self.description = description
        self.exits = exits or {}
        self.items = []
        self.characters = []
        self.enemies = []
        self.events = []

class Item:
    def __init__(self, name, description, use_effect=None):
        self.name = name
        self.description = description
        self.use_effect = use_effect

class Character:
    def __init__(self, name, description, dialogue, quest=None):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.quest = quest

class Quest:
    def __init__(self, name, description, stages, reward):
        self.name = name
        self.description = description
        self.stages = stages
        self.current_stage = 0
        self.reward = reward
        self.completed = False

    def advance_stage(self):
        self.current_stage += 1
        if self.current_stage >= len(self.stages):
            self.completed = True

class Player:
    def __init__(self):
        self.inventory = []
        self.health = 100
        self.sanity = 100
        self.quests = []
        self.completed_quests = []

class Enemy:
    def __init__(self, name, description, health, damage, loot=None):
        self.name = name
        self.description = description
        self.health = health
        self.damage = damage
        self.loot = loot

class Event:
    def __init__(self, description, effect):
        self.description = description
        self.effect = effect

class Game:
    def __init__(self):
        self.rooms = {}
        self.current_room = None
        self.player = Player()

    def add_room(self, room):
        self.rooms[room.name] = room

    def start(self, starting_room):
        self.current_room = self.rooms[starting_room]

    def move(self, direction):
        if direction in self.current_room.exits:
            self.current_room = self.rooms[self.current_room.exits[direction]]
            return True
        return False

    def get_input(self):
        return input("> ").lower().strip()

    def play(self):
        self.show_intro()
        while True:
            self.describe_room()
            self.check_events()
            action = self.get_input()
            if action == "quit":
                print("Thanks for playing!")
                break
            self.process_action(action)

    def show_intro(self):
        intro = """
        Welcome to "Echoes of the Damned", a Grim Dark Fantasy Adventure.

        In a world consumed by darkness and despair, you find yourself trapped within the 
        cursed walls of Castle Shadowmere. Once a bastion of hope, it now stands as a 
        testament to the folly of those who sought to harness powers beyond their control.

        As the last surviving member of an ill-fated expedition, you must uncover the 
        castle's dark secrets, confront the horrors that lurk within its halls, and find 
        a way to escape before your sanity slips away entirely.

        But beware, for every step deeper into the castle brings you closer to the 
        malevolent force that holds sway over this place. Will you unravel the mystery 
        and break free, or will you join the ranks of the damned?

        Your choices will shape your fate. Good luck, brave soul.

        WARNING: This game contains mature themes and is intended for adult audiences only.
        Type 'help' at any time to see available commands.
        """
        print(textwrap.dedent(intro))
        input("Press Enter to begin your journey...")

    def describe_room(self):
        print(f"\n{self.current_room.name}")
        print(textwrap.fill(self.current_room.description, width=80))
        
        if self.current_room.items:
            print("\nYou see:", ", ".join([item.name for item in self.current_room.items]))
        
        if self.current_room.characters:
            print("Characters here:", ", ".join([char.name for char in self.current_room.characters]))
        
        if self.current_room.enemies:
            print("Enemies present:", ", ".join([enemy.name for enemy in self.current_room.enemies]))
        
        print("Exits:", ", ".join(self.current_room.exits.keys()))

    def process_action(self, action):
        if action in self.current_room.exits:
            self.move(action)
        elif action.startswith("take "):
            self.take_item(action[5:])
        elif action.startswith("talk to "):
            self.talk_to_character(action[8:])
        elif action.startswith("attack "):
            self.initiate_combat(action[7:])
        elif action == "inventory":
            self.show_inventory()
        elif action.startswith("use "):
            self.use_item(action[4:])
        elif action == "status":
            self.show_status()
        elif action == "help":
            self.show_help()
        elif action == "look":
            self.describe_room()
        else:
            print("I don't understand that command. Type 'help' for a list of commands.")

    def take_item(self, item_name):
        for item in self.current_room.items:
            if item.name.lower() == item_name:
                self.player.inventory.append(item)
                self.current_room.items.remove(item)
                print(f"You have taken the {item.name}.")
                return
        print("There's no such item here.")

    def talk_to_character(self, char_name):
        for char in self.current_room.characters:
            if char.name.lower() == char_name:
                print(f"{char.name} says: {random.choice(char.dialogue)}")
                if char.quest and not char.quest.completed:
                    if char.quest not in self.player.quests:
                        print(f"{char.name} offers you a quest: {char.quest.description}")
                        if input("Do you accept? (yes/no) ").lower() == "yes":
                            self.player.quests.append(char.quest)
                            print("Quest accepted!")
                    else:
                        self.update_quest(char.quest)
                return
        print("There's no one by that name here.")

    def update_quest(self, quest):
        if not quest.completed:
            print(f"Current objective: {quest.stages[quest.current_stage]}")
            if input("Have you completed this objective? (yes/no) ").lower() == "yes":
                quest.advance_stage()
                if quest.completed:
                    print(f"Congratulations! You've completed the quest: {quest.name}")
                    print(f"You receive: {quest.reward}")
                    self.player.completed_quests.append(quest)
                    self.player.quests.remove(quest)
                else:
                    print(f"Quest updated. New objective: {quest.stages[quest.current_stage]}")
        else:
            print("This quest has already been completed.")

    def show_inventory(self):
        if self.player.inventory:
            print("You are carrying:")
            for item in self.player.inventory:
                print(f"- {item.name}: {item.description}")
        else:
            print("Your inventory is empty.")

    def use_item(self, item_name):
        for item in self.player.inventory:
            if item.name.lower() == item_name:
                if item.use_effect:
                    item.use_effect(self.player)
                    print(f"You used the {item.name}.")
                    self.player.inventory.remove(item)
                else:
                    print(f"You can't use the {item.name}.")
                return
        print("You don't have that item.")

    def show_status(self):
        print(f"Health: {self.player.health}")
        print(f"Sanity: {self.player.sanity}")
        if self.player.quests:
            print("Active quests:")
            for quest in self.player.quests:
                print(f"- {quest.name}: {quest.stages[quest.current_stage]}")

    def check_events(self):
        for event in self.current_room.events:
            print(event.description)
            event.effect(self.player)
        self.current_room.events = []

    def initiate_combat(self, enemy_name):
        for enemy in self.current_room.enemies:
            if enemy.name.lower() == enemy_name:
                self.combat(enemy)
                return
        print("There's no such enemy here.")

    def combat(self, enemy):
        print(f"You engage in combat with {enemy.name}!")
        while enemy.health > 0 and self.player.health > 0:
            print(f"\nYour health: {self.player.health}")
            print(f"{enemy.name}'s health: {enemy.health}")
            action = input("Do you want to attack, use an item, or flee? ").lower()
            if action == "attack":
                damage = random.randint(10, 20)
                enemy.health -= damage
                print(f"You deal {damage} damage to {enemy.name}.")
                if enemy.health <= 0:
                    print(f"You have defeated {enemy.name}!")
                    if enemy.loot:
                        print(f"You find: {enemy.loot.name}")
                        self.player.inventory.append(enemy.loot)
                    self.current_room.enemies.remove(enemy)
                    return
            elif action == "use item":
                self.show_inventory()
                item_name = input("Which item do you want to use? ")
                self.use_item(item_name)
            elif action == "flee":
                if random.random() < 0.5:
                    print("You successfully flee from the battle.")
                    return
                else:
                    print("You fail to flee!")
            else:
                print("Invalid action. Choose 'attack', 'use item', or 'flee'.")
            
            player_damage = random.randint(1, enemy.damage)
            self.player.health -= player_damage
            print(f"{enemy.name} deals {player_damage} damage to you.")
        
        if self.player.health <= 0:
            print("You have been defeated. Game over.")
            exit()

    def show_help(self):
        help_text = """
        Available commands:
        - [direction] (e.g., north, south, east, west): Move in that direction
        - take [item]: Pick up an item
        - talk to [character]: Interact with a character
        - attack [enemy]: Initiate combat with an enemy
        - inventory: Show your inventory
        - use [item]: Use an item from your inventory
        - status: Check your health, sanity, and active quests
        - look: Examine your surroundings
        - help: Show this help message
        - quit: Exit the game
        """
        print(textwrap.dedent(help_text))

# Create game instance
game = Game()

# Create rooms
entrance = Room("Castle Entrance", "You stand before the imposing gates of Castle Shadowmere. The rusted iron bars loom overhead, their twisted forms hinting at the horrors that await within. A cold wind howls through the courtyard, carrying whispers of despair.")
main_hall = Room("Grand Hall", "Once a place of grandeur, the main hall now lies in ruins. Tattered banners bearing forgotten heraldry hang from the walls, and a thick layer of dust covers the cracked marble floor. Shadows dance in the corners, cast by unseen sources.")
library = Room("Forbidden Library", "Rows upon rows of ancient tomes line the walls, their spines etched with eldritch symbols. The air is thick with the musty scent of old parchment and a faint hint of brimstone. Ghostly whispers seem to emanate from the books themselves.")
dungeon = Room("Torture Dungeon", "The acrid stench of blood and decay assaults your senses as you enter this chamber of horrors. Rusted instruments of torture line the walls, and dark stains mar the stone floor. The air is heavy with the echoes of past suffering.")
crypt = Room("Ancient Crypt", "Rows of ornate sarcophagi line the walls of this vast underground chamber. The air is stale and heavy with the dust of ages. Faint, ethereal moans seem to emanate from the very stones, hinting at restless spirits.")
tower = Room("Wizard's Tower", "Arcane symbols cover every surface of this circular room at the top of the highest tower. A large obsidian mirror dominates the center, its surface swirling with dark energies. The very air crackles with eldritch power.")

# Set exits
entrance.exits = {"north": "Grand Hall"}
main_hall.exits = {"south": "Castle Entrance", "east": "Forbidden Library", "west": "Torture Dungeon", "up": "Wizard's Tower"}
library.exits = {"west": "Grand Hall", "down": "Ancient Crypt"}
dungeon.exits = {"east": "Grand Hall"}
crypt.exits = {"up": "Forbidden Library"}
tower.exits = {"down": "Grand Hall"}

# Add rooms to the game
game.add_room(entrance)
game.add_room(main_hall)
game.add_room(library)
game.add_room(dungeon)
game.add_room(crypt)
game.add_room(tower)

# Create items
rusted_key = Item("Rusted Key", "An ancient key, its surface corroded by time. It might still work on some locks.")
entrance.items.append(rusted_key)

grimoire = Item("Forbidden Grimoire", "A heavy tome bound in human skin. Its pages contain unspeakable knowledge.", 
                lambda player: setattr(player, 'sanity', max(0, player.sanity - 15)))
library.items.append(grimoire)

healing_potion = Item("Healing Elixir", "A small vial containing a glowing red liquid. It emanates a faint warmth.", 
                      lambda player: setattr(player, 'health', min(100, player.health + 40)))
dungeon.items.append(healing_potion)

enchanted_amulet = Item("Amulet of Warding", "A silver amulet inscribed with protective runes. It hums with a soft, comforting energy.",
                        lambda player: setattr(player, 'sanity', min(100, player.sanity + 20)))
crypt.items.append(enchanted_amulet)

# Create characters
ghost_knight = Character("Sir Aldric", "The spectral form of a once-noble knight, his translucent armor bearing the scars of a final, fatal battle.",
                         ["The curse... it binds us all...", "Beware the Wizard's bargain, for it leads only to damnation.", "Find the Sword of Dawn... Only it can break the chains of darkness."],
                         Quest("The Knight's Redemption", "Help Sir Aldric find peace by recovering his long-lost Sword of Dawn.",
                               ["Search the library for clues about the Sword of Dawn",
                                "Retrieve the Sword of Dawn from the hidden armory",
                                "Return the Sword to Sir Aldric"],
                               "Spectral Shield"))
main_hall.characters.append(ghost_knight)

mad_librarian = Character("Keeper Malakai", "A hunched figure with wild eyes and ink-stained fingers. His ragged robes bear countless esoteric symbols.",
                          ["The books... they whisper such delicious secrets...", "Have you seen it? The Codex Umbra? It holds the key to unimaginable power!", "Careful where you step, some tomes have... appetites."],
                          Quest("Forbidden Knowledge", "Assist Keeper Malakai in locating the legendary Codex Umbra.",
                                ["Find the hidden key to the Restricted Section",
                                 "Retrieve the Codex Umbra from the Restricted Section",
                                 "Survive reading a passage from the Codex Umbra"],
                                "Eldritch Insight"))
library.characters.append(mad_librarian)

tortured_soul = Character("Unnamed Prisoner", "A wretched figure chained to the wall, its body bearing the marks of unspeakable torments.",
                          ["Please... end this suffering...", "The Inquisitor... he never stops... never tires...", "There is a way out... through the old sewers... but beware the things that dwell below..."],
                          Quest("Mercy's Embrace", "End the prisoner's suffering and uncover the secret escape route.",
                                ["Find a way to release the prisoner from their chains",
                                 "Defeat the Inquisitor",
                                 "Locate the entrance to the old sewers"],
                                "Map of the Undercity"))
dungeon.characters.append(tortured_soul)

# Create enemies
ravenous_ghoul = Enemy("Ravenous Ghoul", "A once-human creature driven mad by hunger, its razor-sharp claws and teeth gleam in the dim light.", 50, 15, 
                       Item("Ghoul Essence", "A viscous, glowing substance extracted from the defeated ghoul. It radiates an unsettling energy."))
crypt.enemies.append(ravenous_ghoul)

shadow_beast = Enemy("Shadow Beast", "A writhing mass of darkness given form, its red eyes gleaming with malevolence.", 75, 20,
                     Item("Shadow Shard", "A fragment of pure darkness, cold to the touch. It seems to absorb the light around it."))
main_hall.enemies.append(shadow_beast)

eldritch_horror = Enemy("Tentacled Abomination", "A monstrous entity of writhing tentacles and countless eyes, defying the laws of nature.", 100, 25,
                        Item("Void Essence", "A swirling orb of nothingness, humming with otherworldly power."))
tower.enemies.append(eldritch_horror)

# Create events
sanity_drain = Event("The oppressive atmosphere of this place weighs heavily on your mind.", 
                     lambda player: setattr(player, 'sanity', max(0, player.sanity - 5)))
dungeon.events.append(sanity_drain)

whispers = Event("Ghostly whispers echo through the hall, carrying fragments of long-forgotten secrets.",
                 lambda player: setattr(player, 'sanity', max(0, player.sanity - 3)))
main_hall.events.append(whispers)

arcane_surge = Event("A surge of arcane energy courses through your body, invigorating yet unsettling.",
                     lambda player: (setattr(player, 'health', min(100, player.health + 10)), 
                                     setattr(player, 'sanity', max(0, player.sanity - 10))))
tower.events.append(arcane_surge)

# Overarching storyline setup
def check_story_progress(player):
    if "Sword of Dawn" in [item.name for item in player.inventory] and "Codex Umbra" in [item.name for item in player.inventory]:
        print("\nWith both the Sword of Dawn and the Codex Umbra in your possession, you feel a shift in the castle's oppressive atmosphere.")
        print("The path to confronting the dark wizard responsible for this nightmare seems clear, yet fraught with danger.")
        print("Do you dare to face the ultimate evil lurking in the depths of Castle Shadowmere?")

# Add story progress check to the main game loop
def play(self):
    self.show_intro()
    while True:
        self.describe_room()
        self.check_events()
        check_story_progress(self.player)
        action = self.get_input()
        if action == "quit":
            print("Thanks for playing!")
            break
        self.process_action(action)

Game.play = play  # Monkey patch the play method to include story progress check

# Final boss setup (to be triggered when certain conditions are met)
dark_wizard = Enemy("Malevolent Archmagus", "A figure cloaked in swirling darkness, eyes burning with eldritch fire. The source of Castle Shadowmere's corruption.", 200, 30,
                    Item("Heart of Darkness", "The still-beating heart of the dark wizard, pulsing with incredible power."))

def confront_final_boss(player):
    print("\nDrawing upon the power of the Sword of Dawn and the knowledge of the Codex Umbra, you confront the Malevolent Archmagus!")
    print("The fate of Castle Shadowmere and your very soul hang in the balance as you face your ultimate challenge.")
    # Implement epic final boss battle here

# Start the game
game.start("Castle Entrance")
game.play()