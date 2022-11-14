from math import sqrt


class Asteroid:
    """
    asteroids in the screen, can destroy the ship and split into small
    asteroids when hit by a torpedo
    """

    def __init__(self, x, y, speed_x, speed_y, size=3):
        """
        create a new asteroid
        """
        self.x = x
        self.y = y
        self.x_speed = speed_x
        self.y_speed = speed_y
        self.size = size
        self.radius = size * 10 - 5

    def get_location_x(self):
        """
        get the asteroid location
        """
        return self.x

    def set_location_x(self, x):
        """
        set the asteroid location to the new location
        """
        self.x = x

    def get_location_y(self):
        """
        get the asteroid location
        """
        return self.y

    def set_location_y(self, y):
        """
        set the asteroid location to the new location
        """
        self.y = y

    def get_speed_x(self):
        """
        get asteroid speed, returns a tuple (x_speed, y_speed)
        """
        return self.x_speed

    def set_speed_x(self, new_x_speed):
        """
        set a new speed to the asteroid
        """
        self.x_speed = new_x_speed

    def get_speed_y(self):
        """
        get asteroid speed, returns a tuple (x_speed, y_speed)
        """
        return self.y_speed

    def set_speed_y(self, new_y_speed):
        """
        set a new speed to the asteroid
        """
        self.y_speed = new_y_speed

    def get_size(self):
        """
        get the size of the asteroid
        """
        return self.size

    def set_size(self, new_size):
        """
        set the size of the asteroid to a new size
        """
        self.size = new_size
        self.radius = new_size * 10 - 5

    def get_radius(self):
        """
        get the size of the asteroid
        """
        return self.radius

    def has_intersection(self, obj):
        """
        check if the asteroid ha collided with something
        param: obj: can be ship or torpedo
        return: True if a collision has accrued, False if none accrued
        """
        x_distance = (obj.get_location_x() - self.x)**2
        y_distance = (obj.get_location_y() - self.y)**2
        distance = sqrt(x_distance + y_distance)
        if distance <= self.radius + obj.get_radius():
            # if there is an intersection
            return True
        return False
