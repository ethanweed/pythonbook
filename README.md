# Learning Statistics with Python


I am a huge fan of <a href="https://djnavarro.net" target="_blank">Danielle Navarro</a>'s book <a href="https://learningstatisticswithr.com" target="_blank">Learning Statistics with R</a>. It is the most accessible statistics book I know of. My students love it. I love it. It's free, and it comes in not only R, but also JASP and JAMOVI flavors. The only problem is, I need to teach intro stats using Python, not R. What to do? Translate the book, obviously!

Since Danielle has been so kind as to open-source the book, I have gone to work translating the R bits to Python, and am learning a lot along the way. <del>To start with, I'm concentrating on translating the code, and putting off editing the textual references to R and R-specific functions for later.</del> Having started with just the code, I have now realized that a better approach is to go through the text line-by-line, and do the job properly the first time. It's a bit slower this way, but ultimately better, I think. 

<del>It's hard to say how far I'll get, but for now</del> I'm having fun, and am excited that the students in my course won't have to forego this fantastic book, just because they need to do their stats in Python.

Update: having by now gotten as far as figuring out how to use Python to overlay the probability density for an F-distribution on top of a distribution created by taking the ratio of scaled random samples from two chi-square distributions, I think I'm committed to seeing this thing through.



## Progress Log

25-05-2023 Making progress again. I finally fixed (I think) Figure 11.8, which illustrates a sample means and confidence intervals from a series of simulated experiments. The figure _looked_ ok before, but was misleading. Now it should actually be accurate. Also, I learned how to set a local random generator for simulating data frather than relying on a global `random.set_seed()` which apparently doesn't always behave the way I would expect it to, coming from R. As I go along cleaning up the wreckage from my initial pass through these earlier chapters, I doing a little more formatting of the figures to make them look nicer. At first I thought I should keep it ultra-simple, for pedagogical purposes, but now I think I would rather have the figures look a little nicer. I'm also trying to make the code more consistent from figure to figure, and hiding more code away behind the "Click to show" button, which will hopefully make the whole thing more readable.

17-02-2023 Done with my second pass through "Descriptive Statistics", which is one of the longer chapters. "Drawing Graphs" should be pretty quick, and "Data Wrangling" was also written recently, so it shouldn't need much revision. Then it is on to "Basic Programming" which will take some time, but is one of the more important chapters for my own teaching, so I am looking forward to tackling that one.

05-01-2023 Nearly two years since I started this project. I never imagined it would take this long, even taking [Hofstadter's law](https://en.wikipedia.org/wiki/Hofstadter%27s_law) into account, which I did. This semester I am starting at the beginning again, and going though the old chapters, cleaning stuff up, and adding details. These are the chapters that I use most in teaching, and they still contain errors like references to R that should have been changed to Python, and important missing stuff like explaining the different variable types, and basic programming stuff like loops and conditionals. Once I have made a second pass through these chapters, I'll do draft versions of the later chapters. I would be thrilled if I could make it to the Bayes chapter by Spring, but let's see how it goes.

23-09-2022 I have added a lot of what I wanted to put into the data wrangling chapter, although there is so much more that could go in there. I would like to add a section on list comprehensions somewhere, but maybe that will go in the basic programming chapter. There was a good deal from the original "practical matters" chapter that I have removed, because it was very specific to R. Instead, it would make more sense at some point to add more about different kinds of data structures and how they work, e.g. `pandas` dataframes and `numpy` series.

01-06-2022 Done with drafts of chi2, t-test, and one-way anova chapters, and almost done with draft of regression chapter.

15-06-2021 Almost done with the theoretical chapters, moving on to the statistical tests now. Saving the chapters on basic programming, graphics, etc. for last. The plan is now to prioritize the chapters that I will need for teaching in the Fall semester.

08-04-2021 Added myst extension -dollarmath to config.yml, so inline math renders now. This seemingly does *not* work for dollarmath inside of a pandas dataframe, so to do tables I will have to knit with kable in R, and then paste the mulitmarkdown into the jupyter notebook. Tables look better this way anyway, so no biggie. I still need to get footnotes to work, though.


06-04-2021 Converted project to jupyterbook format, and added placeholder for all chapters. Currently halfway through code conversion in chapter 4.4 on estimation from a sample.

26-03-2021 Finished correlation section rough draft, and am halfway through binomial distribution section. I am continuing to just focus on the code blocks, leaving text editing for later.

23-03-2021 I have removed the section on mean absolute deviation, because... I dunno, I think I just wanted to hurry on to standard deviation, and I was worrying that students in my course might get bogged down. But then I got to the bit about median absolute deviation, and felt a twinge of regret at taking out mean absolute deviation. So maybe I'll go back and add it back in at some point.

22-03-2021 I'm mostly just concentrating on converting the R code to Python for now. There is much work to be done adapting the text to change the references to the way R works to the way Python works. I have entirely skipped Part 2 for now, because this is 100% R-specific.
