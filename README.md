# Who Owns Berkeley?

*Hello, Projects Team.*

This project has been a wishlist item at DC for a long time. Every time someone on our projects team has attempted it, they've never been able to make something publishable out of it, so I'm doing this very, very long writeup to make sure that the next person who takes up the reigns is able to finish it. **After reading this page, go to the detailed documentation for the data gathering in the** `rent-data` **directory. Please read it.**

## Background
### A brief history
I first heard of the _Who Owns Berkeley_ project when I joined the DC Projects team in Spring 2017. Though he was out of the office that semester, it was assigned to him. His plan was to collect information on the largest landowners in Berkeley: their properties, rents, tenant complaints, etc. I believe the hope was to publish this data in a searchable database and/or interactive map. Aside from that, you'd have to ask him where he specifically wanted to go with it; he's got a great sense for thinking of interesting angles to our data stories.

He was busy that semester and in the fall, and then he graduated, so the project landed in my lap in Spring 2018. While scraping for rent data, I learned that _three other developers_ had also worked on this project in Spring 2016. They were Aakash Japi, Yika Luo, and Shashank Bhargava, and you should read their writeup [here](http://aakashjapi.com/housing-prices-in-berkeley/).

TL;DR, they scraped data on housing prices and ran a statistical analysis to determine where rents were lower or higher. This was really cool, but I imagine the story didn't end up in _The Daily Californian_ because it didn't tell us much that we didn't already know: Northside rents are higher than Southside. Data journalism stories aren't just statistical reports of trends, so I just don't see how rent price ceiling analysis alone is enough for a story.

### What is this project about?
Ultimately, the answer to this question is up to you. Previous attempts at this project failed, I believe, because we couldn't figure out a satisfying answer. Though the rent data is messy, scraping for it is relatively straightforward, and I explain the process in the `rent-data` README. In Spring 2018, several senior staff in DC attempted to do a _Who Owns Berkeley_ series of articles (bringing together the Projects, Multimedia, and News departments) focused on rising rents and abusive landowners. It fell through for a number of reasons, not least because I couldn't follow through on my end of the project. As you'll see, this project falls apart at crucial places, and as I wrote before, we'll need a new angle if we're going to publish this someday.

## Dependencies
All Python dependencies are here:
```
pip install -r requirements.txt
```

## Meta

| Title | who-owns-berkeley |
|-|-|
| Developer    | [Seokhyeon Ryu](seokhyeonryu87@gmail.com) |
| Link | [http://projects.dailycal.org/2018/who-owns-berkeley/](http://projects.dailycal.org/2018/who-owns-berkeley/) |


©2018 The Daily Californian
