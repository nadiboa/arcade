
import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_FROSTFIRE = 0.5
FROSTFIRE_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect frostfire "


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.player_list = None
        self.frostfire_list = None
        self.walls = None


        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.ICEBERG)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.frostfire_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        # Score
        self.score = 0

        # Set up the player
       
        # Create the maze walls
        # Add your code here to define the maze structure using the arcade.Sprite() class and add it to self.walls
       
        img = "player candel).png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(FROSTFIRE_COUNT):

            # Create the frostfire instance
           
            frostfire = arcade.Sprite("frost fire.png",
                                 SPRITE_SCALING_FROSTFIRE)

            # Position the coin
            frostfire.center_x = random.randrange(SCREEN_WIDTH)
            frostfire.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.frostfire_list.append(frostfire)
            
          
    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.frostfire_list.draw()
        self.player_list.draw()
        self.walls.draw()


        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20,
                         color=arcade.color.WHITE, font_size=14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.update()
        if arcade.check_for_collision_with_list(self.player, self.walls):
            self.setup() # Restart the game on collision
        if arcade.check_for_collision_with_list(self.player, self.walls):
            self.setup() # Restart the game on collision

        # Generate a list of all sprites that collided with the player.
        frostfires_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.frostfire_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for frostfire in frostfires_hit_list:
            frostfire.remove_from_sprite_lists()
            self.score += 1
      
def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()