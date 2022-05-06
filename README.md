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
cr.set_token('XXXXXXXXXX') # your token here
```

Let's see the details on `arrest_demographics`. All the info below is coming from Socrata's api.

```py
cr.sources('arrest_demographics')
```

```text
Arrest Data with all Offenses and Demographic Detail
https://dev.socrata.com/foundry/policedata.coloradosprings.gov/jw9n-x43p

This dataset includes all arrests with all offenses listed for each arrest.  Each
offense lists the demographic information for the person arrested for that offense.
There may be multiple offenses for an arrestee.  This dataset should only be used
for counting the number of offenses related to arrests.

COLUMNS:
-------
```


<details><summary><b>SHOW OUTPUT</b></summary>

```text
Arrest Data with all Offenses and Demographic Detail
https://dev.socrata.com/foundry/policedata.coloradosprings.gov/jw9n-x43p

This dataset includes all arrests with all offenses listed for each arrest.  Each
offense lists the demographic information for the person arrested for that offense.
There may be multiple offenses for an arrestee.  This dataset should only be used
for counting the number of offenses related to arrests.

COLUMNS:
-------
Case Number
  Type: text
  Null: 71
  Non-Null: 208937

Arrest Number
  Type: text
  Null: 0
  Non-Null: 209008

Arrest Date Time
  Type: calendar_date
  Null: 0
  Non-Null: 209008

Arrest Type
  Type: text
  Null: 209008
  Non-Null: 0

Age Category
  Type: text
  Null: 0
  Non-Null: 209008
  ITEMS:
     Adult  (200847)
     Juvenile  (8161)

Crime Code
  Type: text
  Null: 0
  Non-Null: 209008

Crime Code Description
  Type: text
  Null: 0
  Non-Null: 209008
  ITEMS:
     All Other Offenses (Except Traffic)  (69395)
     Not Reportable  (21108)
     Driving Under the Influence  (18243)
     Trespass of Real Property  (13704)
     Shoplifting  (11132)
     Drug/Narcotic Violations  (9819)
     Simple Assault  (8084)
     Aggravated Assault  (6645)
     Destruction/Damage/Vandalism of Property  (6508)
     Drug Equipment Violations  (4769)
     Burglary/Breaking & Entering  (3621)
     Family Offenses/Nonviolent  (3552)
     Weapons Law Violations  (3474)
     Motor Vehicle Theft  (3422)
     Intimidation  (3052)
     Disorderly Conduct/Disturbing The Peace  (2482)
     All Other Larceny  (2426)
     Theft From Building  (1890)
     Liquor Law Violations  (1830)
     Identity Theft  (1716)

NCIC Code
  Type: number
  Null: 21452
  Non-Null: 187556
  Max: 7399.0
  Min: 199.0

NCIC Code Description
  Type: text
  Null: 21452
  Non-Null: 187556
  ITEMS:
     Driving Under Influence Liquor  (17555)
     Failure to Appear  (15293)
     Trespassing (describe offense)  (13701)
     Contempt of Court  (13012)
     Harassing Communication  (11439)
     Shoplifting  (11125)
     Public Order Crimes  (9771)
     Flight to Avoid-(Prosecution, confinement, etc.)  (8588)
     Simple Assault  (8084)
     Damage Property-Private  (4965)
     Narcotic Equipment - Possess  (4770)
     Amphetemine - Possess  (4219)
     Cruelty Toward Child  (3513)
     Vehicle Theft  (3420)
     Intimidation (Includes Stalking)  (3050)
     Obstruct Police (Describe Offense)  (2906)
     Larceny (Describe Offense)  (2135)
     Larceny-From Building  (1815)
     Possession of Weapon (specify weapon)  (1814)
     Liquor - Possess  (1792)

Statute or Ordinance
  Type: text
  Null: 0
  Non-Null: 209008

Statute or Ordinance Description
  Type: text
  Null: 0
  Non-Null: 209008
  ITEMS:
     Driving under the influence - alcohol (DUI)  (9774)
     FUGITIVE OTHER JURISDICTION WARRANT  (7797)
     Harassment - Strike, Shove, or Kick  (7741)
     3rd Degree Assault - BI to Another - Simple Assault  (7388)
     SHOPLIFTING  (7354)
     FTA/FTP/FTC El Paso County Traffic Bench Warrants  (6988)
     Driving under the influence - blood alcohol content .08 or m  (6755)
     TRESPASS ON PRIVATE PROPERTY  (6362)
     Failure to Appear  (5385)
     FTA El Paso County Misdemeanor Criminal Bench Warrant  (5179)
     CONTEMPT OF COURT  (4834)
     Possession of Drug Paraphernalia  (4583)
     Repealed - Possess Schedule I, II, Flunitrazepam,  Ketamine,  (4405)
     FTA El Paso County Criminal Felony Bench Warrant  (2963)
     Violation of a Protection Order - MPO  (2927)
     Careless Driving-Accident  (2901)
     Driving Under Restraint - Drove Vehicle w/ License Under Res  (2510)
     CONTEMPT OF COURT-COC  (2192)
     Child Abuse - Knowingly/Recklessly  - NO Injury  (2105)
     Violation of a Protection Order  (2004)

