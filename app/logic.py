from time import perf_counter


def _add_to_unique_coordinates(unique_coordinates, new_coordinates):
    """
    Tiny helper function to add the tuples in `path` to the set of tuples
    in `unique_places`. The set is updated in place, so no need to return
    it.

    :param set unique_coordinates: Set of (x, y) tuples
    :param list new_coordinates: List of (x, y) tuples, to be added to the set
    """
    for coordinate in new_coordinates:
        unique_coordinates.add(coordinate)


def _get_vertices(start, command):
    """
    Helper function to determine all vertices of a command. Starts out
    at the `start` (x, y) coordinates and takes a number of "steps" in
    the "direction". Does not include the `current_place` in the resulting
    output.

    Directions can be "north", "east", "south" and "west" and the path
    should logically follow that direction.

    :param tuple start: Tuple of a (x, y) coordinate
    :param dict command: Dictionary containing "steps" and "direction"
    :return: A list of the path with all (x, y) coordinates
    """

    # Setup for the ranges to be added or subtracted from the coordinates
    range_sequence = range(1, command["steps"] + 1)

    # Moving north means the y-axis will increase
    if command["direction"] == "north":
        return [(start[0], start[1] + i) for i in range_sequence]

    # Moving east means the x-axis will increase
    if command["direction"] == "east":
        return [(start[0] + i, start[1]) for i in range_sequence]

    # Moving south means the y-axis will decrease
    if command["direction"] == "south":
        return [(start[0], start[1] - i) for i in range_sequence]

    # Moving west means the x-axis will decrease
    if command["direction"] == "west":
        return [(start[0] - i, start[1]) for i in range_sequence]

    # This shouldn't happen, but returning the original coordinate here
    # will technically ignore this command
    return [start]


def calculate_unique_coordinates(start_point, commands):
    """
    Main function for calculating the number of unique coordinates the robot
    touches, assuming the robot cleans at every vertex it touches, not
    just where it stops.

    :param tuple start_point: The (x, y) coordinates of the starting point
    :param list commands: List of commands with a "direction" and "steps"
    :return: A tuple containing (result, duration)
    """

    # Start time for the duration
    start_time = perf_counter()

    # Keep track of unique places visited, the starting point is the first
    current_coordinate = start_point
    unique_coordinates = {start_point}

    for command in commands:
        # For each command, calculate its path, then add it to the set of
        # unique places and finally extract the last item from that list
        # as the new current position so that it can be used recursively
        vertices = _get_vertices(current_coordinate, command)
        _add_to_unique_coordinates(unique_coordinates, vertices)
        current_coordinate = vertices[-1]

    # Calculate duration based on the start time
    duration = perf_counter() - start_time

    # Return the results
    return len(unique_coordinates), duration
