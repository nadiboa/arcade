
import random
import arcade
import timeit
import os

from pyglet.gl import GL_NEAREST
from pyglet.gl import GL_LINEAR


NATIVE_TILE_SIZE = 128
SCALE = 0.5
TILE_SIZE = int(NATIVE_TILE_SIZE * SCALE)
SCALE_FROSTFIRE = 3
FROSTFIRE_COUNT = 100

SCALE = 1
SCREEN_WIDTH = 960 * SCALE
SCREEN_HEIGHT = 540 * SCALE
SCREEN_TITLE = "Maze Depth First Example"

MOVEMENT_SPEED = 1

TILE_SIZE = 48 * SCALE
TILE_EMPTY = 0
TILE_CRATE = 1

# Maze must have an ODD number of rows and columns.
# Walls go on EVEN rows/columns.
# Openings go on ODD rows/columns
MAZE_HEIGHT = 51
MAZE_WIDTH = 51

MERGE_SPRITES = True

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200


def _create_grid_with_cells(width, height):
    """ Create a grid with empty cells on odd row/column combinations. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(TILE_EMPTY)
            elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                grid[row].append(TILE_CRATE)
            else:
                grid[row].append(TILE_CRATE)
    return grid

'''
def make_maze_depth_first(maze_width, maze_height):
    maze = _create_grid_with_cells(maze_width, maze_height)

    w = (len(maze[0]) - 1) // 2
    h = (len(maze) - 1) // 2
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x: int, y: int):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                maze[max(y, yy) * 2][x * 2 + 1] = TILE_EMPTY
            if yy == y:
                maze[y * 2 + 1][max(x, xx) * 2] = TILE_EMPTY

            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))

    return maze
'''

class MyGame(arcade.View):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        # super().__init__(width, height, title)
        super().__init__()
        self.window.set_mouse_visible(False)


        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.player_list = None
        self.tilemap = None
        self.scene = None
        self.frostfire_list = None
      
        # Player info
        self.score = 0
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Used to scroll
        self.view_bottom = 0
        self.view_left = 0

        # Time to process
        self.processing_time = 0
        self.draw_time = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.frostfire_list = arcade.SpriteList()

        self.score = 0

        # Create the maze
        #maze = make_maze_depth_first(MAZE_WIDTH, MAZE_HEIGHT)

        layer_options = {
            "walls": {
                "use_spatial_hash": True,
            },
            "doors": {
                "use_spatial_hash": True,
            },
        }
        self.tilemap = arcade.load_tilemap("tilemap test.tmx", SCALE, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tilemap)
        # Set up the player
        self.player_sprite = arcade.Sprite("new player(candel).png.png"
                                          ,
                                           SCALE)
        self.player_list.append(self.player_sprite)

        # Randomly place the player. If we are in a wall, repeat until we aren't.
        placed = False
        while not placed:

            # Randomly position
            self.player_sprite.center_x = random.randrange(MAZE_WIDTH * TILE_SIZE)
            self.player_sprite.center_y = random.randrange(MAZE_HEIGHT * TILE_SIZE)

            # Are we in a wall?
            walls_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene['walls'])
            if len(walls_hit) == 0:
                # Not in a wall! Success!
                placed = True

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene["walls"])

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0
        # print(f"Total wall blocks: {len(self.scene["walls"])}")


          # Create the coins
        for i in range(FROSTFIRE_COUNT):

            # Create the frostfire instance
           
            frostfire = arcade.Sprite("frost fire.png",
                                 SCALE)

            # Position the frost
            
            frostfire.center_x = random.randrange(MAZE_WIDTH * TILE_SIZE)
            frostfire.center_y = random.randrange(MAZE_HEIGHT * TILE_SIZE)

            # Are we in a wall?
            #walls_hit = arcade.check_for_collision_with_list(self.frostfire_list[i], self.scene["walls"])
            walls_hit = arcade.check_for_collision_with_list(frostfire, self.scene["walls"])
            if len(walls_hit) != 0:
                # Not in a wall! Success!
                continue
            self.physics_engine = arcade.PhysicsEngineSimple(frostfire, self.scene["walls"])

            # Add the coin to the lists

            self.frostfire_list.append(frostfire)
            


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # Draw all the sprites.
        self.scene.draw()
        self.player_list.draw()
        self.frostfire_list.draw()

        # Draw info on the screen
        sprite_count = len(self.scene["walls"])

        output = f"Sprite Count: {sprite_count}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         SCREEN_HEIGHT - 20 + self.view_bottom,
                         arcade.color.WHITE, 16)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         SCREEN_HEIGHT - 40 + self.view_bottom,
                         arcade.color.WHITE, 16)

        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         SCREEN_HEIGHT - 60 + self.view_bottom,
                         arcade.color.WHITE, 16)

        self.draw_time = timeit.default_timer() - draw_start_time

       
    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
    
        self.player_sprite.update()
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["walls"]):
            self.setup() # Restart the game on collision
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["walls"]):
            self.setup() # Restart the game on collision

        # Generate a list of all sprites that collided with the player.
        frostfires_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.frostfire_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for frostfire in frostfires_hit_list:
            frostfire.remove_from_sprite_lists()
            self.score += 1

        start_time = timeit.default_timer()

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time
  
  # Generate a list of all sprites that collided with the player.
        frostfires_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.frostfire_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for frostfire in frostfires_hit_list:
            frostfire.remove_from_sprite_lists()
            self.score += 1

class InstructionView(arcade.View):

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

    def main():
        """ Main function """

       

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)

   
    arcade.run()


if __name__ == "__main__":
    main()