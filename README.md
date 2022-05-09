<h1> crime &nbsp;&nbsp;&nbsp; <a href="https://pypi.org/project/crime/" alt="Version"> <img src="https://img.shields.io/pypi/v/crime.svg" /></a> </h1>

#### [View Updated Documentation](https://github.com/ryayoung/crime)

Source code is [here](https://github.com/ryayoung/crime/tree/main/src/crime)

</br>

> Easily load online crime datasts. Explore available datasets from inside a python notebook, with descriptive cell outputs showing general info and descriptions of each dataset and documentation of each column.

<br>

## Install & Use

```text
pip install crime
```
```py
import crime as cr
```

Later, run `pip install -U crime` every few days to make sure you've got the latest version.

> Note: this library should work with any recent Python version, but it has **only been tested with 3.9**.

---

<br>

<details><summary><b>How does it work?</b></summary>

Crime pre-defines nicknames and ids for a collection of Socrata datasets [like this one](https://dev.socrata.com/foundry/data.edd.ca.gov/nt76-4rha) for you to pick from. This info isn't stored in the package itself, but rather in [this json file](https://github.com/ryayoung/crime/blob/main/colorado-crime-datasets-doc.json) on Github, which can be updated anytime without changing the code. Every time you import `crime`, a Github API request is made to retrieve this configuration, so you'll need internet. Calling `cr.sources()` without parameters will just return this info, without making any additional requests.

In addition to letting you load/preview any of these datasets, `crime`'s most important feature is its ability to show a detailed description on each dataset, with full documentation on every column. When you run `cr.sources('dataset_name')`, an api request is made to Socrata to get the metadata on a particular dataset. The most useful information gets formatted & printed to your screen. [Here](https://github.com/ryayoung/crime/blob/main/all_data_info.txt) is what that output would look like if you looped through each dataset name and printed its description.

**Caching:** Any dataset you load fully will get stored in memory. So next time you request it within the same Jupyter notebook session, it will be available immediately.

</details>

---

<br>

# Getting Started

<!-- #### First, [get an App Token](#getting_token) from Socrata. Not required but highly recommended.  -->

<!-- # -->

> Use `cr.help()` for a quick intro.

#

Let's look at the crime data available

```py
cr.sources() # returns a DataFrame
```
<img width="800" alt="image" src="https://user-images.githubusercontent.com/90723578/167237471-51ad543b-9422-4285-a35f-72562c6431bc.png">

> You'll get a DataFrame with basic info on all the sources. The index, `Name` is the nickname with which you'll refer to the dataset moving forward.

<br>

To examine a source, pass the name of the dataset to `sources()`. This will make an api request to get all of its metadata.

<!-- But first, please declare your [App Token](#getting_token). Without it, you'll get warnings and throttling. -->

<!-- ```py -->
<!-- cr.set_token('XXXXXXXXXX') -->
<!-- ``` -->

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

Returns 5-row preview by default, because some datasets have several **million** rows. To get the full dataset:

```py
cr.load('arrest_demographics', full=True)
```
<img width="738" alt="image" src="https://user-images.githubusercontent.com/90723578/167093267-194b382a-ff8c-4a74-ba9f-7bb8e54ac456.png">

#

### Get more info on a source
Return dictionary with full metadata
```py
cr.metadata('dataset_name')
```
Return dataframe with metrics on each column
```py
cr.columns('dataset_name')
```

#

### Caching
> Any dataset you load fully (by passing `full=True`) will only have to be downloaded from the internet once during your notebook session, regardless of whether you've assigned it to a variable.
> 
> After you fully load a dataset, you can leave out the `full=True` next time you want to access it, and the full dataframe will be returned instantly. Or, you can use `cr.df('name')` to fetch straight from the cache.

For example, if you run this at the top of your notebook...
```py
cr.load('arrest_demographics', full=True)
```
Now, elsewhere in your notebook...

EITHER of these 3 lines will return the same thing: the full dataset
```py
cr.load('arrest_demographics', full=True)
```
```py
cr.load('arrest_demographics')
```
```py
# Shorthand to fetch straight from the cache. Returns empty df if none are found in cache
cr.df('arrest_demographics')
```

#

### How to define your own set of data sources.
> First, select a dataset on [OpenDataNetwork](https://www.opendatanetwork.com/) and hit "View API". If you're brought to an API page [like this one](https://dev.socrata.com/foundry/data.colorado.gov/4ykn-tg5h), (not all datasets have one), locate the "Dataset Identifier" on top-right side of page. Use that as `id`. For `base_url`, use the section of the url that comes after `/foundry/`.
```py
# Pass a dictionary
cr.set_sources(
    {
        'district_arrests': { # this is the nickname you'll refer to
            "id": "2e5i-5hfy",
            "base_url": "data.colorado.gov"
        },
        'district_crime': {
            "id": "ya69-n6ta",
            "base_url": "data.colorado.gov"
        },
        # etc...
    }
)
```
To restore the original list of sources, use:
```py
cr.reset_sources()
```



<br>


### No proper documentation yet. View the [source code](https://github.com/ryayoung/crime/tree/main/src/crime) if needed.
#### If there's a dataset not yet listed in our pre-defined sources, you can use the [`sodapy`](https://github.com/xmunoz/sodapy) API wrapper to retrieve it manually.



</br>

<!-- <a id='getting_token'></a>

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
</details> -->
