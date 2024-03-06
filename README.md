

# unidiscover_scraper
# About the Project
simple scrapy project using python Scrapy for [unidiscover](https://discoveruni.gov.uk/) to scrape university course information including but not limited to:
  1. course description
  2. salary
  3. employment

Final output as a csv table in **discover_uni(1).csv**.

Blow is part of the first 5 row:

|    | courseidentifier                       | uniname                   | uniid   | coursename                             | link                                                    | course_name                           | Study mode | Distance learning | Placement year | Year abroad |
|----|-----------------------------------------|---------------------------|---------|----------------------------------------|---------------------------------------------------------|---------------------------------------|------------|-------------------|----------------|-------------|
| 0  | 10008071/AAUNDERRADUATE5YEAR/Full-time  | AA School of Architecture | 10008071| MArch Architecture                    | /course-details/10008071/AAUNDERRADUATE5YEAR/Full-time  | MArch Architecture                    | Full time  | Not Available     | Not Available  | Not Available|
| 1  | 10007783/LV61/Full-time                 | University of Aberdeen    | 10007783| MA (Hons) Anthropology and History     | /course-details/10007783/LV61/Full-time                 | MA (Hons) Anthropology and History    | Full time  | Not Available     | Not Available  | Optional     |
| 2  | 10007783/LV65/Full-time                 | University of Aberdeen    | 10007783| MA (Hons) Anthropology and Philosophy  | /course-details/10007783/LV65/Full-time                 | MA (Hons) Anthropology and Philosophy | Full time  | Not Available     | Not Available  | Optional     |
| 3  | 10007783/LR61/Full-time                 | University of Aberdeen    | 10007783| MA (Hons) Anthropology and French      | /course-details/10007783/LR61/Full-time                 | MA (Hons) Anthropology and French     | Full time  | Not Available     | Not Available  | Compulsory   |
| 4  | 10007783/LQ65/Full-time                 | University of Aberdeen    | 10007783| MA (Hons) Anthropology and Gaelic      | /course-details/10007783/LQ65/Full-time                 | MA (Hons) Anthropology and Gaelic     | Full time  | Not Available     | Not Available  | Optional     |


Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
# Built With
- <p align="left"> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="322" height="100"/> </a> </p>
- <p align="left"> <a href="https://github.com/scrapy/scrapy" target="_blank" rel="noreferrer"> <img src="https://camo.githubusercontent.com/de54ffbef2c6d880ea66ce4b89cbbf21385b4f0c9318907a4f51110272aa9925/68747470733a2f2f7363726170792e6f72672f696d672f7363726170796c6f676f2e706e67" alt="Scrapy" width="322" height="100"/> </a> </p>
- <p align="left"> <a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="322" height="100"/>

# Getting Started

### Prerequisites
-   Python 3.8+
-   Works on Linux, Windows, macOS, BSD

### Install
The quick way:
```
pip install scrapy
```
## Usage
```
scrapy crawl unispider -o course_data_40page.json
```

- output raw data as to course_data_40page.json as json file
- convert the json file into csv tabular format in **convert json to csv.ipynb**



## To-do
- define output as items
- connect to a DB

