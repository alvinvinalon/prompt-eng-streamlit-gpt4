# A Streamlit-based WebApp integrated with Azure OpenAI
This experimental web app uses the Streamlit web development framework and integrates with Azure OpenAI. It supports GPT-3.5 Turbo and GPT-4 deployments.


## Streamlit
Visit the official website: https://streamlit.io/


## Pre-requisites
- Python 3.11.3 and pip. You can download the latest version of Python from the official website (https://www.python.org/downloads/). 
- An Azure Subscription with Azure OpenAI Service provisioned.
- Visual Studio Code

## How to run locally
1. Clone this repository

2. Open the folder in VS Code and run the following from the terminal:

```pip install -r requirements.txt```

3. Rename the ```.env.txt``` file found in the root directory to ```.env```.

Replace the values for the following (The values must come from your Azure OpenAI Service):
OPENAI_API_BASE
OPENAI_API_KEY
OPENAI_API_ENGINE

4. Run ```streamlit run app.py``` in the VS Code terminal

5. Ask away!

## Settings
- Temperature: Used to control the randomness or creativity of the model's output. It is a key element in the fine-tuning process as it affects the text generation behavior.
- Max Response Tokens: Used to control the maximum number of tokens (words or word pieces) in the generated response.
- Select Expertise: Used by the Prompt template which tells the model which topics it should only respond to. Selecting "General Knowledge" will allow the model to answer anything (Note: Azure has its own content filtering. Avoid asking it inappropriate questions).
- Custom Expertise (comma separated): Add more expertise e.g. "Python, OpenAI, Blockchain" (without the double quotes)
- Select Personality: Configures the personality of the model that defines the "tone" of the response.
- Select Writer Style: The model will mimic the selected person/character when writing its response.

Always hit ```Apply``` after changing the System settings.

## Some annoyances
1. The User chat text area does not get cleared in every input. So you'll need to manually clear this out (Select All then delete.).
If you don't clear the user input, and you accidentally invoke the model, it will answer the same question inside the text area.

2. If you are using GPT4, this service tends to be slow in generating response. Use GPT3.5-Turbo if you can.