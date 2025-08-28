from tavily import TavilyClient

def search_and_print(query, api_key="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"):
    tavily_client = TavilyClient(api_key=api_key)
    response = tavily_client.search(query)
    for result in response['results']:
        print(f"Title: {result['title']}")
        print(f"Content: {result['content']}")
        print(f"URL: {result['url']}")
        print("-" * 50)


search_and_print("who is elon musk")