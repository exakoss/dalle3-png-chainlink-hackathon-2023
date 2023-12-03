from flask import Flask, request
import requests
import os
from openai import OpenAI
from PIL import Image
from init import rgba_image_to_svg_pixels
#initializing and loading dotenv for custom path to openai api key
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

client = OpenAI(
   api_key=os.environ.get("OPENAI_API")
)

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/post-generate-svg', methods=['POST'])
def generatePNGandReturnSVG():
    data = request.json
    print(data)

    attack = data['meleeAttack']
    defense = data['meleeDefense']
    print('Attempting to generate a SVG image with attack ' + attack + ' and defense ' + defense)

    svg_prompt = "Generate a 256x256 image of a battle wizard in gaming pixel art style. The image must reflect battle capabilities of the wizard, he has to have a weapon in one hand and a spell book in another hand. This wizard has 2 stats -- melee attack and melee defense, each of them has a maximum value of 20. The bigger is the stat, the more the wizard's appearance should reflect. This wizard has " + attack + " melee attack and " + defense + " melee defense."
    response = client.images.generate(
        model="dall-e-2",
        prompt=svg_prompt,
        size="256x256",
        quality="hd",
        n=1,
    )

    image_url = response.data[0].url

    #Saving generated .PNG data
    content_data = requests.get(image_url).content
    
    f = open('img.png','wb')
    f.write(content_data) 
    f.close()  

    #Creating, outputting and saving .SVG data
    image = Image.open('img.png').convert('RGBA')
    svg_image = rgba_image_to_svg_pixels(image)

    fsvg = open('img.svg','w')
    fsvg.write(svg_image)
    fsvg.close()

    return svg_image

if __name__ == '__main__':
    app.run(debug=True)