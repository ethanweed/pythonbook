#!/usr/bin/env python
# coding: utf-8

# # More Python Concepts

# (mechanics)=
# 
# > *Form follows function*
# >
# >-- Louis Sullivan

# In the chapter on [Getting started with Python](getting-started-with-python) our main goal was to, well, get started with Python. As we go through the book we'll run into a lot of new  Python concepts, which I'll explain alongside the relevant data analysis concepts. However, there's still quite a few things that I need to talk about now, otherwise we'll run into problems when we start trying to work with data and do statistics. So that's the goal in this chapter: to build on the introductory content from the last chapter, to get you to the point that we can start using Python for statistics. Broadly speaking, the chapter comes in two parts. The first half of the chapter is devoted to the "mechanics" of Python: installing and loading packages, managing the workspace, navigating the file system, and loading and saving data. In the second half, I'll talk more about what kinds of variables exist in Python, and introduce three new kinds of variables: factors, data frames and formulas. I'll finish up by talking a little bit about the help documentation in Python as well as some other avenues for finding assistance. In general, I'm not trying to be comprehensive in this chapter, I'm trying to make sure that you've got the basic foundations needed to tackle the content that comes later in the book. However, a lot of the topics are revisited in more detail later. 

# ## Using comments
# 
# Before discussing any of the more complicated stuff, I want to introduce the **_comment_** character, `#`. It has a simple meaning: it tells Python to ignore everything else you've written on this line. You won't have much need of the `#` character immediately, but it's very useful later on when writing scripts. However, while you don't need to use it, I want to be able to include comments in my Python extracts. For instance, if you read this: [^note1]
# 
# [^note1]: Notice that I used `print(keeper)` rather than just typing `keeper`. Later on in the text I'll sometimes use the `print()` function to display things because I think it helps make clear what I'm doing, but in practice people rarely do this.
# 

# In[1]:


seeker = 3.1415           # create the first variable
lover = 2.7183            # create the second variable
keeper = seeker * lover   # now multiply them to create a third one
print( keeper )           # print out the value of 'keeper'


# it's a lot easier to understand what I'm doing than if I just write this:

# In[2]:


seeker = 3.1415
lover = 2.7183
keeper = seeker * lover
print( keeper )    


# From now on, you'll start seeing `#` characters appearing in the code extracts, with some human-readable explanatory remarks next to them. These are still perfectly legitimate commands, since Python knows that it should ignore the `#` character and everything after it. But hopefully they'll help make things a little easier to understand.

# (packageinstall)=
# 
# ## Installing and importing 
# 
# 
# There is lots to love about Python as a programming language. Although it has its quirks and peculiarities like any language (programming or natural), it is relatively flexible and welcoming to newcomers, while still be very, very powerful. But one of the best things about Python isn't even the language itself, it is the rich ecosystem of code written by other people that you can use to make Python do things for you. These **libraries** or **packages** [^note2] contain code that people have written to solve particular problems, and then kindly made available for other people, like you and me, so that we don't have to spend our time reinventing the wheel. By installing and importing libraries, you can achieve very complicated things with only a few lines of your own code, by standing on the shoulders of others. Just ask Cueball from the webcomic xkcd:[^note3]
# 
# [^note2]: There are some subtle differences between libraries, packages, and modules, but we don't need to concern ourselves with these here, and I may well mix up these words in the text. The key thing is, they are bits of code that we need to import to make stuff happen in Python.  
# [^note3]: https://xkcd.com/353/

# ![xkcdpython](https://imgs.xkcd.com/comics/python.png)

