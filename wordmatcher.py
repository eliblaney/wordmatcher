from pathlib import Path
import random
import nltk
from nltk.corpus import words
from PIL import Image, ImageDraw, ImageFont

# Generated images will be put in this folder. Include trailing "/".
OUTPUT_DIR = "images/"

def wordmatcher(adjs, nouns):
    adj = random.choice(adjs)
    lasthalf = adj[int(len(adj)/2):]
    compatible = [noun for noun in nouns if noun[:len(lasthalf)] == lasthalf]
    if(len(compatible) == 0):
        return False
    return (adj, random.choice(compatible))

print("Setting up...")
word_list = words.words()
parsed = nltk.pos_tag(word_list)
allowed_adj = ['JJ', 'JJR', 'JJS', 'CD', 'RB', 'RBR', 'RBS']
allowed_nouns = ['NN', 'NNP', 'NNS']
adjs = [word[0] for word in parsed if word[1] in allowed_adj]
nouns = [word[0] for word in parsed if word[1] in allowed_nouns]

font = ImageFont.truetype('./UbuntuMono-R.ttf', 48)
font_bold = ImageFont.truetype('./UbuntuMono-B.ttf', 48)
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

print("Starting matcher... Press Ctrl + C at any time to quit")
index = 0
while True:
    result = wordmatcher(adjs, nouns)
    if result:
        first = result[0]
        last = result[1]
        split = int(len(first)/2)
        len_shared = len(first) - split

        img = Image.new('RGB', (512, 256), color = 'white')
        d = ImageDraw.Draw(img)
        d.text((50, 50), first[:split], font=font_bold, fill=(0, 0, 0))
        d.text((50 + 24*split, 50), first[split:], font=font, fill=(0, 0, 0))
        d.text((50, 100), last[:len_shared], font=font_bold, fill=(0, 0, 0))
        d.text((50 + 24*len_shared, 100), last[len_shared:], font=font, fill=(0, 0, 0))
        img.save(OUTPUT_DIR + 'image' + str(index) + '.png')
        index += 1
