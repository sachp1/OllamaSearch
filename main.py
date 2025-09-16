from transformers import pipeline
# from transformers import AutoModel, AutoTokenizer
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# token = os.getenv("HF_TOKEN")
bing_key = os.getenv("BING_KEY")
llmmodel = "Qwen/Qwen3-4B"


# bing_search calls the microsoft bing api to perform a web search
def bing_search(query, api_key):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)
    return [item['snippet'] for item in response.json().get('webPages', {}).get('value', [])]

#agent_decision Agent Engine
def agent_decision(query, agent):
    prompt = f"""You are NeuroAgent. If you need external info, respond with SEARCH("query"). Otherwise, answer directly."""
    output = agent(prompt, max_new_tokens=300, truncation=True)[0]['generated_text']
    print("[DEBUG] Agent output:", output)  # Debug print
    return output

# TODO:
#get_weathermakes a tool call to an open source weather provider for corrent weather at a given location:
def get_weather(location):
    api_key = "your_open_weather_api_key"  # Replace with your actual OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    print("[DEBUG] Weather API response status:", response.status_code)  
    print("[DEBUG] Weather API response content:", response.text) 
    print("[DEBUG] Weather API response JSON:", response.json())  
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return f"City {location} not found."
    else:
        return "Error fetching weather data."   

# Router
def route_agent_output(output, api_key):
    if "SEARCH(" in output:
        search_query = output.split('SEARCH("')[1].split('")')[0]
        print(f"[DEBUG] Routing to Bing Search with query: {search_query}")  # Debug print
        snippets = bing_search(search_query, api_key)
        print(f"[DEBUG] Bing Search returned {len(snippets)} snippets")  # Debug print
        return "\n".join(snippets)
    print("[DEBUG] No SEARCH() detected, using agent output as context")  # Debug print
    return output

# Final Answer
def generate_final_answer(context, query, llm):
    prompt = f"Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
    return llm(prompt, max_new_tokens=300)[0]['generated_text']

# Full Flow
def neuroagent_rag(query, api_key, agent, llm):
    agent_output = agent_decision(query, agent)
    context = route_agent_output(agent_output, api_key)
    final_answer = generate_final_answer(context, query, llm)
    return final_answer

if __name__ == "__main__":
    print("Loading LLM pipeline. Please wait...")
    agent = pipeline("text-generation", model=llmmodel)
    llm = agent  # If you want to use the same pipeline for both agent and final answer
    print("Welcome to NeuroAgent! Type your query below (or type 'exit' to quit):")
    while True:
        user_query = input("Enter your query: ")
        if user_query.strip().lower() == "exit":
            print("Goodbye!")
            break
        answer = neuroagent_rag(user_query, bing_key, agent, llm)
        print("Final Answer:", answer)
        print("\nAsk another question or type 'exit' to quit.")
    print("Final Answer:", answer)