# When doing anything other than the very most basic forms of data analysis in Python, we will almost always need to use libraries. However, before we get started, there's a critical distinction that you need to understand, which is the difference between having a package **_installed_** on your computer, and having a package **_imported_** in Python. I do not have any idea how many Python libraries are available out there, but it is a lot. Thousands. If you install Python on your computer, you won't get all of them, just a handfull of the standard ones. Depending on how you install Python on your computer, you may have more or fewer libraries installed, but either way, there are thousands more out there that you do not currently have installed. So that's what installed means: it means "it's on your computer somewhere". The critical thing to remember is that just because something is on your computer doesn't mean Python can use it. In order for Python to be able to *use* one of your installed libraries, that library must also be "imported". Basically what it boils down to is this:
# 
# >A library must be installed before it can be imported.
# 
# >A library must be imported before it can be used.
# 
# This two step process might seem a little odd at first, but the designers of Python had very good reasons to do it this way,[^note4] and you get the hang of it pretty quickly.
# 
# I won't get into the details of installing libraries here, simply because it is too much for me to tackle. If you are using Python in an online enviroment, you may already have access to all the libraries mentioned in this book. If you are working with Python on your own computer, the exact details of how you install packages may vary. If you want to use Python on your own computer, and are just getting started, I recommend [Anaconda](https://www.anaconda.com/products/individual#Downloads) as a relatively easy way to install Python and get quick access to all the most common and important libraries.
# 
# [^note4]: Basically, the reason is that there are thousands of libraries, and probably thousands of authors of libraries, and no-one really knows what all of them do. Keeping the installation separate from the loading minimizes the chances that two libraries will interact with each other in a nasty way. 

# ### What libraries does this book use?
# 
# In this book, I have made a concerted effort to limit the number of libraries needed. Often you will find that you can use different libraries to achieve the same results, and sometimes one of these may suit your needs more than another. This is something that can make doing analysis by code rather than pointing and clicking in a dedicated statistics program a bit off-putting; in Excel, there is usually only way to do things, while in Python, there are many. I think this is part of what makes doing statistics using code better, though: you can make your own informed choices, and do *exactly* the analysis you want to do; you don't have to accept some piece of software's default settings. However, point of this book is to get you started doing data analysis and statistics in Python, not to show you all the different ways you could achieve the same goal, so in an effort to keep things simple, I have tried to limit the libraries used in this book to a few of the most important and most common ones for doing statistics with Python. The most prominent ones are: `numpy`, `scipy`, `pandas`, `matplotlib`, `seaborn`, `statistics`, `pingouin`, `math`, and `statsmodels`, but I may use others as well, as needed.
# 
# ### How will I import libraries in this book?
# 
# Once you import a library into Python's active memory, you don't need to do it again. In writing this book, each chapter is a python file [^note5]. So, if I have imported e.g. `numpy` early in the chapter, I don't need to do it again in a later section of the chapter. But, normally I will, because I want the code snippets in this book to be as easy as possible to copy and paste into your own computer. If I don't put the `import` command at the top of the snippet, and you have not already imported the library, then you might copy and paste my code into your computer and get an error message. Then again, sometimes I might forget to put the import statement in, or I might think it should be obvious, or I might just get lazy, so make sure to keep an eye out for this!
# 
# [^note5]: Well, actually it is an `.ipynb` file, but let's not bicker and argue about who killed who.

# ### Importing libraries
# 
# Assuming you have the libraries you need installed on your computer, or can access them in the virtual Python environment you are using in your browser, you will need to import them before you can actually use them. So, for instance, if I want to find the sum of five numbers, I can write

# In[3]:


numbers = [4, 5, 1, 2, 6]
sum(numbers)


# because the authors of Python felt that adding numbers together was such a basic thing that there should be a built-in command for it. At least, I assume so. I don't really know what the authors of Python thought. But, oddly, enough, Python doesn't have a built-in command called "mean". So if I want to know the mean of those same five numbers, I cannot just write

# In[4]:


mean(numbers)


# because Python doesn't know what mean, er, means. Luckily, we don't have to resort to first finding the sum and then dividing by the number of numbers, because there are libraries that _do_ have built-in commands for finding means. The `statistics` library is one. To use the commands in this library, we first have to `import` it. This gives us access to all the many useful commands in the `statistics` library, one of which is `mean`:

