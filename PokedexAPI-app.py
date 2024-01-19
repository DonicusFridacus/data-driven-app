#Importing from different libraries
import tkinter as tk
import requests
import random
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk

#Creating the tkinter window
root = tk.Tk()

root.title("Simple Pokedex")
root.geometry("1100x600")
root.resizable(False, False)
root.configure(bg = "crimson")

###Creating the code

def get_pokemon_info(pokemon_name):
    poke_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
    response = requests.get(poke_url)
    if response.status_code == 200:
        pokeData = response.json()
        return {
            'name': pokeData['name'].capitalize(),
            'height': pokeData['height'],
            'weight': pokeData['weight'],
            'types': [pokeType['type']['name'].capitalize() for pokeType in pokeData['types']],
            'abilities': [pokeAbility['ability']['name'].capitalize() for pokeAbility in pokeData['abilities']],
            'image_url': pokeData['sprites']['front_default']
        }
    else:
        return None

def pokemon_info():
    pokemon_name = searchEntry.get()
    
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info:
        update_pokedex(pokemon_info)
    else:
        messagebox.showerror("Error: Invalid Pokemon or ID", f"{pokemon_name} is not a valid Pokemon or ID number")

def random_pokemon():
    random_url = "https://pokeapi.co/api/v2/pokemon/"
    random_pokeID = str(random.randint(1, 1025))

    response = requests.get(random_url + random_pokeID)

    randomData = response.json()
    random_info = {
        'name': randomData['name'].capitalize(),
        'height': randomData['height'],
        'weight': randomData['weight'],
        'types': [pokeType['type']['name'].capitalize() for pokeType in randomData['types']],
        'abilities': [pokeAbility['ability']['name'].capitalize() for pokeAbility in randomData['abilities']],
        'image_url': randomData['sprites']['front_default']
    }

    update_pokedex(random_info)

def update_pokedex(pokemon_info):

    image_url = pokemon_info['image_url']
    if image_url:
        image = Image.open(requests.get(image_url, stream = True).raw)
        image = ImageTk.PhotoImage(image.resize((160, 160)))
        picCanvas.image = image
        picCanvas.create_image(72, 60, anchor = "nw", image = image)
    nameLabel.config(text = f"Name: {pokemon_info['name'].capitalize()}")
    typeLabel1.config(text = f"Type(s): {pokemon_info['types']}")
    heightEntry.config(text = f"Height: {pokemon_info['height']}m")
    weightEntry.config(text = f"Weight: {pokemon_info['weight']}kg")
    abilityEntry.config(text = f"Ability: {pokemon_info['abilities'][0].capitalize()}")
    try:
        HabilityEntry.config(text = f"Hidden Ability: {pokemon_info['abilities'][1].capitalize()}")
    except Exception as error:
        print(f"Error: {error}")
        HabilityEntry.config(text = f"Hidden Ability: None")

#Creating a messagebox with instructions on how to use the Pokedex
def show_instructions():
    messagebox.showinfo("How To Use Pokedex", "To begin using the Pokedex, type in a Pokemon name or ID number.\nFor example, type \"Pikachu\" or any number until 1025 into the searchbar.\nOr use the \"Random\" button to get a random Pokemon.")

#Creating and configuring four rows and three columns
root.rowconfigure([i for i in range(4)], minsize = 50, weight = 1)
root.columnconfigure([i for i in range(3)], minsize = 50, weight = 1)

#Creating Pokemon Name frame
pokeName = tk.Frame(root, relief = tk.RAISED, borderwidth = 4)
nameLabel = tk.Label(pokeName, text = "Pokemon Name", font = ("Futura", 16))
nameLabel.pack()
pokeName.grid(row = 0, column = 0)

#Creating Pokemon Picture frame
pokePic = tk.Frame(root, relief = tk.SUNKEN, borderwidth = 2)
picCanvas = tk.Canvas(pokePic, width = 300, height = 200)
picCanvas.grid(row = 1, column = 0, rowspan = 2)
pokePic.grid(row = 1, column = 0, rowspan = 1, sticky = "NS")

#Creating Pokemon Type(s) frame
pokeType = tk.Frame(root, relief = tk.RAISED, borderwidth = 2)
typeLabel1 = tk.Label(pokeType, text = "Type(s)", font = ("Futura", 16))
typeLabel1.grid(row = 0, column = 0)
pokeType.grid(row = 2, column = 0)

#Creating a search frame
pokeSearch = tk.Frame(root, relief = tk.RAISED, borderwidth = 2)
pokeSearch.columnconfigure([0, 1, 2, 3], weight = 1)

#Button to trigger a messagebox with instructions
instructButton = tk.Button(pokeSearch, text = "Help", font = ("Futura", 16), command = show_instructions)
instructButton.grid(row = 0, column = 0)

#Entry for searching Pokemon
searchEntry = tk.Entry(pokeSearch, font = ("Futura", 16))
searchEntry.grid(row = 0, column = 1)

#Button to search for the Pokemon inputted into the above entry
searchButton = tk.Button(pokeSearch, text = "Search", font = ("Futura", 16), command = pokemon_info)
searchButton.grid(row = 0, column = 2)

#Button to generate random Pokemon with its respective info
randButton = tk.Button(pokeSearch, text = "Random", font = ("Futura", 16), command = random_pokemon)
randButton.grid(row = 0, column = 3)

pokeSearch.grid(row = 0, column = 1, columnspan = 2, sticky = "EW")

#Creating a Pokemon info frame
pokeInfo = tk.Frame(root, relief = tk.SUNKEN, borderwidth = 4)
pokeInfo.rowconfigure([0, 1, 2], weight = 1)
pokeInfo.columnconfigure([0, 1], weight = 1)

#Creating entries in the Pokemon Info frame
pokedexEntry = tk.Label(pokeInfo, text = "Pokedex Entry", font = ("Futura", 16))
pokedexEntry.grid(row = 0, column = 0, columnspan = 2)

abilityEntry = tk.Label(pokeInfo, text = "Ability:", font = ("Futura", 16))
abilityEntry.grid(row = 1, column = 0)

HabilityEntry = tk.Label(pokeInfo, text = "Hidden Ability:", font = ("Futura", 16))
HabilityEntry.grid(row = 2, column = 0)

heightEntry = tk.Label(pokeInfo, text = "Height:", font = ("Futura", 16))
heightEntry.grid(row = 1, column = 1)

weightEntry = tk.Label(pokeInfo, text = "Weight:", font = ("Futura", 16))
weightEntry.grid(row = 2, column = 1)

pokeInfo.grid(row = 1, rowspan = 3, column = 1, columnspan = 2, sticky = "NSEW")

#Runs the application
root.mainloop()