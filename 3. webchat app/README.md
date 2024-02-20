About:

    This choose your own adventure web app implements the following

        1) Interactive Streamlit GUI to run the game
        2) Langchain agent backend using query directed tools:
            Tool A) Vector store inventory search populated from a website (localhost)
            Example Query directed to Tool A: Which items in my inventory are best against possessed muppets
            Tool B) Web search powered by Tavily API
            Example Query directed to Tool B: What are the top 3 strategies for outsmarting possessed muppets
        3) User sessions memory

To run:

    python3 -m http.server
    streamlit run app.py debug==True

Tools used in this demo:

    Web search = https://app.tavily.com/home
    Langchain agent = https://python.langchain.com/docs/modules/agents
    Frontend = https://docs.streamlit.io/
    Inventory = https://www.dndbeyond.com/equipment

Remaining:

    1) Graceful app restart