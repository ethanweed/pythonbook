#!/usr/bin/env python
# coding: utf-8

# (regression)=
# # Linear regression

# 
# 
# The goal in this chapter is to introduce **_linear regression_**. Stripped to its bare essentials, linear regression models are basically a slightly fancier version of the [Pearson correlation](correl), though as we'll see, regression models are much more powerful tools.

# Since the basic ideas in regression are closely tied to correlation, we'll return to the `parenthood.csv` file that we were using to illustrate how correlations work. Recall that, in this data set, we were trying to find out why Dan is so very grumpy all the time, and our working hypothesis was that I'm not getting enough sleep. 

# In[1]:


import pandas as pd

file = 'https://raw.githubusercontent.com/ethanweed/pythonbook/main/Data/parenthood.csv'
df = pd.read_csv(file)

df.head()


# We drew some scatterplots to help us examine the relationship between the amount of sleep I get, and my grumpiness the following day. 

# In[2]:


from myst_nb import glue
import seaborn as sns
sns.set_context("notebook", font_scale=1.5)
ax = sns.scatterplot(data = df,
                x = 'dan_sleep', 
                y = 'dan_grump')
ax.set(title = 'Grumpiness and sleep', ylabel = 'My grumpiness (0-100)', xlabel='My sleep (hours)')
sns.despine()

glue("sleepycorrelation_fig", ax, display=False)


#  ```{glue:figure} sleepycorrelation-fig
# :figwidth: 600px
# :name: fig-sleepycorrelation
# 
# Scatterplot showing grumpiness as a function of hours slept.
# 
# ```
# 

# The actual scatterplot that we draw is the one shown in {numref}`fig-sleepycorrelation`, and as we saw previously this corresponds to a correlation of $r=-.90$, but what we find ourselves secretly imagining is something that looks closer to the left panel in {numref}`fig-sleep_regressions_1`. That is, we mentally draw a straight line through the middle of the data. In statistics, this line that we're drawing is called a **_regression line_**. Notice that -- since we're not idiots -- the regression line goes through the middle of the data. We don't find ourselves imagining anything like the rather silly plot shown in the right panel in {numref}`fig-sleep_regressions_1`. 

# In[3]:


import numpy as np 
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# find the regression coefficients to allow manually plotting the line
model = smf.ols(formula="dan_grump ~ dan_sleep", data=df).fit()
intercept = model.params.Intercept
slope = model.params.dan_sleep


fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=True)

x = np.linspace(4,10)


sns.scatterplot(data = df, x = 'dan_sleep', y = 'dan_grump', ax = axes[0])
fig.axes[0].set_title("The best-fitting regression line")
fig.axes[0].set_xlabel("My sleep (hours)")
fig.axes[0].set_ylabel("My grumpiness (0-10)")
fig.axes[0].plot(x,slope*x+intercept)

sns.scatterplot(data = df, x = 'dan_sleep', y = 'dan_grump', ax = axes[1])
fig.axes[1].set_title("Not the best-fitting regression line!")
fig.axes[1].set_xlabel("My sleep (hours)")
fig.axes[1].set_ylabel("My grumpiness (0-10)")
fig.axes[1].plot(x,-3*x+80)

sns.despine()

#glue("sleep_regressions_1-fig", fig, display=False)


#  ```{glue:figure} sleep_regressions_1-fig
# :figwidth: 600px
# :name: fig-sleep_regressions_1
# 
# The panel to the left shows the sleep-grumpiness scatterplot from {numref}`fig-sleepycorrelation` with the best fitting regression line drawn over the top. Not surprisingly, the line goes through the middle of the data. In contrast, the panel to the right shows the same data, but with a very poor choice of regression line drawn over the top.
# 
# ```
# 

# This is not highly surprising: the line that I've drawn in panel to the right doesn't "fit" the data very well, so it doesn't make a lot of sense to propose it as a way of summarising the data, right? This is a very simple observation to make, but it turns out to be very powerful when we start trying to wrap just a little bit of maths around it. To do so, let's start with a refresher of some high school maths. The formula for a straight line is usually written like this:
# 
# $$
# y = mx + c
# $$ 
# 
# 
# Or, at least, that's what it was when I went to high school all those years ago. The two *variables* are $x$ and $y$, and we have two *coefficients*, $m$ and $c$. The coefficient $m$ represents the *slope* of the line, and the coefficient $c$ represents the *$y$-intercept* of the line. Digging further back into our decaying memories of high school (sorry, for some of us high school was a long time ago), we remember that the intercept is interpreted as "the value of $y$ that you get when $x=0$". Similarly, a slope of $m$ means that if you increase the $x$-value by 1 unit, then the $y$-value goes up by $m$ units; a negative slope means that the $y$-value would go down rather than up. Ah yes, it's all coming back to me now. 
# 
# Now that we've remembered that, it should come as no surprise to discover that we use the exact same formula to describe a regression line. If $Y$ is the outcome variable (the DV) and $X$ is the predictor variable (the IV), then the formula that describes our regression is written like this:
# 
# $$
# \hat{Y_i} = b_1 X_i + b_0
# $$
# 
# Hm. Looks like the same formula, but there's some extra frilly bits in this version. Let's make sure we understand them. Firstly, notice that I've written $X_i$ and $Y_i$ rather than just plain old $X$ and $Y$. This is because we want to remember that we're dealing with actual data. In this equation, $X_i$ is the value of predictor variable for the $i$th observation (i.e., the number of hours of sleep that I got on day $i$ of my little study), and $Y_i$ is the corresponding value of the outcome variable (i.e., my grumpiness on that day). And although I haven't said so explicitly in the equation, what we're assuming is that this formula works for all observations in the data set (i.e., for all $i$). Secondly, notice that I wrote $\hat{Y}_i$ and not $Y_i$. This is because we want to make the distinction between the *actual data* $Y_i$, and the *estimate* $\hat{Y}_i$ (i.e., the prediction that our regression line is making). Thirdly, I changed the letters used to describe the coefficients from $m$ and $c$ to $b_1$ and $b_0$. That's just the way that statisticians like to refer to the coefficients in a regression model. I've no idea why they chose $b$, but that's what they did. In any case $b_0$ always refers to the intercept term, and $b_1$ refers to the slope.
# 
# 
# Excellent, excellent. Next, I can't help but notice that -- regardless of whether we're talking about the good regression line or the bad one -- the data don't fall perfectly on the line. Or, to say it another way, the data $Y_i$ are not identical to the predictions of the regression model $\hat{Y_i}$. Since statisticians love to attach letters, names and numbers to everything, let's refer to the difference between the model prediction and that actual data point as a *residual*, and we'll refer to it as $\epsilon_i$.[^noteepsilon] Written using mathematics, the residuals are defined as:
# 
# $$
# \epsilon_i = Y_i - \hat{Y}_i
# $$
# 
# which in turn means that we can write down the complete linear regression model as:
# 
# $$
# Y_i = b_1 X_i + b_0 + \epsilon_i
# $$
# 
# [^noteepsilon]: The $\epsilon$ symbol is the Greek letter epsilon. It's traditional to use $\epsilon_i$ or $e_i$ to denote a residual.

