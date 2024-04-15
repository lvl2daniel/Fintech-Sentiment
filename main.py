# open the positive and negative words files
import os
from zipfile import ZipFile


positive_file = open("wordlists/LoughranMcDonald_Positive.csv", "r")
negative_file = open("wordlists/LoughranMcDonald_Negative.csv", "r")

# read the positive and negative words files

positive_words = positive_file.read().splitlines()
negative_words = negative_file.read().splitlines()

# close the positive and negative words files

positive_file.close()
negative_file.close()




# make a hashmap with key as company name and value as the average ratio of positive to negative words

companies_and_scores = {}
print("Calculating scores for companies...")
for company in os.listdir("companies"):
    # open the zip file
    with ZipFile("companies/" + company, "r") as zip_file:
        # iterate over the articles in the zip file, ignoring those with _doclist in the name
        currRatios = []
        for article in zip_file.namelist():
            if "_doclist" not in article:
                # find the ratio of positive to negative words in the article
                with zip_file.open(article) as file:
                    article_text = file.read().decode("utf-8")
                    # filter out formatting and non-alphanumeric characters
                    article_text = "".join([char for char in article_text if char.isalnum() or char.isspace()])
                    article_text = article_text.upper()
                    positive_count = 0
                    negative_count = 0
                    for word in article_text.split():
                        if word in positive_words:
                            positive_count += 1
                        if word in negative_words:
                            negative_count += 1
                # store each articles ratio in a list
                try:
                    currRatios.append(positive_count / negative_count)
                except ZeroDivisionError:
                    currRatios.append(positive_count)
        # calculate the average ratio of positive to negative words from every article in the list
        average_ratio = sum(currRatios) / len(currRatios)
        # store the average ratio in a dictionary with the company name as the key
        #   and shave off .zip at end of company name
        company = company[:-4]
        companies_and_scores[company] = (int)((average_ratio - 1 ) * 100)
        # close the zip file
        zip_file.close()
    # sort the companies_and_scores dictionary by value
    companies_and_scores = dict(sorted(companies_and_scores.items(), key=lambda item: item[1], reverse=True))
    # print the companies_and_scores dictionary as a numbered list
for i, (company, score) in enumerate(companies_and_scores.items()):
    print(f"{i + 1}. {company}: {score}")
# print the top 5 companies
print("The top 5 companies with the highest sentiment scores are:")
for i, (company, score) in enumerate(list(companies_and_scores.items())[:5]):
    print(f"{i + 1}. {company} with a score of {score}")