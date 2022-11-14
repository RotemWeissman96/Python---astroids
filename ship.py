class Ship:
    """
    The class represents the ship
    """

    SHIP_RADIUS = 1
    STARTING_LIVES = 3

    def __init__(self, x, y, heading=0, x_speed=0, y_speed=0):
        self.x = x
        self.y = y
        self.heading = heading
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.lives = Ship.STARTING_LIVES

    def get_location_x(self):
        """
        gets the ship coordinate on x axis
        :return: (int) x coordinate
        """
        return self.x

    def get_location_y(self):
        """
        gets the ship coordinate on y axis
        :return: (int) y coordinate
        """
        return self.y

    def get_speed_x(self):
        """
        gets the ship's speed in x axis
        :return: (int) speed on x axis
        """
        return self.x_speed

    def get_speed_y(self):
        """
        gets the ship's speed in y axis
        :return: (int) speed on y axis
        """
        return self.y_speed

    def get_heading(self):
        """
        returns the ship's angle
        :return:
        """
        return self.heading

    def set_speed_x(self, new_x_speed):
        """
        sets the speed in the direction of x axis
        :return: (int) the speed on x axis
        """
        self.x_speed = new_x_speed

    def set_speed_y(self, new_y_speed):
        """
        sets the speed in the direction of y axis
        :param new_y_speed: (int) the new speed on y axis
        :return: None
        """

        self.y_speed = new_y_speed

    def set_heading(self, angle):
        """
        changes the ship's angle
        :return:
        """
        self.heading = angle

    def set_location_x(self, new_location_x):
        """
        sets the location in the direction of x axis
        :return: (int) the speed on x axis
        """
        self.x = new_location_x

    def set_location_y(self, new_location_y):
        """
        sets the location in the direction of y axis
        :return: (int) the speed on y axis
        """
        self.y = new_location_y

    def get_radius(self):
        """
        get the radius of the ship
        """
        return Ship.SHIP_RADIUS

    def get_lives(self):
        """
        get the lives the ship has left
        """
        return self.lives

    def lose_live(self):
        """
        lose a life, reduce live by 1
        """
        self.lives = self.lives - 1