# (regressionestimation)=
# ## Estimating a linear regression model
# 
# 
# Okay, now let's redraw our pictures, but this time I'll add some lines to show the size of the residual for all observations. When the regression line is good, our residuals (the lengths of the solid black lines) all look pretty small, as shown in the left panel of {numref}`fig-sleep_regressions_2`, but when the regression line is a bad one, the residuals are a lot larger, as you can see from looking at the right panel of {numref}`fig-sleep_regressions_2`. Hm. Maybe what we "want" in a regression model is *small* residuals. Yes, that does seem to make sense. In fact, I think I'll go so far as to say that the "best fitting" regression line is the one that has the smallest residuals. Or, better yet, since statisticians seem to like to take squares of everything why not say that ...
# 
# > The estimated regression coefficients, $\hat{b}_0$ and $\hat{b}_1$ are those that minimise the sum of the squared residuals, which we could either write as $\sum_i (Y_i - \hat{Y}_i)^2$ or as $\sum_i {\epsilon_i}^2$.
# 
# Yes, yes that sounds even better. And since I've indented it like that, it probably means that this is the right answer. And since this is the right answer, it's probably worth making a note of the fact that our regression coefficients are *estimates* (we're trying to guess the parameters that describe a population!), which is why I've added the little hats, so that we get $\hat{b}_0$ and $\hat{b}_1$ rather than $b_0$ and $b_1$. Finally, I should also note that -- since there's actually more than one way to estimate a regression model -- the more technical name for this estimation process is **_ordinary least squares (OLS) regression_**.  
# 
# At this point, we now have a concrete definition for what counts as our "best" choice of regression coefficients, $\hat{b}_0$ and $\hat{b}_1$. The natural question to ask next is,  if our optimal regression coefficients are those that minimise the sum squared residuals, how do we *find* these wonderful numbers? The actual answer to this question is complicated, and it doesn't help you understand the logic of regression.[^notekungfu] As a result, this time I'm going to let you off the hook. Instead of showing you how to do it the long and tedious way first, and then "revealing" the wonderful shortcut that Python provides you with, let's cut straight to the chase... and use Python to do all the heavy lifting. 
# 
# 
# [^notekungfu]: Or at least, I'm assuming that it doesn't help most people. But on the off chance that someone reading this is a proper kung fu master of linear algebra (and to be fair, I always have a few of these people in my intro stats class), it *will* help *you* to know that the solution to the estimation problem turns out to be $\hat{b} = (X^TX)^{-1} X^T y$, where $\hat{b}$ is a vector containing the estimated regression coefficients,  $X$ is the "design matrix" that contains the predictor variables (plus an additional column containing all ones; strictly $X$ is a matrix of the regressors, but I haven't discussed the distinction yet), and $y$ is a vector containing the outcome variable. For everyone else, this isn't exactly helpful, and can be downright scary. However, since quite a few things in linear regression can be written in linear algebra terms, you'll see a bunch of footnotes like this one in this chapter. If you can follow the maths in them, great. If not, ignore it.

# In[4]:


import numpy, scipy, matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xData = df['dan_sleep']
yData = numpy.array(df['dan_grump'])

# (the solution to this figure stolen shamelessly from this stack-overflow answer by James Phillips:
# https://stackoverflow.com/questions/53779773/python-linear-regression-best-fit-line-with-residuals)

# fit linear regression model and save parameters
def func(x, a, b):
    return a * x + b

initialParameters = numpy.array([1.0, 1.0])

fittedParameters, pcov = curve_fit(func, xData, yData, initialParameters)

modelPredictions = func(xData, *fittedParameters) 

data = pd.DataFrame({'x': xData,
                     'y': yData})

# plot data points
fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
sns.scatterplot(data = data, x = 'x', y = 'y', ax = axes[0])
fig.axes[0].set_title("The best-fitting regression line!")
fig.axes[0].set_xlabel("My sleep (hours)")
fig.axes[0].set_ylabel("My grumpiness (0-10)")

# add regression line
xModel = numpy.linspace(min(xData), max(xData))
yModel = func(xModel, *fittedParameters)

axes[0].plot(xModel, yModel)

# add drop lines
for i in range(len(xData)):
    lineXdata = (xData[i], xData[i]) # same X
    lineYdata = (yData[i], modelPredictions[i]) # different Y
    axes[0].plot(lineXdata, lineYdata)

    
#####

# create poor-fitting model
badParameters = np.array([-3, 80])
badPredictions = func(xData, *badParameters) 

bad_xModel = numpy.linspace(min(xData), max(xData))
bad_yModel = func(bad_xModel, *badParameters)

# plot data with poor-fitting model
sns.scatterplot(data = data, x = 'x', y = 'y', ax = axes[1])
fig.axes[1].set_title("Not the best-fitting regression line!")
fig.axes[1].set_xlabel("My sleep (hours)")
fig.axes[1].set_ylabel("My grumpiness (0-10)")
fig.axes[1].plot(bad_xModel, bad_yModel)  

# add drop lines
for i in range(len(xData)):
    lineXdata = (xData[i], xData[i]) 
    lineYdata = (yData[i], badPredictions[i]) 
    axes[1].plot(lineXdata, lineYdata)
  
    
sns.despine()


#  ```{glue:figure} sleep_regressions_2-fig
# :figwidth: 600px
# :name: fig-sleep_regressions_2
# 
# A depiction of the residuals associated with the best fitting regression line (left panel), and the residuals associated with a poor regression line (right panel). The residuals are much smaller for the good regression line. Again, this is no surprise given that the good line is the one that goes right through the middle of the data.
# 
# ```

# (pingouinregression)=
# ## Linear Regression with Python
# 
# As always, there are several different ways we could go about calculating a linear regression in Python, but we'll stick with `pingouin`, which for my money is one of the simplest and easiest packages to use. The `pingouin` command for linear regression is, well, `linear_regression`, so that couldn't be much more straightforward. After that, we just need to tell `pinguoin` which variable we want to use as a predictor variable (independent variable), and which one we want to use as the outcome variable (dependent variable). `pingouin` wants the predictor variable first, so, since we want to model my grumpiness as a function of my sleep, we write:

# In[5]:


import pingouin as pg

mod1 = pg.linear_regression(df['dan_sleep'], df['dan_grump'])


# In[6]:


# Display results, rounded to two decimal places.
mod1.round(2)


# As is its way, `pingouin` gives us a nice simple table, with a lot of information. Most importantly for now, we can see that `pingouin` has caclulated the intercept $\hat{b}_0 = 125.96$ and the slope $\hat{b}_1 = -8.94$. In other words, the best-fitting regression line that I plotted in {numref}`fig-sleep_regressions_1` has this formula: 
# 
# $$
# \hat{Y}_i = -8.94 \ X_i + 125.96
# $$ 

# ### Warning!!!
# 
# Remember, it's critical that you put the variables in the right order. If you reverse the predictor and outcome variables, `pinguoin` will happily calculate a result for you, but it will not be the one you are looking for. If instead, we had written `pg.linear_regression(df['dan_grump'], df['dan_sleep'])`, we would get the following:

# In[7]:


modx = pg.linear_regression(df['dan_grump'], df['dan_sleep'])
modx.round(2)


# The output looks valid enough on the face of it, and it is even statistically significant. But in this model, we just predicted my son's sleepiness as a function of my grumpiness, which is madness! Reversing the direction of causality would make a great scifi movie[^noteNolan], but it's no good in statistics. So remember, predictor first, outcome second[^noteformula]
# 
# [^noteNolan]: Christopher Nolan, have your people call my people if you're interested, we'll do lunch!
# [^noteformula]: This is extra confusing if you happen to have come from the world of R, where this sort of model is usually defined with a formula, in which the outcome measure comes first, followed by the predictor(s), or even if you have used `statsmodels`, which also preserves the R-style formula notation.

# ### Interpreting the estimated model
# 
# The most important thing to be able to understand is how to interpret these coefficients. Let's start with $\hat{b}_1$, the slope. If we remember the definition of the slope, a regression coefficient of $\hat{b}_1 = -8.94$ means that if I increase $X_i$ by 1, then I'm decreasing $Y_i$ by 8.94. That is, each additional hour of sleep that I gain will improve my mood, reducing my grumpiness by 8.94 grumpiness points. What about the intercept? Well, since $\hat{b}_0$ corresponds to "the expected value of $Y_i$ when $X_i$ equals 0", it's pretty straightforward. It implies that if I get zero hours of sleep ($X_i =0$) then my grumpiness will go off the scale, to an insane value of ($Y_i = 125.96$). Best to be avoided, I think.
# 

