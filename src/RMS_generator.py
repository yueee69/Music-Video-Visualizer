import librosa
import numpy as np
import os
import json
import argparse

from JsonLoader import ConfigLoader

parser = argparse.ArgumentParser()
parser.add_argument("--vl_str", type = float, default = 2, help = "設定擷取音效的強度")
level = parser.parse_args().vl_str

if level < 0:
    raise TypeError("音效強度不可小於0")

print(f"音效強度設定為 {level}")

class FindVideoPath:
    @staticmethod
    def find_file() -> list[str, str]:
        """
        找到資料夾裡的mp4和wav檔案，在多檔案情況下只會返回第一個找到的，請確認檔案是唯一的，不須改檔名

        如果缺少任一就會raise FileNotFoundError

        return:
        [.wav_path, .mp4_path]
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, "video_files")

        wav_file = None
        mp4_file = None

        for item in os.listdir(folder_path):
            if item.lower().endswith(".wav") and wav_file is None:
                wav_file = os.path.join(folder_path, item)

            elif item.lower().endswith(".mp4") and mp4_file is None:
                mp4_file = os.path.join(folder_path, item)

            if wav_file and mp4_file:
                break

        if not wav_file or not mp4_file:
            raise FileNotFoundError("找不到 .wav 或 .mp4 檔案，請確認 video_files 資料夾內含一個 .wav 和 .mp4")

        return [wav_file, mp4_file]
    
    @staticmethod
    def get_mp4_name():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, "video_files")
        for item in os.listdir(folder_path):
            if item.lower().endswith(".mp4"):
                return item[:-4]

def caculate_RMS(bars: np.ndarray, level: int | float = 2.0) -> list[float]:
    """
     Parameters:
        bars  : ndarray，每個元素是某一條 bar 的資料（通常是小區段的波形資料）
        level : 幾階 RMS，預設是 2

    Returns:
        一個 list，對每個 bar 計算的 RMS 值
    """
    if level <= 0:
        raise ValueError("level 必須是正整數")
    
    return (np.mean(np.abs(bars) ** level, axis=1) ** (1 / level)).tolist()


def main():
    FPS = 147
    config = ConfigLoader()

    sounds_path, video_path = FindVideoPath.find_file()
    video_name = FindVideoPath.get_mp4_name()
    
    print("正在執行中...")

    RMS_sample: list[list[float]] = []
    y, sr = librosa.load(sounds_path, sr = None) #sr = 44100
    sample_per_fps = int(sr / FPS)

    for i in range(0, len(y) - sample_per_fps, sample_per_fps):
        frame = y[i: i + sample_per_fps] #一幀

        bars = np.array_split(frame, config.bar_count)
        frame_RMS = caculate_RMS(bars, level)
        RMS_sample.append(frame_RMS)

    output = {
        "fps": FPS,
        "video_name": video_name,
        "sr": sr,
        "time": len(y) / sr,
        "wav_file": sounds_path,
        "mp4": video_path,
        "rms": RMS_sample,
    }

    with open("sound_file.json", 'w', encoding = "utf-8-sig") as file:
        json.dump(output, file, indent = 4, ensure_ascii = False)

    print("success!")

if __name__ == '__main__':
    main()