import re


class TimestampCompressor:
    @staticmethod
    def compress(timestamp_string):
        # 将时间戳拆分为小时和分钟
        timestamps = timestamp_string.split(",")
        compressed = []
        prev_hour = 0

        for ts in timestamps:
            hour, minute = map(int, ts.split(":"))

            # 计算小时差
            hour_diff = hour - prev_hour
            if hour_diff < 0:
                hour_diff += 24  # 处理跨天的情况

            # 使用一个字符来表示小时差和分钟
            compressed.append(chr(hour_diff * 60 + minute))
            prev_hour = hour

        return "".join(compressed)

    @staticmethod
    def decompress(compressed_string):
        decompressed = []
        current_hour = 0

        for char in compressed_string:
            value = ord(char)
            hour_diff = value // 60
            minute = value % 60

            current_hour = (current_hour + hour_diff) % 24
            decompressed.append(f"{current_hour:02d}:{minute:02d}")

        return ",".join(decompressed)


def compress_filename(filename):
    # 提取时间戳部分
    match = re.match(r"(.+)_part(\d+)\.txt", filename)
    if not match:
        return filename

    base_name, part_num = match.groups()
    timestamps = base_name.split("_")

    # 压缩时间戳
    compressor = TimestampCompressor()
    compressed_timestamps = compressor.compress("_".join(timestamps))

    # 使用压缩后的时间戳和部分编号创建新的文件名
    return f"{compressed_timestamps}_p{part_num}.txt"


def decompress_filename(compressed_filename):
    # 提取压缩的时间戳部分和部分编号
    match = re.match(r"(.+)_p(\d+)\.txt", compressed_filename)
    if not match:
        return compressed_filename

    compressed_timestamps, part_num = match.groups()

    # 解压时间戳
    compressor = TimestampCompressor()
    decompressed_timestamps = compressor.decompress(compressed_timestamps)

    # 使用解压后的时间戳和部分编号创建原始文件名
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