# (multipleregression)=
# ## Multiple linear regression
# 
# The simple linear regression model that we've discussed up to this point assumes that there's a single predictor variable that you're interested in, in this case `dan_sleep`. In fact, up to this point, *every* statistical tool that we've talked about has assumed that your analysis uses one predictor variable and one outcome variable. However, in many (perhaps most) research projects you actually have multiple predictors that you want to examine. If so, it would be nice to be able to extend the linear regression framework to be able to include multiple predictors. Perhaps some kind of **_multiple regression_** model would be in order?
# 
# Multiple regression is conceptually very simple. All we do is add more terms to our regression equation. Let's suppose that we've got two variables that we're interested in; perhaps we want to use both `dan_sleep` and `baby_sleep` to predict the `dan_grump` variable. As before, we let $Y_i$ refer to my grumpiness on the $i$-th day. But now we have two $X$ variables: the first corresponding to the amount of sleep I got and the second corresponding to the amount of sleep my son got. So we'll let $X_{i1}$ refer to the hours I slept on the $i$-th day, and $X_{i2}$ refers to the hours that the baby slept on that day. If so, then we can write our regression model like this:
# 
# $$
# Y_i = b_2 X_{i2} + b_1 X_{i1} + b_0 + \epsilon_i
# $$

# As before, $\epsilon_i$ is the residual associated with the $i$-th observation, $\epsilon_i = {Y}_i - \hat{Y}_i$. In this model, we now have three coefficients that need to be estimated: $b_0$ is the intercept, $b_1$ is the coefficient associated with my sleep, and $b_2$ is the coefficient associated with my son's sleep. However, although the number of coefficients that need to be estimated has changed, the basic idea of how the estimation works is unchanged: our estimated coefficients $\hat{b}_0$, $\hat{b}_1$ and $\hat{b}_2$ are those that minimise the sum squared residuals. 

# (pingouinmultiplelinearregression)=
# ## Multiple Linear Regression in Python
# 
# Doing mulitiple linear regression in `pingouin` is just as easy as adding some more predictor variables, like this:

# In[8]:


mod2 = pg.linear_regression(df[['dan_sleep', 'baby_sleep']], df['dan_grump'])


# Still, there is one thing to watch out for. If you look carefully at the command above, you will notice that not only have we added a new predictor (`baby_sleep`), we have also added some extra brackets. While before our predictor variable was `['dan_sleep']`, now we have `[['dan_sleep', 'baby_sleep']]`. Why the extra set of `[]`?
# 
# This is because we are using the brackets in two different ways. When we wrote `['dan_sleep']`, the square brackets mean "select the column with the header 'dan_sleep'". But now we are giving `pingouin` a _list_ of columns to select, and `list` objects are _also_ defined by square brackets in Python. To keep things clear, another way to achieve the same result would be to define the list of predictor variables outside the call to `pingouin`:

# In[9]:


predictors = ['dan_sleep', 'baby_sleep']
outcome = 'dan_grump'

mod2 = pg.linear_regression(df[predictors], df[outcome])


# You could do all the work outside of `pinguoin`, like this:

# In[10]:


predictors = df[['dan_sleep', 'baby_sleep']]
outcome = df['dan_grump']

mod2 = pg.linear_regression(predictors, outcome)


# All three of these will give the same result, so it's up to you choose what makes most sense to you. But now it's time to take a look at the results:

# In[11]:


mod2.round(2)


# The coefficient associated with dan_sleep is quite large, suggesting that every hour of sleep I lose makes me a lot grumpier. However, the coefficient for baby_sleep is very small, suggesting that it doesn’t really matter how much sleep my son gets; not really. What matters as far as my grumpiness goes is how much sleep I get. To get a sense of what this multiple regression model looks like, {numref}`fig-sleep_regressions_3d` shows a 3D plot that plots all three variables, along with the regression model itself.

# In[12]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# style the plot
sns.set_style("whitegrid")

# construct 3d plot space
fig = plt.figure(figsize=(25, 10)) 
ax = fig.add_subplot(111, projection = '3d')

# define axes
x = df['dan_sleep']
y = df['baby_sleep']
z = df['dan_grump']

# set axis labels
ax.set_xlabel("dan_sleep")
ax.set_ylabel("baby_sleep")
ax.set_zlabel("dan_grump")


# get intercept and regression coefficients from the lmm model
coefs = list(mod2['coef'][1:])
intercept = mod2['coef'][0]

# create a 3d plane representation of the lmm predictions
xs = np.tile(np.arange(12), (12,1))
ys = np.tile(np.arange(12), (12,1)).T
zs = xs*coefs[0]+ys*coefs[1]+intercept
ax.plot_surface(xs,ys,zs, alpha=0.5)

# plot the data and plane
ax.plot_surface(xs,ys,zs, alpha=0.01)
ax.scatter(x, y, z, color = 'blue')

# adjust the viewing angle
ax.view_init(11,97)







#  ```{glue:figure} sleep_regressions_3d-fig
# :figwidth: 600px
# :name: fig-sleep_regressions_3d
# 
# A 3D visualisation of a multiple regression model. There are two predictors in the model, `dan_sleep` and `baby_sleep`; the outcome variable is `dan.grump`. Together, these three variables form a 3D space: each observation (blue dots) is a point in this space. In much the same way that a simple linear regression model forms a line in 2D space, this multiple regression model forms a plane in 3D space. When we estimate the regression coefficients, what we're trying to do is find a plane that is as close to all the blue dots as possible.
# 
# ```

# ### Formula for the general case
# 
# The equation that I gave above shows you what a multiple regression model looks like when you include two predictors. Not surprisingly, then, if you want more than two predictors all you have to do is add more $X$ terms and more $b$ coefficients. In other words, if you have $K$ predictor variables in the model then the regression equation looks like this:
# 
# $$
# Y_i = \left( \sum_{k=1}^K b_{k} X_{ik} \right) + b_0 + \epsilon_i
# $$

# (r2)=
# ## Quantifying the fit of the regression model
# 
# So we now know how to estimate the coefficients of a linear regression model. The problem is, we don't yet know if this regression model is any good. For example, the `lm` model *claims* that every hour of sleep will improve my mood by quite a lot, but it might just be rubbish. Remember, the regression model only produces a prediction $\hat{Y}_i$ about what my mood is like: my actual mood is $Y_i$. If these two are very close, then the regression model has done a good job. If they are very different, then it has done a bad job. 

# ### The $R^2$ value
# 
# Once again, let's wrap a little bit of mathematics around this. Firstly, we've got the sum of the squared residuals:
# 
# $$
# \mbox{SS}_{res} = \sum_i (Y_i - \hat{Y}_i)^2
# $$

# which we would hope to be pretty small. Specifically, what we'd like is for it to be very small in comparison to the total variability in the outcome variable, 
# 
# $$
# \mbox{SS}_{tot} = \sum_i (Y_i - \bar{Y})^2
# $$

# While we're here, let's calculate these values in Python. Firstly, in order to make my Python commands look a bit more similar to the mathematical equations, I'll create variables `X` and `Y`:

# In[13]:


X = df['dan_sleep'] # the predictor
Y = df['dan_grump'] # the outcome


# First, lets just examine the output for the simple model that uses only a single predictor:

# In[14]:


mod1 = pg.linear_regression(X, Y)
mod1.round(2)


# In this output, we can see that Python has calculated an intercept of 125.96 and a regression coefficient ($beta$) of -8.94. So for every hour of sleep I get, the model estimates that this will correspond to a decrease in grumpiness of about 9 on my incredibly scientific grumpiness scale. We can use this information to calculate $\hat{Y}$, that is, the values that the model _predicts_ for the outcome measure, as opposed to $Y$, which are the actual data we observed. So, for each value of the predictor variable X, we multiply that value by the regression coefficient -8.84, and add the intercept 125.97:

# In[15]:



