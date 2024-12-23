from app import logic


def test_add_existing_to_unique_coordinates():
    """
    Tests that adding the same coordinate twice does not a new coordinate
    when using the `_add_to_unique_coordinates` function.
    """
    existing_coordinate = (1, 1)
    unique_coordinates = {existing_coordinate}
    logic._add_to_unique_coordinates(unique_coordinates, [existing_coordinate])
    assert unique_coordinates == {existing_coordinate}


def test_add_new_to_unique_coordinates():
    """
    Tests that adding new coordinates adds these coordinate to the
    unique coordinates when using the `_add_to_unique_coordinates` function.
    """
    existing_coordinate = (1, 1)
    new_coordinates = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
    unique_coordinates = {existing_coordinate}
    logic._add_to_unique_coordinates(unique_coordinates, new_coordinates)
    assert len(unique_coordinates) == 6
    assert existing_coordinate in unique_coordinates
    for coordinate in new_coordinates:
        assert coordinate in unique_coordinates


def test_add_mix_to_unique_coordinates():
    """
    Tests that adding a mix of existing and new coordinates to the
    unique coordinates when using the `_add_to_unique_coordinates` function will
    only add the new coordinates.
    """
    existing_coordinate = (1, 1)
    new_coordinates = [(1, 2), (1, 1), (1, 4), (1, 1), (1, 6)]
    unique_coordinates = {existing_coordinate}
    logic._add_to_unique_coordinates(unique_coordinates, new_coordinates)
    assert len(unique_coordinates) == 4
    assert existing_coordinate in unique_coordinates
    assert new_coordinates[0] in unique_coordinates
    assert new_coordinates[2] in unique_coordinates
    assert new_coordinates[4] in unique_coordinates


def test_get_vertices_north():
    """
    Tests that `_get_vertices` correctly creates a list of new coordinates when
    the direction is "north" and the number of steps is 2.
    """
    start = (1, 1)
    command = {"direction": "north", "steps": 2}
    expected = [(1, 2), (1, 3)]
    assert logic._get_vertices(start, command) == expected


def test_get_vertices_east():
    """
    Tests that `_get_vertices` correctly creates a list of new coordinates when
    the direction is "east" and the number of steps is 3.
    """
    start = (1, 1)
    command = {"direction": "east", "steps": 3}
    expected = [(2, 1), (3, 1), (4, 1)]
    assert logic._get_vertices(start, command) == expected


def test_get_vertices_south():
    """
    Tests that `_get_vertices` correctly creates a list of new coordinates when
    the direction is "south" and the number of steps is 4.
    """
    start = (1, 1)
    command = {"direction": "south", "steps": 4}
    expected = [(1, 0), (1, -1), (1, -2), (1, -3)]
    assert logic._get_vertices(start, command) == expected


def test_get_vertices_west():
    """
    Tests that `_get_vertices` correctly creates a list of new coordinates when
    the direction is "west" and the number of steps is 5.
    """
    start = (1, 1)
    command = {"direction": "west", "steps": 5}
    expected = [(0, 1), (-1, 1), (-2, 1), (-3, 1), (-4, 1)]
    assert logic._get_vertices(start, command) == expected


def test_calculate_unique_coordinates():
    """
    Tests that `calculate_unique_coordinates` correctly returns 4 coordinates when
    taking 2 steps east and 1 step north.
    """
    start = (1, 1)
    commands = [
        {"direction": "east", "steps": 2},
        {"direction": "north", "steps": 1},
    ]
    expected = 4
    assert logic.calculate_unique_coordinates(start, commands)[0] == expected


def test_calculate_unique_coordinates_overlapping():
    """
    Tests that `calculate_unique_coordinates` correctly returns the number of unique
    coordinates when there is an overlap in the vertices as it makes a small circle.
    """
    start = (1, 1)
    commands = [
        {"direction": "east", "steps": 2},
        {"direction": "north", "steps": 1},
        {"direction": "west", "steps": 1},
        {"direction": "south", "steps": 2},
    ]
    expected = 6
    assert logic.calculate_unique_coordinates(start, commands)[0] == expected


def test_calculate_unique_coordinates_in_circles():
    """
    Tests that `calculate_unique_coordinates` correctly returns the number of unique
    coordinates when there are a lot of overlaps in the vertices as it makes 100
    circles in this test.
    """
    start = (1, 1)
    commands = [
        {"direction": "east", "steps": 1},
        {"direction": "north", "steps": 1},
        {"direction": "west", "steps": 1},
        {"direction": "south", "steps": 1},
    ] * 100
    expected = 4
    assert logic.calculate_unique_coordinates(start, commands)[0] == expected
