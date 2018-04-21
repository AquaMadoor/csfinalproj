# Brandon Azbill, bta9qf

""" Our game idea is an endless platformer, where the character progresses through an area by jumping to nearby
    (randomly generated) platforms with the ultimate to goal to progress as far as possible.
    The game will feature different kinds of platforms, that will have unique effects, as well as enemies on some of the
    platforms that will get progressively more difficult.


User Inputs:  The game’s controls will be a button to jump, a button to attack, and a button to block enemy attacks.
The scoring will be based off the amount of time the player lasts.

Graphics/Images: There will be graphics and images relating to the game.
This will include the character, different types of blocks, and different types of enemies.

Start screen: There will be a start screen that will say what button to press to start the game,
as well as highlighting the controls for the game.

Small Enough Window: The window will be small enough (800x600).

Timer: The timer will be used as the scoring mechanism for the game as well as a signal to increase the
difficulty after a certain number. For example, if the score hits an arbitrary number of 1000,
then the spawn rate for enemies will increase by a certain rate.

Health Meter: There will be a health bar for the main character (3 life system) where if the enemy takes damage from
enemies/certain blocks, a life will be removed. When all 3 lives are gone, the game will end.

Collectibles: There will be coins that will randomly spawn on certain platforms that can be collected.
The coins will give a bonus to the final score.

Enemies: Yeah, there will be some. Also, the number of enemies that will spawn will increase with the timer.
For example, the probability of the enemies spawning will increase if the timer goes over a certain number.

Animations: There will be animations for the main character when attacking and blocking.  Another animation will be
for when the spikes above the platforms fall, which will also force the main character to keep moving.
"""

import pygame
import gamebox
import random

camera = gamebox.Camera(800, 600)

score = 0
grav_counter = 0

jump_sheet = gamebox.load_sprite_sheet("game-assets/jump-sprite1.png", 5, 1)
player = gamebox.from_image(200, 200, jump_sheet[0])
player.speedy = 0
platforms = [gamebox.from_color(0, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(100, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(200, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(300, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(400, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(500, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(600, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(700, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(800, 500, (0, 153, 76), 100, 30),
             gamebox.from_color(900, 500, (0, 153, 76), 100, 30)
             ]
plat_counter = 0
start_game = False
start_screen = gamebox.from_text(390, 250, "Press Space to Start", 70, "white")
time = 0
can_move = True
controls = gamebox.from_text(390,450, "Controls:Space to Move, L-Click to Attack", 45, "white")


def tick(keys):
    global jump_sheet, player, grav_counter, platforms, plat_counter, start_game, start_screen, time, can_move
    global controls

    # Grey display
    camera.clear('grey')

    # Checks whether game has started
    if start_game is False:
        camera.draw(start_screen)
        camera.draw(controls)
        camera.display()

        if pygame.K_SPACE in keys:
            start_game = True

    if start_game is True:

        time += 1
        # Gravity

        if grav_counter <= 30:
            grav_counter += 2
            player.speedy += 5
        else:
            grav_counter = 0

        # jump animation
        if player.speedy == -15:
            player.image = jump_sheet[2]
        elif player.speedy == 15:
            player.image = jump_sheet[1]

        # Jumps when space bar is pressed
        if pygame.K_SPACE in keys and can_move is True:
            player.speedy = -30
            player.image = jump_sheet[1]
            for platform in platforms:
                platform.x -= 100
            platforms.append(gamebox.from_color(900, 500 + random.randrange(-18, 18, 3), (0, 153, 76), 100, 30))
            can_move = False
            keys.clear()

        # Stops player on platform, and makes sure only one jump can happen until platform is touched
        if player.touches(platforms[2]):
            player.bottom = platforms[2].top
            player.speedy = 0
            player.image = jump_sheet[0]
            can_move = True

        # Player is moving
        player.move_speed()

        # Removes platform after it gets off the screen
        if platforms[0].x <= -100:
            platforms.remove(platforms[0])

        # All platforms are moving and drawn
        for platform in platforms:
            # platform.move_speed()
            camera.draw(platform)

        # Sets time and scoreboard
        seconds = str(int((time / ticks_per_second)))
        score_display = gamebox.from_text(100, 50, "Score: " + seconds, 30, "black")
        camera.draw(score_display)

        camera.draw(player)
        camera.display()



ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)