# Project Proposal 

## Title 
FindYourFood
## Project Summary 
Our application provides users with the best dining options available on campus using their dietary preferences.  
## Application Description 
First, students can enter their information into a database (eg. name, allergies, cuisine preferences, vegetarian/vegan). Next, we will construct a database of the on-campus dining options (eg. name, cusine options, meals, ingredient lists). Then based on the student's profile, we will guide the student to a desirable dining location.
## Application Use 
This application is incredibly helpful for all students looking to find accomodations suiting their personal dietary preferences. Because allergies are a severe form of danger to students, the application gives us a solution to maintaining the health of students. 
## Application Realness 
There are two categories to the data we’re storing for this project; information about the student user and information about the dining halls.. For each user, we will store their preferences for cuisines of food and their dietary restrictions, in order to match these to open dining halls. For each dining hall, we will store their locations and hours of operation throughout the week. We will also store the “restaurants” in each of them, and try incorporating their daily menus (like in the current Illinois app). Depending on how much time we have after completing the MVP, we might also add information about how well-rated specific restaurant items are to give users more details when picking where to eat.
## Application Functionality 
 * Once again, we will be storing information about the user and dining halls. For each user, we will store an ID (UUID string), and their inputted cuisine preferences and dietary restrictions (strings, from a set of enumerations). For each dining hall we will store an ID (UUID string), location (string of their address), hours of operation (array of days to numbers), and restaurants (array of strings(name) to strings(cuisine). The information about the dining hall will be static and declared when we create the app. If we incorporate the daily menus, we would store all that information as sets of strings, and possibly get the data from the same source as the Illinoi app (more research is needed for this).
 * Web app functions; on our website, a user could…
    * Enter their dietary restrictions from a set of strings we provide
    * Enter their cuisine preferences from a set of strings we provide
    * Enter their current location
    * View open dining halls that match their preferences and dietary restrictions, listed based on distance from their current location and relevance to their restrictions/preferences
    * Determining the distance would be a more complex feature - we need to decide between simple physical distance and somehow determining the time it  would realistically take to reach a particular dining hall, like on Google Maps
 * If we had extra time after reaching a minimal version of the project we could add…
    * A way for users to rate restaurants or their menu items to give other users more details when making their choice
    * A way to integrate more accurate distance measurements (for example, if a student wanted to sort the results by what they could reach the soonest by walking or bus)
## UI Mockup 
<img width="1069" alt="Screen Shot 2022-09-26 at 4 06 58 PM" src="https://user-images.githubusercontent.com/39881644/192380832-e9afa25b-6bfd-4eba-87e0-767aa18d2a62.png">

Some additinal mockups 

<img width="620" alt="Screen Shot 2022-09-26 at 10 03 31 PM" src="https://user-images.githubusercontent.com/39881644/192422246-96c41e13-0db1-4167-9fd6-7569e2e50dfa.png">
<img width="688" alt="Screen Shot 2022-09-26 at 10 03 39 PM" src="https://user-images.githubusercontent.com/39881644/192422258-6c611b6d-7f6e-4378-a658-5222851ec466.png">
<img width="656" alt="Screen Shot 2022-09-26 at 10 03 45 PM" src="https://user-images.githubusercontent.com/39881644/192422273-93b4f593-2741-48a1-99c0-0ef9f214efd6.png">



## Work Distribution 
We plan on delegating the project work as following:
 * Liza - Creation of stored Database (dining hall information) and co-ordinating group activities.
 * Prathamesh - Designing backend logic, the query functions, and finding required APIs.
 * Keerthana  - UI design, implementing the rating system, and debugging.
 * Eesha - Work on map distance function, helping with backend logic, and debugging.
