class Torpedo:
    """
    The class represents the torpedoes in the game
    """
    TORPEDO_RADIUS = 4

    def __init__(self, x, y, heading, x_speed, y_speed):
        self.x = x
        self.y = y
        self.heading = heading
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.time = 0

    def get_location_x(self):
        """
        gets the ship coordinate
        :return: (int) x coordinate
        """
        return self.x

    def get_location_y(self):
        """
        gets the ship coordinate
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
        returns torpedo's angle
        :return:
        """
        return self.heading

    def set_speed_x(self):
        """
        set the speed in the direction of x axis
        :return: (int) the speed on x axis
        """
        return self.x_speed

    def set_speed_y(self):
        """
        set the speed in the direction of y axis
        :return: (int) the speed on y axis
        """
        return self.y_speed

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

    def set_time(self, new_time):
        """
        set the life span of the torpedo
        """
        self.time = new_time

    def get_time(self):
        """
        get the life span of the torpedo
        """
        return self.time

    def add_1_sec(self):
        """
        add 1 game loop to the torpedo life span
        """
        self.time += 1

    def get_radius(self):
        """
        get the radius of the torpedo
        """
        return Torpedo.TORPEDO_RADIUS