# In[5]:


import statistics

numbers = [4, 5, 1, 2, 6]

statistics.mean(numbers)


# You probably noticed the `.` in the code above. This is the way we tell Python that we want to use a command called `mean` which is found inside the library `statistics`. Without the `.`, even though we have imported `statistics`, which has a command called `mean`, we still can't just write `mean(numbers)`. We have to tell Python where to look for this command. This all seems very cumbersome, but it's really not so bad, there are good reasons for doing it this way[^noteconflicts], and you will get used to it fairly quickly.
# 
# [^noteconflicts]: Chiefly among them, this helps avoid unpleasant situations where we may have imported two different libraries that each contain a function with the same name, but which do different things, or worse yet, do different things but _appear_ to do the same thing, which could really get us in trouble!

# One of the ways in which Python is quite flexible is that it gives you some options in terms of how you import libraries. More precisely, you can:
# 
# >Choose to import only a portion of a library
# >rename libraries of portions of libraries when importing
# 
# Let's say we don't want to import the entire `statistics` library — we only want the `mean` command. We can achieve this like this:

# In[6]:


from statistics import mean


# Why would we want to do this? Well, one good reason is that now we *can* simply write `mean(numbers)`; we no longer have to write out `statistics.mean(numbers)`:

# In[7]:


numbers = [4, 5, 1, 2, 6]
mean(numbers)


# Is this the height of laziness? Maybe. But if you start writing the same thing over and over again, saving a few characters here and there is pretty sweet. And this brings us to the other import option: renaming libraries. It is common practice in Python to give libraries abbreviations when we import them. Many of the most common libraries have conventional abbreviations, although you could use anything you like. Thus, you will often see e.g.

# In[8]:


import numpy as np
import seaborn as sns


# This is very convenient, but be careful: if you e.g. import `numpy` as `np`, the Python will only recognize it as `np`, at least for the time your code is in Python's active memory. Also, although you can use whatever abbreviations you like, I highly recommend sticking to the conventional ones, for your sake and for the sake of others trying to read your code. It's kind of fun the first time to do something like

# In[9]:


import statistics as why_you_gotta_be_so

why_you_gotta_be_so.mean(numbers)


# but good code should be easy to read by yourself and others, and if you start playing too fast and loose with renaming, it starts to get less clear what's going on.

# ## Listing the objects in active memory
# 
# Let's suppose that you're reading through this book, and what you're doing is sitting down with it once a week and working through a whole chapter in each sitting. Not only that, you've been following my advice and typing in all these commands into Python. So far during this chapter, you'd have typed quite a few commands, although not all of them actually created variables.
# 
# An important part of learning to program is to develop the ability to keep a mental model of what Python knows and doesn't know at any given time active in your mind. This sounds very abstract, and it is, but as you become more familar with coding I think you will see what I mean. I won't dwell on this here, but it may be useful to take a quick peak at what I mean. If you are working in e.g. a Jupyter Notebook (and I do suggest you do this, at least at first), then by typing `%who` you can see a list of all the variables that Python is currently aware of. So, in my case, I get the following:

# In[10]:


get_ipython().run_line_magic('who', '')


# Here we can see variables that we defined, like `keeper` and `lover`, and also libraries that we imported (and renamed), like `np` and `sns`, as well as the library `statistics` which I then ill-advisedly re-imported and renamed `why_you_gotta_be_so`. To see more details on these variables, we can type `%whos`

# In[11]:


get_ipython().run_line_magic('whos', '')


# This tells us that e.g. `keeper` is a floating-point decimal number with the value 8.539539450000001, and shows us the true names of the objects we have renamed on import. These commands that start with a `%` sign, by the way, are called "magic" commands, and can only be used in environments like Jupyter, which support them. If you are not working in such an environment, you can use the command `dir()`, which achieves the same thing, but will also show you lots of information you probably aren't interested in at this stage.

