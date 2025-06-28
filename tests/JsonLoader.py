import json
import numpy as np
import os

class ConfigLoader:
    def __init__(self):
        self._config = load_json("config")

        self.enable_video = self._load("enable_video", True, lambda x: isinstance(x, bool))
        self.enable_audio = self._load("enable_audio", True, lambda x: isinstance(x, bool))
        self.enable_bar = self._load("enable_bar", True, lambda x: isinstance(x, bool))
        self.volume = self._load("volume", 0.5, lambda x: 0.0 <= x <= 1.0)
        self.smoothing = self._load("smoothing", 0.3, lambda x: isinstance(x, (int, float)) and x > 0)
        self.amplify = self._load("amplify", 1.5, lambda x: isinstance(x, (int, float)) and x >= 0.1)
        self.bar_color = tuple(self._load("bar_color", [255, 255, 255], lambda x: isinstance(x, list) and len(x) == 3))
        self.bar_alpha = self._load("bar_alpha", 200, lambda x: 0 <= x <= 256)
        self.bar_count = self._load("bar_count", 60, lambda x: x in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 25, 30, 50, 60, 75, 100, 150, 300]) #300的因數
        self.window_width = self._load("window_width", 800, lambda x: x > 0)
        self.window_high = self._load("window_high", 400, lambda x: x > 0)
        self.bar_width = self._load("bar_width", 400, lambda x: x > 0)
        self.bar_high = self._load("bar_high", 400, lambda x: x > 0)
        self.bar_x = self._load("bar_x", 0 , lambda x: x >= 0)
        self.bar_y = self._load("bar_y", 0 , lambda x: x >= 0)


    def _load(self, key, default, rule):
        val = self._config.get(key, default)
        valid = rule(val) if callable(rule) else isinstance(val, rule)
        if not valid:
            print(f"(!!!) {key} 設定不合法，使用預設值: {default}")
            return default
        return val


class SoundFileLoader:
    def __init__(self):
        self._file = load_json("sound_file")

        self.video_title = self._file["video_name"]
        self.fps = self._file["fps"]
        self.sr = self._file["sr"]
        self.time = self._file["time"]
        self.wav_file = self._file["wav_file"]
        self.mp4 = self._file["mp4"]
        self.rms = np.array(self._file["rms"], dtype = np.float32)


def load_json(file_name: str) -> dict:
    """
    load json
    如果path(檔名)不對會raise FileNotFoundError

    請確認config.json、sound.json在與此檔案同級的位置。
    """
    json_path = f"{file_name}.json" if not file_name.endswith(".json") else file_name
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"找不到{json_path}")

    with open(json_path, "r", encoding = "utf-8-sig") as file:
        data = json.load(file)

    return data