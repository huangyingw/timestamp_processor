import os


def split_timestamps(input_path, max_length=100):
    with open(input_path, "r") as file:
        content = file.read().strip()

    timestamps = content.split(",")
    parts = []
    current_part = []
    current_length = 0

    for timestamp in timestamps:
        if current_length + len(timestamp) + 1 > max_length and current_part:
            parts.append(",".join(current_part))
            current_part = []
            current_length = 0
        current_part.append(timestamp)
        current_length += len(timestamp) + 1

    if current_part:
        parts.append(",".join(current_part))

    directory, filename = os.path.split(input_path)
    base_name, _ = os.path.splitext(filename)

    output_paths = []
    for i, part in enumerate(parts):
        output_filename = f"{base_name}_part{i+1}.txt"
        output_path = os.path.join(directory, output_filename)
        with open(output_path, "w") as file:
            file.write(part)
        output_paths.append(output_path)

    return output_paths


if __name__ == "__main__":
    input_path = input("Enter the relative path of the input file: ")
    output_paths = split_timestamps(input_path)
    print("Output files created:")
    for path in output_paths:
        print(path)