Y_pred = -8.94 * X + 125.97


# Okay, now that we've got a variable which stores the regression model predictions for how grumpy I will be on any given day, let's calculate our sum of squared residuals. We would do that using the following command:

# In[16]:


SS_resid = sum( (Y - Y_pred)**2 )
SS_resid


# Wonderful. A big number that doesn't mean very much. Still, let's forge boldly onwards anyway, and calculate the total sum of squares as well. That's also pretty simple:

# In[17]:


import numpy as np
SS_tot = sum( (Y - np.mean(Y))**2 )
SS_tot


# 
# Hm. Well, it's a much bigger number than the last one, so this does suggest that our regression model was making good predictions. But it's not very interpretable. 
# 
# Perhaps we can fix this. What we'd like to do is to convert these two fairly meaningless numbers into one number. A nice, interpretable number, which for no particular reason we'll call $R^2$. What we would like is for the value of $R^2$ to be equal to 1 if the regression model makes no errors in predicting the data. In other words, if it turns out that the residual errors are zero, that is, if $\mbox{SS}_{res} = 0$, then we expect $R^2 = 1$. Similarly, if the model is completely useless, we would like $R^2$ to be equal to 0. What do I mean by "useless"? Tempting as it is demand that the regression model move out of the house, cut its hair and get a real job, I'm probably going to have to pick a more practical definition: in this case, all I mean is that the residual sum of squares is no smaller than the total sum of squares, $\mbox{SS}_{res} = \mbox{SS}_{tot}$. Wait, why don't we do exactly that? The formula that provides us with out $R^2$ value is pretty simple to write down,
# 
# $$
# R^2 = 1 - \frac{\mbox{SS}_{res}}{\mbox{SS}_{tot}}
# $$

# and equally simple to calculate in Python:

# In[18]:


R2 = 1- (SS_resid / SS_tot)
R2


# The $R^2$ value, sometimes called the **_coefficient of determination_**[^notenever] has a simple interpretation: it is the *proportion* of the variance in the outcome variable that can be accounted for by the predictor. So in this case, the fact that we have obtained $R^2 = .816$ means that the predictor (`my.sleep`) explains 81.6\% of the variance in the outcome (`my.grump`). 
# 
# Naturally, you don't actually need to type in all these commands yourself if you want to obtain the $R^2$ value for your regression model. And as you have probably already noticed, `pingouin` calculates $R^2$  for us without even being asked to. But there's another property of $R^2$ that I want to point out. 
# 
# [^notenever]: And by "sometimes" I mean "almost never". In practice everyone just calls it "$R$-squared".

# ### The relationship between regression and correlation
# 
# At this point we can revisit my earlier claim that regression, in this very simple form that I've discussed so far, is basically the same thing as a correlation. Previously, we used the symbol $r$ to denote a Pearson correlation. Might there be some relationship between the value of the correlation coefficient $r$ and the $R^2$ value from linear regression? Of course there is: the squared correlation $r^2$ is identical to the $R^2$ value for a linear regression with only a single predictor. To illustrate this, here's the squared correlation:

# In[19]:


r = X.corr(Y)  # calculate the correlation
r**2    # print the squared correlation


# 
# Yep, same number. In other words, running a Pearson correlation is more or less equivalent to running a linear regression model that uses only one predictor variable.
# 
# ### The adjusted $R^2$ value
# 
# One final thing to point out before moving on. It's quite common for people to report a slightly different measure of model performance, known as "adjusted $R^2$". The motivation behind calculating the adjusted $R^2$ value is the observation that adding more predictors into the model will *always* cause the $R^2$ value to increase (or at least not decrease). The adjusted $R^2$ value introduces a slight change to the calculation, as follows. For a regression model with $K$ predictors, fit to a data set containing $N$ observations, the adjusted $R^2$ is:
# 
# $$
# \mbox{adj. } R^2 = 1 - \left(\frac{\mbox{SS}_{res}}{\mbox{SS}_{tot}} \times \frac{N-1}{N-K-1} \right)
# $$

# This adjustment is an attempt to take the degrees of freedom into account. The big advantage of the adjusted $R^2$ value is that when you add more predictors to the model, the adjusted $R^2$ value will only increase if the new variables improve the model performance more than you'd expect by chance. The big disadvantage is that the adjusted $R^2$ value *can't* be interpreted in the elegant way that $R^2$ can. $R^2$ has a simple interpretation as the proportion of variance in the outcome variable that is explained by the regression model; to my knowledge, no equivalent interpretation exists for adjusted $R^2$. 
# 
# An obvious question then, is whether you should report $R^2$ or adjusted $R^2$. This is probably a matter of personal preference. If you care more about interpretability, then $R^2$ is better. If you care more about correcting for bias, then adjusted $R^2$ is probably better. Speaking just for myself, I prefer $R^2$: my feeling is that it's more important to be able to interpret your measure of model performance. Besides, as we'll soon see in the section on [hypothesis tests for regression models](regressiontests), if you're worried that the improvement in $R^2$ that you get by adding a predictor is just due to chance and not because it's a better model, well, we've got hypothesis tests for that. 

# (regressiontests)=
# ## Hypothesis tests for regression models
# 
# So far we've talked about what a regression model is, how the coefficients of a regression model are estimated, and how we quantify the performance of the model (the last of these, incidentally, is basically our measure of effect size). The next thing we need to talk about is hypothesis tests. There are two different (but related) kinds of hypothesis tests that we need to talk about: those in which we test whether the regression model as a whole is performing significantly better than a null model; and those in which we test whether a particular regression coefficient is significantly different from zero. 
# 
# At this point, you're probably groaning internally, thinking that I'm going to introduce a whole new collection of tests. You're probably sick of hypothesis tests by now, and don't want to learn any new ones. Me too. I'm so sick of hypothesis tests that I'm going to shamelessly reuse the $F$-test from the [chapter on ANOVAs](anova) and the $t$-test from [the chapter on t-tests](ttest). In fact, all I'm going to do in this section is show you how those tests are imported wholesale into the regression framework.  

# ### Testing the model as a whole
# 
# Okay, suppose you've estimated your regression model. The first hypothesis test you might want to try is one in which the null hypothesis that there is *no relationship* between the predictors and the outcome, and the alternative hypothesis is that *the data are distributed in exactly the way that the regression model predicts*. Formally, our "null model" corresponds to the fairly trivial "regression" model in which we include 0 predictors, and only include the intercept term $b_0$
# 
# $$
# H_0: Y_i = b_0 + \epsilon_i
# $$

# If our regression model has $K$ predictors, the "alternative model" is described using the usual formula for a multiple regression model:
# 
# $$
# H_1: Y_i = \left( \sum_{k=1}^K b_{k} X_{ik} \right) + b_0 + \epsilon_i
# $$

# How can we test these two hypotheses against each other? The trick is to understand that just like we did with ANOVA, it's possible to divide up the total variance $\mbox{SS}_{tot}$ into the sum of the residual variance $\mbox{SS}_{res}$ and the regression model variance $\mbox{SS}_{mod}$. I'll skip over the technicalities, since we covered most of them in the [ANOVA chapter](anova), and just note that:
# 
# $$
# \mbox{SS}_{mod} = \mbox{SS}_{tot} - \mbox{SS}_{res}
# $$

# And, just like we did with the ANOVA, we can convert the sums of squares into mean squares by dividing by the degrees of freedom. 
# 
# $$
# \begin{array}{rcl}
# \mbox{MS}_{mod} &=& \displaystyle\frac{\mbox{SS}_{mod} }{df_{mod}} \\ \\
# \mbox{MS}_{res} &=& \displaystyle\frac{\mbox{SS}_{res} }{df_{res} }
# \end{array}
# $$

