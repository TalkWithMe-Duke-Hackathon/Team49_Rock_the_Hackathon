'''
Author: Jeff_L
Date: 2023-11-04 01:11:04
LastEditors: Jeff_L && yanxinluo28@gmail.com
LastEditTime: 2023-11-04 01:17:43
FilePath: \Test_code\changeThefiletOut.py
Description: 

Copyright (c) 2023 by ${yanxinluo28@gmail.com}, All Rights Reserved. 
'''
import re

# Read text files containing Chinese and English sentences
with open('listening_text_2.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Use regular expressions to split sentences and add carriage returns
sentences = re.split(r'[。！？]', content)
formatted_sentences = [sentence.strip() + '。\n\t' for sentence in sentences if sentence.strip()]

# Write the processed content to a new text file
formatted_content = ''.join(formatted_sentences)
with open('formatted_sentences.txt', 'w', encoding='utf-8') as file:
    file.write(formatted_content)
