#!/usr/bin/env python
# coding: utf-8

# (datawrangling)=
# 
# # Data Wrangling

# >*The garden of life never seems to confine itself to the plots philosophers have
# laid out for its convenience. Maybe a few more tractors would do the trick.*
# >
# >--Roger Zelazny [^note1]
# 
# [^note1]: The quote comes from *Home is the Hangman*, published in 1975.]
# 

# This is a somewhat strange chapter, even by my standards. My goal in this chapter is to talk a bit more honestly about the realities of working with data than you'll see anywhere else in the book. The problem with real world data sets is that they are *messy*. Very often the data file that you start out with doesn't have the variables stored in the right format for the analysis you want to do. Sometimes might be a lot of missing values in your data set. Sometimes you only want to analyse a subset of the data. Et cetera. In other words, there's a lot of **_data manipulation_** that you need to do, just to get all your data set into the format that you need it. The purpose of this chapter is to provide a basic introduction to all these pragmatic topics. Although the chapter is motivated by the kinds of practical issues that arise when manipulating real data, I'll stick with the practice that I've adopted through most of the book and rely on very small, toy data sets that illustrate the underlying issue. Because this chapter is essentially a collection of "tricks" and doesn't tell a single coherent story, it may be useful to start with a list of topics:
# 
# - [Dataframes](pandas)
# - [Tabulating data](freqtables)
# - [Transforming or recoding a variable](transform)
# - [Some useful mathematical functions](mathfunc)
# - Section \@ref(subset). Extracting a subset of a vector.
# - Section \@ref(subsetdataframe). Extracting a subset of a data frame.
# - Section \@ref(sort). Sorting, flipping or merging data sets.
# - Section \@ref(reshape). Reshaping a data frame.
# - Section \@ref(textprocessing). Manipulating text.
# - Section \@ref(importing). Opening data from different file types.
# - Section \@ref(coercion). Coercing data from one type to another.
# - Section \@ref(datastructures). Other important data types.
# - Section \@ref(miscdatahandling). Miscellaneous topics.
# 
# As you can see, the list of topics that the chapter covers is pretty broad, and there's a *lot* of content there. Even though this is one of the longest and hardest chapters in the book, I'm really only scratching the surface of several fairly different and important topics. My advice, as usual, is to read through the chapter once and try to follow as much of it as you can. Don't worry too much if you can't grasp it all at once, especially the later sections. The rest of the book is only lightly reliant on this chapter, so you can get away with just understanding the basics. However, what you'll probably find is that later on you'll need to flick back to this chapter in order to understand some of the concepts that I refer to here.

# (pandas)=
# 
# ## Dataframes

# We've already used the `pandas` package [here](descriptives) and [there](DrawingGraphs), and [even over here](loadingcsv), but now it's time to look more closely at `pandas` dataframes. 
# 
# In order to understand why we use dataframes, it helps to try to see what problem the solve. So let's imagine a little scenario in which I collected some data from nine participants. Let's say I divded the participants in two groups ("test" and "control"), and gave them a task. I then recorded their score on the task, as well as the time it took them to complete the task. I also noted down how old they were.
# 
# the data look like this:

# In[1]:


age = [17, 19, 21, 37, 18, 19, 47, 18, 19]
score = [12, 10, 11, 15, 16, 14, 25, 21, 29]
rt = [3.552, 1.624, 6.431, 7.132, 2.925, 4.662, 3.634, 3.635, 5.234]
group = ["test", "test", "test", "test", "test", "control", "control", "control", "control"]


