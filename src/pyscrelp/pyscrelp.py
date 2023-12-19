from bs4 import BeautifulSoup
from pyparsing import alphas
import requests
import re
import csv
from datetime import datetime

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
        str += f"-{city}"
        hyphen_restaurants.append(str)
    print('done hyphenating')
    return hyphen_restaurants

def get_reviews(restaurants):
    non_valid = []
    reviews = {}
    for restaurant in restaurants:
        print(restaurant)
        # create the restaurant's url using the hyphenated names and provided city
        url = f"https://www.yelp.com/biz/{restaurant}"
        print(url)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        review_information = {}
        reviews_list = []
        regex = r"(\d+)\sreviews"
        regex2 = r"[A-Z][a-z]{2}\s\d+,\s\d{4}"

        # extract comments, ratings, and review count from the restaurant's main Yelp page
        first_ten = soup.find_all('p', class_="comment__09f24__D0cxf")

        # skips restaurant if not in city/url does not exist
        if first_ten == []:
            print(f"{restaurant} is not valid")
            non_valid.append(restaurant)
            continue 
        
        first_ten_stars = soup.find_all('div', class_="css-14g69b3")
        raw_first_ten_dates = soup.find_all('span', class_="css-chan6m")
        num_reviews_extract = soup.find_all('span', class_='css-1x9ee72')

        # extract review dates
        first_ten_dates = []
        for date in raw_first_ten_dates:
            reg_input = re.findall(regex2, date.text)
            if reg_input != []:
                first_ten_dates.append(reg_input)

        # get the number of reviews using regex expression
        for review in num_reviews_extract:
            reg_input = re.findall(regex, review.text)
            if reg_input != []:
                num_reviews = int(reg_input[0])
                review_information['number of reviews'] = num_reviews
        print(f"{restaurant} has {num_reviews} reviews") 

        # builds a dictionary for the first 10 reviews
        for i in list(range(len(first_ten))):
            rating = first_ten_stars[i]['aria-label']
            review = first_ten[i].text.strip()
            review_d = {}
            review_d['date'] = first_ten_dates[i][0]
            review_d['rating'] = rating
            review_d['review'] = review
            reviews_list.append(review_d)

        # loops through the remaining reviews and adds to review dictionary
        counter = 10
        while num_reviews > counter:
            # time.sleep(3)
            new_url = url + f"?start={str(counter)}"
            print(new_url)
            soup = BeautifulSoup(requests.get(new_url).text, 'html.parser')
            next_ten = soup.find_all('p', class_="comment__09f24__D0cxf")
            next_ten_stars = soup.find_all('div', class_="css-14g69b3")
            raw_next_ten_dates = soup.find_all('span', class_="css-chan6m")

            next_ten_dates = []
            for date in raw_next_ten_dates:
                reg_input = re.findall(regex2, date.text)
                if reg_input != []:
                    next_ten_dates.append(reg_input)

            old_reviews = 0
            for i in range(len(next_ten)):
                rating = next_ten_stars[i]['aria-label']
                review = next_ten[i].text.strip()
                review_d = {}
                review_d['date'] = next_ten_dates[i][0]
                review_d['rating'] = rating
                review_d['review'] = review
                reviews_list.append(review_d)

            counter += 10
            if old_reviews == 10:
                break
        review_information['Yelp user reviews'] = reviews_list
        reviews[restaurant] = review_information

    print(f"these restaurants are not valid: {non_valid}")
    return reviews

def write_review_files(restaurants):
    reviews = get_reviews(restaurants)

    for restaurant in reviews.keys():
        all_reviews = []

        for subd in reviews[restaurant]['Yelp user reviews']:
            date = datetime.strptime(subd['date'], '%b %d, %Y') 
            rat = int(subd['rating'][0])
            rev = subd['review']
            
            # creates data list for each review
            review_list = [date, int(rat), rev.replace('¬†', '').replace(' \xa0', ' ')]

            if rev in all_reviews:
                continue
            else:
                all_reviews.append(review_list)

        # sorts reviews based on date
        sorted_data = sorted(all_reviews, key = lambda x:x[1])

        # writes csv file with averaged value for each restaurant
        filename = f"{restaurant}.csv"
        with open(filename, "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["date", "converted_date", "rating", "review"])
            for row in sorted_data:
                csvwriter.writerow(row) 

# if this error: UnboundLocalError: local variable 'num_reviews' referenced before assignment
# class names have changed. Updated BeautifulSoup lines

aliases = ['detroit-pizza-factory-dearborn-heights-3']

for alias in aliases:
    write_review_files([alias])