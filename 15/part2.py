from typing import Optional

STOPPING_OPERATIONS = {"=", "-"}


def get_answer() -> int:
    initialization_sequence = get_data()
    boxes = get_box_contents(initialization_sequence)
    sum_components = [
        (box_nr + 1) * (slot_nr + 1) * focal_length
        for box_nr, box in enumerate(boxes)
        for slot_nr, (_, focal_length) in enumerate(box)
    ]
    return sum(sum_components)


def get_data() -> list[str]:
    with open("15/input.txt", "r") as f:
        line = f.read()

    return line.split(",")


def get_box_contents(initialization_sequence: list[str]) -> list[list[str]]:
    boxes = [{} for _ in range(256)]

    for i, command in enumerate(initialization_sequence):
        box_nr, label, focal_length = get_box_nr_operation_and_focal_length(command)

        box = boxes[box_nr]
        if focal_length is None:  # remove
            if label in box:
                del box[label]
        else:
            if label in box:
                box[label] = (box[label][0], focal_length)
            else:
                box[label] = (i, focal_length)

    boxes = convert_box_contents_to_list(boxes)

    return boxes


def get_box_nr_operation_and_focal_length(
    command: str,
) -> tuple[int, Optional[str], Optional[int]]:
    box_nr = 0

    for i, c in enumerate(command):
        if c in STOPPING_OPERATIONS:
            label = command[:i]

            if c == "=":
                focal_length = int(command[i + 1 :])
            else:
                focal_length = None

            return box_nr, label, focal_length

        box_nr += ord(c)
        box_nr *= 17
        box_nr %= 256

    raise ValueError


def convert_box_contents_to_list(box_contents: list[dict[str, tuple[int, int]]]) -> list[list[str, int]]:
    return [sorted_box_contents(box_content) for box_content in box_contents]


def sorted_box_contents(box_content: dict[str, tuple[int, int]]) -> list[tuple[str, int]]:
    list_box_content = [(label, time_step, focal_length) for label, (time_step, focal_length) in box_content.items()]
    list_box_content.sort(key=lambda x: x[1])
    list_box_content = [(label, focal_length) for label, _, focal_length in list_box_content]
    return list_box_content


print(get_answer())
