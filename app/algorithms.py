from abc import ABC, abstractmethod
from bisect import bisect_left, bisect_right


class CoordinateCounter(ABC):

    def __init__(self, x_ranges, y_ranges):
        """
        Initialize any of the coordinate counters with common input.

        :param set x_ranges: Set of tuples (y_pos, start_x, end_x) for horizontal lines
        :param set y_ranges: Set of tuples (x_pos, start_y, end_y) for vertical lines
        """
        self.total = 0
        self.x_ranges = x_ranges
        self.y_ranges = y_ranges

    @abstractmethod
    def unique_coordinates(self):
        """
        Main method to be implemented for counting the unique coordinates, should return
        the number of unique coordinates.

        :return: Integer representing the number of unique coordinates
        """
        pass


class BinarySearch(CoordinateCounter):
    """Binary search implementation, which turned out to be the fastest."""

    @staticmethod
    def count_intersections(start_y, end_y, x_pos, x_by_y, y_positions):
        """
        Counts the number of intersections between vertical lines defined in `relevant_ys`
        and a horizontal line.

        :param int start_y: The start y-coordinate of the horizontal line
        :param int end_y: The ending y-coordinate of the horizontal line
        :param int x_pos: The x-coordinate of the horizontal line
        :param dict x_by_y: Dictionary for quick lookup of x-by-y coordinates
        :param list y_positions: List of relevant sorted y-coordinates

        :return: Integer representing the number of intersections
        """
        start_idx = bisect_left(y_positions, start_y)
        end_idx = bisect_right(y_positions, end_y)
        relevant_ys = y_positions[start_idx:end_idx]
        return sum(
            1
            for y in relevant_ys
            for x_start, x_end in x_by_y[y]
            if x_start <= x_pos <= x_end
        )

    def unique_coordinates(self):
        """
        Main method to be implemented for counting the unique coordinates, should return
        the number of unique coordinates.

        :return: Integer representing the number of unique coordinates
        """

        # Sort x_ranges by y position for binary search and sum of all points
        # on horizontal lines
        y_positions = sorted(set(y for y, _, _ in self.x_ranges))
        x_by_y = {y: [] for y in y_positions}
        for y, start_x, end_x in self.x_ranges:
            x_by_y[y].append((start_x, end_x))
            self.total += (end_x - start_x + 1)

        # Count vertical lines and subtract intersections
        for x_pos, start_y, end_y in self.y_ranges:
            points_in_line = end_y - start_y + 1

            # Binary search for relevant y positions
            intersections = self.count_intersections(start_y, end_y, x_pos, x_by_y, y_positions)
            self.total += points_in_line - intersections

        return self.total


class EarlyIntersectionFiltering(CoordinateCounter):
    """Second try by adding a quick looking for x-by-y coordinates before subtracting."""

    @staticmethod
    def count_intersections(start_y, end_y, x_pos, x_by_y):
        """
        Counts the number of intersections between vertical lines defined in `relevant_ys`
        and a horizontal line.

        :param int start_y: The start y-coordinate of the horizontal line
        :param int end_y: The ending y-coordinate of the horizontal line
        :param int x_pos: The x-coordinate of the horizontal line
        :param dict x_by_y: Dictionary for quick lookup of x-by-y coordinates

        :return: Integer representing the number of intersections
        """
        relevant_ys = [y for y in x_by_y if start_y <= y <= end_y]
        return sum(
            1
            for y in relevant_ys
            for x_start, x_end in x_by_y[y]
            if x_start <= x_pos <= x_end
        )

    def unique_coordinates(self):
        """
        Main method to be implemented for counting the unique coordinates, should return
        the number of unique coordinates.

        :return: Integer representing the number of unique coordinates
        """

        # Store x_ranges by y position for quick lookup and sum of all points
        # on horizontal lines
        x_by_y = {}
        for y, start_x, end_x in self.x_ranges:
            x_by_y.setdefault(y, []).append((start_x, end_x))
            self.total += (end_x - start_x + 1)

        # Count vertical lines and subtract intersections
        for x_pos, start_y, end_y in self.y_ranges:
            points_in_line = end_y - start_y + 1

            # Only check y positions that have horizontal lines
            intersections = self.count_intersections(start_y, end_y, x_pos, x_by_y)
            self.total += points_in_line - intersections

        return self.total


class SimpleIntersection(CoordinateCounter):
    """Initial try of simply subtracting intersections when counting vertical lines."""

    def count_intersections(self, start_y, end_y, x_pos):
        """
        Counts the number of intersections between vertical lines defined by `x_ranges`
        and a horizontal line.

        :param int start_y: The start y-coordinate of the horizontal line
        :param int end_y: The ending y-coordinate of the horizontal line
        :param int x_pos: The x-coordinate of the horizontal line

        :return: Integer representing the number of intersections
        """
        return sum(
            1
            for y, x_start, x_end in self.x_ranges
            if start_y <= y <= end_y and x_start <= x_pos <= x_end
        )

    def unique_coordinates(self):
        """
        Main method to be implemented for counting the unique coordinates, should return
        the number of unique coordinates.

        :return: Integer representing the number of unique coordinates
        """

        # Sum of all points on horizontal lines
        for y_pos, start_x, end_x in self.x_ranges:
            self.total += (end_x - start_x + 1)

        # Sum of all points on vertical lines, but subtract intersections
        for x_pos, start_y, end_y in self.y_ranges:
            points_in_line = end_y - start_y + 1

            # Subtract intersection points
            intersections = self.count_intersections(start_y, end_y, x_pos)
            self.total += points_in_line - intersections

        return self.total