# So, how many degrees of freedom do we have? As you might expect, the $df$ associated with the model is closely tied to the number of predictors that we've included. In fact, it turns out that $df_{mod} = K$. For the residuals, the total degrees of freedom is $df_{res} = N -K - 1$. 
# 
# Now that we've got our mean square values, you're probably going to be entirely unsurprised (possibly even bored) to discover that we can calculate an $F$-statistic like this:
# 
# $$
# F =  \frac{\mbox{MS}_{mod}}{\mbox{MS}_{res}}
# $$

# and the degrees of freedom associated with this are $K$ and $N-K-1$. This $F$ statistic has exactly the same interpretation as the one we introduced [when learning about ANOVAs](anova). Large $F$ values indicate that the null hypothesis is performing poorly in comparison to the alternative hypothesis.

# "Ok, this is fine", I hear you say, "but now show me the easy way! Show me how easy it is to get an $F$ statistic from `pingouin`! `pingouin` makes everything so much easier! Surely `pingouin` does this for me as well?"
# 
# Yeah. About that... actually, as of the time of writing (Tuesday the 17th of May, 2022), `pingouin` does _not_ automatically calculate the $F$ statistic for the model for you. This seems like kind of a strange omission to me, since it is pretty normal to report overall $F$ and $p$ values for a model, and `pingouin` seems to be all about making the normal things easy. So, I can only assume this will get added at some point, but for now, sadly, we are left to ourselves on this one. 
# 
# I should mention that there are other statistics packages for Python that will do this for you. [statsmodels](https://www.statsmodels.org/stable/regression.html) comes to mind, for instance. But this is opening a whole new can of worms that I'd rather avoid for now, so instead I provide you with code to calculate the $F$ statistic and $p$-value for the model "manually" below:

# In[20]:


import numpy as np
from scipy import stats as st

# your predictor and outcome variables (aka, "the data")
predictors = df[['dan_sleep', 'baby_sleep']]
outcome = df['dan_grump']

# model the data, and store the model information in a variable called "mod"
mod = pg.linear_regression(predictors, outcome)


# call the outcome data "Y", just for the sake of generalizability
Y = outcome

# get the model residuals from the model object
res = mod.residuals_

# calculate the residual, the model, and the total sums of squares
SS_res = np.sum(np.square(res))
SS_tot = sum( (Y - np.mean(Y))**2 )
SS_mod = SS_tot - SS_res

# get the degrees of freedom for the model and the residuals
df_mod = mod.df_model_
df_res = mod.df_resid_

# caluculate the mean squares for the model and the residuals
MS_mod = SS_mod / df_mod
MS_res = SS_res / df_res

# calculate the F-statistic
F = MS_mod / MS_res

# estimate the p-value
p = st.f.sf(F, df_mod, df_res)

# display the results
print("F=",F, "p=", p)


# ### An F-test function
# 
# A more compact way to do this would be to take everything I have done above and put it inside a function. I've done this below, not least so that I will be able to copy/paste from it myself at some later date. Here is a function called `regression_f` that takes as its arguments a list of predictors, and an outcome variable, and spits out the $F$ and $p$ values.

# In[21]:


def regression_f(predictors, outcome):
    mod = pg.linear_regression(predictors, outcome)
    Y = outcome
    res = mod.residuals_
    SS_res = np.sum(np.square(res))
    SS_tot = sum( (Y - np.mean(Y))**2 )
    SS_mod = SS_tot - SS_res
    df_mod = mod.df_model_
    df_res = mod.df_resid_
    MS_mod = SS_mod / df_mod
    MS_res = SS_res / df_res
    F = MS_mod / MS_res
    p = st.f.sf(F, df_mod, df_res)
    return(F, p)


# Once we have run the function, all we need to do is plug in our values, and `regression_f` does the rest:

# In[22]:


predictors = df[['dan_sleep', 'baby_sleep']]
outcome = df['dan_grump']

regression_f(predictors, outcome)


# ### Tests for individual coefficients
# 
# The $F$-test that we've just introduced is useful for checking that the model as a whole is performing better than chance. This is important: if your regression model doesn't produce a significant result for the $F$-test then you probably don't have a very good regression model (or, quite possibly, you don't have very good data). However, while failing this test is a pretty strong indicator that the model has problems, *passing* the test (i.e., rejecting the null) doesn't imply that the model is good! Why is that, you might be wondering? The answer to that can be found by looking at the coefficients for the multiple linear regression model we calculated earlier:

# In[23]:


predictors = df[['dan_sleep', 'baby_sleep']]
outcome = df['dan_grump']

mod2 = pg.linear_regression(predictors, outcome)
mod2.round(2)


# 
# I can't help but notice that the estimated regression coefficient for the `baby_sleep` variable is tiny (0.01), relative to the value that we get for `dan_sleep` (-8.95). Given that these two variables are absolutely on the same scale (they're both measured in "hours slept"), I find this suspicious. In fact, I'm beginning to suspect that it's really only the amount of sleep that *I* get that matters in order to predict my grumpiness.
# 
# Once again, we can reuse a hypothesis test that we discussed earlier, this time the $t$-test. The test that we're interested has a null hypothesis that the true regression coefficient is zero ($b = 0$), which is to be tested against the alternative hypothesis that it isn't ($b \neq 0$). That is:
# 
# $$
# \begin{array}{rl}
# H_0: & b = 0 \\
# H_1: & b \neq 0 
# \end{array}
# $$

# How can we test this? Well, if the central limit theorem is kind to us, we might be able to guess that the sampling distribution of $\hat{b}$, the estimated regression coefficient, is a normal distribution with mean centred on $b$. What that would mean is that if the null hypothesis were true, then the sampling distribution of $\hat{b}$ has mean zero and unknown standard deviation. Assuming that we can come up with a good estimate for the standard error of the regression coefficient, $\mbox{SE}({\hat{b}})$, then we're in luck. That's *exactly* the situation for which we introduced the one-sample $t$ way back in [the chapter on t-tests](ttest). So let's define a $t$-statistic like this,
# 
# $$
# t = \frac{\hat{b}}{\mbox{SE}({\hat{b})}}
# $$

# I'll skip over the reasons why, but our degrees of freedom in this case are $df = N- K- 1$. Irritatingly, the estimate of the standard error of the regression coefficient, $\mbox{SE}({\hat{b}})$, is not as easy to calculate as the standard error of the mean that we used for the simpler $t$-tests [earlier](ttest). In fact, the formula is somewhat ugly, and not terribly helpful to look at. For our purposes it's sufficient to point out that the standard error of the  estimated regression coefficient depends on both the predictor and outcome variables, and is somewhat sensitive to violations of the homogeneity of variance assumption (discussed shortly). 
# 
# In any case, this $t$-statistic can be interpreted in the same way as the $t$-statistics that we discussed [earlier](ttest). Assuming that you have a two-sided alternative (i.e., you don't really care if $b >0$ or $b < 0$), then it's the extreme values of $t$ (i.e., a lot less than zero or a lot greater than zero) that suggest that you should reject the null hypothesis. 

# Now we are in a position to understand all the values in the multiple regression table provided by `pingouin`:

# In[24]:


mod2.round(2)


# Each row in this table refers to one of the coefficients in the regression model. The first row is the intercept term, and the later ones look at each of the predictors. The columns give you all of the relevant information. The first column is the actual estimate of $b$ (e.g., 125.96 for the intercept, -8.9 for the `dan_sleep` predictor, and -0.01 for the `baby_sleep` predictor). The second column is the standard error estimate $\hat\sigma_b$. The third column gives you the $t$-statistic, and it's worth noticing that in this table $t= \hat{b}/\mbox{SE}({\hat{b}})$ every time. The fourth column gives you the actual $p$ value for each of these tests.[^notecorrection] Then next column gives the $r^2$ value and the adjusted $r^2$ for the model, and the last two columns give us the upper and lower [confidence interval](ci) bounds for each estimate.
# 
# [^notecorrection]: Note that, although `pingouin` has done multiple tests here, it hasn't done a Bonferroni correction or anything. These are standard one-sample $t$-tests with a two-sided alternative. If you want to make corrections for multiple tests, you need to do that yourself.

# If we add our F-test results to the mix:

# In[25]:


f = regression_f(predictors, outcome)
print("F:", f[0].round(2), "p:", f[1])


# we have everything we need to evaluate our model. In this case, the model performs significantly better than you'd expect by chance ($F(2,97) = 215.2$, $p<.001$), which isn't all that surprising: the $R^2 = .812$ value indicate that the regression model accounts for 81.2\% of the variability in the outcome measure. However, when we look back up at the $t$-tests for each of the individual coefficients, we have pretty strong evidence that the `baby_sleep` variable has no significant effect; all the work is being done by the `dan_sleep` variable. Taken together, these results suggest that `lmm` is actually the wrong model for the data: you'd probably be better off dropping the `baby_sleep` predictor entirely. In other words, the `mod1` model that we started with is the better model.

# (corrhyp)=
# ## Testing the significance of a correlation
# 
# 
# ### Hypothesis tests for a single correlation
# 
# I don't want to spend too much time on this, but it's worth very briefly returning to the point I made earlier, that Pearson correlations are basically the same thing as linear regressions with only a single predictor added to the model. What this means is that the hypothesis tests that I just described in a regression context can also be applied to correlation coefficients. To see this, let's just revist our `mod1` model:

# In[26]:


X = df['dan_sleep'] # the predictor
Y = df['dan_grump'] # the outcome
mod1 = pg.linear_regression(X, Y)
mod1.round(2)


# The important thing to note here is the $t$ test associated with the predictor, in which we get a result of $t(98) = -20.85$, $p<.001$. Now let's compare this to the output of the `corr` function from `pinguoin`, which runs a hypothesis test to see if the observed correlation between two variables is significantly different from 0. 

# In[27]:


pg.corr(X,Y)


# Now, just like the $F$-test from earlier, `pingouin` unfortunately doesn't calculate a $t$-statistic for us automatically when running a correlation. But the formula for the $t$-statistic of a Pearson correlation is just
# 
# 
# $$
# t = r\sqrt{\frac{n-2}{1-r^2}}
# $$
# 
# so, with the output from `pg.corr(X,Y)` above, it's not too difficult to find $t$:

# In[28]:


from math import sqrt

t = -0.903384*sqrt((100-2) / (1-(-0.903384)**2))
t


# Look familiar? -20.85 was the same $t$-value that we got when we ran the regression model. That's because the test for the significance of a correlation is identical to the $t$ test that we run on a coefficient in a regression model. 

# (corrhyp2)=
# ### Hypothesis tests for all pairwise correlations
# 
# Okay, one more digression before I return to regression properly. In the previous section I talked about you can run a hypothesis test on a single correlation. But we aren't restricted to computing a single correlation: you can compute *all* pairwise correlations among the variables in your data set. This leads people to the natural question: can we also run hypothesis tests on all of the pairwise correlations in our data using `pg.corr`?
# 
# The answer is no, and there's a very good reason for this. Testing a single correlation is fine: if you've got some reason to be asking "is A related to B?", then you should absolutely run a test to see if there's a significant correlation. But if you've got variables A, B, C, D and E and you're thinking about testing the correlations among all possible pairs of these, a statistician would want to ask: what's your hypothesis? If you're in the position of wanting to test all possible pairs of variables, then you're pretty clearly on a fishing expedition, hunting around in search of significant effects when you don't actually have a clear research hypothesis in mind. This is *dangerous*, and perhaps the authors of the `corr` function didn't want to endorse this sort of behavior. `corr` does have the nice feature that you can call it as an attribute of your dataframe, so for our parenthood data, if we want to see all the parwise correlations in the data, you can simply write

# In[29]:


df.corr()


# and you get a nice correlation matrix, but no p-values.
# 
# On the other hand... a somewhat less hardline view might be to argue we've encountered this situation before, back when we talked about *post hoc tests* in ANOVA. When running post hoc tests, we didn't have any specific comparisons in mind, so what we did was apply a correction (e.g., Bonferroni, Holm, etc) in order to avoid the possibility of an inflated Type I error rate. From this perspective, it's okay to run hypothesis tests on all your pairwise correlations, but you must treat them as post hoc analyses, and if so you need to apply a correction for multiple comparisons. `rcorr`, also from `pingouin`, lets you do this. You can use the `padjust` argument to specify what kind of correction you would like to apply; here I have chosen a Bonferroni correction:

# In[30]:


df.rcorr(padjust = 'bonf')


# The little stars indicate the "significance level": one star for $p<0.05$, two stars for $p<0.01$, and three stars for $p<0.001$.
# 
# So there you have it. If you really desperately want to do pairwise hypothesis tests on your correlations, the `rcorr` function will let you do it. But please, **please** be careful. I can't count the number of times I've had a student panicking in my office because they've run these pairwise correlation tests, and they get one or two significant results that don't make any sense. For some reason, the moment people see those little significance stars appear, they feel compelled to throw away all common sense and assume that the results must correspond to something real that requires an explanation. In most such cases, my experience has been that the right answer is "it's a Type I error". 

# (regressioncoefs)=
# ### Calculating standardised regression coefficients
# 
# One more thing that you might want to do is to calculate "standardised" regression coefficients, often denoted $\beta$. The rationale behind standardised coefficients goes like this. In a lot of situations, your variables are on fundamentally different scales. Suppose, for example, my regression model aims to predict people's IQ scores, using their educational attainment (number of years of education) and their income as predictors. Obviously, educational attainment and income are not on the same scales: the number of years of schooling can only vary by 10s of years, whereas income would vary by 10,000s of dollars (or more). The units of measurement have a big influence on the regression coefficients: the $b$ coefficients only make sense when interpreted in light of the units, both of the predictor variables and the outcome variable. This makes it very difficult to compare the coefficients of different predictors. Yet there are situations where you really do want to make comparisons between different coefficients. Specifically, you might want some kind of standard measure of which predictors have the strongest relationship to the outcome. This is what **_standardised coefficients_** aim to do. 

# The basic idea is quite simple: the standardised coefficients are the coefficients that you would have obtained if you'd converted all the variables to [standard scores](zscores) $z$-scores before running the regression.[^noteregressors]  The idea here is that, by converting all the predictors to $z$-scores, they all go into the regression on the same scale, thereby removing the problem of having variables on different scales. Regardless of what the original variables were, a $\beta$ value of 1 means that an increase in the predictor of 1 standard deviation will produce a corresponding 1 standard deviation increase in the outcome variable. Therefore, if variable A has a larger absolute value of $\beta$ than variable B, it is deemed to have a stronger relationship with the outcome. Or at least that's the idea: it's worth being a little cautious here, since this does rely very heavily on the assumption that "a 1 standard deviation change" is fundamentally the same kind of thing for all variables. It's not always obvious that this is true. 
# 
# [^noteregressors]: Strictly, you standardise all the *regressors*: that is, every "thing" that has a regression coefficient associated with it in the model. For the regression models that I've talked about so far, each predictor variable maps onto exactly one regressor, and vice versa. However, that's not actually true in general: we'll see some examples of this when we learn about [factorial ANOVA](anova2). But for now, we don't need to care too much about this distinction.

# Still, let's give it a try on the `parenthood` data.
# 
# 

# In[31]:


from scipy import stats

df['dan_sleep_standard'] = stats.zscore(df['dan_sleep'])
df['baby_sleep_standard'] = stats.zscore(df['baby_sleep'])


predictors = df[['dan_sleep_standard', 'baby_sleep_standard']]
outcome = df['dan_grump']

mod3 = pg.linear_regression(predictors, outcome)
mod3.round(2)


# This clearly shows that the `dan_sleep` variable has a much stronger effect than the `baby_sleep` variable. However, this is a perfect example of a situation where it would probably make sense to use the original coefficients $b$ rather than the standardised coefficients $\beta$. After all, my sleep and the baby's sleep are *already* on the same scale: number of hours slept. Why complicate matters by converting these to $z$-scores?

