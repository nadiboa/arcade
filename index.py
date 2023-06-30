import random
import arcade
import timeit
import os


FROSTFIRE_COUNT = 100


SCALE = 1
SCREEN_WIDTH = 960 * SCALE
SCREEN_HEIGHT = 540* SCALE
SCREEN_TITLE = "Maze Depth First Example"

MOVEMENT_SPEED = 1

TILE_SIZE = 48 * SCALE


MERGE_SPRITES = True
PLAYER_MAX_HEALTH = 3
DAMAGE_COOLDOWN=0.5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 100


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
        self.heart_list = None
        
        
      
        # Player info
        self.score = 0
        self.player_sprite = None
        self.player_health= 0
        self.time_since_last_damage = 0

        # Physics engine
        self.physics_engine = None

        # Used to scroll
        self.view_bottom = 0
        self.view_left = 0

        # Map size
        self.map_height = 0
        self.map_width = 0

        # Time to process
        self.processing_time = 0
        self.draw_time = 0

        self.timer = 0

    def setup(self, level):
        """ Set up the game and initialize the variables. """
        self.player_health=PLAYER_MAX_HEALTH
        self.time_since_last_damage = 0
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.frostfire_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()
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
             "player spawn": {
                "use_spatial_hash": True,
            },
             "icechunk": {
                "use_spatial_hash": True,
            },
        }
        self.level = level
        if self.level == 1:
            arcade.set_background_color(arcade.color.ICEBERG)
            self.tilemap = arcade.load_tilemap("tilemap test.tmx", SCALE, layer_options)
        elif self.level == 2:
            arcade.set_background_color(arcade.color.BLUE_GREEN)
            self.tilemap = arcade.load_tilemap("tilemapleveltwo.tmx", SCALE, layer_options)
        elif self.level== 3:
            arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)
            self.tilemap = arcade.load_tilemap("tilemaplevelthree.tmx", SCALE, layer_options)
        else:
            game_view= WinView()
            self.window.show_view(game_view)



                
            

        self.scene = arcade.Scene.from_tilemap(self.tilemap)
        # give number tiles not pixel size
        self.map_width = self.tilemap.width
        self.map_height = self.tilemap.height

        # Set up the player
        self.player_sprite = arcade.Sprite("new player(candel).png.png"
                                          ,
                                           SCALE)
        self.player_list.append(self.player_sprite)
        # Randomly place the player. If we are in a wall, repeat until we aren't.


        # Randomly position
        self.player_sprite.center_x = self.scene["player spawn"][0].center_x
        self.player_sprite.center_y = self.scene["player spawn"][0].center_y
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene["walls"])
        #for heart
        if self.level>1:
            for i in range(self.player_health):
                playerhealth = arcade.Sprite("playerhealth.png",
                                 SCALE)
                playerhealth.center_x = self.player_sprite.center_x
                playerhealth.center_y = self.player_sprite.center_y
                self.heart_list.append(playerhealth)

        

       

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
            
            frostfire.center_x = random.randrange(self.map_width * TILE_SIZE)
            frostfire.center_y = random.randrange(self.map_height * TILE_SIZE)

            # Are we in a wall?
            #walls_hit = arcade.check_for_collision_with_list(self.frostfire_list[i], self.scene["walls"])
            walls_hit = arcade.check_for_collision_with_list(frostfire, self.scene["walls"])
            if len(walls_hit) != 0:
                # Not in a wall! Success!
                continue
            self.physics_engine = arcade.PhysicsEngineSimple(frostfire, self.scene["walls"])

            # Add the coin to the lists

            self.frostfire_list.append(frostfire)
        arcade.schedule(self.update_timer, 1.0)  # Schedule timer update every 1 second
            


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
        self.heart_list.draw()

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
        
        output = f"Timer: {self.timer}"
        arcade.draw_text(output, self.player_sprite.center_x, self.player_sprite.center_y, arcade.color.BLACK, 14)

        self.draw_time = timeit.default_timer() - draw_start_time

       
    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
       
        movement_x = dx * MOVEMENT_SPEED
        movement_y = dy * MOVEMENT_SPEED

        # Update the player's position by applying the movement vector
        self.player_sprite.center_x += movement_x
        self.player_sprite.center_y += movement_y
        


    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.update()

        left, right, bottom, top = arcade.get_viewport()

        for index, sprite in enumerate(self.heart_list):

            # Set the sprite's position relative to the viewport
            sprite.left = left + sprite.width / 2 + index*sprite.width
            sprite.top = top - sprite.height / 2


        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["walls"]):
            game_view = WallDeathView()
            self.window.show_view(game_view)

        # Generate a list of all sprites that collided with the player.
        frostfires_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.frostfire_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for frostfire in frostfires_hit_list:
            frostfire.remove_from_sprite_lists()
            self.score += 1 

        # Generate a list of all sprites that collided with the player.
        ice_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.scene['icechunk'])

        # Loop through each colliding sprite, remove it, and add to the score.
        
        for icechunk in ice_hit_list:
            icechunk.remove_from_sprite_lists()
            self.player_health-=1
            self.heart_list[-1].remove_from_sprite_lists()
            if self.player_health<=0:
                game_view= WallDeathView()
                self.window.show_view(game_view)

        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["doors"]):
            self.setup(self.level+1) # going to next level

        start_time = timeit.default_timer()

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()
        #camera code

        print(self.player_sprite.center_x - SCREEN_WIDTH/2)
        arcade.set_viewport(
            self.player_sprite.center_x - SCREEN_WIDTH/2,
            self.player_sprite.center_x + SCREEN_WIDTH/2,
            self.player_sprite.center_y - SCREEN_HEIGHT/2,
            self.player_sprite.center_y + SCREEN_HEIGHT/2
        )

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time

  
  # Generate a list of all sprites that collided with the player.
        frostfires_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.frostfire_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for frostfire in frostfires_hit_list:
            frostfire.remove_from_sprite_lists()
            self.score += 1

        

    def update_timer(self, delta_time):
        self.timer += 1

