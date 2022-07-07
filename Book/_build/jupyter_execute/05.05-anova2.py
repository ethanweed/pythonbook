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

# Okay, what about the remaining entries? For instance, how should we describe the average mood gain across the entire (hypothetical) population of people who might be given Joyzepam in an experiment like this, regardless of whether they were in CBT? We use the "dot" notation to express this. In the case of Joyzepam, notice that we're talking about the mean associated with the third row in the table. That is, we're averaging across two cell means (i.e., $\mu_{31}$ and $\mu_{32}$). The result of this averaging is referred to as a **_marginal mean_**, and would be denoted $\mu_{3.}$ in this case. The marginal mean for CBT corresponds to the population mean associated with the second column in the table, so we use the notation $\mu_{.2}$ to describe it. The grand mean is denoted $\mu_{..}$ because it is the mean obtained by averaging (marginalising[^notemarginalising]) over both. So our full table of population means can be written down like this:
# 
# [^notemarginalising]: Technically, marginalising isn't quite identical to a regular mean: it's a weighted average, where you take into account the frequency of the different events that you're averaging over. However, in a balanced design, all of our cell frequencies are equal by definition, so the two are equivalent. We'll discuss unbalanced designs later, and when we do so you'll see that all of our calculations become a real headache. But let's ignore this for now.

# |         |no therapy |CBT        |total      |
# |:--------|:----------|:----------|:----------|
# |placebo  |$\mu_{11}$ |$\mu_{12}$ |$\mu_{1.}$ |
# |anxifree |$\mu_{21}$ |$\mu_{22}$ |$\mu_{2.}$ |
# |joyzepam |$\mu_{31}$ |$\mu_{32}$ |$\mu_{3.}$ |
# |total    |$\mu_{.1}$ |$\mu_{.2}$ |$\mu_{..}$ |

# Now that we have this notation, it is straightforward to formulate and express some hypotheses. Let's suppose that the goal is to find out two things: firstly, does the choice of drug have any effect on mood, and secondly, does CBT have any effect on mood? These aren't the only hypotheses that we could formulate of course, and we'll see a really important example of a different kind of hypothesis in the section on [interactions](interactions), but these are the two simplest hypotheses to test, and so we'll start there. Consider the first test. If drug has no effect, then we would expect all of the row means to be identical, right? So that's our null hypothesis. On the other hand, if the drug does matter then we should expect these row means to be different. Formally, we write down our null and alternative hypotheses in terms of the *equality of marginal means*:

# |                              |                                                             |
# |:-----------------------------|:------------------------------------------------------------|
# |Null hypothesis $H_0$:        |row means are the same i.e. $\mu_{1.} = \mu_{2.} = \mu_{3.}$ |
# |Alternative hypothesis $H_1$: |at least one row mean is different.                          |

# It's worth noting that these are *exactly* the same statistical hypotheses that we formed when we ran a one-way ANOVA on these data [way back when](anova). Back then I used the notation $\mu_P$ to refer to the mean mood gain for the placebo group, with $\mu_A$ and $\mu_J$ corresponding to the group means for the two drugs, and the null hypothesis was $\mu_P = \mu_A = \mu_J$. So we're actually talking about the same hypothesis: it's just that the more complicated ANOVA requires more careful notation due to the presence of multiple grouping variables, so we're now referring to this hypothesis as $\mu_{1.} = \mu_{2.} = \mu_{3.}$. However, as we'll see shortly, although the hypothesis is identical, the test of that hypothesis is subtly different due to the fact that we're now acknowledging the existence of the second grouping variable.
# 
# Speaking of the other grouping variable, you won't be surprised to discover that our second hypothesis test is formulated the same way. However, since we're talking about the psychological therapy rather than drugs, our null hypothesis now corresponds to the equality of the column means:
# 

# |                              |                                                          |
# |:-----------------------------|:---------------------------------------------------------|
# |Null hypothesis $H_0$:        |column means are the same, i.e., $\mu_{.1} = \mu_{.2}$    |
# |Alternative hypothesis $H_1$: |column means are different, i.e., $\mu_{.1} \neq \mu_{.2}$|

# ### Running the analysis in Python
# 
# If the data you're trying to analyse correspond to a balanced factorial design, then running your analysis of variance is easy. To see how easy it is, let's start by reproducing the original analysis from [earlier](anova). In case you've forgotten, for that analysis we were using only a single factor (i.e., `drug`) as our between-subjects variable to predict our outcome (dependent) variable (i.e., `mood_gain`), and so this was what we did:

