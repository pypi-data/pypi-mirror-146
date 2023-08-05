"""
Task: Create a triangle class. Your triangle class should have three default values.
Your triangle class should have methods `get_base, get_height, get_area, is_`.

"""

class Triangle:
    def __init__(self, first, second, third):
        self.first_side = first
        self.second_side = second
        self.third_side = third

    def get_area(self):
        semi = self.calculate_semi_perimeter()
        area = sqrt(semi * (semi - self.first_side) * (semi - self.second_side) * (semi - self.third_side))
        return ('%0.2f' %area)

    def is_isosceles(self):
        if (
            (self.first_side == self.second_side and self.third_side < self.first_side) or
            (self.first_side == self.third_side and self.second_side < self.first_side) or
            (self.second_side == self.third_side and self.first_side < self.second_side)
        ):
            return True
        return False

    def is_equilateral(self):
        return self.first_side == self.second_side == self.third_side

    def is_scalene(self):
        return self.first_side != self.second_side != self.third_side

    def calculate_semi_perimeter(self):
        semi_perimeter = (self.first_side + self.second_side + self.third_side) / 2
        return semi_perimeter
