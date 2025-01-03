from app import algorithms, logic


def test_add_to_ranges_east():
    """
    Tests that `_add_to_ranges` correctly adds a new entry to the `x_ranges` set in the
    'east' direction.
    """
    starting_coordinate = (10, 20)
    command = {"direction": "east", "steps": 2}
    x_ranges = set()
    y_ranges = set()

    new_coordinate = logic._add_to_ranges(starting_coordinate, command, x_ranges, y_ranges)
    assert new_coordinate == (12, 20)
    assert x_ranges == {(20, 10, 12)}
    assert y_ranges == set()


def test_add_to_ranges_north():
    """
    Tests that `_add_to_ranges` correctly adds a new entry to the `y_ranges` set in the
    'north' direction.
    """
    starting_coordinate = (12, 20)
    command = {"direction": "north", "steps": 5}
    x_ranges = {(20, 10, 12)}
    y_ranges = set()

    new_coordinate = logic._add_to_ranges(starting_coordinate, command, x_ranges, y_ranges)
    assert new_coordinate == (12, 25)
    assert x_ranges == {(20, 10, 12)}
    assert y_ranges == {(12, 20, 25)}


def test_add_to_ranges_west():
    """
    Tests that `_add_to_ranges` correctly adds a new entry to the `x_ranges` set in the
    'west' direction.
    """
    starting_coordinate = (12, 25)
    command = {"direction": "west", "steps": 9999}
    x_ranges = {(20, 10, 12)}
    y_ranges = {(12, 20, 25)}

    new_coordinate = logic._add_to_ranges(starting_coordinate, command, x_ranges, y_ranges)
    assert new_coordinate == (-9987, 25)
    assert x_ranges == {(20, 10, 12), (25, -9987, 12)}
    assert y_ranges == {(12, 20, 25)}


def test_add_to_ranges_south():
    """
    Tests that `_add_to_ranges` correctly adds a new entry to the `y_ranges` set in the
    'south' direction.
    """
    starting_coordinate = (-9987, 25)
    command = {"direction": "south", "steps": 3456}
    x_ranges = {(20, 10, 12), (25, -9987, 12)}
    y_ranges = {(12, 20, 25)}

    new_coordinate = logic._add_to_ranges(starting_coordinate, command, x_ranges, y_ranges)
    assert new_coordinate == (-9987, -3431)
    assert x_ranges == {(20, 10, 12), (25, -9987, 12)}
    assert y_ranges == {(12, 20, 25), (-9987, -3431, 25)}


def test_merge_ranges_without_overlap():
    """
    Tests that `_merge_ranges` correctly leaves ranges in places that do no need to
    be merged.
    """
    ranges = {(1, 1, 100), (2, 1, 100), (3, 50, 100)}
    assert logic._merge_ranges(ranges) == ranges


def test_merge_ranges_with_overlap():
    """
    Tests that `_merge_ranges` correctly merges ranges when there is overlap.
    """
    ranges = {(1, 1, 100), (1, 1, 101), (3, 50, 100)}
    expected = {(1, 1, 101), (3, 50, 100)}
    assert logic._merge_ranges(ranges) == expected

    ranges = {(1, -21, 100), (1, 1, 101), (3, 50, 100)}
    expected = {(1, -21, 101), (3, 50, 100)}
    assert logic._merge_ranges(ranges) == expected

    ranges = {(1, -999, 999), (1, 1, 101), (3, 50, 100)}
    expected = {(1, -999, 999), (3, 50, 100)}
    assert logic._merge_ranges(ranges) == expected

    ranges = {(1, 50, 999), (1, 1, 101), (3, 50, 100)}
    expected = {(1, 1, 999), (3, 50, 100)}
    assert logic._merge_ranges(ranges) == expected


