John Comstock
Week 04

WSGI project

You can view my wsgi project by going to the following link: http://block647045-6ca.blueboxgrid.com/wsgi-bin/lab2.py

I used the Armin Roacher reading to accomplish most of the work.
Wilson Bull had thrown down the gauntlet challenge of adding an image to the pages, so that was a challenge that took a bit of time with the help of stack-overflow.

The images I believe are from creative commons sources: 
books.png
http://www.clipartpal.com/clipart_pd/education/openbook_10945.html

books3.png
http://reads-to-go.blogspot.com/2011/01/book-club-spectrum.html

The only difference between the code on my VM and the submitted code is the pathing. The submitted copy when running locally will run from python ./lab.py will point to localhost:8080/, but my VM one uses the wsgi-bin/lab2.py path as the root.

There is still a bunch that can be improved. I have horrible error checking and I would like my HTML template for the main page to be scalable so if more books are added to the DB, then they would be shown. Also maybe an in page back button, but the browser back button works just as well.

I did run into the sys.path error trying to import the bookdb.py file, but Will showed me a response you sent to another student and I was able to solve that problem.

