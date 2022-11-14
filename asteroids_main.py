from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from math import cos, sin, radians, sqrt
from random import randint
import sys

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    POINT_DICT = {3: 20, 2: 50, 1: 100}
    RIGHT = "right"
    LEFT = "left"
    CRUSH_MSG_DICT = {"title": "CRUSHED!!!",
                      "crush": "You crushed into asteroid, be more careful ",
                      "lives": "lives left"}
    END_GAME_MSG = {"Win": "The Force is strong with this one",
                    "Lose": "The dark side was victorious today...",
                    "Quit": "quitters will be quitters"}
    TORPEDO_LIFE_SPAN = 200
    TORPEDO_LIMIT = 10
    DEGREES_PER_PRESS = 7

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        x, y = self.rand_location()
        self.ship = Ship(x, y)
        self.delta_x = self.__screen_max_x - self.__screen_min_x
        self.delta_y = self.__screen_max_y - self.__screen_min_y
        self.torpedo_lst = []
        self.asteroids_list = []
        self.points = 0
        for i in range(asteroids_amount):
            self.asteroids_list.append(self.create_asteroid())
            self.__screen.register_asteroid(self.asteroids_list[-1], 3)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        the main function of the game, all the actions the game does every
        loop
        return: None
        """
        self.check_key_pressed()  # check if a key is pressed
        self.update_locations()  # update all the objects location
        self.check_hits()  # check if there were any torpedoes hits or crushes
        self.update_screen()  # draw current objects locations on screen
        self.end_of_game()  # checks if the game is over and closes the func

    # initiate game methods ##################################################

    def rand_location(self):
        """
        create a random location inside the board
        return: x location and y location
        """
        x = randint(self.__screen_min_x, self.__screen_max_x)
        y = randint(self.__screen_min_y, self.__screen_max_y)
        return x, y

    def rand_asteroid_speed(self):
        """
        gets a random heading and speed for the asteroid
        the number for x and y speed can be ints between (-4, 4)
        return: x speed and y speed
        """
        speed_x = randint(1, 8)
        speed_y = randint(1, 8)
        if speed_x > 4:  # if the number should be between (-1 to -4)
            speed_x = -1 * (speed_x - 4)
        if speed_y > 4:  # if the number should be between (-1 to -4)
            speed_y = -1 * (speed_y - 4)
        return speed_x, speed_y

    def create_asteroid(self):
        """
        creates a new asteroid for the beginning of the game
        makes sure the asteroid doesn't collapse with ship when created
        return: the new valid asteroid
        """
        while True:  # creating new asteroids until one doesnt crush with ship
            x, y = self.rand_location()
            speed_x, speed_y = self.rand_asteroid_speed()
            new_asteroid = Asteroid(x, y, speed_x, speed_y)
            if not new_asteroid.has_intersection(self.ship):
                # if asteroid doesnt crush with ship
                return new_asteroid

    # update screen methods ##################################################

    def update_screen(self):
        """
        draw all the current objects locations on the screen
        return None
        """
        self.__screen.draw_ship(self.ship.get_location_x(),
                                self.ship.get_location_y(),
                                self.ship.get_heading())
        self.draw_asteroids()
        self.draw_torpedoes()

    def draw_asteroids(self):
        """
        update the screen with all the asteroids new locations
        return: None
        """
        for asteroid in self.asteroids_list:  # run through all asteroids
            self.__screen.draw_asteroid(asteroid, asteroid.get_location_x(),
                                        asteroid.get_location_y())

    def draw_torpedoes(self):
        """
        update the screen with all the torpedoes new locations
        return: None
        """
        for torpedo in self.torpedo_lst:  # run through all torpedoes
            self.__screen.draw_torpedo(torpedo, torpedo.get_location_x(),
                                       torpedo.get_location_y(),
                                       torpedo.get_heading())

    # player press keyboard methods ##########################################

    def check_key_pressed(self):
        """
        Checks which key was pressed and moves the ship or shoots a torpedo
        according
        to the key which was pressed
        return None
        """
        if self.__screen.is_right_pressed():
            self.turn_ship(GameRunner.RIGHT)

        if self.__screen.is_left_pressed():
            self.turn_ship(GameRunner.LEFT)

        if self.__screen.is_up_pressed():
            self.speed_up_ship()

        if self.__screen.is_space_pressed():
            self.shoot_torpedo()

    def shoot_torpedo(self):
        """
        if there are less torpedoes than torpedoes limit Shoot a torpedo
        based on ship's arguments and add it to the game
        :return: None
        """
        if len(self.torpedo_lst) < GameRunner.TORPEDO_LIMIT:
            # if the max torpedo number wasn't reached, then create another
            x = self.ship.get_location_x()
            y = self.ship.get_location_y()
            heading = self.ship.get_heading()
            torpedo_speed_x, torpedo_speed_y = self.cal_torpedo_speed()
            torpedo = Torpedo(x, y, heading, torpedo_speed_x, torpedo_speed_y)
            self.__screen.register_torpedo(torpedo)
            self.torpedo_lst.append(torpedo)

    def cal_torpedo_speed(self):
        """
        Calculates the torpedo speed from the given formula in the exercise
        :return: (tuple) torpedo_speed_x, torpedo_speed_y the speed on x and
        y axises
        """
        torpedo_speed_x = self.ship.get_speed_x() + 2 * cos(
            radians(self.ship.get_heading()))
        torpedo_speed_y = self.ship.get_speed_y() + 2 * sin(
            radians(self.ship.get_heading()))
        return torpedo_speed_x, torpedo_speed_y

    def turn_ship(self, direction):
        """
        turns the ship 7 degrees in the given direction
        param: direction: the direction to turn to
        return: None
        """
        if direction == GameRunner.RIGHT:
            self.ship.set_heading(self.ship.get_heading() -
                                  GameRunner.DEGREES_PER_PRESS)
        if direction == GameRunner.LEFT:
            self.ship.set_heading(self.ship.get_heading() +
                                  GameRunner.DEGREES_PER_PRESS)

    def speed_up_ship(self):
        """
        Accelerates the self.ship using the given formula
        :return: None
        """
        x_speed = self.ship.get_speed_x()
        y_speed = self.ship.get_speed_y()
        new_speed_x = x_speed + cos(radians(self.ship.get_heading()))
        new_speed_y = y_speed + sin(radians(self.ship.get_heading()))
        self.ship.set_speed_x(new_speed_x)
        self.ship.set_speed_y(new_speed_y)

    # check hits methods #####################################################

    def check_hits(self):
        """
        Checks if there was a hit of the ship in asteroid or a torpedo in
        asteroid, and updates the game if there was a hit
        return None
        """
        self.ship_crush_asteroid()
        self.search_torpedo_hit()

    def ship_crush_asteroid(self):
        """
        check if the ship has crushed into one of the asteroids
        if it did, reduce ship's life and removing the asteroid
        return: None
        """
        for asteroid in self.asteroids_list:  # checking all asteroids
            if asteroid.has_intersection(self.ship):  # if ship crushed
                self.ship.lose_live()
                self.__screen.unregister_asteroid(asteroid)
                self.asteroids_list.remove(asteroid)
                self.__screen.remove_life()
                if self.ship.get_lives() != 0:  # if there are lives left
                    self.__screen.show_message(GameRunner.CRUSH_MSG_DICT[
                                                   "title"],
                                               GameRunner.CRUSH_MSG_DICT[
                                                   "crush"]
                                               + str(self.ship.lives)
                                               + GameRunner.CRUSH_MSG_DICT[
                                                   "lives"])

    def search_torpedo_hit(self):
        """
        The function check if the torpedo hit an asteroid
        return: None
        """
        for asteroid in self.asteroids_list:  # checking all asteroids
            for torpedo in self.torpedo_lst:  # checking all torpedoes
                if asteroid.has_intersection(torpedo):  # if a torpedo hit
                    self.torpedo_hit(torpedo, asteroid)
                    break  # break to avoid double torpedo hit

    def torpedo_hit(self, torpedo, asteroid):
        """
        The function does sequence of action that happens when a torpedo hits
        an asteroid
        :param torpedo: (torpedo) our torpedo in game
        :param asteroid: (asteroid) the asteroid which was hit by torpedo
        :return: None
        """
        size = asteroid.get_size()
        self.add_points(size)
        self.split_asteroid(asteroid, torpedo)
        self.__screen.unregister_asteroid(asteroid)
        self.__screen.unregister_torpedo(torpedo)
        self.asteroids_list.remove(asteroid)
        self.torpedo_lst.remove(torpedo)

    def split_asteroid(self, asteroid, torpedo):
        """
        the function splits an asteroid that was hit by a torpedo  into two
        smaller asteroids
        :param asteroid: (asteroid) the asteroid which was hit by torpedo
        :param torpedo: (torpedo) our torpedo in game
        :return: None
        """

        size = asteroid.get_size()
        if size > 1:  # if the asteroid size is 1, skip this method
            new_size = size - 1
            new_speed1, new_speed2 = self.asteroid_speed_after_split(asteroid,
                                                                     torpedo)
            x, y = asteroid.get_location_x(), asteroid.get_location_y()
            asteroid1 = Asteroid(x, y, new_speed1[0], new_speed1[1], new_size)
            asteroid2 = Asteroid(x, y, new_speed2[0], new_speed2[1], new_size)
            self.asteroids_list.append(asteroid1)
            self.asteroids_list.append(asteroid2)
            self.__screen.register_asteroid(asteroid1, new_size)
            self.__screen.register_asteroid(asteroid2, new_size)

    def asteroid_speed_after_split(self, asteroid, torpedo):
        """
        Calculates the speed of the new asteroids after the old asteroid was
        hit by torpedo
        :param asteroid: (asteroid) the asteroid which was hit by torpedo
        :param torpedo: (torpedo) our torpedo in game
        :return:(tuple of two tuples) pos_speed, neg_speed
        """
        old_asteroid_speed_x = asteroid.get_speed_x()
        old_asteroid_speed_y = asteroid.get_speed_y()

        new_asteroid_speed_x = (torpedo.get_speed_x() + old_asteroid_speed_x) \
                               / sqrt((old_asteroid_speed_x ** 2
                                       + old_asteroid_speed_y ** 2))
        new_asteroid_speed_y = (torpedo.get_speed_y() + old_asteroid_speed_y) \
                               / sqrt((old_asteroid_speed_x ** 2 +
                                       old_asteroid_speed_y ** 2))

        pos_speed = (new_asteroid_speed_x, new_asteroid_speed_y)
        neg_speed = (- new_asteroid_speed_x, - new_asteroid_speed_y)
        return pos_speed, neg_speed

    def add_points(self, size):
        """
        adds points, to the player if he hit asteroid with torpedo,
        updating the screen with the new score
        return: None
        """
        self.points += GameRunner.POINT_DICT[size]
        self.__screen.set_score(self.points)

    # update location methods ################################################

    def update_locations(self):
        """
        update all the objects location
        return: None
        """
        self.move_ship()
        self.move_asteroids()
        self.move_torpedoes()
        self.torpedo_life_time()

    def move_object(self, obj):
        """
        The function moves objects according to the formula which was given.
        :param self: (game) The game
        :param obj: (ship/asteroid/torpedo)
        :return: None
        """
        new_spot_x = self.__screen_min_x + (
                obj.get_location_x() + obj.get_speed_x()
                - self.__screen_min_x) % self.delta_x
        new_spot_y = self.__screen_min_y + (
                obj.get_location_y() + obj.get_speed_y()
                - self.__screen_min_y) % self.delta_x
        obj.set_location_x(new_spot_x)
        obj.set_location_y(new_spot_y)

    def move_ship(self):
        """
        uses move_object method in order to move ship
        """
        self.move_object(self.ship)

    def move_asteroids(self):
        """
        uses move_object method in order to move all asteroids
        """
        for asteroid in self.asteroids_list:  # run thorough all asteroids
            self.move_object(asteroid)

    def move_torpedoes(self):
        """
        uses move_object method in order to move all torpedoes
        """
        for torpedo in self.torpedo_lst:  # run thorough all torpedoes
            self.move_object(torpedo)

    def torpedo_life_time(self):
        """
        Updates the torpedo life time and removes torpedo that passed the
        time limit
        :return: None
        """
        for torpedo in self.torpedo_lst:  # checks all torpedoes
            if torpedo.get_time() == self.TORPEDO_LIFE_SPAN:
                # if a torpedo reached his iterations limit
                self.__screen.unregister_torpedo(torpedo)
                self.torpedo_lst.remove(torpedo)
            else:
                torpedo.add_1_sec()

    # end game methods #######################################################

    def close_game(self, msg):
        """
        sending a message of why the game ended,
        terminate the screen, then terminate the function.
        return: None
        """
        self.__screen.show_message(msg, self.END_GAME_MSG[msg])
        self.__screen.end_game()
        sys.exit()

    def end_of_game(self):
        """
        check whether the game should end, win, lose or quit
        return: None
        """
        if self.ship.get_lives() == 0:  # if no lives left
            self.close_game("Lose")
        if len(self.asteroids_list) == 0:  # if no more asteroids are "alive"
            self.close_game("Win")
        if self.__screen.should_end():  # if the player wants to quit
            self.close_game("Quit")


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
