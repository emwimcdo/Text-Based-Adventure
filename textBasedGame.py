import pyautogui as pi
import keyboard
import time
import subprocess
import json
import webbrowser
from pathlib import Path
import pygetwindow as pg
import tkinter as tk
import secrets as secrets
import textwrap

items = {
    "Overpriced Apple": {
        "sellPrice": 0.4,
        "useDescription": "Hope it tasted good.",
        "useFunction": lambda: removeFromInventory("Overpriced Apple")
        },
    "+3 Sword": {
        "sellPrice": 100,
        "useDescription": "Don't cut yourself!"
        },
    "Prison Garb": {
        "sellPrice": -5,
        "useDescription": "You put them on, but it just made you depressed."
        },
    "Milk": {
        "sellPrice": 0.9,
        "useDescription": "You drink some nice, spoiled, rotten milk. Just kidding.",
        "useFunction": lambda: removeFromInventory("Milk")
    },
    "Bread Loaf": {
        "sellPrice": 0.9,
        "useDescription": "You eat a loaf of bread.",
        "useFunction": lambda: removeFromInventory("Bread Loaf")
    },
    "Cheese Wedge": {
        "sellPrice": 0.5,
        "useDescription": "You eat a wedge of cheese.",
        "useFunction": lambda: removeFromInventory("Cheese Wedge")
    },
    "Apple": {
        "sellPrice": 0,
        "useDescription": "You eat a nice juicy Red Delicious.",
        "useFunction": lambda: removeFromInventory("Apple")
    },
    "Kebab": {
        "sellPrice": 0.6,
        "useDescription": "You eat a nice yummy kebab.",
        "useFunction": lambda: replaceItem("Kebab", "Stick")
    },
    "Hardtack": {
        "sellPrice": 0.07,
        "useDescription": "You take a bite of hardtack. It doesn't taste great.",
        "useFunction": lambda: removeFromInventory("Hardtack")
    },
    "Pork": {
        "sellPrice": 0.7,
        "useDescription": "You rip a piece of raw pork off a bone. Disgusting. Now you have Dysentary.",
        "useFunction": lambda: replaceItem("Pork", "Bone")
    }
}

