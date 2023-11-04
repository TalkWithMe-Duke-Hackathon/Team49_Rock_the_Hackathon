'''
Author: Jeff_L
Date: 2023-11-03 23:13:01
LastEditors: Jeff_L && yanxinluo28@gmail.com
LastEditTime: 2023-11-04 00:31:05
FilePath: \project\gTTS.py
Description: 

Copyright (c) 2023 by ${yanxinluo28@gmail.com}, All Rights Reserved. 
'''
from gtts import gTTS
import os

# the text
text_to_convert = "Typical of the grassland dwellers of the continent is the American antelope, or pronghorn."

# text to speech
tts = gTTS(text=text_to_convert, lang='zh')  # 'en'means English, 'zh' means Chinese
tts.save('output.mp3')  # save for .mp3 file

# 播放生成的语音（可选）
os.system("mpg321 output.mp3")  # Please make sure your system supports the mpg321 command for playing mp3 files
