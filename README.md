# Music Video Visualizer
這是一個用 Python 製作的 音樂波浪(Wave)視覺化工具，可從 .wav 檔案中提取音訊內容，並根據 RMS(Root Mean Square)音量 計算生成對應波形動畫。
同時，支持搭配播放 .mp4 、音檔，**將波浪動畫真正同步渲染在 MV 畫面中**。

使用者可以透過 `config.json` 調整最終輸出效果的樣式與行為。
支援影片背景 / 音訊同步播放 / 自訂 bar 效果，還能切換顯示參數！

## 背景
最近不知道為什麼[長號冠軍(Trombone Champ)](https://store.steampowered.com/app/1059990/Trombone_Champ/?l=tchinese)很紅，一直在yt刷到，就很好奇他的長號是怎麼發出聲音的(他的聲音是線性發聲，非固定音檔)，所以就問了ai，他跟我說其實程式也可以弄出線性發聲，而不用固定音檔。

(~~雖然這不是重點~~)

但這讓我聯想到另一個問題：
> 音樂視覺化(Waveform)到底是怎麼實作的？

> 總不可能音樂在那播，波浪在那瞎亂跳吧？

於是我就繼續連同Trombone Champ問了ai，他跟我說實際技術就是提取.wav(或其他音檔)中的資料作分析啦

於是本專案就誕生了！

# Features
- 支援 影片背景播放(.mp4) [可選]

- 音訊播放 + 自動視覺化(rms 條紋動畫) [可選]

- 可自訂背景圖(當mp4設定為關閉時啟用)

- 完全自訂的樣式（bar 顏色、位置、高度）

- 使用 config.json 快速調整參數(無需改程式碼)

# 安裝方式(Installation)
1. 安裝 Python 套件
```bash
pip install -r requirements.txt
```

2. 準備以下檔案
- `default_background.jpg`: 預設背景圖(可選，放置於`main.py`同級資料夾)
- `.wav`檔案(不需改檔名，放置於`\video_files`)
- `.mp4`檔案(不需改檔名，放置於`\video_files`)

# 使用方式(Usage)
## RMS_generator.py
### 參數
本檔案在啟動時可添加參數(可選)
```bash
python RMS_generator.py --vl_str value[float]
```

此設定可指定**音波的敏感度(強度表現)**
> 數字越大，分析對音波的「差異感知」越弱(越不敏感)

音波敏感度的計算方式採用 [Generalised Mean（一般化平均）](https://en.wikipedia.org/wiki/Generalized_mean)：
$\left(\frac{1}{n}\sum_{i=1}^{n}|x_i|^{s}\right)^{1/s}$

其中
${x_i}$ 為 音樂的樣本(sample)
${s}$ 為 輸入的力度 ``--vl_str``


限制：`value >= 0`

### 前置準備
使用 `main.py` 前，請先完成以下步驟：

1. 將 `.wav`、`.mp4` 檔案放入 `video_files` 資料夾中

2. 至少運行一次 `RMS_generator.py`，用於生成音訊分析資料
```bash
python RMS_generator.py
```
此檔案會：
- 讀取並分析`.wav`檔案
- 抓`.wav`, `.mp4`檔案的路徑(Path)
- 計算影片長度
> [!note]
> 擷取、分析時間依歌曲長度有所不同，通常需要10~30秒不等。

> [!Important]
> 若有更換音檔或重新命名等操作，請**重新執行本檔案**。
> 不建議手動修改 `sound_file.json`，可能導致資料不同步。

### 影音相關檔案
1. 請備妥`.wav`、`.mp4`檔案，將檔案放入 `video_files` 資料夾中，不須改名
2. 更換背景請放在和`main.py`的同級資料夾中，**並將圖片命名為`default_background.jpg`**

<h2>main.py</h2>

完成前置準備後，可直接執行本檔案
```bash
python main.py
```
輸出：
- PyGame視窗
- 終端機log

關於設定檔`config.json`請參閱下方說明。

## 設定檔
本專案設定檔位於和main.py同級的`config.json`
### 📁 顯示與播放設定
| 設定 | 限制 | 說明 |
| --- | --- | --- | 
| enable_video | 必須是boolean型態 | 是否播放.mp4檔，若關閉將使用`default_background.jpg`作為背景 |
| enable_audio | 必須是boolean型態 | 是否播放.wav檔 |
| enable_bar | 必須是boolean型態 | 是否渲染音浪 |
| volume | 0.0 ≤ value[float] ≤ 1.0 | 設定音量，1.0為最大聲，0.0為靜音 |
| smoothing | 0.0 ≤ value[float] ≤ 1.0 | 波型的緩衝幅度，數字越大整體看起來越"抖" |
| amplify | value[float] ≥ 0.0 | 對波型的敏感度補正。數字越大，視覺高上較陡峭；數字越低，視覺上較平緩 |

### 🎨 外觀與視窗設定
| 設定 | 限制 | 說明 |
| --- | --- | --- | 
| bar_color | list[r, g, b] | 指定波浪整體的顏色
| bar_alpha | 0 ≤ value[int] ≤ 256 | 指定波浪的透明度，0為完全透明 |
| bar_count | 必須為$300$的因數，因應FPS整除採樣率(Sample Rate) | 指定畫面上的波浪條數量 |
| window_width | value[int] ≥ 0 | 主視窗的寬度 |
| window_high | value[int] ≥ 0 | 主視窗的高度 |
| bar_width | value[int] ≥ 0 | 整體波浪的寬度 |
| bar_high | value[int] ≥ 0 | 整體波浪的高度 |
| bar_x | value[int] ≥ 0 | 波浪的位置 $x$ |
| bar_y | value[int] ≥ 0 | 波浪的位置 $y$ |

> [!Note]
> 波浪位置 $x,y$ 是以**畫面左下角為** ($0, 0$) 的**第一象限**

> [!Important]
> 此檔案沒有自動補齊/生成設定的功能，若設定項有缺失，請複製本專案`config.json`的內容

# 專案結構
```
SOUND_WAVES_VISUALIZER/
├── src/
│   ├── video_files/               # 放置影片與音訊素材（.wav / .mp4）
│   ├── config.json                # 主設定檔，調整視覺化樣式與播放行為
│   ├── default_background.jpg     # 預設背景圖（若未使用影片）
│   ├── JsonLoader.py              # 載入 config.json 與 sound_file.json 的工具模組
│   ├── main.py                    # 主執行檔，載入資料並開始視覺化動畫
│   ├── RMS_generator.py           # 音訊資料預處理腳本，分析音檔生成聲音強度資訊
│   └── sound_file.json            # 由 RMS_generator.py 生成的音訊分析資料
│
├── tests/
│   ├── video_files/               # 測試用音訊與影片素材資料夾
│   ├── config.json                # 測試用設定檔
│   ├── default_background.jpg     # 測試用背景圖
│   ├── JsonLoader.py              # 測試版本的 Json 載入工具
│   ├── main.py                    # 測試執行主程式
│   ├── RMS_generator.py           # 測試音訊分析模組
│   └── sound_file.json            # 測試產出的音訊資料
│
├── .gitignore                     # Git 忽略規則
├── README.md                      # 專案說明文件（你現在正在寫的）
├── requirements.txt               # Python 相依套件列表

```
程式運行以 src/ 為主，tests/ 可用於隔離測試或備份。

# Requirements
```
pygame
numpy
opencv-python
librosa
```

# Demo