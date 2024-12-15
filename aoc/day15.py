DIR_MAP = {">": (0, 1), "v": (1, 0), "^": (-1, 0), "<": (0, -1)}


def parse(lines, scale=1):
    walls = set()
    boxes = set()
    robot = None
    for r, line in enumerate(lines):
        if not line:
            break
        for c, char in enumerate(line):
            if char == "#":
                walls.update((r, scale * c + dc) for dc in range(scale))
            if char == "O":
                # regardless of scale, represent boxes by their leftmost coordinate
                boxes.add((r, scale * c))
            if char == "@":
                robot = r, scale * c

    assert robot

    moves = [DIR_MAP[char] for line in lines for char in line if line.startswith(tuple(DIR_MAP))]

    return walls, boxes, robot, moves


def run(lines, push_boxes, scale=1):
    walls, boxes, (r, c), moves = parse(lines, scale)

    for dr, dc in moves:
        # find which boxes we'll be pushing on this move, if possible
        pushed_boxes = push_boxes(r, c, dr, dc, walls, boxes)

        # `None` means we've hit a wall and can't move
        if pushed_boxes is None:
            continue

        # move the boxes in two passes so we don't discard just-added boxes
        for box_r, box_c in pushed_boxes:
            boxes.discard((box_r, box_c))
        for box_r, box_c in pushed_boxes:
            boxes.add((box_r + dr, box_c + dc))

        r += dr
        c += dc

    return sum(100 * r + c for r, c in boxes)


def part1(lines):
    def push_boxes(r, c, dr, dc, walls, boxes):
        pushed_boxes = set()

        # look at space directly ahead
        r += dr
        c += dc

        while (r, c) not in walls:
            if (r, c) not in boxes:
                # found empty space, success!
                return pushed_boxes
            
            pushed_boxes.add((r, c))

            # consider the next further space
            r += dr
            c += dc


    return run(lines, push_boxes)


def part2(lines):
    def push_boxes(r, c, dr, dc, walls, boxes):
        pushed_boxes = set()

        # `front` is the set of "furthest" spaces which will be entered by the robot or a box on an
        # iteration, initially just due to the robot
        front = {(r + dr, c + dc)}

        while not front & walls:
            if not front & boxes and not {(r, c - 1) for r, c in front} & boxes:
                # found empty spaces, success!
                return pushed_boxes

            new_front = set()

            for r, c in front:
                # check if a new box is at this point in the front
                new_box = {(r, c), (r, c - 1)} & boxes

                # if not, this point in the front is no longer relevant
                if not new_box:
                    continue

                new_r, new_c = new_box.pop()
                pushed_boxes.add((new_r, new_c))

                # if moving vertically, add both box positions to the new front; if moving
                # horizontally, add only the further box position (positions adjusted for the next
                # iteration in any case)
                if dr or dc == -1:
                    new_front.add((new_r + dr, new_c + dc))
                if dr or dc == 1:
                    new_front.add((new_r + dr, new_c + 1 + dc))

            front = new_front

    return run(lines, push_boxes, 2)