# ### Removing variables from the workspace
# 
# Looking over that list of variables, it occurs to me that I really don't need them any more. I created them originally just to make a point, but they don't serve any useful purpose anymore, and now I want to get rid of them.  I'll show you how to do this, but first I want to warn you -- there's no "undo" option for variable removal. Once a variable is removed, it's gone forever. Most of the time this doesn't matter, though, because we still have the code we used to create the variable, so unless you delete that too, you can always just re-run the cells in your Jupyter Notebook, and Python will re-make your variables for you, just like they were before. But quite clearly we have no need for these variables any more, so we can safely get rid of them by using the `del()` command.

# In[12]:


del(keeper, lover)


# With `%who` or `dir()` we can check that they are gone.

# In[13]:


get_ipython().run_line_magic('who', '')


# If you want to remove all the variables in memory, and you are working in a Jupyter environment, then `%reset` is a handy way to do this, although I must say that in practice I rarely, if ever, have a need to remove variables from memory. There is usually no harm in them sitting around unused, and if you define a new variable with the same name as an old one, it will just write over the old variable with the same name.

# (load)=
# ## Loading and saving data
# 
# 
# There are several types of files that are likely to be relevant to us when doing data analysis, and there are two in particular that are especially important from the perspective of this book:
# 
# 
# - *Comma separated value (CSV) files* are those with a .csv file extension. These are just regular old text files, and they can be opened with almost any software. It's quite typical for people to store data in CSV files, precisely because they're so simple.
# - *Script files* are those with a .py file extension or an .ipynb extension. These aren't data files at all; rather, they're used to save a collection of commands that you want Python to execute later. They're just text files, but we won't make use of them until later.
#  
# 
# In this section I'll talk about how to import data from a CSV file. First though, we need to make a quick digression, and talk about file systems. I know this is not a very exciting topic, but it is absolutely _critical_ to doing data analysis. If you want to work with your data in Python, you need to be able to tell Python where the data is located.

# (filesystem)=
# ### Filesystem paths
# 
# In this section I describe the basic idea behind file locations and file paths. Regardless of whether you're using Window, macOS or Linux, every file on the computer is assigned a (fairly) human readable address, and every address has the same basic structure: it describes a *path* that starts from a *root* location, through as series of *folders* (or if you're an old-school computer user, *directories*), and finally ends up at the file. 
# 
# On a Windows computer the root is the physical drive [^notedrive] on which the file is stored, and for most home computers the name of the hard drive that stores all your files is C: and therefore most file names on Windows begin with C:. After that come the folders, and on Windows the folder names are separated by a `\` symbol. So, the complete path to this book on my Windows computer might be something like this:
# 
# ```
# C:\Users\ethan\pythonbook\book\LSP.pdf
# ```
# and what that *means* is that the book is called LSP.pdf, and it's in a folder called `book` which itself is in a folder called `ethan` which itself is ... well, you get the idea. On Linux, Unix and Mac OS systems, the addresses look a little different, but they're more or less identical in spirit. Instead of using the backslash, folders are separated using a forward slash, and unlike Windows, they don't treat the physical drive as being the root of the file system. So, the path to this book on my Mac might be something like this:
# 
# ```
# /Users/ethan/pythonbook/book/LSP.pdf
# ```
# 
# So that's what we mean by the "path" to a file, and before we move on, it is critical that you learn how to copy the path to a file on your computer so that you can paste it into Python. There are (again!) multiple ways to do this on the various operating systems, and it doesn't really matter which method you use. A quick search will lead you to many many online tutorials; just find a method that works for you, on your computer. Even if you are working in a virtual Python environment in the browser (such as Google Colab), you will need some concept of file structure to navigate to your data and scripts.
# 
# [^notedrive]: Well, the partition, technically.

