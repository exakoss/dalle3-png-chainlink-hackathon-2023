# 3x Battle Wizards Flask Python API to generate PNG images with DALLE-3

This API connects MyChainNFT.sol contract instances to Open AI API through Chainlink Functions. Built by @exakoss for 3x Battle Wizards @ Chainlink Hackathon 2023 Constellation.

Read more about the project: https://devpost.com/software/3xnft

Smart Contracts Repo: https://github.com/exakoss/chainlink-hackathon-2023

Set Up Instructions:

0) Depending on your platform, follow a guide to set up a python virtual environment in *venv* folder and activate it.
1) Set up your OpenAI key in main.py and/or .env files.
2) Run the following command to deploy a development Flask server on localhost:

```shell
python main.py
```

3) Query your local server via your browser or Postman to make sure that /get-last-image-link and /get-generate-png routes work properly.
4) Deploy the server on Google Cloud Run or other cloud platform of your choice:

```shell
gcloud run deploy
```