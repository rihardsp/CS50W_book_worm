# Book Worm

Book Worm is a website where users can create their accounts and search for various books online for comparison.

## User Instructions

Any user has to create their profile to use the application. Users can do that by registering on the log-in screen. Once registered users arrive at the main landing site where they can see blogs for other users. Main features of the application involvelve Comparer, Library and Write Blog. 

## Distinctiveness and Complexity 

I believe the website I built over the last month or so is quite complex. Although I didn't focus a lot on the visual effects, I spent a lot of time trying and interacting with various website APIs. The website doesn't store a lot of data, but it pulls data mostly from Google's API service. While users are searching for the book website suggests users various books which are dynamically received from Google Books search engine. The next complex part was to once the search is entered to dynamically build a pagination mechanism that only loads that page where the user is currently looking at. Server side pagination calculates which part of search results we have to request from Google's API and index it correctly. Then only those results are returned to the page. This increases performance noticeably. 
Another complexity was around pulling other data from the Google API and displaying it to users, as well building dynamic links to the other pages where users can find more information about each of the books. 

As I am not a UI designer I relied heavily on a template provided by BootstrapMade - [Template Moderna](https://bootstrapmade.com/demo/Moderna/). This actually increased the amount of work I had to spend on the website as I had to study other developers' code a lot and had to adjust and copy only things that were required for my website. I believe I would be finished some good 2 weeks sooner if I would just rely on simple bootstrap. However, I learned a lot during this process and saw how professional website design code is developed, especially CSS. 

Django utilization - I used models to save user settings and profiles, book table to save books by users, blog model to save blogs written by users and emails to save any information sent to the support team by application users. I also heavily invested in pagination making it as dynamic as possible. Other Django features I learned additionally to the course was PasswordChange class which are prebuilt for the developer and using Forms to get profile data. As well, Django is used heavily to load various content on the site and help with navigation.

Javascript - website runs numerous javascript functions to interact with the back-end and APIs across the web. Javascript is used to save data into the databases, receive data from the back-end to load it on the screen  and also query Google API. 

AWS - The website is built on AWS and I am now working on deploying it on one of the free tier services in order to publish it on Linkedin. This also increased the complexity as I had to learn how to work with AWS and still need to move the Database over to one of AWS storage solutions. 

## Failures
I also struggled a lot with the APIs as I had to study loads of documentation to finally arrive at the conclusion that a particular API doesn't work for me. Especially huge blow to my initial idea was that Amazon doesn't share their ratings and prices to external websites simply and that Goodreads has ceased to support their API programm and are not providing developers with new account keys anymore. If these two (and other) services would be feasible it would increase the functionality and speed of the website drastically. 

## Further development
Since I am looking forward to deploying the application on AWS and sharing it on my Linkedin profile I will keep on developing additional features. The users will be able to like blogs and follow various profiles similar to what we had in the Networking site project. The users will also be able to filter blogs based on various criteria like, book name, genre or author. I will also pull from other projects done within this course to add some quick to build features like wordcounters for blogs, like count and other things which I had to leave out as they would be too similar to any of the previous work done. 

## How to run application
1) Pull the application source code from the repository.
2) Navigate to the environment/project folder. 
3) run python manage.py runserver 8080.


## File Contents

#### HTML Files

```comparer.html``` Most important page of the whole application. It allows users to search for books and shows results retrieved from Google Books API. The file extends the ```comparer.js``` file and has two main parts. Search block and Results block with paginator at the bottom of it. 

```about_us.html```This is a static HTML template to talk about me

```book_view.html```This is a dynamic page to show information about selected book. Page receives all information from Django Back end application

```change_password.html```Standard Django change password template

```contact_us.html```Form that receives users inputs for saving a message in the DB

```index.html``` Landing page with picture of library and all blogs written by users. 

```layout.html```Layout that is extended in every page. This is mainly used for navigation and footers. 

```library.html``` All saved books by the user are displayed here. 

```login.html```Used to be displayed for users that have not been logged in.

```register.html``` For the users that have not been logged in gives an option to register. Django standard generated. 

```settings.html``` Allow users to update their details and can also lead to change password template

#### JS Files

```book_view.js``` script for ```book_view.html``` file and works to save/unsave books in the library and save blogs to the back end. 

```comparere.js``` interacts with the django backend to send searches and also allows dynamically suggest search results. 

```contact.js``` monitors the contact input form and sends it to be saved to django back end. If successful returns a success message. This was a nice learning curve as I relayed on the templates script. 

```main.js``` templates script file used to add visual effects like onscroll changes and jump to the top of the page. 

#### CS File

```style.css``` the file used to copy in templates style patterns and also to add my own styling rules like - center. 

#### Python Files

```views.py``` main views file, with all application views in it and few helper functions. 

```apis.py``` backend APIs application is communicating with. 

```models.py``` Django database models

```urls.py``` Django urls links