# (loadingcsv)=
# 
# ### Loading data from CSV files into Python
# 
# One quite commonly used data format is the humble "comma separated value" file, also called a CSV file, and usually bearing the file extension .csv. CSV files are just plain old-fashioned text files, and what they store is basically just a table of data. This is illustrated below, which shows a file called booksales.csv that I've created. As you can see, each row corresponds to a variable, and each row represents the book sales data for one month. The first row doesn't contain actual data though: it has the names of the variables.
# 
#     
#     

# ```{image} ../img/mechanics/booksalescsv.png
# :alt: booksales
# :width: 600px
# :align: center
# ```

# As is often the case, there are many different ways to get the data from a CSV file into Python so that you can begin doing things with it. Here we will use the `pandas` library, which happens to have a handy command called `read_csv()` which does just what it says.
# 
# We can't just read the data in willy-nilly, though. We need some place to put it. As you may have already guessed, we need to define a variable to put our data into. We haven't talked about variable types yet, and now is not the time, but let it suffice to say that there are different kinds of variables, and some of them can store structured data like the rows and columns in a CSV file. `pandas` calls this kind of variable a "dataframe". You can name your dataframe whatever you like, of course, but by convention they are often called "df", so we'll do that too. Thus:

# In[14]:


# import pandas, and call it "pd" for short

import pandas as pd

# make a new dataframe variable, and use the "read_csv" command from the pandas library to put the contents
# of the file located at "/Users/ethan/Documents/GitHub/pythonbook/Data/booksales.csv" in the dataframe df

df = pd.read_csv("/Users/ethan/Documents/GitHub/pythonbook/Data/booksales.csv")


# Here I have put the full path into the parentheses following `pd.read_csv`, but often I prefer to save the path as a variable, and put that variable into the parentheses instead, like this:

# In[15]:


import pandas as pd

file = "/Users/ethan/Documents/GitHub/pythonbook/Data/booksales.csv"

df = pd.read_csv(file)


# Either way works, but I think this looks nicer, and it also has an additional advantage: it makes the code more versitile. Right now we are just loading a single CSV, but if we want to load many CSV files, it might be useful to write a [loop](loops) that puts different paths into the same variable `file`. But that is a discussion for another time.

# ### Saving a dataframe as a CSV
# 
# Sometimes we create new dataframes using Python. Maybe the CSV we loaded had lots of information that we don't need, or maybe we have loaded several CSV's in, taken a few columns of data from each one, and then combined these into a new dataframe. Or perhaps we have done some calculations on the original data and added a column with e.g. the sum of each row. If we want to save this new dataframe as a csv, `pandas` has a command for that as well:
# 
# ``df.to_csv('/Users/ethan/Desktop/my_file.csv')``
# 
# Every `pandas` dataframe has the built-in ability to be exported as a CSV file. We just need to tell Python what the new file should be called, and where we want it to go in our filesystem. Pretty straightforward, really.

# (useful)=
# ## Useful things to know about variables
# 
# In the chapter on [Getting started with Python](getting-started-with-python), I talked a lot about variables, how they're assigned and some of the things you can do with them, but there are a lot of additional complexities. That probably comes as no great surprise, and we can't go over all of these now, but this section is basically just a bunch of things that I want to briefly mention, that don't really fit in anywhere else. In short, now I'll talk about several different issues in this section, which are only loosely connected to one another.

# (types)=
# ### Variable types
# 
# As we've seen, Python allows you to store different kinds of data. We have seen variables that store text (_strings_), numbers (_integers_ or _floats_), and even whole datasets (_dataframes_). These are just three of the many different types of variable that Python can store. Other common variable types in Python include _dictionaries_, _lists_, and _tuples_. It's important that we remember what kind of information each variable stores (and even more important that Python remembers) since different kinds of variables allow you to do different things to them. For instance, if your variables have numerical information in them, then it's okay to add them together:

# In[16]:


x = 1    # a is a number
y = 2    # b is a number
z = x + y
print(z)


