from collections import defaultdict
from time import perf_counter

from app.algorithms import BinarySearch


DIRECTIONS = {
    "east": (1, 0),
    "north": (0, 1),
    "south": (0, -1),
    "west": (-1, 0),
}


def _add_to_ranges(coordinate, command, x_ranges, y_ranges):
    """
    Helper function to store the start and end coordinate in either `x_ranges` or
    `y_ranges`, depending on the direction. Also calculates and returns the ending
    coordinate, to be used in future iterations.

    :param tuple coordinate: Tuple of the starting (x, y) coordinate
    :param dict command: Dictionary containing the 'direction' and 'steps'
    :param set x_ranges: Set of existing horizontal ranges of (x-axis, start, end)
    :param set y_ranges: Set of existing vertical ranges of (y-axis, start, end)

    :return: Tuple of the ending coordinate
    """

    # Calculate the distance to be traveled and the ending (x, y) coordinate
    delta_x, delta_y = DIRECTIONS[command["direction"]]
    new_x = coordinate[0] + delta_x * command["steps"]
    new_y = coordinate[1] + delta_y * command["steps"]

    # For horizontal movement, add range to the `x_ranges` set
    if not delta_y:
        start, end = sorted((coordinate[0], new_x))
        x_ranges.add((coordinate[1], start, end))

    # For vertical movement, add range to the `y_ranges` set
    elif not delta_x:
        start, end = sorted((coordinate[1], new_y))
        y_ranges.add((coordinate[0], start, end))

    # Return the ending (x, y) coordinate
    return new_x, new_y


def _merge_ranges(ranges):
    """
    After processing all ranges, they could be overlapping and should therefore be
    merged to get to the counts.

    :param set ranges: Set of tuples (y_pos, start_x, end_x) for the lines

    :return: Set of tuples (y_pos, start_x, end_x) for the lines, merged
    """

    merged_ranges = set()

    # Group ranges by axis
    grouped = defaultdict(list)
    for axis, start, end in ranges:
        grouped[axis].append((start, end))

    # Sort intervals by start and merge overlapping ranges
    for axis, intervals in grouped.items():
        intervals.sort()
        merged = []

        for start, end in intervals:
            # No overlap
            if not merged or start > merged[-1][1]:
                merged.append((start, end))

            # There's an overlap, merge ranges
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))

        # Add back to merged_ranges with axis
        for start, end in merged:
            merged_ranges.add((axis, start, end))

    return merged_ranges


def calculate_unique_coordinates(start_point, commands, algorithm=BinarySearch):
    """
    Main function to calculate the number of unique coordinates, based on the starting
    point, the commands and the used algorithm.

    :param tuple start_point: Tuple of the starting (x, y) coordinate
    :param list commands: List of dictionaries containing the 'direction' and 'steps' commands
    :param CoordinateCounter algorithm: Algorithm to be used (default is BinarySearch)

    :return: Tuple of (Integer of unique coordinates, Float of the duration)
    """

    # Start the timer
    start_time = perf_counter()

    # Initial values setup
    current = start_point
    x_ranges = set()
    y_ranges = set()

    # For each command, add a (axis, start, end) tuple to the correct range variable
    for command in commands:
        current = _add_to_ranges(current, command, x_ranges, y_ranges)

    # Use the `algorithm` to calculate the unique coordinates and return
    # that number as well as the duration of that calculation
    total = algorithm(_merge_ranges(x_ranges), _merge_ranges(y_ranges)).unique_coordinates()
    duration = perf_counter() - start_time
    return total, duration
