import unittest
import os
import tempfile
from timestamp_splitter import split_timestamps


class TestTimestampSplitter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, "input.txt")

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_split_timestamps(self):
        timestamps = "14:19,15:57,18:24,20:07,20:51,21:20,22:31,23:43,24:27,25:08,30:51,31:45,32:28,33:35,34:48,35:39,36:21,37:24,38:36,39:07,39:48,40:45,41:43,42:32,43:12,43:54,44:58,45:29,46:37,47:40,53:49,57:02,1:00:27,1:02:01,1:03:31,1:04:38,1:09:34,1:10:39,1:11:48,1:12:54,1:13:52,1:14:54,1:15:56,1:17:22,1:18:33,1:19:42,1:20:32,1:21:08,1:22:11,1:23:39,1:24:42,1:27:42,1:29:49,1:31:31,1:32:12,1:33:27,1:34:23,1:35:44,1:36:24,1:37:49,1:38:36,1:39:55,1:42:34,1:43:47,1:46:25,1:47:30,1:48:14,1:49:07,1:50:27,1:55:21,1:56:32,1:57:32,1:58:17,1:59:07,2:00:36,2:01:21,2:02:38,2:03:19,2:04:17,2:05:48,2:06:59,2:07:54,2:08:53,2:09:56,2:10:37,2:11:40,2:12:29"

        with open(self.input_file, "w") as f:
            f.write(timestamps)

        output_paths = split_timestamps(self.input_file, max_length=100)

        self.assertEqual(len(output_paths), 4)  # Expecting 4 output files

        for path in output_paths:
            self.assertTrue(os.path.exists(path))
            with open(path, "r") as f:
                content = f.read()
                self.assertLessEqual(len(content), 100)


if __name__ == "__main__":
    unittest.main()