# If they contain character data, Python will still let you add the variables, but the outcome might be unexpected:

# In[17]:


x = "1"   # x is character, as indicated by the quotation marks
y = "2"   # y is character, as indicated by the quotation marks
x + y           


# To us, there isn't really that big a difference between 1 and "1", but to Python, these are entirely different classes of things.

# ### Checking variable types
# 
# Okay, let's suppose that I've forgotten what kind of data I stored in the variable `x` (which happens depressingly often). Python provides a function that will let us find out: `type()`

# In[18]:


x = "hello world"     # x is text (aka a "string")

type(x)


# In[1]:


import pandas as pd

file = "/Users/ethan/Documents/GitHub/pythonbook/Data/booksales.csv"

x = pd.read_csv(file) # x is a dataframe

type(x)


# In[20]:


x = 100     # x is an integer
type(x)


# In[21]:


x = 3.14
type(x)


# Exciting, no? Trust me, you'll need to do this more often than you might think.

# (lists)=
# 
# ## Lists
# 
# A kind of variable that shows up all the time in data analysis with Python is the list. A list is just what it sounds like, it is a single variable that contains a list of items. Just about any variable type you can think of can be listed in a Python list:

# In[2]:


shopping = ["apples", "pears", "bananas"] # a list strings
scores = [90, 65, 100, 82]                # a list of integers
mixed = ["cats", 7, 309.42]               # a list of mixed strings, integers, and floats
combined = [shopping, scores, mixed]      # a list of lists!


# In[3]:


print(shopping)
print(scores)
print(mixed)
print(combined)


# Let's say I am so enamored with Python that I actually decided to keep my shopping list in a Python list. Seems unlikely, I know, but bear with me. Later, I realize I have forgotten what I wrote on the list. This does kind of sound like me, actually. To see the contents of the entire list, I can use `print()`, the way I did above. But let's say I only want to see the second item on the list. Python has a way access specific items in lists, but it will seem strange at first!

# Let's take a look. To access an item in a list, we need to know its `index`, that is, its location in the list. We indicate an index with square brackets. So to find the item with the index 2 in my shopping list, I can write `shopping[2]`, like so:

# In[24]:


shopping = ["apples", "pears", "bananas"]
shopping[2]


# What?!?!? We asked for item 2, and Python gives us "bananas"? But "bananas" is the third item in the list?!?! What's going on?
# 
# The simple answer for this is that Python uses "zero-based indexing": basically, Python starts counting at zero. So "apples" is in the zeroeth position, "pears" is in the first position, and "bananas" is in the second position. If it helps, maybe think of it like buildings in Europe that start with the ground floor, and then go up to the first floor, etc.
# 
# Now just when you have started to get used to zero-indexing, try negative indexing on for size. We can also count backwards from the end of the list, by using negative indices such as `shopping[-2]` But be careful: when you use negative indexing, Python behaves the way you might have originally expected it to. Thus, `shopping[-1]` will return "bananas", `shopping[-2]` will give us "pears", etc. That's just how Python is.
# 
# ### Finding the length of a list
# 
# One last thing on lists for now: it can often be useful to check how many items are in your list. With the toy examples we are using here, of course, it is easy to see how long the list is, because we just typed in the items ourselves. But in actual data analysis, we often deal with very long lists that contain an unknown number of items. In these cases we can use `len()` to check how long the list is:

# In[25]:


len(shopping)


# (dataframes)=
# 
# ## Data frames
# 
# It's now time to go back and take a closer look at dataframes.
# 
# In order to understand why we use dataframes, it helps to try to see what problem the solve. So let's imagine a little scenario in which I collected some data from nine participants. Let's say I divded the participants in two groups ("test" and "control"), and gave them a task. I then recorded their score on the task, as well as the time it took them to complete the task. I also noted down how old they were.
# 
# the data look like this:

# In[5]:


