import sys

from objects import room
from characters import player
from setup import SAVE_DIR


# stored in file as
# "room number, name, description, directions:room;dir:room..., item;item;..., character;character;..."
def load_rooms():
    """
    Loads saved rooms from saves/rooms
    In file as:
    room#,name,description,[directions],[items],[characters],
    Where directions, items and characters are separated by ';'
    And directions are in format -> dir:room#
    :return: Dictionary of room objects
    """
    rooms = {}
    with open(SAVE_DIR + "/rooms") as file:
        for line in file:
            data = line.split(',')
            index = data[0]
            this_room = room.Room()
            this_room.set_name(data[1])
            this_room.set_description(data[2])
            for direction in data[3].split(';')[:-1]:
                dirr = direction.split(':')
                this_room.add_direction(dirr[0], dirr[1])
            for item in data[4].split(';')[:-1]:
                this_room.add_item(item)
            for character in data[5].split(';')[:-1]:
                this_room.add_character(character)
            rooms[index] = this_room

    for i in rooms:
        aroom = rooms[i]
        aroom.id = i
        if aroom:
            for direction in aroom.directions:
                aroom.directions[direction] = rooms[aroom.directions[direction]]

    return rooms


def save_rooms(rooms):
    """
    Saves the room objects' information to saves/rooms
    :param rooms: Dictionary of room objects
    """
    with open(SAVE_DIR + "/rooms", mode='w') as file:
        for key in rooms:
            room = rooms[key]
            data = "{},{},{},".format(key, room.name, room.description)
            for dir_key in room.directions:
                data += "{}:{};".format(dir_key, room.directions[dir_key].id)
            data += ','
            for item in room.items:
                data += "{};".format(item)
            data += ','
            for char in room.characters:
                data += "{};".format(char)
            data += ','

            print(data, file=file)
    print("rooms saved")


# squiggles,gun;mega gun;nuke;ninja sword;,22,
# name,item;item;...,room,
def load_player_saves(rooms):
    """
    Loads saved players from saves/players
    In file as:
    name,[items],room#,
    Where items are separated by ';'
    :param rooms: Dictionary of room objects
    :return: Dictionary of player objects
    """
    players = {}
    with open(SAVE_DIR + "/players") as file:
        for line in file:
            p = player.Player()
            data = line.split(',')
            p.set_name(data[0])
            for item in data[1].split(';')[:-1]:
                p.inventory.append(item)
            p.currentRoom = rooms[data[2]]
            players[p.name] = p

    return players


def save_players(players):
    """
    Saves the player objects' information to saves/players
    :param players: Dictionary of player objects
    """
    with open(SAVE_DIR + "/players", mode='w') as file:
        for name in players:
            p = players[name]
            data = "{},".format(name)
            for item in p.inventory:
                data += "{};".format(item)
            data += ",{},".format(p.currentRoom.id)
            print(data, file=file)
    print("players saved")


def load_saved_data():
    """
    Loads room and player save data
    rooms from saves/rooms
    players from saves/players
    :return: Tuple of dictionaries confining loaded info
    """
    try:
        rooms = load_rooms()
    except:
        e = sys.exc_info()[0]
        quit("Load Rooms Failed: {}".format(e))

    try:
        players = load_player_saves(rooms)
    except:
        e = sys.exc_info()[0]
        quit("Load Rooms Failed: {}".format(e))
    return rooms, players


def save_data(rooms, players):
    """
    Saves room and player information
    rooms from saves/rooms
    players from saves/players
    :param rooms:   Dictionary of rooms to save
    :param players: Dictionary of players to save
    """
    try:
        save_rooms(rooms)
    except:
        e = sys.exc_info()[0]
        quit("Save Rooms Failed: {}".format(e))

    try:
        save_players(players)
    except:
        e = sys.exc_info()[0]
        quit("Save Players Failed: {}".format(e))