# (regressionassumptions)=
# 
# ## Assumptions of regression
# 
# The linear regression model that I've been discussing relies on several assumptions. In the section on [regression diagnostics](regressiondiagnostics) we'll talk a lot more about how to check that these assumptions are being met, but first, let's have a look at each of them.
# 
# 
# - *Normality*. Like half the models in statistics, standard linear regression relies on an assumption of normality. Specifically, it assumes that the *residuals* are normally distributed. It's actually okay if the predictors $X$ and the outcome $Y$ are non-normal, so long as the residuals $\epsilon$ are normal. See [](regressionnormality).
# - *Linearity*. A pretty fundamental assumption of the linear regression model is that relationship between $X$ and $Y$ actually be linear! Regardless of whether it's a simple regression or a multiple regression, we assume that the relatiships involved are linear. See [](regressionlinearity).
# - *Homogeneity of variance*. Strictly speaking, the regression model assumes that each residual $\epsilon_i$ is generated from a normal distribution with mean 0, and (more importantly for the current purposes) with a standard deviation $\sigma$ that is the same for every single residual. In practice, it's impossible to test the assumption that every residual is identically distributed. Instead, what we care about is that the standard deviation of the residual is the same for all values of $\hat{Y}$, and (if we're being especially paranoid) all values of every predictor $X$ in the model. See [](regressionhomogeneity).
# - *Uncorrelated predictors*. The idea here is that, is a multiple regression model, you don't want your predictors to be too strongly correlated with each other. This isn't  "technically" an assumption of the regression model, but in practice it's required. Predictors that are too strongly correlated with each other (referred to as "collinearity") can cause problems when evaluating the model. See [](regressioncollinearity)
# - *Residuals are independent of each other*. This is really just a "catch all" assumption, to the effect that "there's nothing else funny going on in the residuals". If there is something weird (e.g., the residuals all depend heavily on some other unmeasured variable) going on, it might screw things up.
# - *No "bad" outliers*. Again, not actually a technical assumption of the model (or rather, it's sort of implied by all the others), but there is an implicit assumption that your regression model isn't being too strongly influenced by one or two anomalous data points; since this raises questions about the adequacy of the model, and the trustworthiness of the data in some cases. See [](regressionoutliers).
# 
# 

# (regressiondiagnostics)=
# ## Model checking
# 
# The main focus of this section is **_regression diagnostics_**, a term that refers to the art of checking that the assumptions of your regression model have been met, figuring out how to fix the model if the assumptions are violated, and generally to check that nothing "funny" is going on. I refer to this as the "art" of model checking with good reason: it's not easy, and while there are a lot of fairly standardised tools that you can use to diagnose and maybe even cure the problems that ail your model (if there are any, that is!), you really do need to exercise a certain amount of judgment when doing this. It's easy to get lost in all the details of checking this thing or that thing, and it's quite exhausting to try to remember what all the different things are. This has the very nasty side effect that a lot of people get frustrated when trying to learn *all* the tools, so instead they decide not to do *any* model checking. This is a bit of a worry! 
# 
# In this section, I describe several different things you can do to check that your regression model is doing what it's supposed to. It doesn't cover the full space of things you could do, but it's still much more detailed than what I see a lot of people doing in practice; and I don't usually cover all of this in my intro stats class myself. However, I do think it's important that you get a sense of what tools are at your disposal, so I'll try to introduce a bunch of them here. 
# 
# 
# ### Three kinds of residuals
# 
# The majority of regression diagnostics revolve around looking at the residuals, and by now you've probably formed a sufficiently pessimistic theory of statistics to be able to guess that -- precisely *because* of the fact that we care a lot about the residuals -- there are several different kinds of  residual that we might consider. In particular, the following three kinds of residual are referred to in this section: "ordinary residuals", "standardised residuals", and "Studentised residuals". There is a fourth kind that you'll see referred to in some of the Figures, and that's the "Pearson residual": however, for the models that we're talking about in this chapter, the Pearson residual is identical to the ordinary residual. 
# 
# The first and simplest kind of residuals that we care about are **_ordinary residuals_**. These are the actual, raw residuals that I've been talking about throughout this chapter. The ordinary residual is just the difference between the fitted value $\hat{Y}_i$ and the observed value $Y_i$. I've been using the notation $\epsilon_i$ to refer to the $i$-th ordinary residual, and by gum I'm going to stick to it. With this in mind, we have the very simple equation
# 
# $$
# \epsilon_i = Y_i - \hat{Y}_i
# $$

# This is of course what we saw earlier, and unless I specifically refer to some other kind of residual, this is the one I'm talking about. So there's nothing new here: I just wanted to repeat myself. In any case, if you have run your regression model using `pingouin`, you can access the residuals from your model (in our case, our `mod2`)like this:

# In[32]:


res = mod2.residuals_


# One drawback to using ordinary residuals is that they're always on a different scale, depending on what the outcome variable is and how good the regression model is. That is, Unless you've decided to run a regression model without an intercept term, the ordinary residuals will have mean 0; but the variance is different for every regression. In a lot of contexts, especially where you're only interested in the *pattern* of the residuals and not their actual values, it's convenient to estimate the **_standardised residuals_**, which are normalised in such a way as to have standard deviation 1. The way we calculate these is to divide the ordinary residual by an estimate of the (population) standard deviation of these residuals. For technical reasons, mumble mumble, the formula for this is:
# 
# $$
# \epsilon_{i}^\prime = \frac{\epsilon_i}{\hat{\sigma} \sqrt{1-h_i}}
# $$

# where $\hat\sigma$ in this context is the estimated population standard deviation of the ordinary residuals, and $h_i$ is the "hat value" of the $i$th observation. I haven't explained hat values to you yet (but have no fear,[^notehope] it's coming shortly), so this won't make a lot of sense. For now, it's enough to interpret the standardised residuals as if we'd converted the ordinary residuals to $z$-scores. In fact, that is more or less the truth, it's just that we're being a bit fancier. To get the standardised residuals, the command you want is this:
# 
# [^notehope]: Or have no hope, as the case may be.

# Note that this function uses a different name for the input argument, but it's still just a linear regression object that the function wants to take as its input here.
# 
# The third kind of residuals are **_Studentised residuals_** (also called "jackknifed residuals") and they're even fancier than standardised residuals. Again, the idea is to take the ordinary residual and divide it by some quantity in order to estimate some standardised notion of the residual, but the formula for doing the calculations this time is subtly different:
# 
# $$
# \epsilon_{i}^* = \frac{\epsilon_i}{\hat{\sigma}_{(-i)} \sqrt{1-h_i}}
# $$

# Notice that our estimate of the standard deviation here is written $\hat{\sigma}_{(-i)}$. What this corresponds to is the estimate of the residual standard deviation that you *would have obtained*, if you just deleted the $i$th observation from the data set. This sounds like the sort of thing that would be a nightmare to calculate, since it seems to be saying that you have to run $N$ new regression models (even a modern computer might grumble a bit at that, especially if you've got a large data set). Fortunately, some terribly clever person has shown that this standard deviation estimate is actually given by the following equation:
# 
# $$
# \hat\sigma_{(-i)} = \hat{\sigma} \ \sqrt{\frac{N-K-1 - {\epsilon_{i}^\prime}^2}{N-K-2}}
# $$

# Isn't that a pip?
# 
# Before moving on, I should point out that you don't often need to manually extract these residuals yourself, even though they are at the heart of almost all regression diagnostics. Most of the time the various functions that run the diagnostics will take care of these calculations for you.