Age At Arrest
  Type: number
  Null: 10
  Non-Null: 208998
  Max: 101.0
  Min: 9.0

Age Range
  Type: text
  Null: 0
  Non-Null: 209008

Race
  Type: text
  Null: 30
  Non-Null: 208978
  ITEMS:
     White  (164243)
     Black  (39406)
     Asian/Pacific Islander  (2214)
     Unknown  (1899)
     American Indian/Alaskan Native  (1216)

Gender
  Type: text
  Null: 4
  Non-Null: 209004
  ITEMS:
     Male  (153038)
     Female  (55833)
     Unknown  (125)
     Non-Binary  (8)

Ethnicity
  Type: text
  Null: 90
  Non-Null: 208918
  ITEMS:
     Non Hispanic Origin  (163973)
     Hispanic  (36591)
     Unknown  (8354)

Arrest Location
  Type: text
  Null: 7428
  Non-Null: 201580

City
  Type: text
  Null: 3361
  Non-Null: 205647
  ITEMS:
     COLORADO SPRINGS  (203005)
     FOUNTAIN  (424)
     FALCON  (227)
     PUEBLO  (183)
     MANITOU SPRINGS  (178)
     FORT CARSON  (170)
     Colorado Springs  (166)
     Denver  (120)
     Golden  (90)
     MONUMENT  (82)
     PETERSON AFB  (77)
     DIVIDE  (48)
     CASTLE ROCK  (45)
     USAF ACADEMY  (43)
     Canon City  (43)
     CENTENNIAL  (34)
     CRIPPLE CREEK  (31)
     Castle Rock  (30)
     DENVER  (29)
     BLACK FOREST  (28)

Zip Code
  Type: text
  Null: 6456
  Non-Null: 202552

Location Point
  Type: point
  Null: 16128
  Non-Null: 192880
  ITEMS:
     {'coordinates': [-104.777148, 38.789016], 'type': 'Point'}  (10815)
     {'coordinates': [-104.799951, 38.838812], 'type': 'Point'}  (8460)
     {'coordinates': [-104.822327, 38.824511], 'type': 'Point'}  (6690)
     {'coordinates': [-104.76814, 38.840052], 'type': 'Point'}  (3568)
     {'coordinates': [-104.840147, 38.824583], 'type': 'Point'}  (3418)
     {'coordinates': [-104.822473, 38.817906], 'type': 'Point'}  (2090)
     {'coordinates': [-104.723441, 38.853379], 'type': 'Point'}  (1947)
     {'coordinates': [-104.714681, 38.891221], 'type': 'Point'}  (1901)
     {'coordinates': [-104.758533, 38.96597], 'type': 'Point'}  (1418)
     {'coordinates': [-104.8431, 38.824914], 'type': 'Point'}  (1344)
     {'coordinates': [-104.823732, 38.83086], 'type': 'Point'}  (1334)
     {'coordinates': [-104.820181, 38.864326], 'type': 'Point'}  (1208)
     {'coordinates': [-104.750955, 38.811371], 'type': 'Point'}  (1136)
     {'coordinates': [-104.828812, 38.837017], 'type': 'Point'}  (1083)
     {'coordinates': [-104.80397, 38.944961], 'type': 'Point'}  (1024)
     {'coordinates': [-104.82644, 38.834634], 'type': 'Point'}  (889)
     {'coordinates': [-104.822395, 38.807876], 'type': 'Point'}  (773)
     {'coordinates': [-104.82957637104, 38.8185852544053], 'type'  (755)
     {'coordinates': [-104.82068, 38.835227], 'type': 'Point'}  (746)
     {'coordinates': [-104.823293, 38.838124], 'type': 'Point'}  (590)

Patrol Division
  Type: text
  Null: 16178
  Non-Null: 192830
  ITEMS:
     Gold Hill  (75072)
     Sand Creek  (61486)
     Stetson Hills  (30377)
     Falcon  (25895)

Neighborhoods
  Type: number
  Null: None
  Non-Null: None
```

</details>


Notice the text/categorical columns...

```text
Race
  Type: text
  Null: 30
  Non-Null: 208978
  ITEMS:
     White  (164243)
     Black  (39406)
     Asian/Pacific Islander  (2214)
     Unknown  (1899)
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