def test_calculate_unique_coordinates():
    """
    Tests that `calculate_unique_coordinates` correctly returns 4 coordinates when
    taking 2 steps east and 1 step north and using all 3 algorithms.
    """
    counting_algorithms = [
        algorithms.BinarySearch,
        algorithms.EarlyIntersectionFiltering,
        algorithms.SimpleIntersection,
    ]
    start = (1, 1)
    commands = [
        {"direction": "east", "steps": 2},
        {"direction": "north", "steps": 1},
    ]
    expected = 4

    for algorithm in counting_algorithms:
        assert logic.calculate_unique_coordinates(start, commands, algorithm)[0] == expected


def test_calculate_unique_coordinates_overlapping():
    """
    Tests that `calculate_unique_coordinates` correctly returns the number of unique
    coordinates when there is an overlap in the vertices as it makes a small circle and
    using all 3 algorithms.
    """
    counting_algorithms = [
        algorithms.BinarySearch,
        algorithms.EarlyIntersectionFiltering,
        algorithms.SimpleIntersection,
    ]
    start = (1, 1)
    commands = [
        {"direction": "east", "steps": 2},
        {"direction": "north", "steps": 1},
        {"direction": "west", "steps": 1},
        {"direction": "south", "steps": 2},
    ]
    expected = 6

    for algorithm in counting_algorithms:
        assert logic.calculate_unique_coordinates(start, commands, algorithm)[0] == expected


def test_calculate_unique_coordinates_in_circles():
    """
    Tests that `calculate_unique_coordinates` correctly returns the number of unique
    coordinates when there are a lot of overlaps in the vertices as it makes 100
    circles in this test, using all 3 algorithms.
    """
    counting_algorithms = [
        algorithms.BinarySearch,
        algorithms.EarlyIntersectionFiltering,
        algorithms.SimpleIntersection,
    ]
    start = (1, 1)
    commands = [
        {"direction": "east", "steps": 1},
        {"direction": "north", "steps": 1},
        {"direction": "west", "steps": 1},
        {"direction": "south", "steps": 1},
    ] * 100
    expected = 4

    for algorithm in counting_algorithms:
        assert logic.calculate_unique_coordinates(start, commands, algorithm)[0] == expected


def test_calculate_unique_coordinates_complicated_movement():
    """
    Tests that `calculate_unique_coordinates` correctly returns the number of unique
    coordinates when there are a lot of overlaps in the vertices as it makes 100
    circles in this test, using all 3 algorithms.
    """
    counting_algorithms = [
        algorithms.BinarySearch,
        algorithms.EarlyIntersectionFiltering,
        algorithms.SimpleIntersection,
    ]
    start = (1, 1)
    commands = [
        {"direction": "east", "steps": 5},
        {"direction": "north", "steps": 1},
        {"direction": "east", "steps": 5},
        {"direction": "south", "steps": 2},
        {"direction": "west", "steps": 8},
        {"direction": "north", "steps": 1},
        {"direction": "west", "steps": 5},
    ]
    expected = 25

    for algorithm in counting_algorithms:
        assert logic.calculate_unique_coordinates(start, commands, algorithm)[0] == expected


def test_calculate_unique_coordinates_maximum_input():
    """
    Tests that `calculate_unique_coordinates` is performant for large inputs, ensuring that
    it does not take longer than 10s to finish, using all 3 algorithms.

    NOTE: takes approximately 20s to run, since it takes 5 to 10s per algorithm
    """
    counting_algorithms = [
        algorithms.BinarySearch,
        algorithms.EarlyIntersectionFiltering,
        algorithms.SimpleIntersection,
    ]
    start = (-100000, -100000)
    commands = [
        {"direction": "east", "steps": 99999},
        {"direction": "north", "steps": 99999},
        {"direction": "west", "steps": 99998},
        {"direction": "south", "steps": 99998},
    ] * 2500
    expected = 993737501

    for algorithm in counting_algorithms:
        unique_coordinates, duration = logic.calculate_unique_coordinates(start, commands, algorithm)
        assert unique_coordinates == expected
        assert duration < 10
