# Learning Statistics with Python


I am a huge fan of <a href="https://djnavarro.net" target="_blank">Danielle Navarro</a>'s book <a href="https://learningstatisticswithr.com" target="_blank">Learning Statistics with R</a>. It is the most accessible statistics book I know of. My students love it. I love it. It's free, and it comes in not only R, but also JASP and JAMOVI flavors. The only problem is, I need to teach intro stats using Python, not R. What to do? Translate the book, obviously!

Since Danielle has been so kind as to open-source the book, I have gone to work translating the R bits to Python, and am learning a lot along the way. <del>To start with, I'm concentrating on translating the code, and putting off editing the textual references to R and R-specific functions for later.</del> Having started with just the code, I have now realized that a better approach is to go through the text line-by-line, and do the job properly the first time. It's a bit slower this way, but ultimately better, I think. 

<del>It's hard to say how far I'll get, but for now</del> I'm having fun, and am excited that the students in my course won't have to forego this fantastic book, just because they need to do their stats in Python.

Update: having by now gotten as far as figuring out how to use Python to overlay the probability density for an F-distribution on top of a distribution created by taking the ratio of scaled random samples from two chi-square distributions, I think I'm committed to seeing this thing through.



#### Log

15-06-2021 Almost done with the theoretical chapters, moving on to the statistical tests now. Saving the chapters on basic programming, graphics, etc. for last. The plan is now to prioritize the chapters that I will need for teaching in the Fall semester.

08-04-2021 Added myst extension -dollarmath to config.yml, so inline math renders now. This seemingly does *not* work for dollarmath inside of a pandas dataframe, so to do tables I will have to knit with kable in R, and then paste the mulitmarkdown into the jupyter notebook. Tables look better this way anyway, so no biggie. I still need to get footnotes to work, though.


06-04-2021 Converted project to jupyterbook format, and added placeholder for all chapters. Currently halfway through code conversion in chapter 4.4 on estimation from a sample.

26-03-2021 Finished correlation section rough draft, and am halfway through binomial distribution section. I am continuing to just focus on the code blocks, leaving text editing for later.

23-03-2021 I have removed the section on mean absolute deviation, because... I dunno, I think I just wanted to hurry on to standard deviation, and I was worrying that students in my course might get bogged down. But then I got to the bit about median absolute deviation, and felt a twinge of regret at taking out mean absolute deviation. So maybe I'll go back and add it back in at some point.

22-03-2021 I'm mostly just concentrating on converting the R code to Python for now. There is much work to be done adapting the text to change the references to the way R works to the way Python works. I have entirely skipped Part 2 for now, because this is 100% R-specific.