# In[6]:


import pingouin as pg

model1 = pg.anova(dv='mood_gain', between='drug', data=df, detailed=True)
round(model1, 2)


# Note that this time around I've used the name `model1` as the label for my `aov` object, since I'm planning on creating quite a few other models too. To start with, suppose I'm also curious to find out if `therapy` has a relationship to `mood_gain`. In light of what we've seen from our discussion of [multiple regression](regression), you probably won't be surprised that all we have to do is extend the formula: in other words, if we specify `dv=mood.gain, between=['drug', 'therapy']` as our model, we'll probably get what we're after:

# In[7]:


model2 = pg.anova(dv='mood_gain', between=['drug', 'therapy'], data=df, detailed=True)
round(model2, 2)


# Most of this output is pretty simple to read too: the first row of the table reports a between-group sum of squares (SS) value associated with the `drug` factor, along with a corresponding between-group $df$ value. It also calculates a mean square value (MS), and $F$-statistic, an (uncorrected) $p$-value, and an estimate of the effect size (`np2`, that is, partial eta-squared). There is also a row corresponding to the `therapy` factor, and a row corresponding to the residuals (i.e., the within groups variation). 
# 
# Now, the third row is a little trickier, so let's just save that one for [later](interactions), shall we? (Spoiler: this is the interaction of `drug` and `therapy`, but we'll get there soon).
# 
# Not only are all of the individual quantities pretty familiar, the relationships between these different quantities has remained unchanged: just like we saw with the original one-way ANOVA, note that the mean square value is calculated by dividing SS by the corresponding $df$. That is, it's still true that
# 
# $$
# \mbox{MS} = \frac{\mbox{SS}}{df}
# $$
# 
# 

# regardless of whether we're talking about `drug`, `therapy` or the residuals. To see this, let's not worry about how the sums of squares values are calculated: instead, let's take it on faith that Python has calculated the SS values correctly, and try to verify that all the rest of the numbers make sense. First, note that for the `drug` factor, we divide $3.45$ by $2$, and end up with a mean square value of $1.73$. For the `therapy` factor, there's only 1 degree of freedom, so our calculations are even simpler: dividing $0.47$ (the SS value) by 1 gives us an answer of $0.47$ (the MS value). 
# 
# Turning to the $F$ statistics and the $p$ values, notice that we have two of each: one corresponding to the `drug` factor and the other corresponding to the `therapy` factor. Regardless of which one we're talking about, the $F$ statistic is calculated by dividing the mean square value associated with the factor by the mean square value associated with the residuals. If we use "A" as shorthand notation to refer to the first factor (factor A; in this case `drug`) and "R" as shorthand notation to refer to the residuals, then the $F$ statistic associated with factor A is denoted $F_A$, and is calculated as follows:
# 
# $$
# F_{A} = \frac{\mbox{MS}_{A}}{\mbox{MS}_{R}}
# $$
# 
# To apply this formula to the  `drugs` factor, we take the mean square of $1.73$ and divide it by the residual mean square value of $0.07$, which gives us an $F$-statistic of $26.15$. The corresponding calculation for the `therapy` variable would be to divide $0.47$ by $0.07$ which gives $7.08$ as the $F$-statistic. Not surprisingly, of course, these are the same values that R has reported in the ANOVA table above.
# 
# The last part of the ANOVA table is the calculation of the $p$ values. Once again, there is nothing new here: for each of our two factors, what we're trying to do is test the null hypothesis that there is no relationship between the factor and the outcome variable (I'll be a bit more precise about this later on). To that end, we've (apparently) followed a similar strategy that we did in the one way ANOVA, and have calculated an $F$-statistic for each of these hypotheses. To convert these to $p$ values, all we need to do is note that the  that the sampling distribution for the $F$ *statistic* under the null hypothesis (that the factor in question is irrelevant) is an $F$ *distribution*: and that two degrees of freedom values are those corresponding to the factor, and those corresponding to the residuals. For the `drug` factor we're talking about an $F$ distribution with 2 and 14 degrees of freedom (I'll discuss degrees of freedom in more detail later). In contrast, for the `therapy` factor sampling distribution is $F$ with 1 and 14 degrees of freedom.

# In[ ]:




