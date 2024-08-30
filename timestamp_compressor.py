import re


class TimestampCompressor:
    @staticmethod
    def compress(timestamp_string):
        timestamps = timestamp_string.split(",")
        compressed = []
        prev_minutes = 0

        for ts in timestamps:
            hour, minute = map(int, ts.split(":"))
            current_minutes = hour * 60 + minute

            if prev_minutes == 0:  # 第一个时间戳
                compressed.append(chr(hour))
                compressed.append(chr(minute))
            else:
                diff = current_minutes - prev_minutes
                compressed.append(chr(diff))

            prev_minutes = current_minutes

        return "".join(compressed)

    @staticmethod
    def decompress(compressed_string):
        decompressed = []
        prev_minutes = 0

        for i, char in enumerate(compressed_string):
            if i == 0:  # 第一个时间戳的小时
                hour = ord(char)
            elif i == 1:  # 第一个时间戳的分钟
                minute = ord(char)
                decompressed.append(f"{hour:02d}:{minute:02d}")
                prev_minutes = hour * 60 + minute
            else:  # 后续时间戳
                diff = ord(char)
                current_minutes = prev_minutes + diff
                hour, minute = divmod(current_minutes, 60)
                decompressed.append(f"{hour:02d}:{minute:02d}")
                prev_minutes = current_minutes

        return ",".join(decompressed)


def compress_filename(filename):
    match = re.match(r"(.+)_part(\d+)\.txt", filename)
    if not match:
        return filename

    base_name, part_num = match.groups()
    timestamps = base_name.replace("_", ",")

    compressor = TimestampCompressor()
    compressed_timestamps = compressor.compress(timestamps)

    # 将压缩后的字符串转换为十六进制表示
    hex_compressed = "".join(f"{ord(c):02x}" for c in compressed_timestamps)
    return f"{hex_compressed}_p{part_num}.txt"


def decompress_filename(compressed_filename):
    match = re.match(r"([0-9a-f]+)_p(\d+)\.txt", compressed_filename)
    if not match:
        return compressed_filename

    hex_compressed, part_num = match.groups()

    # 将十六进制表示转换回原始的压缩字符串
    original_compressed = "".join(
        chr(int(hex_compressed[i : i + 2], 16))
        for i in range(0, len(hex_compressed), 2)
    )

    compressor = TimestampCompressor()
    decompressed_timestamps = compressor.decompress(original_compressed)

    return f"{decompressed_timestamps.replace(',', '_')}_part{part_num}.txt"


# 测试代码
if __name__ == "__main__":
    original_timestamp_string = (
        "14:19,15:57,18:24,20:07,20:51,21:20,22:31,23:43,24:27,25:08,30:51"
    )
    compressor = TimestampCompressor()

    compressed = compressor.compress(original_timestamp_string)
    decompressed = compressor.decompress(compressed)

    print(f"Original: {original_timestamp_string}")
    print(f"Compressed: {compressed}")
    print(f"Decompressed: {decompressed}")
    print(
        f"Compression successful: {original_timestamp_string == decompressed}"
    )

    original_filename = "14:19_15:57_18:24_20:07_20:51_21:20_22:31_23:43_24:27_25:08_30:51_part1.txt"
    compressed_filename = compress_filename(original_filename)
    decompressed_filename = decompress_filename(compressed_filename)

    print(f"\nOriginal filename: {original_filename}")
    print(f"Compressed filename: {compressed_filename}")
    print(f"Decompressed filename: {decompressed_filename}")
    print(
        f"Filename compression successful: {original_filename == decompressed_filename}"
    )
