# Cuttlefish3 Requirements 
A LangGraph Based Multi-Agent System to perform RAG queries on Jira tickets, 

## Overall Requirement

We want to build a LangGraph multi-agent system where we take in 3 parameters:

1. A query from a user - see section "Use Cases" in `Cuttlefish3.md` for examples
2. A boolean flag called 'user_can_wait'  
3. A boolean flag called 'production_incident'

And the output is to be:

1. The outcome of the analysis
2. The relevant Jira tickets:
   - Ticket key (key field)
   - Ticket title

See `cuttlefish2-main.py` `/rag` endpoint response for the output

## Overall design

The system will have the following LangGraph agents:

1. A **SUPERVISOR** agent that will 

   - take the query and flags and decides on whether:
     * The query is a keyword search eg. the query is about a particular Jira ticket. If so send the query to the **BM25** Agent
     * The user is able wait for a more comprehensive result (see `user_can_wait` flag to be true). If so send the query to the **ENSEMBLE** Agent
     * The user is dealing with a production incident (see `user_can_wait` is false and `production_incident` is true. If so send the query to the **CONTEXTUALCOMPRESSION** Agent and let it know it is a Production Incident
     * Send the query to the **CONTEXTUALCOMPRESSION** Agent for any other query
   - with the RAG retrieval results, send it to a **RESPONSEWRITER** agent 
   - Display the results from the RESPONSEWRITER agent

   As this requires some nuanced reasoning, we will need a reasoning model. 

2. **BM25** Agent
   
   Use the 'bm25_chain' in 'Cuttlefish3_RAG_Chunking_Retrieval_Evaluation.ipynb' as reference except that we are using the QDrant vectorstore as defined in 'cuttlefish3-main.py'. This agent basically performs a RAG retrieval and returns the results.  

3. **ENSEMBLE** Agent

	Use the 'ensemble_chain' in 'Cuttlefish3_RAG_Chunking_Retrieval_Evaluation.ipynb' as reference. You will have to implement all the retrievers listed. Also all the retrievers will need to use the QDrant vectorstore as defined in 'cuttlefish3-main.py'. This agent basically performs a RAG retrieval and returns the results.

4. **CONTEXTUALCOMPRESSION** Agent

	Use the 'compression_chain' in 'Cuttlefish3_RAG_Chunking_Retrieval_Evaluation.ipynb' as reference. Also all the retrievers will need to use the QDrant vectorstore as defined in 'cuttlefish3-main.py'. This agent basically performs a RAG retrieval and returns the results.

5. **RESPONSEWRITER** Agent

	This agent takes the (a) query from the user (b) the result from the retrievers and formulates the response. The agent needs to take into consideration the intent of the query eg. if it is due to a production incident. As this task requires nuanced reasoning, a reasoning model is required
	
Most of these you can get ideas from the `Multi_Agent_RAG_LangGraph.ipynb` in this workspace 


## Other considerations

Please include the necessary configurations to troubleshoot this system via LangSmith 

This Multi Agent System is to be a notebook like `Multi_Agent_RAG_LangGraph.ipynb` but I would like at the end of the notebook to implement it as a Flask API like in the bottom of 'Cuttlefish.ipynb' but take inspiration from 'cuttlefish2-main.py' especially with handling CORS issues. 

Please name the notebook 'Cuttlefish3.ipynb'

