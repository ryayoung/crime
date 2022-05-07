<h1> crime &nbsp;&nbsp;&nbsp; <a href="https://pypi.org/project/crime/" alt="Version"> <img src="https://img.shields.io/pypi/v/crime.svg" /></a> </h1>

**[See Github](https://github.com/ryayoung/crime)**

</br>

> Easily load online crime datasts. Explore available datasets from inside a python notebook, with descriptive cell outputs showing general info and descriptions of each dataset and each of its columns.
> 
> With detailed metadata, you'll even see a full list of possible categories in any text column, and a frequency count of each, without ever loading the data.

<br>

## Install & Use

```text
pip install crime
```
```py
import crime as cr
```

> Note: this library should work with any recent Python version, but it has **only been tested with 3.9**. If you're getting errors anywhere, check to make sure you have the latest python version.

---

<br>

# Getting Started

#### First, [get an App Token](#getting_token) from Socrata. It's not required but highly recommended. 

#

Let's look at the crime data available

```py
cr.sources() # returns a DataFrame
```
<img width="800" alt="image" src="https://user-images.githubusercontent.com/90723578/167085160-60aacd51-f4c4-4a7f-8c0b-b62551f42236.png">

> You'll get a df with basic info on all the sources. The index, `Name` is the nickname with which you'll refer to the dataset moving forward. The `Type` column can be "Records" or "Aggregate". Aggregate is usually a small, year-by-year dataset with 30-100 rows, from which you can easily make charts.

<br>

To examine a source, pass the name of the dataset to `sources()`. This will make an api request to get all of its metadata.

But first, please declare your [App Token](#getting_token). Without it, you'll get warnings and throttling.

```py
cr.set_token('XXXXXXXXXX')
```

Let's see the details on `crime_vs_incarceration` rate. All the info below is coming from Socrata's api.

```py
cr.sources('crime_vs_incarceration') 
```

```text
Total Crime Rate vs Incarceration Rate Chart
https://dev.socrata.com/foundry/data.colorado.gov/ae3x-wvn9

Total Crime includes: Violent crimes- Murder and non-negligent manslaughter, 
forcible rape, robbery, and aggravated assault. Property crimes - Burglary,
larceny/theft, and motor vehicle theft. National or state offense totals are
based on data from all reporting agencies and estimates for unreported areas.
Rates are the number of reported offenses per 100,000 population. These
figures are based on end of calendar year populations.

COLUMNS:
-------
Year
  Field:  year
  Type:   text
  Null:   0
  Count:  31

Population
  Field:  population
  Type:   number
  Null:   0
  Count:  31
  Avg:    4019137.064516129
  Max:    5187582
  Min:    3045000
  Sum:    124593249

Violent Crime Total
  Field:  violent_crime_total
  Type:   number
  Null:   0
  Count:  31
  Avg:    16445.54838709677
  Max:    20229
  Min:    13811
  Sum:    509812
```

(output is truncated to save space)

Here's what you'll see for text/categorical columns...

```text
Race
  Field:  race
  Type:   text
  Null:   30
  Count:  209078
  ITEMS:
     White  (164276)
     Black  (39469)
     Asian/Pacific Islander  (2216)
     Unknown  (1901)
     American Indian/Alaskan Native  (1216)
```

# 

Now we'll load some data

```py
cr.load('arrest_demographics')
```

<img width="800" alt="image" src="https://user-images.githubusercontent.com/90723578/167092481-f535265f-8cce-49d7-80e9-318c598d44b9.png">

You'll get a 5-row preview by default, because some datasets have several **million** rows. To get the full dataset:

```py
cr.load('arrest_demographics', full=True)
```
<img width="738" alt="image" src="https://user-images.githubusercontent.com/90723578/167093267-194b382a-ff8c-4a74-ba9f-7bb8e54ac456.png">

<br>


### No proper documentation yet. View the [source code](https://github.com/ryayoung/crime/tree/main/src/crime) if needed.
#### If there's a dataset not yet listed in our pre-defined sources, you can use the [`sodapy`](https://github.com/xmunoz/sodapy) API wrapper to retrieve it with little effort.



</br>

<a id='getting_token'></a>

## Getting your App Token

> Not required, but without one, you'll get warnings and be subject to "strict throttling limits" though it's unclear what those limits are.

### 1. Create a [Socrata account](https://data.colorado.gov/signup)

You just need an email and password.

> This takes you to the Colorado signup page, but your account will be universal for Socrata, so it doesn't matter.

**[Sign up](https://data.colorado.gov/signup)**

### 2. Create App Token

After verifying your email and entering your account, hit **Developer Settings** on the left side of the page.

<img width="450" alt="image" src="https://user-images.githubusercontent.com/90723578/167081904-e097b744-9d13-4ea9-82b7-8912d9989308.png">

#### Click "Create New App Token"

<img width="450" alt="image" src="https://user-images.githubusercontent.com/90723578/167082118-fdc04b27-3e14-4c6a-a53f-0dff5cbc76ca.png">

#### Only two fields are required so you can skip the rest, but 'Application Name' must be unique.

<img width="250" alt="image" src="https://user-images.githubusercontent.com/90723578/167082884-b1a0b7c2-9352-45d6-abfd-aa7d3b892ad4.png">

#### Copy the key

<img width="250" alt="image" src="https://user-images.githubusercontent.com/90723578/167083268-13baf6e4-43aa-44d9-8d74-7747d2503ef0.png">

<br>

<details><summary><i>Where'd you find the signup link?</i></summary>

Find a dataset you want to work with on [Open Data Network](https://www.opendatanetwork.com/search?q=california), then select "View API", and you should get to a page like [this](https://dev.socrata.com/foundry/data.edd.ca.gov/nt76-4rha). Scroll down and find the "Sign up for an app token!" button, and continue. 
</details>
