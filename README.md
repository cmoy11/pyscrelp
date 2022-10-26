## Pyscrelp
**A Python module to scrape Yelp reviews with no authentication required.**

By [@cmoy11](https://github.com/cmoy11)

This code was originally developed in collaboration with the Race and Data Lab and Dr. Matthew Bui at the University of Michigan School of Information. I have since repurposed this code for simple Yelp review scraping! Simply input a list of Yelp aliases (more on that later) and receive comprehensive csv files containing these businesses' reviews, date reviewed, and star rating.

**Installation**

```pip install pyscrelp```

**requirements**

Pyscrelp relies on the following packages:

    - BeautifulSoup
    - requests

**Usage**

```python
import pyscrelp as pyscr
```    

To generate csv files for a list of businesses:
```python
pyscr.get_reviews(['green-dot-stables-detroit-2', 'brew-detroit-detroit'])
```
* *Note:* * 
get_reviews() takes a list of Yelp aliases as its only parameter and does not return a value. CSV files are generated and non-valid businesses are printed in the terminal.

* *What is a Yelp alias?* *
The Yelp alias is the unique tag following "https://www.yelp.com/biz/". It can be identified here "https://www.yelp.com/biz/**brew-detroit-detroit**" as "brew-detroit-detroit".

* *Why Yelp aliases?* *
The Yelp aliases are conveniently generated by the [Yelp Fusion  API](https://www.yelp.com/developers/documentation/v3/get_started). I also offer another function for basic Yelp alias generation.

To generate a list of Yelp aliases from a list of businesses and a city:
```python
pyscr.hyphenate(['Green Dot Stables', 'Brew Detroit'], 'detroit')
```
* *Note:* * Accepts a list of businesses and a city (please hyphenate multile word cities ~ los-angeles, st-paul). This is **not** 100% accurate, but rather offers a quick way to generate the most likely alias for businesses. The only guaranteed way to find Yelp aliases is manually via [yelp.com](yelp.com) or using the [Yelp Fusion  API](https://www.yelp.com/developers/documentation/v3/get_started). Be sure to check the not-valid print statement in the terminal if you choose to use the hyphenate function.

**Troubleshooting**
Surprise surprise, Yelp does not like mass scraping from their website. I have time.sleep()s scattered throughout the program to try and mitigate this, but if you are scraping hundreds of thousands of Yelp reviews like I have, you will likely run into issues with the Yelp server. Here are some, not so helpful tips! 

The first roadblock you will likely hit is the recaptcha. If your code stops working all of the sudden, try going to yelp.com. If you see this:
![image](images/capterra.png)
proceed through the recaptcha and continue scraping!

If you see this on the other hand:
![image](images/troubleshooting.png)
You are out of luck :/ Yelp has caught you and you have no choice but to wait until you are unblocked. Hopefully you have some coworkers who want thousands of reviews on their computer?

**Diclaimer**
This program may stop working suddenly if Yelp changes their website structure (they have already done this once, I like to think because of me). I will do my best to stay on top of this, but you were warned.