class InstructionView(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()  # Start the rendering
        arcade.draw_text("CANDELABRA CHAMPION", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance.WATCH OUT FOR ICE YOU'RE A CANDEL. USE THE MOUSE TO AVOID THE ICE", self.window.width / 2, self.window.height / 2-75,
                         color=arcade.color.WHITE,multiline=True, width=SCREEN_WIDTH, font_size=20,anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = MyGame()
        game_view.setup(1)
        self.window.show_view(game_view)

class WinView(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        print("Switched to WinView")
        arcade.set_background_color(arcade.csscolor.YELLOW)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        print("Drawing WinView")
        arcade.start_render()  # Start the rendering

        self.clear()
        arcade.draw_text("CANDELABRA CHAMPION", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance.WATCH OUT FOR ICE YOU'RE A CANDEL. USE THE MOUSE TO AVOID THE ICE", self.window.width / 2, self.window.height / 2-75,
                         color=arcade.color.WHITE,multiline=True, width=self.window.width, font_size=20,anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = InstructionView()
        self.window.show_view(game_view)


class WallDeathView(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        print("Switched to WallDeathView")
        arcade.set_background_color(arcade.color.ICEBERG)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        print("Drawing WallDeathView")
        arcade.start_render()  # Start the rendering

        arcade.draw_text("CANDELABRA CHAMPION", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance.WATCH OUT FOR ICE YOU'RE A CANDEL. USE THE MOUSE TO AVOID THE ICE", self.window.width / 2, self.window.height / 2-75,
                         color=arcade.color.WHITE,multiline=True, width=self.window.width, font_size=20,anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = InstructionView()
        self.window.show_view(game_view)
'''       
#player death screen one(walls)
class WallDeathView(arcade.View):
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ICEBERG)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_text("CANDELABRA CHAMPION", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance.WATCH OUT FOR ICE YOU'RE A CANDEL. USE THE MOUSE TO AVOID THE ICE", self.window.width / 2, self.window.height / 2-75,
                         color=arcade.color.WHITE,multiline=True, width=SCREEN_WIDTH, font_size=20,anchor_x="center")
                         

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = InstructionView()
        self.window.show_view(game_view)
'''

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_exclusive_mouse(True)
    start_view = InstructionView()
    window.show_view(start_view)

   
    arcade.run()


if __name__ == "__main__":
    main()