age = [17, 19, 21, 37, 18, 19, 47, 18, 19]
score = [12, 10, 11, 15, 16, 14, 25, 21, 29]
rt = [3.552, 1.624, 6.431, 7.132, 2.925, 4.662, 3.634, 3.635, 5.234]
group = ["test", "test", "test", "test", "test", "control", "control", "control", "control"]


# So there are four variables in active memory: `age`, `rt`, `group` and `score`. And it just so happens that all four of them are the same size (i.e., they're all lists with 9 elements). Aaaand it just so happens that `age[0]` corresponds to the age of the first person, and `rt[0]` is the response time of that very same person, etc. In other words, you and I both know that all four of these variables correspond to the *same* data set, and all four of them are organised in exactly the same way. 
# 
# However, Python *doesn't* know this! As far as it's concerned, there's no reason why the `age` variable has to be the same length as the `rt` variable; and there's no particular reason to think that `age[1]` has any special relationship to `score[1]` any more than it has a special relationship to `score[4]`. In other words, when we store everything in separate variables like this, Python doesn't know anything about the relationships between things. It doesn't even really know that these variables actually refer to a proper data set. The data frame fixes this: if we store our variables inside a data frame, we're telling Python to treat these variables as a single, fairly coherent data set. 
# 
# To see how they do this, let's create one. So how do we create a data frame? One way we've already seen: if we use `pandas` to import our data from a CSV file, it will store it as a data frame. A second way is to create it directly from some existing lists using the `pandas.Dataframe()` function. All you have to do is type a list of variables that you want to include in the data frame. The output is, well, a data frame. So, if I want to store all four variables from my experiment in a data frame called `df` I can do so like this[^note6]:
# 
# [^note6]: Although it really doesn't matter at this point, you may have noticed a new symbol here: the "curly brackets" or "curly braces". Python uses these to indicate yet another variable type: the dictionary. Here we are using the dictionary variable type in passing to feed our lists into a `pandas` dataframe.

# In[6]:


df = pd.DataFrame(
    {'age': age,
     'score': score,
     'rt': rt,
     'group': group
    })


# In[7]:


df


# Note that `df` is a completely self-contained variable. Once you've created it, it no longer depends on the original variables from which it was constructed. That is, if we make changes to the original `age` variable, it will *not* lead to any changes to the age data stored in `df`. 

# (indexing)=
# ### Indexing and slicing
# 
# ADD A SECTION HERE ON HOW INDICES AND SLICES WORK IN PYTHON
# 
# Ok, I still need to finish this section. In the meantime, check out the link below!
# 
# LINK TO: https://docs.python.org/2/tutorial/introduction.html
# 
# "One way to remember how slices work is to think of the indices as pointing between characters, with the left edge of the first character numbered 0. Then the right edge of the last character of a string of n characters has index n, for example:"
# 
# 
# 

# In[29]:


#  +---+---+---+---+---+---+
#  | P | y | t | h | o | n |
#  +---+---+---+---+---+---+
#  0   1   2   3   4   5   6
# -6  -5  -4  -3  -2  -1


# (indexingdataframes)=
# ### Pulling out the contents of a data frame

# Let's take another look at our dataframe. We have created a dataframe called `df`, which contains all of our data for "The Very Exciting Psychology Experiment". Each row contains the data for one participant, so we can see that e.g. the first participant (in row zero, because Python!) was 17 years old, had a score of 12, responded in 3.552 seconds, and was placed in the test group. That's great, but how do we get this information out again? After all, there's no point in storing information if you don't use it, and there's no way to use information if you can't access it. So let's talk a bit about how to pull information out of a data frame. 
# 
# The first thing we might want to do is pull out one of our stored variables, let's say `score`. To access the data in the `score` column by the column name, we can write:

# In[8]:


score_data = df['score']
score_data


# Pretty easy, right? We could also choose to ask for only data from e.g. the first 4 particpants. To do this, we write:

