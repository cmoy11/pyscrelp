from bs4 import BeautifulSoup
from pyparsing import alphas
import requests
import re
from datetime import datetime
import pandas as pd

def hyphenate(restaurants, city):
    hyphen_restaurants = []
    for restaurant in restaurants:
        str = ""
        for char in restaurant:
            if char.isalpha():
                str += char.lower()
            elif char == " ":
                str += "-"
            elif char == "&":
                str += "and"
        str += f"-{city.lower().replace(' ', '-').replace('.', '')}"
        hyphen_restaurants.append(str)
    print('done hyphenating')
    return hyphen_restaurants

def collect_reviews(soup, filename, restaurant):    
    stars_regex = r"(\d) star rating"
    dates_regex = r"([A-Z][a-z]{2}\s\d+,\s\d{4})"

    # extract comments, ratings, and review count from the restaurant's main Yelp page
    first_ten = soup.find_all('p', class_="comment__09f24__D0cxf")
    first_ten = [comment for comment in first_ten if 'truncated__09f24__IiW9r' not in comment.get('class', [])]
    first_ten_reviews = [review.text.strip().replace('¬†', '').replace(' \xa0', ' ') for review in first_ten]
    
    first_ten_stars_raw = soup.find_all('div', class_="y-css-1gng1og")
    first_ten_stars_raw = [str(comment) for comment in first_ten_stars_raw]
    filtered_stars = [star for star in first_ten_stars_raw if 'Previous review' not in star]
    first_ten_stars = [re.search(stars_regex, text).group(1) for text in filtered_stars if re.search(stars_regex, text)]        
    first_ten_dates = [re.search(dates_regex, text).group(1) for text in filtered_stars if re.search(dates_regex, text)]

    first_ten_reviewers = soup.find_all('div', class_="user-passport-info")
    if len(first_ten_reviewers) > len(first_ten_dates):
        first_ten_reviewers = first_ten_reviewers[1:]
    names = [link.text for reviewer in first_ten_reviewers for link in reviewer.find_all('a', class_='y-css-12ly5yx')]
    locations = [link.text for reviewer in first_ten_reviewers for link in reviewer.find_all('span', class_='y-css-h9c2fl')]
    elite = [1 if re.search('elite-badge', str(reviewer)) else 0 for reviewer in first_ten_reviewers]


    # builds a dictionary for the first 10 reviews
    review_d = {
        'date': [datetime.strptime(original_date_str, "%b %d, %Y") for original_date_str in first_ten_dates],
        'converted_date': [datetime.strptime(original_date_str, "%b %d, %Y").strftime("%m/%d/%Y") for original_date_str in first_ten_dates],
        'rating': first_ten_stars,
        'reviewer': names,
        'location': locations,
        'elite': elite,
        'review': first_ten_reviews
    }
    print(review_d)
    df = pd.DataFrame(review_d, columns=list(review_d.keys()))
    df['restaurant'] = restaurant
    df.to_csv(filename, mode='a', header=False, index=False)

def get_reviews(restaurants, filename='reviews.csv', composite=False):
    if type(restaurants) == str:
        restaurants = [restaurants]

    not_valid = []

    for restaurant in restaurants:
        if not composite:
            new_filename = restaurant + ".csv"
        else:
            new_filename = filename

        print(restaurant)
        # create the restaurant's url using the hyphenated names and provided city
        url = f"https://www.yelp.com/biz/{restaurant}"
        print(url)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        collect_reviews(soup, new_filename, restaurant)

        regex = r"(\d+)\sreviews"
        num_reviews_extract = soup.find_all('span', class_='y-css-loq5qn')

        try:
            reg_input = re.findall(regex, num_reviews_extract[0].text)
            num_reviews = int(reg_input[0])
        except:
            print('bad url, skipping')
            not_valid.append(restaurant)
            continue

        # if reg_input != []:
        #     num_reviews = int(reg_input[0])
        # else:
        #     print('wrong url, skipping')
        #     break
            
        print(f"{restaurant} has {num_reviews} reviews") 

        # loops through the remaining reviews and adds to review dictionary
        counter = 10
        while num_reviews > counter:
            # time.sleep(3)
            new_url = url + f"?start={str(counter)}"
            soup = BeautifulSoup(requests.get(new_url).text, 'html.parser')
            print(new_url)
            collect_reviews(soup, new_filename, restaurant)
            counter += 10   

    print("unable to collect reviews for the following businesses:", not_valid)
    print("done")     