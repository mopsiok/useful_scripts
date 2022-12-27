#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
from pathlib import Path

BACKGROUND_FILE = 'background.png'
GUESTLIST_FILE = 'guestlist.txt'
OUTPUT_DIR_PATH = Path('output/')

FONT_FILE = r'C:/Windows/Fonts/calibrib.ttf' # r'C:\Windows\Fonts\BOOKOSBI.TTF'
FONT_SIZE = 80
TEXT_POS = (1340, 559)
TEXT_COLOR = (232,232,232)

GUESTS_PER_PAGE = 5
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 2000, 647

def getGuests():
    with open(GUESTLIST_FILE, encoding="utf8") as f:
        data = f.read()
    return data.split('\n')
    

def createTicket(text):
    f = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    img = Image.open(BACKGROUND_FILE)
    draw = ImageDraw.Draw(img)
    draw.text(TEXT_POS, text, TEXT_COLOR, font=f, anchor='rm')
    return img.convert("RGB")


def createAll(guests):
    count = int(len(guests)/GUESTS_PER_PAGE)
    if len(guests) % GUESTS_PER_PAGE: count = count + 1

    guest_counter = 0
    images = []
    for page in range(count):
        img = Image.new('RGB', (BACKGROUND_WIDTH, BACKGROUND_HEIGHT*GUESTS_PER_PAGE), 'white')
        page_counter = 0
        while (page_counter < GUESTS_PER_PAGE) and (guest_counter < len(guests)):
            text = guests[guest_counter]
            print(page,page_counter,text)
            img.paste(createTicket(text), (0, page_counter*BACKGROUND_HEIGHT, BACKGROUND_WIDTH, (page_counter+1)*BACKGROUND_HEIGHT))
            page_counter += 1
            guest_counter += 1
        images.append(img)
    return images


if __name__ == "__main__":
    guests = getGuests()
    pages = createAll(guests)

    OUTPUT_DIR_PATH.mkdir(parents=True, exist_ok=True)

    # generate separate png file for each page
    for i, page in enumerate(pages):
        page.save(OUTPUT_DIR_PATH / f'tickets_{i+1}.png', 'png')
    
    # generate single PDF - easier to use, but a bit more noisy
    pages[0].save(OUTPUT_DIR_PATH / "tickets.pdf", save_all=True, append_images=pages[1:])