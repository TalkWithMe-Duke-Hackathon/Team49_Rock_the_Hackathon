'''
Author: Jeff_L
Date: 2023-10-26 14:50:29
LastEditors: Jeff_L && yanxinluo28@gmail.com
LastEditTime: 2023-11-04 01:15:04
FilePath: \Test_code\test.py
Description: 

Copyright (c) 2023 by ${yanxinluo28@gmail.com}, All Rights Reserved. 
'''
import requests
from bs4 import BeautifulSoup

# The URL of the target website
url = 'https://m.hujiang.com/en/p92485/'

# Send HTTP request and get web page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the HTML element of the original listening text (use the appropriate selector)
listening_elements = soup.select('.article-content')

# Save the original listening text to a text file
for index, listening_element in enumerate(listening_elements):
    # create file name
    file_name = f'listening_text_{index + 2}.txt'
    
    # Get the original listening content
    listening_text = listening_element.text.strip()
    
    # Save to text file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(listening_text)
    
    print(f'The original listening text has been saved to the file:{file_name}')
