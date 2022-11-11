# import the arcade library
import arcade
import arcade.gui
# import random library
import random
import time

#set screen width, height and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Simon"


class StartView(arcade.View):
    # Starting View

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.GOLDENROD)
        # import uimanager for the start button
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)


    def on_draw(self):
        # Draw Start View
        arcade.start_render()
        arcade.draw_text("SIMON", self.window.width / 2, self.window.height / 1.5,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        # initialize start button
        start_button = arcade.gui.UIFlatButton(text="Click Here To Start",
                                               width=200)

        # Assigning our on_buttonclick() function
        start_button.on_click = self.on_startclick


        # Adding button in our uimanager
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=start_button)
        )
        self.uimanager.draw()

    def on_startclick(self, event):
        # When the user presses the button start the game at level 1
        self.uimanager.disable()
        # disable and clear the uimanager so the button doesn't keep showing up
        self.uimanager.clear()
        main_game = MainGame(1)
        # Open a new window
        self.window.show_view(main_game)


class LevelView(arcade.View):
    # View for when the user levels up

    def __init__(self, level):
        # init gets passes the level so it can tell user what the next level is
        super().__init__()
        arcade.set_background_color(arcade.color.FOREST_GREEN)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.level = level

    def on_draw(self):
        # Draw the view
        self.clear()
        arcade.draw_text(f"Nice! Moving On To Level {self.level}", self.window.width / 2, self.window.height / 1.5,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Click anywhere to move on", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=25, anchor_x="center")
        arcade.finish_render()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # The user can click anywhere on screen to move on
        game_view = MainGame(self.level)

        self.window.show_view(game_view)


class GameOverView(arcade.View):
    # View for when the game is over

    def __init__(self, level):
        # passed level to display what the last level they made it to was
        super().__init__()
        arcade.set_background_color(arcade.color.AUBURN)
        self.level = level

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        # draw the view
        self.clear()
        arcade.draw_text("Sorry! Game Over", self.window.width / 2, self.window.height / 1.5,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text(f"You made it to level {self.level}", self.window.width / 2, self.window.height / 1.8,
                         arcade.color.WHITE, font_size=32, anchor_x="center")
        arcade.draw_text("Click anywhere to close", self.window.width / 2, self.window.height / 2.5,
                         arcade.color.WHITE, font_size=18, anchor_x="center")
        arcade.finish_render()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # click anywhere to close the window
        self.window.close()


class MainGame(arcade.View):
    def __init__(self, level):
        super().__init__()
        # passed level from start as 1 and adds whenever the game is run
        # Changing background color of screen
        arcade.set_background_color(arcade.color.BLACK)

        # track mouse movement
        self.x = 100
        self.y = 100

        # z keeps track of user input. p keeps track of the game input
        self.z = []
        self.p = []
        # i is used to track the index
        self.i = 0
        self.level = level
        
        # draw simon twice with a short break so there is time between start and when the 
        # game starts providing output
        self.draw_simon()
        arcade.finish_render()
        time.sleep(.25)
        self.draw_simon()
        # play game
        self.game_play()

        arcade.finish_render()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.x = x
        self.y = y

    # Creating function to check the mouse clicks
    def on_mouse_press(self, x, y, button, modifiers):
        # checks the square and passes input to the answer function to get checked
        if 75 < x < 375 and 290 < y < 525:
        # Red
            self.z.append("R")
            self.answer()

        elif 75 < x < 375 and 25 < y < 260:
        # Green
            self.z.append("G")
            self.answer()

        elif 425 < x < 725 and 25 < y < 260:
        # Blue
            self.z.append("B")
            self.answer()

        elif 425 < x < 725 and 290 < y < 525:
        # Yellow
            self.z.append("Y")
            self.answer()

    def draw_simon(self):
    # This draws the main board
        self.clear()
        arcade.draw_lrtb_rectangle_filled(75, 375, 525, 290, arcade.color.RED)
        arcade.draw_lrtb_rectangle_filled(75, 375, 260, 25, arcade.color.GREEN)
        arcade.draw_lrtb_rectangle_filled(425, 725, 260, 25, arcade.color.BLUE)
        arcade.draw_lrtb_rectangle_filled(425, 725, 525, 290, arcade.color.YELLOW)


    def game_play(self):
        # l is the list of possible outputs
        l = ["R", "G", "B", "Y"]
        a = ""
        for i in range(self.level):
        # output as many times as level ex level 3 has 3 outputs 
            c = random.choice(l)
            # no repeat colors
            while c == a:
                c = random.choice(l)
            a = c
            self.colors(c)
            self.p.append(c)


    def answer(self):
        # print functions I used when testing
        # print(f"z: {self.z[self.i]}")
        # print(f"P: {self.p[self.i]}")
        # print(f"I: {self.i}")
        # print(f"L: {self.level-1}")
        # print(f"TRUE: {self.i == self.level-1}")

        if self.z[self.i] == self.p[self.i]:
        # check the input and output match
            if self.i == self.level-1:
            # see if we reached the end of the input if we did call new level
                self.level += 1
                levelView = LevelView(self.level)
                self.window.show_view(levelView)

        else:
        # if input and output don't match end the game
            view = GameOverView(self.level)
            self.window.show_view(view)

        self.i += 1

    def colors(self, c):
    # This draws the output onto the simon board
    # There is a time delay so the output stays on the screen long enough to see
        if c == "R":
            arcade.draw_circle_filled(225, 50 + 360, 50, arcade.color.AUBURN)
            arcade.finish_render()
            time.sleep(.85)
            self.draw_simon()

        elif c == "G":
            arcade.draw_circle_filled(225, 50 + 90, 50, arcade.color.FOREST_GREEN)
            arcade.finish_render()
            time.sleep(.85)
            self.draw_simon()

        elif c == "B":

            arcade.draw_circle_filled(575, 50 + 90, 50, arcade.color.CELESTIAL_BLUE)
            arcade.finish_render()
            time.sleep(.85)
            self.draw_simon()

        else:
            arcade.draw_circle_filled(575, 50 + 360, 50, arcade.color.GOLDENROD)
            arcade.finish_render()
            time.sleep(.85)
            self.draw_simon()


def main():
    # Open a window and call the start function 

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

