import openai
import logging
import azure.functions as func


def getGpt3Response(inputPrompt, max_tokens=1372, temp=.5, top_p=1, frequency_penalty=.6, presence_penalty=.5):
    
    openai.api_key = ""
    response = openai.Completion.create(model="text-davinci-003", prompt=inputPrompt, temperature=temp, max_tokens=1372, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty)
    
    return response.choices[0].text

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #Get the promptType from the query string
    prompt = None
    promptType = req.params.get('promptType')
    
    if not promptType:
        return func.HttpResponse("This HTTP triggered function requires a promptType in the query string.",status_code=400)
    
    try:
        prompt = req.get_json().get('prompt')
    except ValueError:
        return func.HttpResponse("This HTTP triggered function requires a prompt in the request body.",status_code=400)

    responseString = None

    #TODO - store timing information in some storage resource
    logging.info("Fetching response from openAI")
    responseString = getGpt3Response(prompt)
    logging.info("Received response from openAI")
    
    return func.HttpResponse(responseString,status_code=200)
