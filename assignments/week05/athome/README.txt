John Comstock
Week05
Small Framework

I worked through the assignment from flaskr_1 and not skipping up to the other pre-built labs. I encountered many typos that I was able to find by running flaskr_test.py. I got it running just fine on my local machine.

Getting it running on my VM was a different story. I was able to get the files copied over, update the apache2/sites-available/default file, and created the flaskr.wsgi file. That is when I ran into the same issues that a few people on the email thread were dealing with.

After a few attempts trying some of the suggestions, (read: not doing any of the radical ideas) I figured out that either the flaskr-wsgi file or the default file only liked absolute paths and could not resolve paths like: ~/flaskr.

Then my next error was not being able to find sqlite, but that was quickly buttoned up and I was on my way.

I have setup a LAMP stack once on my work Linux box and helped some people to troubleshoot theirs(not very well I will say), so this is not something that I would say I am comfortable with. But it can be frustrating when your work environment holds you up from the actual task at hand.  

That being said, I did enjoy the TDD side of this assignment. I was introduced to TDD in my first C# class when we had to create our programs that way and turn in our TDD tests.