# So there are four variables in active memory: `age`, `rt`, `group` and `score`. And it just so happens that all four of them are the same size (i.e., they're all lists with 9 elements). Aaaand it just so happens that `age[0]` corresponds to the age of the first person, and `rt[0]` is the response time of that very same person, etc. In other words, you and I both know that all four of these variables correspond to the *same* data set, and all four of them are organised in exactly the same way. 
# 
# However, Python *doesn't* know this! As far as it's concerned, there's no reason why the `age` variable has to be the same length as the `rt` variable; and there's no particular reason to think that `age[1]` has any special relationship to `score[1]` any more than it has a special relationship to `score[4]`. In other words, when we store everything in separate variables like this, Python doesn't know anything about the relationships between things. It doesn't even really know that these variables actually refer to a proper data set. The data frame fixes this: if we store our variables inside a data frame, we're telling Python to treat these variables as a single, fairly coherent data set. 
# 
# To see how they do this, let's create one. So how do we create a data frame? One way we've already seen: if we use `pandas` to [import our data from a CSV file](loadingcsv), it will store it as a data frame. A second way is to create it directly from some existing lists using the `pandas.Dataframe()` function. All you have to do is type a list of variables that you want to include in the data frame. The output is, well, a data frame. So, if I want to store all four variables from my experiment in a data frame called `df` I can do so like this[^notedict]:
# 
# [^notedict]: Although it really doesn't matter at this point, you may have noticed a new symbol here: the "curly brackets" or "curly braces". Python uses these to indicate yet another variable type: the dictionary. Here we are using the dictionary variable type in passing to feed our lists into a `pandas` dataframe.

# In[2]:


import pandas as pd

df = pd.DataFrame(
    {'age': age,
     'score': score,
     'rt': rt,
     'group': group
    })


# In[3]:


df


# Note that `df` is a completely self-contained variable. Once you've created it, it no longer depends on the original variables from which it was constructed. That is, if we make changes to the original `age` variable, it will *not* lead to any changes to the age data stored in `df`. 

# (indexingdataframes)=
# ### Pulling out the contents of a data frame

# Let's take another look at our dataframe. We have created a dataframe called `df`, which contains all of our data for "The Very Exciting Psychology Experiment". Each row contains the data for one participant, so we can see that e.g. the first participant (in row zero, because Python!) was 17 years old, had a score of 12, responded in 3.552 seconds, and was placed in the test group. That's great, but how do we get this information out again? After all, there's no point in storing information if you don't use it, and there's no way to use information if you can't access it. So let's talk a bit about how to pull information out of a data frame. 
# 
# The first thing we might want to do is pull out one of our stored variables, let's say `score`. To access the data in the `score` column by the column name, we can write:

# In[4]:


score_data = df['score']
score_data


# Pretty easy, right? We could also choose to ask for only data from e.g. the first 4 particpants. To do this, we write:

# In[5]:


score_data = df['score'][0:4]
score_data


# As always, we have to be very careful about the numbering, and things are even more confusing than I have let on, because what we are doing here is what Python calls *slicing* the data, and slice numbers work a little differently than index numbers. To get a slice of data from the first to the fourth rows, we need to write `[0:4]`, rather than `[0:3]`. Is this confusing? Yes, I think so! In any case, this is the way Python behaves, and we just need to get used to it. The best way to get the hang of it just to practice slicing a bunch of data, until you learn how to get the results you want.

# What if we want to get data from a row instead? In this case, we will use the loc attribute of a pandas dataframe, and use a number instead of name (i.e., no quotation marks), like this:

# In[6]:


score_data = df.loc[2]
score_data


# Now we have what we need to get the data for columns and rows. Great! Unfortunately, there is one more thing I should mention[^note7]. If you look at the contents of score_data above, you will see that it is still not just the data: it also has information about the data, including which column and row it came from. And if we use type() to check, we can see that it is yet another variable type: this time, a pandas.core.series.Series. Yikes!
# [^note7]: Actually, there are lots more things I should mention, but now is not the time. Working with dataframes takes practice, and there are some catches, but it's worth the effort!

# In[7]:


type(score_data)


# Luckily, it's not too hard to get the raw data out of a `pandas` series. The simplest way is to just turn it into a list variable, using the command `list()`:

# In[8]:


my_row = list(score_data)
my_row


# If you want to get fancy, you can combine these steps, and do it all in one go:

# In[9]:


my_row = list(df.loc[2])
my_column = list(df['score'])
print(my_row)
print(my_column)


# ### Some more dataframe tips for the road
# 
# One problem that sometimes comes up in practice is that you forget what you called all your variables. To get a list of the column names, you can use the command:

# In[10]:


list(df)


# Sometimes dataframes can be very large, and we just want to peek at them, to check what they look like, without data scrolling endlessly over the screen. The dataframe attribute head() is useful for this. By default it shows the first 5 lines of the dataframe:

# In[11]:


df.head()


# And if you want to see the last rows of the dataframe? `tail()` has got you covered:

# In[12]:


df.tail()