locations = {
    "startingSquare": {
        "description": """\
        You stand in a bustling square. People move around you, shouting to each other and getting on with their busy days. 
        You look around, and see a short man in a trench coat standing by the town hall, who you vaguely recognize. You think about TALKing 
        to him. To the EAST, there is a road heading to a market square. To the NORTH, a road stretches into the distance to the city wall. 
        To the SOUTH, another road goes into the center of the city where the town hall is. To the WEST, your home lies. """,
        "talk": {
                "text": '''You walk over to the man and say "Hello! I seem to recognize you, but I can't seem to place it!"''',
                "next": "short man"
                 },
        "east": {
                "text": 'You walk east towards the busy market. ',
                "next": "busyMarket"
                },
        "west": {
                "text": 'You walk west towards your home. ',
                "next": 'home'
                },
        "north": {
                "text": 'You walk north towards the distant city wall. ',
                "next": "cityWallNorth"
                },
        "south": {
                "text": 'You walk south towards the peacful park in the center of the city. ',
                "next": "centralPark"
                }
    },
    "short man": {
        "description": '''He looks up, and a surprised expression comes across his face. He yells, startled, and runs away. You think about whether or not to CHASE him or GIVE UP. ''',
        "chase": {
                "text": "You decide to chase the short man, thinking he would be easy to catch, but he runs surprisingly fast. As you chase him, you notice that he is going towards the city wall. Do you want to KEEP CHASING him?",
                "next": "cityWallNorth",
                "textTime": 7000
                },
        "give up": {
                "text": "You decide that he isn't worth your time, and wander around. ",
                "next": "startingSquare"
                },
        "visited": {
            "did": False,
            "newDescription": "Oops. You didn't know him. ",
            "back": "startingSquare"
            }
    },
    "cityWallNorth": {
        "description": '''\
        A tall city wall stands ahead of you, looming over the city. You wonder about it, thinking about how long it took to make. 
        You also think about where to go. You could LEAVE the city through the gate, or you could go back to the SQUARE. You also see a STAIRCASE that seems unguarded. ''',
        "keep chasing": {
            "text": "You finally catch up to the man at the foot of the city wall. He is out of breath, and so are you. ",
            "next": "manAtCityWall"
        },
        "leave": {
            "text": "You walk up to the city guard and ask to leave. He nods and lets you through the gate. You don't know how to feel about the great outdoors. ",
            "next": "northForest"
        },
        "staircase": {
            "text": "You climb the staircase, but when you get to the top, you just see a bunch of guards. ",
            "next": "northTopWall"
        },
        "square": {
            "next": "startingSquare"
        }
    },
    "northTopWall": {
        "description": '''\
        As you stand there taking in the view, the guards see you. They yell "Who are you?" And like an idiot you respond "Ur mom."
        Obviously, they don't take it well, and they draw their swords. They walk over and yell "You're gonna regret that!!"
        Do you RUN?''',
        "run": {
            "text": "You run away, but they catch you and knock you out. When you awaken, you are outside on the ground. ",
            "next": "northForest"
        },
        "attack": {
            "text": '''\
            You decide you aren't going down without a fight. You run at them, trip, and take one down at the knees. 
            He is angry now, and tries to slash you with his sword but misses and hits the guard behind you who falls. One left. 
            You lunge, he lunges, but a guard grabs your leg. The guard who lunged at you misses, falls, and knocks out the other two. 
            He is unconsius as well. +3 sword. ''',
            "item": "+3 sword",
            "next": "cityWallNorth",
            "textTime": 20000
        },
        "visited": {
            "did": False,
            "newDescription": "Nothing up here. Strange. ",
            "back": "cityWallNorth"
        }
    },
    "northForest": {
        "description": '''\
        In front of you stands a large dark forest. You see mostly coniferous trees, although there are some deciduous trees. 
        There is a PATH heading into the forest that seems slightly sketchy. To the LEFT, there is a farm, and to the RIGHT there is another farm. 
        Behind you lies the GATE. ''',
        "path": {
            "text": "You venture slightly along the path, but you can't see much. ",
            "next": "banditCart"
        },
        "left": {
            "text": "You go to the farm on the left, but all you see is an abandoned building. Creeped out, you return to the city. ",
            "next": "cityWallNorth"
            },
        "right": {
            "text": "You go to the farm on the right, and see a man in a field. ",
            "next": "farmhouse"
        },
        "gate": {
            "text": "It is getting late, so you decide to go back to the city. ",
            "next": "cityWallNorth"
        }
        },
    "manAtCityWall": {
        "description": 'When you corner him at the wall, he looks up at you and starst laughing. '
        'He says between laughs "Hahahaha!!...I-I-...HAHAHAHAHAAA!!! thought you were...HAHAHAHHHAA! SOMEONE ELSE!! HAHAHAHA!!" He was very'
        'obviously drunk. You smell the alchohol on his breath. He slaps his knee again and walks off, and you have the sudden urge to SLAP him. '
        'You also feel like you could just ignore him and RETURN to the main wall. ',
        "kill": {
            "text": '''\
            In a sudden flash of anger, you pull a sword from a nearby guard and strike him down. He falls to the ground bleeding
            and the guard you took the sword from tackles you. He smacks you over the head and as you fall down you hear him faintly say
            '"You'll be going away for a long long time. " In the background you hear the man's wife screaming. ''',
            "next": "prison",
            "textTime": 10000,
            "item": "Prison Garb",
            "xitem": "5 gold"
        },
        "slap": {
            "text": "You try to slap him in the face, but miss and hit is butt. EMBARRASING!!!",
            "next": "cityWallNorth",
            "item": "A lot of embarrassment"
        },
        "return": {
            "text": "You go back to the gate area. ",
            "next": "cityWallNorth"
        },
        "visited": {
            "did": False,
            "newDescription": "Odd. Nothing here. ",
            "back": "cityWallNorth"
            }
        },
    "home": {
        "description": '''\
        You open the door and enter your home. It is a relatively basic house, nothing much special, with three rooms. 
        One of the rooms is a BEDROOM, one a KITCHEN, (You are in this one), and one a STORAGE ROOM for food. Your bathroom is the window and a CHAMBERPOT. Hooray. 
        As you look around, you realize that your home had been broken in to. Looking around, you realize nothing is amiss, and go on with your day. Maybe LEAVE? 
        Must've had nothing valuable. Imagine. ''',
        "chamberpot": {
            "text": "Why? You sit down and take a dump, then put it back under your bed. To throw out the window tomorrow. Yay. ",
            "next": "home"
        },
        "bedroom": {
            "text": "A relatively small bedroom. Hope the bedbugs don't bite. ",
            "next": "home"
        },
        "kitchen": {
            "text": "A small fire with a pot over it and some pans in the corner. Also a table. ",
            "next": "home"
        },
        "storage room": {
            "text": "A small closet like space with no food. Maybe you should get some of that. ",
            "next": "home"
        },
        "leave": {
            "text": "A good idea. ",
            "next": "westStreet"
        }
    },
    "farmhouse": {
        "description": 'You look out into the distance and see a large field behind the man. '
        'You wonder about WAVEing to the man, but he seems busy. In the farmhouse, someone is visible through the windows, doing dishes. '
        'They seem to be dancing. Odd. Maybe you want to VISIT. Or LEAVE. ',
        "wave": {
            "text": "You wave and wave and wave, but he doesn't seem to notice. Oh well. ",
            "next": "farmhouse"
        },
        "visit": {
            "text": "You walk up to the house and knock. The person inside, a young man, comes out and sees you. "
            "He gets quite angry, but he seems to be speaking a different language. You are trying to understand when the farmer comes out of nowhere and clobbers you. "
            "When you awaken, you are back right outside the gate. ",
            "textTime": 10000,
            "next": "northForest"
        },
        "leave": {
            "text": "You walk back along the path. ",
            "next": "northForest"
        },
        "visited": {
            "did": False,
            "newDescription": "The man walks up to you and tells you to leave. Better listen. ",
            "back": "northForest"
        }
        },
    "centralPark": {
            "description": "A beautiful park in the center of the city. You wander around, taking in the sights. To the NORTH lies a town square, to the EAST lies "
            "a straight path into a bustling market, to the SOUTH lies a path to another town square, to the WEST lies your parent's house, and over to the side slightly lies the GOVERNOR'S MANSION. "
            "Also a TOWN HALL. "
            "The PARK is really very nice, with a fountain in the middle and lots of trees. Of course, being poor you aren't allowed in, but it's nice to look at. ",
            "north": {
                    "text": "You go back to the town square. ",
                    "next": "startingSquare"
                },
            "east": {
                    "text": "You walk into the large, bustling market. ",
                    "next": "busyMarket"
                },
            "south": {
                    "text": "You walk down into another town square. ",
                    "next": "otherTownSquare"
                },
            "west": {
                    "text": "You walk towards your parent's house. ",
                    "next": "graveyard"
                },
            "governor's mansion": {
                    "text": "You walk towards the governor's mansion. Some guards give you a stink eye. ",
                    "next": "governors mansion"
                },
            "park": {
                    "text": "You walk up to the gate and rattle it. Doesn't open. Oh well. ",
                    "next": "centralPark"
                },
            "town hall": {
                    "text": "You walk up to the town hall and knock. The door opens and you walk in. ",
                    "next": "town hall"
            }
        },
    "banditCart": {
            "description": '''\
You get knocked out. When you awaken, you are tied up in a bandit's cart. As you look around, you realize that the cart isn't moving. You think about how to escape. As you brainstorm, you hear the
bandits talking. \n"What do we do with it?"\n"I don't know Jim. What do we do with it?"\n"Don't ask me! You're the one who captured it!"
"Yeah yeah yeah. I didn't know it was broke!"\n"Maybe we could sell it?"\n"But then we need to keep it alive until we get to a big city!"
"True true. I have an idea! Maybe we could turn it in as a bounty!"\n"But he isn't wanted."\n"We have that disguise kit from that performer cart we robbed!"
"Great idea!" They then proceeded to completely cover you in makeup and disguise materials until you looked somewhat like a wanted person. 
All you could do was WAIT. They eventually made it into the city, then went all the way to the South Wall where the prison was. 
They pulled you out of the cart, handed you to the warden, and got their money. Dang. ''',
            "wait": {
                "text": "Oof. That sucks. They didn't believe that you weren't the wanted person, even when they took off the disguise. ",
                "next": "prison"
            },
            "visited": {
                "did": False,
                "newDescription": "I don't know why you would ever try to walk on the path again. You got scared and turned around. ",
                "back": "northForest"
            }
        },
    "busyMarket": {
            "description": 'A busy market stands ahead of you. Within, there are countless merchants selling their wares. '
            'Among them, you see a FOODSELLER, a BLACKSMITH, a COBBLER, a COOPER, a TAILOR, a BEERMAKER, a WINE MERCHANT, a POTION MAKER,'
            'a PAWNSHOP, and finally a HATMAKER. Someone asks you if you want to BUY AN APPLE for 0.5 gold. In the distance, you see'
            'a street leading EAST to the eastern wall, and another street leading WEST to the square.',
            "foodseller": {
                "text": "You walk up to the foodseller stall and take a look at their wares.",
                "next": "foodseller"
            },
            "blacksmith": {
                "text": "You walk up to the blacksmith stall and take a look at their wares.",
                "next": "blacksmith"
            },
            "cobbler": {
                "text": "You walk up to the cobbler stall and take a look at their wares.",
                "next": "cobbler"
            },
            "cooper": {
                "text": "You walk up to the cooper stall and take a look at their wares.",
                "next": "cooper"
            },
            "tailor": {
                "text": "You walk up to the tailor stall and take a look at their wares.",
                "next": "tailor"
            },
            "beermaker": {
                "text": "You walk up to the beermaker stall and take a look at their wares.",
                "next": "beermaker"
            },
            "wine merchant": {
                "text": "You walk up to the wine merchant stall and take a look at their wares.",
                "next": "wine merchant"
            },
            "potion maker": {
                "text": "You walk up to the potion maker stall and take a look at their wares.",
                "next": "potion maker"
            },
            "hatmaker": {
                "text": "You walk up to the hatmaker stall and take a look at their wares.",
                "next": "hatmaker"
            },
            "pawnshop": {
                "text": "You walk up to the pawnshop and tell them you want to sell something.",
                "next": "pawnshop"
            },
            "buy an apple": {
                "success": "Foolishly, you ask to buy an extremely overpriced apple.",
                "fail": "You don't even have enough money for that.",
                "toBuy": {
                    "item": "Overpriced Apple",
                    "price": 0.5
                },
                },
            "west": {
                "text": "You walk back to the square.",
                "next": "startingSquare"
            },
            "east": {
                "text": "You walk to the eastern wall",
                "next": "cityWallEast"
            }
    }, # Add a buying mechanic. 
    "foodseller": {
        "description": """\
            This is obviously a food cart. You see plenty of food items including MILK for 1 gold, BREAD for 1 gold, CHEESE for 0.8 gold, APPLE for 0.1 gold, KEBAB for 1 gold, HARDTACK for 0.2 gold,
            PORK for 1 gold, BEEF for 1 gold, POTATO for 0.5 gold, TOMATO for 1 gold, and BUTTER for 0.3 gold.
            """,
        "milk": {
            "success": "You buy some milk",
            "fail": "You are too poor to buy some milk",
            "toBuy": {
                "item": "Milk",
                "price": 1
            },
            "next": "foodseller"
        },
        "bread": {
            "success": "You buy some bread",
            "fail": "You are too poor to buy some bread",
            "toBuy": {
                "item": "Bread Loaf",
                "price": 1
            },
            "next": "foodseller"
        }        ,
        "cheese": {
            "success": "You buy some cheese",
            "fail": "You are too poor to buy some cheese",
            "toBuy": {
                "item": "Cheese Wedge",
                "price": 0.8
            },
            "next": "foodseller"
        }        ,
        "apple": {
            "success": "You buy an apple",
            "fail": "You are too poor to buy an apple",
            "toBuy": {
                "item": "Apple",
                "price": 0.1
            },
            "next": "foodseller"
        }        ,
        "kebab": {
            "success": "You buy a kebab",
            "fail": "You are too poor to buy a kebab",
            "toBuy": {
                "item": "Kebab",
                "price": 1
            },
            "next": "foodseller"
        }        ,
        "hardtack": {
            "success": "You buy some hardtack",
            "fail": "You are too poor to buy some hardtack",
            "toBuy": {
                "item": "Hardtack",
                "price": 0.2
            },
            "next": "foodseller"
        }        ,
        "pork": {
            "success": "You buy some pork",
            "fail": "You are too poor to buy some pork",
            "toBuy": {
                "item": "Pork",
                "price": 1
            },
            "next": "foodseller"
        }        ,
        "beef": {
            "success": "You buy some beef",
            "fail": "You are too poor to buy some beef",
            "toBuy": {
                "item": "Beef",
                "price": 1
            },
            "next": "foodseller"
        }        ,
        "potato": {
            "success": "You buy a potato",
            "fail": "You are too poor to buy a potato",
            "toBuy": {
                "item": "Potato",
                "price": 0.5
            },
            "next": "foodseller"
        }        ,
        "tomato": {
            "success": "You buy a tomato",
            "fail": "You are too poor to buy a tomato",
            "toBuy": {
                "item": "Tomato",
                "price": 1
            },
            "next": "foodseller"
        }        ,
        "butter": {
            "success": "You buy a tub of butter",
            "fail": "You are too poor to buy a tub of butter",
            "toBuy": {
                "item": "Tub of Butter",
                "price": 0.3
            },
            "next": "foodseller"
        },
        "leave": {
            "text": "You walk away from the cart.",
            "next": "busyMarket"
        }
        },
    "blacksmith": {},
    "cobbler": {},
    "cooper": {},
    "tailor": {},
    "beermaker": {},
    "wine merchant": {},
    "potion maker": {},
    "hatmaker": {},
    "pawnshop": {},
    "westStreet": {
            "description": "You stand outside your house on the street. To your RIGHT, the western wall. To your LEFT, the square. Or BACK to the house. ",
            "left": {
                "text": "You go to the square. ",
                "next": "startingSquare"
            },
            "right": {
                "text": "You walk to the western wall. ",
                "next": "cityWallWest"
            },
            "back": {
                "text": "Open the door and close the door.",
                "next": "home"
            }
        }, # You can't leave the house. Fix it. 
    "prison": {},
    "otherTownSquare": {}, # I want to add a pub or something. Maybe a nice restaurant, or a pickpocket. 
    "graveyard": {}, # Parent's house
    "governors mansion": {}, # Possibly a break in. 
    "town hall": {},
    "cityWallEast": {},
}

