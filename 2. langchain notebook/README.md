# langchain web loading and document search example

This notebook demonstrates how to implement chains in order to:
    1) Load data from the web into a highly searchable vectorstore as a db
    2) Implement prompts that can search for the relevant Documents in the db
    3) Chain prompts together to load data and respond to a users queries

Final thoughts:
    Seeing how to chain prompts together is insightful into how more complex 
    behaviour works. I believe this feature will likely get implemented directly 
    into Langchain agents.