# Finally, if you just want to get all of your data out of the dataframe and into a list, then .values.tolist() will do the job, giving you a list of lists, with each item in the list containing the data for a single row:

# In[13]:


df.values.tolist()


# (freqtables)=
# 
# ## Tabulating and cross-tabulating data
# 
# A very common task when analysing data is the construction of frequency tables, or cross-tabulation of one variable against another. There are several functions that you can use in Python for that purpose.
# 
# Let's start with a simple example. As the father of a small child, I naturally spend a lot of time watching TV shows like *In the Night Garden*, and I have transcribed a short section of the dialogue. Let's make a `pandas` dataframe with two variables, `speaker` and `utterance`. When we take a look at the data, it becomes very clear what happened to my sanity. 

# In[14]:


import pandas as pd

data = {'speaker':["upsy-daisy",  "upsy-daisy",  "upsy-daisy",  "upsy-daisy",  "tombliboo",   "tombliboo",   "makka-pakka", "makka-pakka",
  "makka-pakka", "makka-pakka"],
       'utterance':["pip", "pip", "onk", "onk", "ee",  "oo",  "pip", "pip", "onk", "onk"]}

df = pd.DataFrame(data, columns=['speaker','utterance'])

df


# With these as my data, one task I might find myself needing to do is construct a frequency count of the number of utterances each character produces during the show. As usual, there are more than one way to achieve this, but the `crosstab` method from `pandas` provides an easy way to do this:

# In[15]:


pd.crosstab(index = df["speaker"], columns = "count")


# The output here tells us on the first line that what we’re looking at is a tabulation of the speaker variable. On the second line it lists all the different speakers that exist in the data, and on the third line it tells you how many times that speaker appears in the data. In other words, it’s a frequency table. Notice that we set the argument `columns` to "count". If instead we want to cross-tabulate the speakers with the utterances, we can set `columns` to the "utterances" column in the dataframe:

# In[16]:


pd.crosstab(index=df["speaker"], columns=df["utterance"],margins=True)


# ### Converting a table of counts to a table of proportions
# 
# The tabulation commands discussed so far all construct a table of raw frequencies: that is, a count of the total number of cases that satisfy certain conditions. However, often you want your data to be organised in terms of proportions rather than counts. This could be as a proportion of the row totals or the column totals. Currently, these are both just called "All", so let's first save the output of our crosstab to a variable, and rename the row and column totals to "rowtotals" and "coltotals".

# In[17]:


tabs = pd.crosstab(index=df["speaker"], columns=df["utterance"],margins=True)

tabs.columns = list(tabs.columns)[0:-1] + ['rowtotals']
tabs.index = list(tabs.index)[0:-1] + ['coltotals']

tabs


# Now we can divide the entire frequency table by the totals in each column:

# In[18]:


tabs/tabs.loc['coltotals']


# The columns sum to one, so we can see that makka-pakka and upsy-daisy each produced 40% of the utterances, while tombliboo only produced 20%. We can also see the proportion of characters associated with each utterance. For instance, whenever the utterance “ee” is made (in this data set), 100% of the time it’s a Tombliboo saying it. 
# 
# The procedure to obtain the row-wise proportion, the procedure is slightly different:

# In[19]:


tabs.div(tabs["rowtotals"], axis=0)


# Each row now sums to one, but that’s not true for each column. What we’re looking at here is the proportions of utterances made by each character. In other words, 50% of Makka-Pakka’s utterances are “pip”, and the other 50% are “onk”.

# (transform)=
# 
# ## Transforming and recoding a variable
# 
# It's not uncommon in real world data analysis to find that one of your variables isn't quite equivalent to the variable that you really want. For instance, it's often convenient to take a continuous-valued variable (e.g., age) and break it up into a smallish number of categories (e.g., younger, middle, older). At other times, you may need to convert a numeric variable into a different numeric variable (e.g., you may want to analyse at the absolute value of the original variable). In this section I'll describe a few key tricks that you can make use of to do this.
# 
# ### Creating a transformed variable
# 
# The first trick to discuss is the idea of **_transforming_** a variable. Taken literally, *anything* you do to a variable is a transformation, but in practice what it usually means is that you apply a relatively simple mathematical function to the original variable, in order to create new variable that either (a) provides a better way of describing the thing you're actually interested in or (b) is more closely in agreement with the assumptions of the statistical tests you want to do.  Since -- at this stage -- I haven't talked about statistical tests or their assumptions, I'll show you an example based on the first case. 
# 
# To keep the explanation simple, the variable we'll try to transform isn't inside a data frame, though in real life it almost certainly would be. However, I think it's useful to start with an example that doesn't use data frames because it illustrates the fact that you already know how to do variable transformations. To see this, let's go through an example. Suppose I've run a short study in which I ask 10 people a single question: 
# 
# >On a scale of 1 (strongly disagree) to 7 (strongly agree), to what extent do you agree with the proposition that "Dinosaurs are awesome"?
# 
# The data look like this:

# In[20]:


data = [1, 7, 3, 4, 4, 4, 2, 6, 5, 5]


# However, if you think about it, this isn't the best way to represent these responses.   Because of the fairly symmetric way that we set up the response scale, there's a sense in which the midpoint of the scale should have been coded as 0 (no opinion), and the two endpoints should be $+3$ (strong agree) and $-3$ (strong disagree). By recoding the data in this way, it's a bit more reflective of how we really think about the responses. The recoding here is trivially easy: we just subtract 4 from the raw scores. Since these data are in a list, we can use a "list comprehension" to step through each element in the list, and subtract 4 from it:

# In[21]:


data = [1, 7, 3, 4, 4, 4, 2, 6, 5, 5]
data = [x-4 for x in data]
data


# If your data is in a `numpy array` rather than a `list`, it is even easier: just subtract 4 from array, and Python takes care of the rest:

# In[22]:


import numpy as np
data = np.array([1, 7, 3, 4, 4, 4, 2, 6, 5, 5])
data = data - 4
data


# One reason why it might be useful to center the data is that there are a lot of situations where you might prefer to analyse the *strength* of the opinion separately from the *direction* of the opinion. We can do two different transformations on this variable in order to distinguish between these two different concepts. Firstly, to compute an `opinion_strength` variable, we want to take the absolute value of the centred data (using the `abs()` function that we've seen previously), like so:

# In[23]:


data = np.array([1, 7, 3, 4, 4, 4, 2, 6, 5, 5])
data = abs(data)
data


# Secondly, to compute a variable that contains only the direction of the opinion and ignores the strength, we can use the `numpy.sign()` method to do this. This method is really simple: all negative numbers are converted to $-1$, all positive numbers are converted to $1$ and zero stays as $0$. So, when we apply `numpy.sign()` to our data we obtain the following:

# In[24]:


data = np.array([1, 7, 3, 4, 4, 4, 2, 6, 5, 5])
data = data - 4
data = np.sign(data)
data


# And we're done. We now have three shiny new variables, all of which are useful transformations of the original likert data. Before moving on, you might be curious to see what these calculations look like if the data had started out in a data frame. So, we can put our data in a dataframe, in a column called "scores"...

# In[25]:


import pandas as pd
df = pd.DataFrame(
    {'scores': np.array([1, 7, 3, 4, 4, 4, 2, 6, 5, 5])
    })

df


# ... and then do some calculations:

# In[26]:


df['centered'] = df['scores']-4
df['opinion_strength'] = abs(df['centered'])
df['opinion_direction'] = np.sign(df['scores']-4)
df


# In other words, even though the data are now columns in a dataframe, we can use exactly the same means to calculate new variable. Even better, we can simply create new columns willy-nilly within the same dataframe, so we can keep everything together, all neat and tidy.

# ### Cutting a numeric variable into categories
# 
# One pragmatic task that arises more often than you'd think is the problem of cutting a numeric variable up into discrete categories. For instance, suppose I'm interested in looking at the age distribution of people at a social gathering:

# In[27]:


#age = [60,58,24,26,34,42,31,30,33,2,9]
import pandas as pd
df = pd.DataFrame(
    {'age': np.array([60,58,24,26,34,42,31,30,33,2,9])
    })

df


# In some situations it can be quite helpful to group these into a smallish number of categories. For example, we could group the data into three broad categories: young (0-20), adult (21-40) and older (41-60). This is a quite coarse-grained classification, and the labels that I've attached only make sense in the context of this data set (e.g., viewed more generally, a 42 year old wouldn't consider themselves as "older").
# 
# As it happens, `pandas` has a convenient method called `cut` for grouping data in this way:

