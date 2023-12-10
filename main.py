from flask import Flask, request, Response
from threading import Thread
import requests
import os
from openai import OpenAI
from PIL import Image
# from init import rgba_image_to_svg_pixels
#initializing and loading dotenv for custom path to openai api key
# from dotenv import load_dotenv,find_dotenv
# load_dotenv(find_dotenv())

client = OpenAI(
   api_key="your Open AI API key" #alternatively use dotenv library to load it from .env file
)

app = Flask(__name__)

last_image_link = 'empty image link'

def process_request(attack, defense):
    print('Attempting to generate a PNG image with attack ' + attack + ' and defense ' + defense)

    svg_prompt = "Generate an image of a battle wizard from a dark fantasy world in a fantasy style. The image must look somewhat realistic, like it is an illustration from a high budget movie, do not make it look it is from a video game. A battle wizard has to have a weapon in one hand and a spell book in another hand. A wizard has 2 main stats -- melee attack and melee defense, each of them has a maximum value of 20. The bigger is the stat, the more the wizard's appearance should reflect its battle capabilities in the respective way. This wizard has " + attack + " melee attack and " + defense + " melee defense. A battle wizard must be wearing some armor and have its own unique style that make it look different from other Battle Wizards. You have to adhere to very strict standards and all instructions in this prompt."
    
    #UPD: upgraded to dall-e-3 and 1024x1024 since the image is not being converted to SVG anymore
    response = client.images.generate(
        model="dall-e-3",
        prompt=svg_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
 
    global last_image_link
    last_image_link = image_url

    print('Image URL obtained from Dalee, returning it')

    return image_url

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/get-last-image-link', methods = ['GET'])
def getLastImageLink():
    if(last_image_link == 'empty image link'):
      return last_image_link
    
    response = requests.get(last_image_link)
   # Check if the request was successful
    if response.status_code == 200:
        # Return the content of the response and specify the mimetype as 'image/png'
        return Response(response.content, mimetype="image/png")
    else:
        return "Image could not be fetched", 404

@app.route('/get-generate-png', methods=['GET'])
def generatePNG():

    attack = request.args.get('meleeAttack', default='0', type=str)
    defense = request.args.get('meleeDefense', default='0', type=str)

    # Start the processing in a new thread
    thread = Thread(target=process_request, args=(attack, defense))
    thread.start()

    return "true"

if __name__ == '__main__':
    app.run(debug=True)