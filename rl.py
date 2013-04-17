import libtcodpy as libtcod
import os
 
#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
 
LIMIT_FPS = 20  #20 frames-per-second maximum

#define map variables
MAP_WIDTH = 80
MAP_HEIGHT = 45
color_dark_wall = libtcod.Color(0,0,100)
color_dark_ground = libtcod.Color(50,50,150)

#general map objects
class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight



class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        #Move by the given amount, if destination is not a blocked tile
        if not map[self.x+dx][self.y+dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        #set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

#map making function
def make_map():
    global map

    #fill map with "unblocked" tiles
    map = [[Tile(False)
        for y in range(MAP_HEIGHT)]
            for x in range(MAP_WIDTH)]
    #two testing pillars        
    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[50][22].blocked = True
    map[50][22].block_sight = True


def render_all():
    global color_light_wall
    global color_light_ground

    #draw map
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                #libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                libtcod.console_put_char(con, x, y, '#', libtcod.BKGND_NONE)
            else:
                #libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET) 
                libtcod.console_put_char(con, x, y, '.', libtcod.BKGND_NONE)

    #draw everything from the objects list
    for object in objects:
        object.draw()

    #blit the contents of "con" to the root console and present it   
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def handle_keys():
    #key = libtcod.console_check_for_keypress()  #real-time
    key = libtcod.console_wait_for_keypress(True)  #turn-based
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fgaddullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
 
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0,-1)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0,1)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1,0)



#############################################
# Initialization & Main Loop
#############################################

font = os.path.join('data','fonts', 'arial10x10.png') 
libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)


#create the player object  
player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)

#create the npc object
npc = Object(SCREEN_WIDTH/2-5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
#list of both objects
objects = [npc, player]

#generate map (it is not drawn to the screen at this point)
make_map()



while not libtcod.console_is_window_closed():

    #render the screen
    render_all()

    libtcod.console_flush()
 
    #erase all objects at their old locations before they move
    for object in objects:
        object.clear()

    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break