# In[28]:


df['categories'] = pd.cut(x = df['age'], bins = [0,20,40,60], labels = ['young', 'adult', 'older'])
df


# Note that there are four numbers in the `bins` argument, but only three labels in the `labels` argument; this is because the `cut()` function requires that you specify the *edges* of the categories rather than the mid-points. In any case, now that we've done this, we can use the `cut()` function to assign each observation to one of these three categories. There are several arguments to the `cut()` function, but the three that we need to care about are:
# 
# - `x`. The variable that needs to be categorised. 
# - `bins`. This is either a vector containing the locations of the breaks separating the categories, or a number indicating how many categories you want.
# - `labels`. The labels attached to the categories. This is optional: if you don't specify this Python will attach a boring label showing the range associated with each category.

# In the example above, I made all the decisions myself, but if you want to you can delegate a lot of the choices to Python. For instance, if you want you can specify the *number* of categories you want, rather than giving explicit ranges for them, and you can allow Python to come up with some labels for the categories. To give you a sense of how this works, have a look at the following example:

# In[29]:


df['categories'] = pd.cut(x = df['age'], bins = 3)
df


# With this command, I've asked for three categories, but let Python make the choices for where the boundaries should be. All of the important information can be extracted by looking at the tabulated data:

# In[30]:


pd.crosstab(index = df["categories"], columns = "count")


# This output takes a little bit of interpretation, but it's not complicated. What Python has done is determined that the lowest age category should run from 1.94 years up to 21.3 years, the second category should run from 21.3 years to 40.7 years, and so on. These labels are not nearly as easy on the eyes as our "young, adult, and older" categories, so it's usually a good idea to specify your own, meaningful labels to the categories.
# 
# Before moving on, I should take a moment to talk a little about the mechanics of the `cut()` function. Notice that Python has tried to divide the `age` variable into three roughly equal sized bins. Unless you specify the particular breaks you want, that's what it will do. But suppose you want to divide the `age` variable into three categories of different size, but with approximately identical numbers of people. How would you do that? Well, if that's the case, then what you want to do is have the breaks correspond to the 0th, 33rd, 66th and 100th percentiles of the data. One way to do this would be to calculate those values using the `np.quantile()` function and then use those quantiles as input to the `cut()` function. That's pretty easy to do, but it does take a couple of lines to type. So instead, the `pandas` library has a function called `qCut()` that does exactly this:

# In[31]:


df['categories'] = pd.qcut(x = df['age'], q = [0, .33, .66, 1] )
df


# Notice the difference in the boundaries that the `qcut()` method selects. The first and third categories now span an age range of about 25 years each, whereas the middle category has shrunk to a span of only 6 years. There are some situations where this is genuinely what you want (that's why I wrote the function!), but in general you should be careful. Usually the numeric variable that you're trying to cut into categories is already expressed in meaningful units (i.e., it's interval scale), but if you cut it into unequal bin sizes then it's often very difficult to attach meaningful interpretations to the resulting categories. 
# 
# More generally, regardless of whether you're using the original `cut()` method or the `qcut()` version, it's important to take the time to figure out whether or not the resulting categories make any sense at all in terms of your research project. If they don't make any sense to you as meaningful categories, then any data analysis that uses those categories is likely to be just as meaningless. More generally, in practice I've noticed that people have a very strong desire to carve their (continuous and messy) data into a few (discrete and simple) categories; and then run analysis using the categorised data instead of the original one.[^note2] I wouldn't go so far as to say that this is an inherently bad idea, but it does have some fairly serious drawbacks at times, so I would advise some caution if you are thinking about doing it. 
# 
# [^note2]: If you've read further into the book, and are re-reading this section, then a good example of this would be someone choosing to do an ANOVA using age categories as the grouping variable, instead of running a regression using `age` as a predictor. There are sometimes good reasons for do this: for instance, if the relationship between `age` and your outcome variable is highly non-linear, and you aren't comfortable with trying to run non-linear regression! However, unless you really do have a good rationale for doing this, it's best not to. It tends to introduce all sorts of other problems (e.g., the data will probably violate the normality assumption), and you can lose a lot of power.

# (mathfunc)=
# 
# ## A few more mathematical functions and operations

# In[ ]:




