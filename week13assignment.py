"""
Description about this program: This is a program that shows news in terms of a particular country.
"""



import requests
from pprint import pprint
NEWS_API_KEY = "f5e4460103194ba2bd6e53a5510a2520"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def get_country_code(country_name):
    """
    This function gets the country code of the input country(like USA)
    """
    try:    
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        if response.status_code == 200:
            data = response.json()
            country_code = data[0]["cca2"]
            return country_code.lower()
        else:
            print("Check your input data or network and try again")
            return None
    except (requests.exceptions.RequestException, ValueError) as error:
        print(f"An error occured: {error} Try again!")
        return None

def get_news(country_code):
    """
    This functions takes the country code as a input and gives the articles of news as an output
    """
    params = {
        "country": country_code,
        "apiKey": NEWS_API_KEY
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('articles', [])
    except requests.exceptions.RequestException:
        print("Network error while fetching news.")
    except ValueError:
        print("Invalid response from News API.")
    return []

def article_sorting(articles, limit):
    """
    This function takes the article as an input and converts it into sorted and readable strings as an output
    """
    if limit > len(articles):
        print('Please, enter less number of news')
        return []
    sorted_articles = articles[:limit]
    news_list = []
    counter = 1
    for article in sorted_articles:
        article_str = f"Number {counter}\n Title: {str(article['title'])},\n Author: {str(article['author'])},\n Content: {str(article['content'])},\n Description: {str(article['description'])}\n"
        news_list.append(article_str)
        counter += 1
    return news_list

def main():
    """
    This is the main function than combines all functions and data
    """
    print("🌍 Country-Based News Explorer")
    country_name = str(input("Enter country name(fully): ")).strip()
    if country_name == "":
        pprint("Please, enter the country name correctly!!!")
        return
    country_code = get_country_code(country_name)
    try:
        limit = int(input("How many news articles do you want to see? "))
    except ValueError:
        print("Please, enter an integer number")
        return
    if limit <= 0:
        pprint('Please, enter a positive number')
        return
    data = get_news(country_code)
    list_of_strings = article_sorting(data, limit)
    with open("news.txt", "w", encoding="utf-8") as file:
        for line in list_of_strings:
            file.write(line)
main()
