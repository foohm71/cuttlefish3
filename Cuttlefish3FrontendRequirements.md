# Cuttlefish3 Frontend Requirements

## Background

Review `Cuttlefish3MultiAgentRequirements.md` for the overview of the system and the understanding of how the Multi Agent system works. 

Review `references/frontend` for the Cuttlefish2 NextJS UI as this UI will be very similar.

Review `test/cuttlefish3-sanity.py` for how the Cuttlefish3 API is defined

## UI Design

The UI will have 2 tabs:

1. Query Tab
2. Reference Queries Tab

### Reference Queries Tab

This just displays a generated set of reference queries that is in stored in `SampleQuestions.md`. The file is already in Markdown format, so format it accordingly on the tab. 

### Query Tab

This tab will be very similar to the Cuttlefish2 NextJS frontend. 

1. There is no need to input and store the OpenAI key
2. There will need to be 2 toggle switches: (a) Not Urgent (b) Production Issue. These will map to the API payloads `user_can_wait` and `production_incident` respectively
3. Like the Cuttlefish2 UI there will be a Input box for the query
4. The display of the result of the query will be like Cuttlefish2 UI where there will be a summary of the findings and the list of Jira key and titles 

## Folder Structure

Follow a similar folder structure as `references/frontend` (Cuttlefish2 UI) but have all the code be in `frontend` folder   
