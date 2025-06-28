import pygame
import cv2
import numpy as np
import time

from JsonLoader import ConfigLoader, SoundFileLoader

config = ConfigLoader()
sound_file = SoundFileLoader()

class AVPlayer:
    def __init__(self, config: ConfigLoader, sound_file: SoundFileLoader):
        self.config = config
        self.sound_file = sound_file

        pygame.init()
        pygame.display.set_caption(self.sound_file.video_title)
        self.screen = pygame.display.set_mode((config.window_width, config.window_high))
        self.clock = pygame.time.Clock()

        self.cap = cv2.VideoCapture(self.sound_file.mp4) if config.enable_video else None
        self.video_fps = self.cap.get(cv2.CAP_PROP_FPS) if self.cap else 30
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) if self.cap else 0
        if self.total_frames == 0:
            self.Error()
            return

        self.current_heights = [0] * config.bar_count

        self.default_bg = pygame.image.load("default_background.jpg").convert()
        self.default_bg = pygame.transform.scale(self.default_bg, (config.window_width, config.window_high))

        self.audio()

    def Error(self):
        raise FileNotFoundError(f"{self.sound_file.mp4} 路徑錯誤")

    def audio(self):
        if self.config.enable_audio:
            pygame.mixer.quit()
            pygame.mixer.init()
            pygame.mixer.music.load(self.sound_file.wav_file)
            pygame.mixer.music.set_volume(self.config.volume)
            pygame.mixer.music.play()

    def video(self, frame_index: int):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame_img = self.cap.read()
            if not ret:
                print("(log) 無法讀取影片，將使用預設背景")
                return self.default_bg

            frame_img = cv2.resize(frame_img, (self.config.window_width, self.config.window_high))
            frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)
            return pygame.surfarray.make_surface(np.transpose(frame_img, (1, 0, 2)))
        return self.default_bg

    def bar(self, rms_index: int):
        if not self.config.enable_bar or rms_index >= len(self.sound_file.rms):
            return None

        bar_surface = pygame.Surface((self.config.window_width, self.config.window_high), pygame.SRCALPHA)
        bar_surface.set_alpha(self.config.bar_alpha)
        bar_width = self.config.bar_width / self.config.bar_count

        for i, val in enumerate(self.sound_file.rms[rms_index]):
            target = int((val ** self.config.amplify) * self.config.bar_high)
            self.current_heights[i] += (target - self.current_heights[i]) * self.config.smoothing
            height = int(self.current_heights[i])
            x = i * bar_width
            pygame.draw.rect(
                bar_surface,
                self.config.bar_color,
                (
                    x + self.config.bar_x,
                    self.config.window_high - self.config.bar_y - height,
                    max(bar_width - 2, 1),
                    height
                )
            )
        return bar_surface

    def run(self):
        try:
            running = True
            start_time = time.time()

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                elapsed_time = time.time() - start_time

                current_frame = int(elapsed_time * self.video_fps)

                if self.cap and current_frame >= self.total_frames:
                    print("(log) 影片播放完畢")
                    break

                surface = self.video(current_frame)
                self.screen.blit(surface, (0, 0))

                if self.config.enable_bar:
                    rms_index = int(elapsed_time * self.sound_file.fps)
                    bar_surface = self.bar(rms_index)
                    if bar_surface:
                        self.screen.blit(bar_surface, (0, 0))

                pygame.display.flip()
                self.clock.tick(60)

        except KeyboardInterrupt:
            print("(log) 影片意外被關閉。")

        finally:
            if self.cap:
                self.cap.release()
            pygame.quit()

AVPlayer(config, sound_file).run()