# (regressionoutliers)=
# 
# ### Three kinds of anomalous data
# One danger that you can run into with linear regression models is that your analysis might be disproportionately sensitive to a smallish number of "unusual" or "anomalous" observations. In the context of linear regression, there are three conceptually distinct ways in which an observation might be called "anomalous". All three are interesting, but they have rather different implications for your analysis.
# 
# The first kind of unusual observation is an **_outlier_**. The definition of an outlier (in this context) is an observation that is very different from what the regression model predicts. An example is shown in {numref}`fig-outlier`. In practice, we operationalise this concept by saying that an outlier is an observation that has a very large Studentised residual, $\epsilon_i^*$. Outliers are interesting: a big outlier *might* correspond to junk data -- e.g., the variables might have been entered incorrectly, or some other defect may be detectable. Note that you shouldn't throw an observation away just because it's an outlier. But the fact that it's an outlier is often a cue to look more closely at that case, and try to find out why it's so different.

# In[33]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import seaborn as sns


df = pd.DataFrame(
    {'x': [1, 1.3, 1.8, 1.9, 2.4, 2.3, 2.4, 2.6, 2.8, 3.6, 4],
     'y': [1.5, 1.4, 1.9, 1.7, 2.3, 2.1, 2.6, 2.8, 2.4, 2.6, 2.8],
     'y2': [1.5, 1.4, 1.9, 1.7, 4, 2.1, 2.6, 2.8, 2.4, 2.6, 2.8]
    })



# fit linear regression model and save parameters
def func(x, a, b):
    return a * x + b

initialParameters = np.array([1.0, 1.0])

fittedParameters, pcov = curve_fit(func, df['x'], df['y'], initialParameters)

modelPredictions = func(df['x'], *fittedParameters) 

xModel = np.linspace(min(df['x']), max(df['x']))
yModel = func(xModel, *fittedParameters)


# plot data
fig = plt.figure() 
ax = fig.add_subplot()


sns.scatterplot(data = df, x='x', y='y')

# add regression line
ax.plot(xModel, yModel)


initialParameters = np.array([1.0, 1.0])

fittedParameters, pcov = curve_fit(func, df['x'], df['y2'], initialParameters)

modelPredictions = func(df['x'], *fittedParameters) 

xModel = np.linspace(min(df['x']), max(df['x']))
yModel = func(xModel, *fittedParameters)

ax.plot(xModel, yModel)
ax.plot(2.4, 4, 'ro')
ax.plot([2.4, 2.4], [2.4 ,4], linestyle='dashed')
ax.grid(False)

sns.despine()


#  ```{glue:figure} outlier-fig
# :figwidth: 600px
# :name: fig-outlier
# 
# An illustration of outliers. The orange line plots the regression line estimated when the anomalous (red) data point is included, and the dotted line shows the residual for the outlier. The blue line shows the regression line that would have been estimated without the anomalous observation included. The outlier has an unusual value on the outcome (y axis location) but not the predictor (x axis location), and lies a long way from the regression line.
# 
# ```

# The second way in which an observation can be unusual is if it has high **_leverage_**: this happens when the observation is very different from all the other observations. This doesn't necessarily have to correspond to a large residual: if the observation happens to be unusual on all variables in precisely the same way, it can actually lie very close to the regression line. An example of this is shown in panel A of {numref}`fig-leverage-influence`. The leverage of an observation is operationalised in terms of its *hat value*, usually written $h_i$. The formula for the hat value is rather complicated[^notehatmatrix] but its interpretation is not: $h_i$ is a measure of the extent to which the $i$-th observation is "in control" of where the regression line ends up going. We won't bother extracting the hat values here, but if you want to do this, you can use the `get_influence` method from the `statsmodel` package to inspect the relative influence of data points. For now, it is enough to get an intuitive, visual idea of what leverage can mean.
# 
# [^notehatmatrix]: Again, for the linear algebra fanatics: the "hat matrix" is defined to be that matrix $H$ that converts the vector of observed values $y$ into a vector of fitted values $\hat{y}$, such that $\hat{y} = H y$. The name comes from the fact that this is the matrix that "puts a hat on $y$". The  hat *value* of the $i$-th observation is the $i$-th diagonal element of this matrix (so technically I should be writing it as $h_{ii}$ rather than $h_{i}$). Oh, and in case you care, here's how it's calculated: $H = X(X^TX)^{-1} X^T$. Pretty, isn't it?

# In[34]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import seaborn as sns
import string

fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=True)

df = pd.DataFrame(
    {'x': [1, 1.3, 1.8, 1.9, 2.4, 2.3, 2.4, 2.6, 2.8, 3.6, 4, 8],
     'y': [1.5, 1.4, 1.9, 1.7, 2.3, 2.1, 2.6, 2.8, 2.4, 2.6, 2.8, 7.8],
     'y2': [1.5, 1.4, 1.9, 1.7, 4, 2.1, 2.6, 2.8, 2.4, 2.6, 2.8, 7.4]
    })



# fit linear regression model and save parameters
def func(x, a, b):
    return a * x + b

initialParameters = np.array([1.0, 1.0])

fittedParameters, pcov = curve_fit(func, df['x'], df['y'], initialParameters)

modelPredictions = func(df['x'], *fittedParameters) 

xModel = np.linspace(min(df['x']), max(df['x']))
yModel = func(xModel, *fittedParameters)


# plot data
#fig = plt.figure() 
#ax = fig.add_subplot()


sns.scatterplot(data = df, x='x', y='y', ax = axes[0])

# add regression line
axes[0].plot(xModel, yModel)


initialParameters = np.array([1.0, 1.0])

fittedParameters, pcov = curve_fit(func, df['x'], df['y2'], initialParameters)

modelPredictions = func(df['x'], *fittedParameters) 

xModel = np.linspace(min(df['x']), max(df['x']))
yModel = func(xModel, *fittedParameters)

axes[0].plot(xModel, yModel)
axes[0].plot(8, 7.4, 'ro')
axes[0].plot([8, 8], [7.4 ,7.6], linestyle='dashed')
axes[0].grid(False)

# Plot 2

df = pd.DataFrame(
    {'x': [1, 1.3, 1.8, 1.9, 2.4, 2.3, 2.4, 2.6, 2.8, 3.6, 4, 8],
     'y': [1.5, 1.4, 1.9, 1.7, 2.3, 2.1, 2.6, 2.8, 2.4, 2.6, 2.8, 7.8],
     'y2': [1.5, 1.4, 1.9, 1.7, 4, 2.1, 2.6, 2.8, 2.4, 2.6, 2.8, 5]
    })



# fit linear regression model and save parameters
def func(x, a, b):
    return a * x + b

initialParameters = np.array([1.0, 1.0])

fittedParameters, pcov = curve_fit(func, df['x'], df['y'], initialParameters)

modelPredictions = func(df['x'], *fittedParameters) 

xModel = np.linspace(min(df['x']), max(df['x']))
yModel = func(xModel, *fittedParameters)


# plot data
#fig = plt.figure() 
#ax = fig.add_subplot()


sns.scatterplot(data = df, x='x', y='y', ax = axes[1])

# add regression line
axes[1].plot(xModel, yModel)


initialParameters = np.array([1.0, 1.0])

fittedParameters, pcov = curve_fit(func, df['x'], df['y2'], initialParameters)

modelPredictions = func(df['x'], *fittedParameters) 

xModel = np.linspace(min(df['x']), max(df['x']))
yModel = func(xModel, *fittedParameters)

axes[1].plot(xModel, yModel)
axes[1].plot(8, 5, 'ro')
axes[1].plot([8, 8], [5 ,7.3], linestyle='dashed')
axes[1].grid(False)


for n, ax in enumerate(axes):   
    ax.text(-0.1, 1.1, string.ascii_uppercase[n], transform=ax.transAxes, 
            size=20)


sns.despine()


#  ```{glue:figure} leverage-influence-fig
# :figwidth: 600px
# :name: fig-leverage-influence
# 
# Outliers showing high leverage points (panel A) and high influence points (panel B).
# 
# ```

# In[ ]:




