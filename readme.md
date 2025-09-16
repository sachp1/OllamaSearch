# OllamaSearch

OllamaSearch is an intelligent agent that combines an offline LLM (Large Language Model) with live web Search to answer user queries. It uses the [transformers](https://github.com/huggingface/transformers) library for text generation and can fetch real-time information from the web.

## How Search Works

1. **User Query**:  
   You enter a question or prompt in the console.

2. **Agent Decision**:  
   The agent (offline LLM) receives a prompt instructing it to answer directly if possible, or to request a web search if external information is needed.  
   - If the LLM decides it needs more information, it responds with `SEARCH("your query")`.

3. **Routing**:  
   The system detects if the agent requested a search.  
   - If so, it extracts the search query and sends it to Bing Search using the Bing API.
   - The Bing Search API returns relevant snippets from the web.

4. **Final Answer Generation**:  
   The LLM receives the context (either its own answer or the Bing search results) and generates a final, comprehensive answer for you.

## Offline LLM Model

- The LLM model (e.g., `Qwen/Qwen3-4B`) runs locally using HuggingFace's `pipeline`.
- It can answer questions directly using its trained knowledge.
- For questions requiring up-to-date or external information, it requests a web search.

## Bing Search Integration

- Bing Search is accessed via the Bing Web Search API.
- The API key is loaded from environment variables or set directly in the code.
- The agent can fetch live data (news, facts, etc.) and use it to enhance its answers.

## Setup

1. **Install Dependencies**
   ```sh
   pip install transformers requests python-dotenv
   ```

2. **Set Environment Variables**
   - Add your Bing API key to a `.env` file:
     ```
     BING_KEY=your_bing_api_key
     ```
   - (Optional) Add your OpenWeather API key if you want weather queries.

3. **Run the Agent**
   ```sh
   python main.py
   ```

## Example Usage

```
Welcome to NeuroAgent! Type your query below (or type 'exit' to quit):
Enter your query: Who is the president of France?
Final Answer: [LLM or Bing-powered answer]
```

## How It Works (Code Reference)

- Agent decision logic: [`agent_decision`](main.py)
- Bing search integration: [`bing_search`](main.py)
- Routing and context handling: [`route_agent_output`](main.py)
- Final answer generation: [`generate_final_answer`](main.py)

---

For more details, see [main.py](main.py).

---

> **Current Model:**  
> OllamaSearch currently uses the `Qwen/Qwen3-4B` model