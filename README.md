README.md

This is the Fall 2018 Managing Software Development Project Repository  

Authors 
Aditya Rathi  
Survi Satpathy 


About the project  
------------------  
Book Catalog
Background
I have an enormous collection of books; I'm also really particular about keeping them organized and discoverable. I want to be able to lend them to people for some period of time, know where they are and remind people to return them to me on time. I need a way to help me find books by author, subject, time period and even be able to possibly add some personal notes about the book.

Use cases
As a user, I want to be able to:

Add, remove, and update books in my library
Find books by a particular author
Find all books published in a given date range
Find books on a certain subject or genre (i.e scientific books, sci-fi, horror, reference)
Group books together into lists (i.e "my favorite sci-fi books of 2016")
Combine any of the above to create a more complex search query (i.e all horror books published by Stephen Hawking between 1815 and 1820)
Mark a book as "loaned out" to an individual
Remind the individual I loaned my book to that they need to return it by some date I've chosen
Add, remove or update notes about a particular book for later reference
See which books are loaned out and to whom; also see whether they have returned them on time or not
What you need to build
Your team needs to build a web-service that presents an API exposing these features. This does not require building a web interface on top of it; though that should definitely be a possible consumer of your API. To that end, you need to come up with a reasonable set of APIs that a developer can call using HTTP. This API needs to be able to accept and return JSON data for ease of inter-operation with other systems since that is a widely accepted data format these days. In addition it should have proper documentation so that any developer can write an API client or interfaces for this service.

Tools and technologies
We will be using the following tools this semester:

Python
Flask (simple web framework)
Sphinx (for overall documentation)
PostgreSQL (for data storage)
Heroku (for deployments)
Bitbucket (for source control)
Swagger (for API documentation)
JSON (for API interoperability)
Peer review
Peer review is an important part of building software; you can't build in a vacuum and often it helps to get an outsider's perspective. There will be 3 points at which you will be assigned a peer-review for another team:

Application design documentation
API design
API documentation
Deliverables
You will need to deliver, by the 10th week of class, a functional and deployed API that manages to enable the user stories listed above. In addition to the functional service you need to provide documentation (the details of which we will cover later) both for your service at a high level as well as for your API (expectations, behavior, responses).

Components / Points
Functioning, deployed, and adheres to specifications - 50%
API Documentation - 20%
Design Documentation - 15%
Peer-review of another team's service - 15%
