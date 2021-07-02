# NLP Contract Analytics
In this project I'm building a machine learning model using natural language processing (NLP) to identify various contract clause types. My goal is that the model can recognize clauses in unseen contracts and categorize them with at least 70% accuracy.



I'm using the [**Atticus Open Contract Dataset**](https://www.kaggle.com/konradb/atticus-open-contract-dataset-aok-beta) from **kaggle**, which is a hand labelled corpus of 200 legal contracts - courtesy of **atticusprojectai.org**. 

The commercial contracts in the dataset are  sourced from the EDGAR (Electronic Data Gathering, Analysis, and Retrieval) system used by the U.S. Securities and Exchange Commission (SEC). Publicly traded companies in the United States are required to file certain material contracts under SEC rules. Access to these contracts is available to the public for free at https://www.sec.gov/edgar.

The contracts were downloaded from EDGAR between March and July 2020, and manually labeled between March and October 2020.

[^1]: source: Datasheet for Atticus Open Contract Dataset (AOK) (beta).pdf



The dataset includes commercial contracts from the below 22 contract types.

| Type of Contracts            | # of Docs |
| ---------------------------- | --------- |
| Affiliate Agreement          | 9         |
| Co-Branding Agreement        | 22        |
| Development Agreement        | 23        |
| Distributor Agreement        | 13        |
| Endorsement Agreement        | 13        |
| Franchise Agreement          | 8         |
| Hosting agreement            | 4         |
| IP Agreement                 | 4         |
| Joint Venture Agreement      | 10        |
| License Agreement            | 33        |
| Maintenance Agreement        | 9         |
| Manufacturing Agreement      | 8         |
| Marketing Agreement          | 6         |
| Non-Competition Agreement    | 3         |
| Outsourcing Agreement        | 4         |
| Reseller Agreement           | 5         |
| Service Agreement            | 4         |
| Sponsorship Agreement        | 4         |
| Supply Agreement             | 4         |
| Transportation Agreement     | 4         |
| Strategic Alliance Agreement | 6         |
| Promotion Agreement          | 4         |



There are around 3,000 labels in the dataset corrseponding to 40 categories of legal clauses.