# In[31]:


score_data = df['score'][0:4]
score_data


# As always, we have to be very careful about the numbering, and things are even more confusing than I have let on, because what we are doing here is what Python calls *slicing* the data, and slice numbers work a little differently than index numbers. To get a slice of data from the first to the fourth rows, we need to write `[0:4]`, rather than `[0:3]`. Is this confusing? Yes, I think so! In any case, this is the way Python behaves, and we just need to get used to it. The best way to get the hang of it just to practice slicing a bunch of data, until you learn how to get the results you want.

# What if we want to get data from a row instead? In this case, we will use the `loc` attribute of a `pandas` dataframe, and use a number instead of name (i.e., no quotation marks), like this:

# In[11]:


score_data = df.loc[2]
score_data


# Now we have what we need to get the data for columns and rows. Great! Unfortunately, there is one more thing I should mention[^note7]. If you look at the contents of `score_data` above, you will see that it is still not *just* the data: it also has information about the data, including which column and row it came from. And if we use `type()` to check, we can see that it is yet another variable type: this time, a `pandas.core.series.Series`. Yikes!
# 
# 
# [^note7]: Actually, there are lots more things I should mention, but now is not the time. Working with dataframes takes practice, and there are some catches, but it's worth the effort!

# In[33]:


type(score_data)


# Luckily, it's not too hard to get the raw data out of a `pandas` series. The simplest way is to just turn it into a list variable, using the command `list()`:

# In[34]:


my_row = list(score_data)
my_row


# If you want to get fancy, you can combine these steps, and do it all in one go:

# In[35]:


my_row = list(df.loc[2])
my_column = list(df['score'])
print(my_row)
print(my_column)


# ### Three more dataframe tips for the road
# 
# One problem that sometimes comes up in practice is that you forget what you called all your variables. To get a list of the column names, you can use the command:

# In[13]:


list(df)


# Sometimes dataframes can be very large, and we just want to peek at them, to check what they look like, without data scrolling endlessly over the screen. The dataframe attribute `head` is useful for this. By default it shows the first 5 lines of the dataframe:

# In[37]:


df.head()


# Finally, if you just want to get all of your data out of the dataframe and into a list, then `.values.tolist()` will do the job, giving you a list of lists, with each item in the list containing the data for a single row:

# In[38]:


df.values.tolist()


# ### Looking for more on data frames?
# 
# There's a lot more that can be said about data frames: they're fairly complicated beasts, and the longer you use Python the more important it is to make sure you really understand them. We'll talk a lot more about them in the chapter on [Data Wrangling](datawrangling)
# 
# 
# 
# ## Summary
# 
# This chapter continued where [the previous chapter](getting-started-with-python) left off. The focus was still primarily on introducing basic Python concepts, but this time at least you can see how those concepts are related to data analysis:
# 
# - [Installing and importing libraries](packageinstall). Knowing how to extend the functionality of Python by installing and using libraries is critical to becoming an effective Python user
# - [Loading and saving data](load). Finally, we encountered actual data files. Loading and saving data is obviously a crucial skill, this was dealt with here.
# - [Getting around]. This section dealt very briefly with the concept of filesystems. Mostly, I just told you what a filesystem path is, and left it up to you to figure out how to find paths on your machine.
# - [Useful things to know about variables](useful). In this section, we talked about variable types, with a special focus on lists and dataframes. There is much more to say about these topics, but hopefully this is enough to get you started.
# 
# 
# Taken together, the chapter on [Getting Started with Python](getting-started-with-python) and [More Python Concepts](mechanics) provide enough of a background that you can finally get started doing some statistics! Yes, there's a lot more Python concepts that you ought to know (and we'll talk about some of them in the chapters on [Data Wrangling](datawrangling) and [Basic Programming](programming), but I think that we've talked quite enough about programming for the moment. It's time to see how your experience with programming can be used to do some data analysis...

# In[ ]:




