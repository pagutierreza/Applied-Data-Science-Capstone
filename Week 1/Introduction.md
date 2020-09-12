# <div align = "center">Applied Data Science Capstone, Week 1<br>Introduction: Modeling Foursquare Restaurant Ratings</div>

## Description of the problem.
For the final assignment of the Applied Data Science Capstone, I've decided to explore the problem of finding a suitable neighbourhood to open a new restaurant in Toronto.

The solution of this problem is aimed towards a possible investor who has these traits:

 * The investor has no particular interest in any neighbourhood or type of restaurant.
 * The investor is interested in the safest type and location of a restaurant that can be opened in Toronto.
 
The concept "safe" in this particular context means: finding the type of restaurant and neighbourhood that would improve the chances of the restaurant being highly rated according to Foursquare. 

To achieve the goal of determing the type and location of restaurant, I will try to model Foursquare restaurant ratings in Toronto. I decided to build this model because from previous observations of acquaintances who opened venues similar to a restaurant, I noticed they chose the business and location out of convenience and personal taste, not if the market values that particular combination of location and type of business. They chose the location because it was close to where they lived, the type of business was a long time ambition and/or saw similar businesses nearby.

Another reason I chose to build this particular model is to try to reduce some uncertainty when a person attempts to start a business, in this case a restaurant. Out of all the possible decisions a person can make, what are the decisions that can have a bigger impact on the success of the business? How is the success of the business going to be measured? I hope the approach I will use in this model can reduce the amount of uncertainty involved, by giving an approximation of possible outcomes derived from choosing a neighbourhood and type of restaurant. In this case, success is going to be measured by the restaurant rating.

## Data.
In order to build a model than can extrapolate the restaurant ratings in Toronto, I will use the following groups of data:

 1. Average commercial rental cost in Toronto per neighbourhood.
 2. Population description of each neighbourhood.
 3. Restaurant traits and ratings of each neighbourhood.
 4. Geographic data of Toronto's neighbourhoods.
 
 ### Average commercial rental cost in Toronto.
 This information will be obtained by using Selenium to scrape commecial rent webpages. The search will be based in Toronto, and no further analysis will be made to determine how appropiate the venue might be for a restaurant. The goal is to get a baseline of how much it costs to rent a commercial venue in each neighbourhood of Toronto.
 
 ### Population description of each neighbourhood.
 This information will be obtained from the 2016 Toronto Census, readily available from Toronto's government page. The I will look for information regarding the population of each neighbourhood, age segregation, average income, population density. These traits may affect the type of restaurant that's preffered on each neighborhood.
 
 ### Restaurant traits and ratings.
 Foursquare will be used to obtain the restaurant's rating, categories and other relevant traits. The search will be made on a neighbourhood basis, tweaking the  search radius for each neighbourhood to get the most possible amount of data related to restaurants.
 
 ### Geographic data of Toronto's neighbourhoods.
 This information will be obtained from Toronto's government page. It's a GEOjson file that describes the geometry of each neighbourhood in Toronto. This information will be used to fine tune the searh radius and to segmentate the rental venues locations.
 


