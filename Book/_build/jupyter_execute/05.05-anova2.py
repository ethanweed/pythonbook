#!/usr/bin/env python
# coding: utf-8

# (anova2)=
# # Factorial ANOVA

# Over the course of the last few chapters you can probably detect a general trend. We started out looking at tools that you can use to compare two groups to one another, most notably the [$t$-test](ttest). Then, we introduced [analysis of variance](anova) (ANOVA) as a method for comparing more than two groups. The chapter on [regression](regression) covered a somewhat different topic, but in doing so it introduced a powerful new idea: building statistical models that have *multiple* predictor variables used to explain a single outcome variable. For instance, a regression model could be used to predict the number of errors a student makes in a reading comprehension test based on the number of hours they studied for the test, and their score on a standardised IQ test. The goal in this chapter is to import this idea into the ANOVA framework. For instance, suppose we were interested in using the reading comprehension test to measure student achievements in three different schools, and we suspect that girls and boys are developing at different rates (and so would be expected to have different performance on average). Each student is classified in two different ways: on the basis of their gender, and on the basis of their school. What we'd like to do is analyse the reading comprehension scores in terms of *both* of these grouping variables. The tool for doing so is generically referred to as **_factorial ANOVA_**. However, since we have two grouping variables, we sometimes refer to the analysis as a two-way ANOVA, in contrast to the one-way ANOVAs that we [ran earlier](anova).

# (factorialanovasimple)=
# ## Factorial ANOVA 1: balanced designs, no interactions
# 
# When we discussed [analysis of variance](anova), we assumed a fairly simple experimental design: each person falls into one of several groups, and we want to know whether these groups have different means on some outcome variable. In this section, I'll discuss a broader class of experimental designs, known as **_factorial designs_**, in we have more than one grouping variable. I gave one example of how this kind of design might arise above. Another example appears in the chapter on [ANOVA](anova), in which we were looking at the effect of different drugs on the `mood_gain` experienced by each person. In that chapter we did find a significant effect of drug, but at the end of the chapter we also ran an analysis to see if there was an effect of therapy. We didn't find one, but there's something a bit worrying about trying to run two *separate* analyses trying to predict the same outcome. Maybe there actually *is* an effect of therapy on mood gain, but we couldn't find it because it was being "hidden" by the effect of drug? In other words, we're going to want to run a *single* analysis that includes *both* `drug` and `therapy` as predictors. For this analysis each person is cross-classified by the drug they were given (a factor with 3 levels) and what therapy they received (a factor with 2 levels). We refer to this as a $3 \times 2$ factorial design. If we cross-tabulate `drug` by `therapy` using the `crosstab()` in `pandas`, we get the following table:

# In[1]:


import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/ethanweed/pythonbook/main/Data/clintrial.csv")

pd.crosstab(index=df["drug"], columns=df["therapy"],margins=False)


# As you can see, not only do we have participants corresponding to all possible combinations of the two factors, indicating that our design is **_completely crossed_**, it turns out that there are an equal number of people in each group. In other words, we have a **_balanced_** design. In this section I'll talk about how to analyse data from balanced designs, since this is the simplest case. The story for unbalanced designs is quite tedious, so we'll put it to one side for the moment.

# (factanovahyp)=
# ### What hypotheses are we testing?
# 
# Like one-way ANOVA, factorial ANOVA is a tool for testing certain types of hypotheses about population means. So a sensible place to start would be to be explicit about what our hypotheses actually are. However, before we can even get to that point, it's really useful to have some clean and simple notation to describe the population means. Because of the fact that observations are cross-classified in terms of two different factors, there are quite a lot of different means that one might be interested. To see this, let's start by thinking about all the different sample means that we can calculate for this kind of design. Firstly, there's the obvious idea that we might be interested in this table of group means:

# In[2]:


round(df.groupby(['therapy', 'drug'])[['mood_gain']].mean(),2)


# Now, this output shows a cross-tabulation of the group means for all possible combinations of the two factors (e.g., people who received the placebo and no therapy, people who received the placebo while getting CBT, etc). However, we can also construct tables that ignore one of the two factors. That gives us output that looks like this:

# In[3]:


round(df.groupby(['therapy'])[['mood_gain']].mean(),2)


# In[4]:


round(df.groupby(['drug'])[['mood_gain']].mean(),2)


# But of course, if we can ignore one factor we can certainly ignore both. That is, we might also be interested in calculating the average  mood gain across all 18 participants, regardless of what drug or psychological therapy they were given:

# In[5]:


round(df['mood_gain'].mean(),2)


# At this point we have 12 different sample means to keep track of! It is helpful to organise all these numbers into a single table, which would look like this:
# 
# |         |no therapy |CBT  |total |
# |:--------|:----------|:----|:-----|
# |         |no therapy |CBT  |total |
# |placebo  |0.30       |0.60 |0.45  |
# |anxifree |0.40       |1.03 |0.72  |
# |joyzepam |1.47       |1.50 |1.48  |
# |total    |0.72       |1.04 |0.88  |

# Now, each of these different means is of course a sample statistic: it's a quantity that pertains to the specific observations that we've made during our study. What we want to make inferences about are the corresponding population parameters: that is, the true means as they exist within some broader population. Those population means can also be organised into a similar table, but we'll need a little mathematical notation to do so. As usual, I'll use the symbol $\mu$ to denote a population mean. However, because there are lots of different means, I'll need to use subscripts to distinguish between them. 
# 
# Here's how the notation works. Our table is defined in terms of two factors: each row corresponds to a different level of Factor A (in this case `drug`), and each column corresponds to a different level of Factor B (in this case `therapy`). If we let $R$ denote the number of rows in the table, and $C$ denote the number of columns, we can refer to this as an $R \times C$ factorial ANOVA. In this case $R=3$ and $C=2$. We'll use lowercase letters to refer to specific rows and columns, so $\mu_{rc}$ refers to the population mean associated with the $r$th level of Factor A (i.e. row number $r$) and the $c$th level of Factor B (column number $c$).[^notesubscript] So the population means are now written like this:
# 
# [^notesubscript]: The nice thing about the subscript notation is that generalises nicely: if our experiment had involved a third factor, then we could just add a third subscript. In principle, the notation extends to as many factors as you might care to include, but in this book we'll rarely consider analyses involving more than two factors, and never more than three. 

# |         |no therapy |CBT        |total |
# |:--------|:----------|:----------|:-----|
# |placebo  |$\mu_{11}$ |$\mu_{12}$ |      |
# |anxifree |$\mu_{21}$ |$\mu_{22}$ |      |
# |joyzepam |$\mu_{31}$ |$\mu_{32}$ |      |
# |total    |           |           |      |

# 