room = "startingSquare"

gold = 2

inventoryItems = [f"{gold} gold"]

if Path("save.json").exists():
    with open("save.json", "r") as f:
        data = json.load(f)
        room = data[0]
        inventoryItems = data[1]
        gold = data[2]
        locations = data[3]

window = tk.Tk()
window.title("Text-Based Adventure")
window.geometry("2000x500")

for col in range(3):
    window.columnconfigure(col, weight=1)

for row in range(2):
    window.rowconfigure(row, weight=1)

description = tk.Text(window, wrap="word", width=80, height=20)
inputField = tk.Entry(window, borderwidth=3, width=100)
inventory = tk.Label(window, text="Inventory", justify="left", anchor="n", relief="groove")

description.grid(column=0, columnspan=3, padx=100, pady=100, row=0, rowspan=2, sticky="nsew")
inventory.grid(column=10, row=0, columnspan=1, rowspan=6, padx=100, pady=100, ipadx=300, sticky="nsew")
inputField.grid(column=0, columnspan=20, row=10, rowspan=3, pady=20, ipady=10, ipadx=100)
description.config(state="disabled")

move = ""
    
def replaceItem(a, b):
    removeFromInventory(a)
    addToInventory(b)

def continueText():
    runRoom(room)

def runContinue():
    continueButton = tk.Button(window, text="Continue", command=lambda: continueText())
    description.window_create(tk.END, window=continueButton)

def setDescription(text):
    description.config(state="normal")
    description.delete("1.0", tk.END)
    description.insert("1.0", textwrap.dedent(text))
    description.config(state="disabled")

def runRoom(room):
    desc = locations[room].get("description", "ERR0R: DESCRIPTI0N N0T F0UND")
    setDescription(desc)
    
def handleAction(action): 
    global room, inventoryItems, locations, continueStory
    
    currentAction = locations.get(room, {})
    result = currentAction.get(action)
    
    if isinstance(result, str):
        setDescription(result)
        return
    
    textToShow = result.get("text", "")
    nextRoom = result.get("next")
    item = result.get("item")
    textTime = result.get("textTime")
    buyI = result.get("toBuy")
    sellI = result.get("toSell")
    xitem = result.get("xitem")
    visit = locations[nextRoom].get("visited", {})
    visited = visit.get("did", False)
    successText = result.get("success")
    failText = result.get("fail")
    
    if visited:
        setDescription(locations[nextRoom]["visited"].get("newDescription", "Odd. Not there anymore."))
        room = visit.get("back", "startingSquare")
        window.after(5000, lambda: runRoom(room))
        return
    if buyI:
        if buy(buyI["price"], buyI["item"]):
            setDescription(successText)
        else:
            setDescription(failText)
        runContinue()
        return
    if sellI:
        if sell(sellI["price"], sellI["item"]):
            setDescription(successText)
        else:
            setDescription(failText)
        runContinue()
        return
    if textToShow:
        setDescription(textToShow)
        runContinue()
    if nextRoom:
        room = nextRoom
    if item:
        addToInventory(item)
    if xitem:
        removeFromInventory(xitem)
    if visit:
        visit["did"] = True
        # print(locations["short man"]["visited"])
    '''
    with open("save.json", "w") as f:
        json.dump([room, inventoryItems, gold, locations], f, indent=4) # type: ignore
    '''
    inventoryItems[0] = f"{gold} gold"
    newText = ""
    for i in inventoryItems:
        newText += f"{i}\n"

def updateInventory():
    global inventoryItems, gold
    if round(gold, 2) == 0:
        gold = 0
    inventoryItems[0] = f"{round(gold, 2)} gold"
    newText = "Inventory:\n"
    for i in inventoryItems:
        newText += f"{i}\n"
    inventory.config(text=newText)

def addToInventory(item):
    global inventoryItems
    inventoryItems.append(item)
    updateInventory()
    
def removeFromInventory(item):
    global inventoryItems
    if item:
        inventoryItems.remove(item)
    updateInventory()
    
def buy(price, item):
    global inventoryItems, gold
    
    worked = False
    
    if round(gold, 2) >= price:
        addToInventory(item)
        gold -= price
        worked = True
        
    inventoryItems[0] = f"{gold} gold"
    updateInventory()
    return worked

def sell(price, item):
    global inventoryItems, gold
    
    worked = False
    
    if item in inventoryItems:
        removeFromInventory(item)
        gold += price
        worked = True
    
    updateInventory()
    return worked

runRoom(room)

def on_enter(event=None):
    action = inputField.get().strip().lower()
    inputField.delete(0, tk.END)
    handleAction(action)

inventoryItems[0] = f"{gold} gold"

updateInventory()

inputField.bind("<Return>", on_enter)


window.mainloop()