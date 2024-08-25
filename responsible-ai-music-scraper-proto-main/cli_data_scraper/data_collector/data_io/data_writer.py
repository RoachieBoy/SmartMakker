import csv
import json

from data_collector.text_computing.text_container import TextContainer


def save_to_csv(data: TextContainer, filepath: str) -> None:
    """
    Save the data in the TextContainer object to a CSV file at the given filepath.

    :param data: a TextContainer object containing data to be saved
    :param filepath: a string containing the path to the output CSV file
    """

    data = remove_null_value_per_column(data)

    with open(filepath, mode="w", newline="") as csv_file:
        fieldnames = list(data.text_table.keys())
        writer = csv.DictWriter(csv_file, fieldnames)

        # Write the header row to the CSV file
        writer.writeheader()

        # Calculate maximum number of rows based on the length of the longest list in the text_table variable
        # This is done to prevent data cutoff
        maximum_num_rows = max(len(value) for value in data.text_table.values())
        complete_rows = []

        # Iterate over each row and column in the TextContainer object,
        # adding empty strings as necessary to fill out the rows
        for row_index in range(maximum_num_rows):
            row_data = {}
            for key, value in data.text_table.items():
                if row_index < len(value):
                    row_data[key] = value[row_index]
                else:
                    row_data[key] = ""

            complete_rows.append(row_data)

        # Write the complete rows to the CSV file
        writer.writerows(complete_rows)


def save_to_txt(data: TextContainer, filepath: str) -> None:
    """
    Save the data in the TextContainer object to a tab-delimited text file at the given filepath.

    @:param data: a TextContainer object containing data to be saved
    @:param filepath: a string containing the path to the output text file
    """

    data = remove_null_value_per_column(data)

    with open(filepath, "w") as txt_file:
        # Write the header row to the text file
        header = "\t".join(data.text_table.keys()) + "\n"
        txt_file.write(header)

        # Write the data to the text file, with empty strings used to fill out
        # rows that are shorter than the longest row
        max_rows = max(len(value) for value in data.text_table.values())

        for row_index in range(max_rows):
            row_values = []
            for value in data.text_table.values():
                row_values.append(value[row_index] if row_index < len(value) else "")

            row_str = "\t".join(row_values) + "\n"

            txt_file.write(row_str)


def save_to_json(data: TextContainer, filepath: str) -> None:
    """
    Save the contents of a TextContainer object to a JSON file.

    @:param data: The TextContainer object to be saved.
    @:param filepath: The path to the output JSON file.
    """

    data = remove_null_value_per_column(data)

    with open(filepath, "w") as json_file:
        json.dump(data.text_table, json_file, default=str, indent=4)


def remove_null_value_per_column(input_container: TextContainer) -> TextContainer:
    """
    Remove null and empty values from the TextContainer object.

    @:param input_container: The TextContainer object to be processed.
    @:return: A new TextContainer object with null values removed.
    """

    keys = input_container.text_table.keys()

    for key in keys:
        input_container.text_table[key] = [x for x in input_container.text_table[key] if x != ""]

    return input_container
