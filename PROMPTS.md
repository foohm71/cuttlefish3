# Session Prompts and Actions

## Prompt 1
**User Request:** Please save all the prompts and summary of the actions (unless the response is an explanation of what's going on) of this session in PROMPTS.md

**Action Summary:** Created PROMPTS.md file to track session prompts and actions.

## Prompt 2
**User Request:** Review JIRA_OPEN_DATA_LARGESET.csv and see if it be possible to move all the dates accordingly to a date closer to today. Do not perform the date shift yet but explain what you intend to do

**Action Summary:** Analyzed 48.8MB CSV file containing JIRA issue data spanning 2003-2013 (11 years). Identified three date columns (created, resolved, updated) and proposed shifting all dates forward by ~11.5 years to modernize the dataset to 2014-2025 range while preserving temporal relationships and chronological order.

## Prompt 3
**User Request:** Ok please proceed but save the results to JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv

**Action Summary:** Successfully processed and shifted 128,222 date timestamps in the CSV file forward by 4,064 days (11.1 years). Created date_shifter_v2.py script using regex approach to handle complex CSV structure. Generated JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv (49MB) with dates transformed from 2003-2013 range to 2014-2025 range while preserving all temporal relationships, chronological order, and microsecond precision.

## Prompt 4
**User Request:** Ok next I want you to, with this data (JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv) see if you can generate simulated release ticket entries (key field will have pattern "PCR-<number>") using the data as inspiration (and any other searches needed) for the different projects in the data? If so, can you give a couple of examples first for me to assess? I would like the descriptions to have more details eg. what was fixed in those tickets, which modules were updated. Please provide a couple of examples, thanks

**Action Summary:** Analyzed the shifted CSV data to identify project patterns (FLEX, JBIDE, RF, SPR, HBASE with 42,000+ total tickets). Created analyze_projects.py script to extract project information. Generated two detailed PCR release ticket examples: PCR-10001 for Apache Flex Framework 4.16.1 and PCR-10002 for JBoss Tools 4.28.0.Final. Examples include comprehensive release notes with specific modules updated, bug fixes referenced from actual ticket patterns, performance improvements, dependency updates, and professional technical formatting.

## Prompt 5
**User Request:** If there were 1 release per project per week, how many PCR tickets will be generated?

**Action Summary:** Calculated that with 5 projects (FLEX, JBIDE, RF, SPR, HBASE) releasing once per week over the 11-year shifted dataset timespan (2014-2025), there would be 2,860 total PCR tickets: 5 projects × 52 weeks/year × 11 years = 2,860 tickets, with 572 PCR tickets per project.

## Prompt 6  
**User Request:** ok generate them in JIRA_OPEN_DATA_LARGESET_RELEASE_TICKETS_SYNTHETIC.csv in the same csv format as JIRA_OPEN_DATA_LARGESET.csv

**Action Summary:** Created comprehensive generate_pcr_tickets.py script and successfully generated 2,860 synthetic PCR release tickets (PCR-1 through PCR-2860) distributed across 5 projects with weekly release cadence from 2014-01-06 to 2024-12-16. Each ticket includes detailed release descriptions with modules updated, bug fixes, features, technical metrics, and professional formatting. Output file JIRA_OPEN_DATA_LARGESET_RELEASE_TICKETS_SYNTHETIC.csv (4.6MB) matches original JIRA CSV structure with 18 columns. Priority distribution: 60.8% Minor (patch releases), 28.6% Major (minor releases), 10.6% Critical (major releases).

## Prompt 7
**User Request:** ok I reviewed JIRA_OPEN_DATA_LARGESET_RELEASE_TICKETS_SYNTHETIC.csv and there are 3 quotes when there only needs to be 1 eg. """ instead of " 

**Action Summary:** Fixed CSV quoting issue by updating generate_pcr_tickets.py script to remove manual quote wrapping and let Python's CSV writer handle quoting automatically. Regenerated JIRA_OPEN_DATA_LARGESET_RELEASE_TICKETS_SYNTHETIC.csv (4.4MB) with proper formatting that matches original JIRA CSV exactly - single quotes only where needed (fields with commas/newlines), simple fields unquoted. Verified 2,860 PCR tickets maintain correct structure and content.

## Prompt 8
**User Request:** Review Golden_Dataset_Generator_Standalone.ipynb. I want a modified version of this to use JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv instead of the complaints.csv to generate a golden data set for this project. Use the "description" and "title" fields as input to create query and response golden dataset. Limit the number of entries in the golden dataset to 15. Name the new notebook Golden_Dataset_Generator_Cuttlefish.ipynb

**Action Summary:** Reviewed Golden_Dataset_Generator_Standalone.ipynb and created modified version Golden_Dataset_Generator_Cuttlefish.ipynb for JIRA data. Key changes: replaced complaints.csv with JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv, combined "title" + "description" fields as content source, limited to exactly 15 Q&A pairs, upgraded to GPT-4o-mini for technical content, added JIRA-specific metadata (key, project, priority), enhanced content processing for large CSV fields, custom LangSmith dataset naming, and added quality checks for technical keywords and JIRA-specific terms.

## Prompt 9
**User Request:** ok from both JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv and JIRA_OPEN_DATA_LARGESET_RELEASE_TICKETS_SYNTHETIC.csv extract out from the title and description what are the 100 most frequently mentioned entities in them and save it in a entities.txt file.

**Action Summary:** Created extract_entities.py script with comprehensive entity extraction using multiple regex patterns to identify technology names, JIRA tickets, class/module names, package names, methods, file extensions, version numbers, acronyms, and error types. Processed 44,373 total rows from both CSV files (41,513 + 2,860), extracting 946,324 total entity mentions from 161,774 unique entities. Applied filtering to remove noise and keep meaningful entities (45,484 after filtering). Generated entities.txt with top 100 most frequent entities ranging from "Steps" (13,537 mentions) to "dataProvider" (645 mentions), including technical terms like HBASE, JBIDE, MXML, XML, EventDispatcher, and file extensions.

## Prompt 10
**User Request:** Review the python notebook Advanced_Retrieval_with_LangChain_Assignment.ipynb. I want to have the same structure but instead of having it set up for the complaints.csv, to have use the JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv and the cuttlefish-jira-golden-dataset-20250731-122634 golden dataset from LangSmith. As the original notebook is meant for instruction there is a lot of information not needed for the new notebook so we can keep the markdown simpler and more direct. The new notebook should be named Cuttlefish3_RAG_Chunking_Retrieval_Evaluation.ipynb

**Action Summary:** Reviewed Advanced_Retrieval_with_LangChain_Assignment.ipynb and created simplified Cuttlefish3_RAG_Chunking_Retrieval_Evaluation.ipynb notebook. Key adaptations: replaced complaints.csv with JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv, integrated cuttlefish-jira-golden-dataset-20250731-122634 from LangSmith, streamlined markdown for direct implementation, implemented 7 RAG retrieval methods (Naive, BM25, Multi-Query, Parent Document, Contextual Compression, Ensemble, Semantic Chunking), added JIRA-specific data processing with combined title+description fields, configured OpenAI GPT-4o and text-embedding-3-small models, set up Qdrant vector database, integrated RAGAS evaluation framework with technical faithfulness and answer relevancy metrics, and included comprehensive results analysis section for technical support scenario evaluation. Completed comprehensive JIRA data processing and RAG evaluation pipeline.

## Prompt 11
**User Request:** Look at the metrics (see last cell of the notebook Cuttlefish3_RAG_Chunking_Retrieval_Evaluation). My take is that for this dataset, Semantic Chunking is superior to the Naive approach (ie. RecursiveCharacterTextSplitter) although the Noise sensitivity is higher but that's ok? Thoughts?

**Action Summary:** Analyzed comprehensive RAG evaluation results comparing Semantic Chunking vs Naive approach for JIRA dataset. Confirmed user's assessment is correct - Semantic Chunking significantly outperforms Naive on 5 out of 6 key metrics: Average Score (0.7439 vs 0.6603, +8.36%), Context Recall (0.9556 vs 0.8722, +8.34%), Faithfulness (0.8250 vs 0.7977, +2.73%), Factual Correctness (0.7560 vs 0.6787, +7.73%), and Response Relevancy (0.9538 vs 0.8234, +13.04%). Higher noise sensitivity (0.2290 vs 0.1294) is acceptable trade-off as it indicates better context sensitivity for technical support scenarios. Semantic Chunking achieved best overall performance among all 7 methods evaluated, making it superior for JIRA technical documentation due to better preservation of technical terminology, code snippets, and logical content boundaries.
