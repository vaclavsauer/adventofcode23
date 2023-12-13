import os

print("*" * 80)
print("Advent of Code 2022 - Day 3: Gear Ratios")
print("*" * 80)
"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

input_file_number = os.path.basename(__file__).split(".")[0]
file = open(f"input_{input_file_number}.txt", "r")
lines = file.readlines()
for i, line in enumerate(lines):
    lines[i] = lines[i].strip()

NUMBERS = "0123456789"
NOT_SYMBOLS = "0123456789."


def get_part_numbers(schematic):
    schematic_length = len(schematic)
    line_length = len(schematic[0])
    part_numbers_sum = 0

    for i, line in enumerate(schematic):
        line = line
        numbers = []
        number = ""
        is_part_number = False
        for j, char in enumerate(line):
            if char in NUMBERS:
                number += char

                checked_digits = line[max(j - 1, 0) : min(j + 2, line_length)]
                if i > 0:
                    checked_digits += schematic[i - 1][
                        max(j - 1, 0) : min(j + 2, line_length)
                    ]
                if i < schematic_length - 1:
                    checked_digits += schematic[i + 1][
                        max(j - 1, 0) : min(j + 2, line_length)
                    ]

                is_part_number = is_part_number or any(
                    [symbol for symbol in checked_digits if symbol not in NOT_SYMBOLS]
                )

            # End of number
            elif number:
                numbers.append("p" + number if is_part_number else number)
                if is_part_number:
                    part_numbers_sum += int(number)
                    # print(f"+{number}  = {part_numbers_sum}")
                number = ""
                is_part_number = False

        # End of line
        if number:
            numbers.append("p" + number if is_part_number else number)
            if is_part_number:
                part_numbers_sum += int(number)
                # print(f"+{number}  = {part_numbers_sum}")
        # print(f"{i + 1}:", " ".join(numbers))

    return part_numbers_sum


print(
    f"Sum of all of the part numbers in the engine schematic is {get_part_numbers(lines)}."
)

"""
--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""


def get_number(x, y, schematic):
    if any([x < 0, y < 0, y > len(schematic), x > len(schematic[0])]):
        return

    if schematic[y][x] not in NUMBERS:
        return

    index = 1
    number = schematic[y][x]
    while x - index >= 0 and schematic[y][x - index] in NUMBERS:
        number = schematic[y][x - index] + number
        index += 1

    index = 1
    length = len(schematic[y])
    while x + index < length and schematic[y][x + index] in NUMBERS:
        number = number + schematic[y][x + index]
        index += 1

    return number


def calculate_gears(schematic):
    total_ratio = 0
    for y, line in enumerate(schematic):
        # print(y + 1, ":")
        for x, char in enumerate(line):
            if char != "*":
                continue
            numbers = {
                get_number(x - 1, y - 1, schematic),
                get_number(x - 1, y, schematic),
                get_number(x - 1, y + 1, schematic),
                get_number(x, y - 1, schematic),
                get_number(x, y + 1, schematic),
                get_number(x + 1, y - 1, schematic),
                get_number(x + 1, y, schematic),
                get_number(x + 1, y + 1, schematic),
            }
            numbers = [number for number in numbers if number is not None]
            if len(numbers) < 2:
                continue

            gear_ratio = int(numbers[0])
            for next_gear in numbers[1:]:
                gear_ratio = gear_ratio * int(next_gear)

            total_ratio += gear_ratio

            # print(f"{" * ".join(numbers)}\t= {gear_ratio}\t-> {total_ratio}")

    return total_ratio


print(f"Sum of all of the gear ratios in engine schematic is {calculate_gears(lines)}.")

print("*" * 80)
