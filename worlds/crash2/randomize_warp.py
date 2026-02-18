from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

from . import data

if TYPE_CHECKING:
    from .world import Crash2World

# five levels per warp room, starting at the fifth level of each warp room
# this matches the way the level IDs are ordered in the monty hall (warp room) object and keeps things simple.
# the 0x100 bit denotes secret entrance. this also makes it simpler to shuffle things around.

# locations.py has the level IDs mapped to level names. they are also available at https://wiki.cbhacks.com/w/Level_ID#Crash_2
warpRoomLevelIds = [
    0x18, 0x1F, 0x19, 0x0E, 0x1E,
    0x23, 0x1B, 0x1D, 0x20, 0x11,
    0x17, 0x16, 0x22, 0x0A, 0x21,
    0x24, 0x0F, 0x13, 0x15, 0x0D,
    0x26, 0x1A, 0x0C, 0x12, 0x10,
    0x27, 0x25, 0x116, 0x10E, 0x120
]

levelIdsWithSecretEntrance = [
    0x0E, # snow go
    0x16, # road to ruin
    0x20 # air crash
]

warpRoomLevelNumber = [
    1, 1, 1, 1, 1,
    2, 2, 2, 2, 2,
    3, 3, 3, 3, 3,
    4, 4, 4, 4, 4,
    5, 5, 5, 5, 5,
    4, 3, 3, 1, 2
]

# Not actually randomized (yet??), determines the level ID for the boss of each warp room.
# warp room 6, the secret one, has no boss, so it is excluded.
warpRoomBossLevelIds = [
    0x06,
    0x08,
    0x03,
    0x09,
    0x07
]

def shuffle_warp_room_destinations(world, excluded):
    print("test A")
    print(warpRoomLevelIds)

    # list of levels for each warp room.
    levels_per_warp_room = [
        [],
        [],
        [],
        [],
        []
    ]
    
    # Step 1: Grab original level ist and remove secret entrances + their levels. Shuffle that.
    temp_warp_dests:list = warpRoomLevelIds
    for level in levelIdsWithSecretEntrance:
        temp_warp_dests.remove(level)
        temp_warp_dests.remove(level | 0x100)
    world.random.shuffle(temp_warp_dests)

    # Step 2: Determine where secret entrances will be.
    # Secret entrances will always be in a warp room after the original level's.
    # This means they cannot be in warp room 1, and original levels cannot be in warp room 5.
    for original_level in levelIdsWithSecretEntrance:
        # determine warp rooms
        secret_warp_dest = world.random.randint(2, 5)
        original_warp_dest = 1 if secret_warp_dest == 2 else world.random.randint(1, secret_warp_dest-1)
        levels_per_warp_room[original_warp_dest-1].append(original_level)
        levels_per_warp_room[secret_warp_dest-1].append(original_level | 0x100)

    # Step 3: Randomly assign all remaining levels to each warp rooms!
    for i in range(5):
        # until enough levels have been assigned to that warp room...
        warp_room_level_count = warpRoomLevelNumber.count(i+1)
        while len(levels_per_warp_room[i]) < warp_room_level_count:
            # assign a level!
            levels_per_warp_room[i].append(temp_warp_dests.pop())
        assert(len(levels_per_warp_room[i]) == warp_room_level_count) # make sure warp room was filled up.
    assert(len(temp_warp_dests) == 0) # make sure all levels were used up.

    # Step 4: Build final warp room list.
    shuffled_warp_dests = []
    for warp_room in warpRoomLevelNumber:
        shuffled_warp_dests.append(levels_per_warp_room[warp_room-1].pop())

    print(shuffled_warp_dests)
    return shuffled_warp_dests
