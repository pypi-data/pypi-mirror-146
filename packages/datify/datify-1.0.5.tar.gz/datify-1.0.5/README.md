# Datify
This Python3 module allows extracting parts of valid date from user input.
User input is processed through class `Datify`.
## Languages supported: 
- [x] English
- [x] Russian  -  [Readme на русском](README-ru.md) 
- [x] Ukrainian.

---

## Installing
Simply run `pip install datify` from your command line (pip must be installed).


## Class:
` Datify(user_input, year, month, date) ` : takes str when creating. Also, can take particular parameters like `year`, `month`, and `day` along with user input or without it. If no parameters are given, raises ValueError. **See the section [*Formats*](#default-formats) to discover default Datify's formats.**
### Class methods:
  #### Static:
  1. `find_date(string)` : Takes string. Returns substring with date in General Date format if it is contained in the given string.
  2. `is_year(year)` : Takes str or int. Returns True if given parameter suits year format.
  3. `is_digit_month(month)` : Takes str or int. Returns True if given parameter suits digit month format.
  4. `is_alpha_month(string)` : Takes str. Returns True if given string suits months dictionary. *For languages in which there are multiple forms of words it's basically enough to have only the main form of the word in dictionary.*
  5. `get_alpha_month(string)` :  Takes str. Returns number(int) of month name in given string according to months dictionary. If no month name is found in the string, returns None.
  6. `is_day(day)` : Takes str or int. Returns True if given parameter suits day format.
  7. `is_date(date)` : Takes str or int. Returns True if given parameter suits general date format (See the section [*Formats*](#default-formats)).
  8. `is_date_dart(string)` : Takes str. Returns True if given string contains at least one of date parts such as day, month, or year.

  #### Instance:
  1. `date()` : returns datetime object from parameters of Datify object. If not all of the necessary parameters are known (`year`, `month`, and `day`), raises TypeError.
  2. `tuple()` : returns tuple from all parameters in format (day, month, year).
  3. `date_or_tuple()` : returns datetime object if all of the necessary parameters are known, otherwise returns tuple of all parameters.
  4. `set_year(year)` : Takes str or int. Extracts year from given parameter and sets `year` field of the called Datify object. If given parameter doesn't suit year format, raises ValueError. *If the year is given in shortened format, counts it as 20YY.*
  5. `set_month(month)` : Takes str or int. Extracts month from given parameter and sets `month` field of the called Datify object. If given parameter doesn't suit month format and doesn't contain any month names, raises ValueError.
  6. `set_day(day)` : Takes str or int. Extracts day from given parameter and sets `day` field of the called Datify object. If given parameter doesn't suit day format, raises ValueError.

## Default formats:
> **Note that in this module the day is checked firstly, the month - after it. `06.07.2021` stands for `6th of July, 2021`!**
- General date format:
  `'[12][01]\d\d[01]\d[0123]\d$'` - `YYYYMMDD` - e.g. `20210706`
- Day formats:
  0 < day <= 31
  - For digit-only entries: `'[0123]?\d$'` - `D?D` - e.g. `13`, `05`, `6` etc.
  - For alpha-numeric entries: `'[0123]?\d\D+$'` - e.g. `1st`, `2nd`, `25th`, `3-е` etc.
- Month formats:
  0 < month <= 12
  - For digit-only entries: `'[01]?\d$'` - `M?M` - e.g. `06`, `7` etc.
  - For alphabethic strings: tries to find similar words in months dict.
- Year format:
  `'([012]\d\d\d$)|(\d\d$)'` - `YYYY` or `YY` - e.g. `2021` or `21`.
  > Note that if shortened year `YY` is given, it counts as `20YY`.

## Config:
You can customize splitters list, and change format of the all date parts, accessing them using `Datify.config['KEY']`.
Also, you can choose, what is coming first: a day or a month.

Dict keys:
1. Splitters : `'SPLITTERS'` -- set of the separators. Contains ` `, `.`, `-`, and `/` by default.
2. Formats (See section [*Formats*](#default-formats)) :
  - Digit day : `'FORMAT_DAY_DIGIT'`
  - Alpha-numeric day : `'FORMAT_DAY_ALNUM'`
  - Digit month : `'FORMAT_MONTH_DIGIT'`
  - Digit year : `'FORMAT_YEAR_DIGIT'`
  - General date : `'FORMAT_DATE'`
3. Day is first? : `'DAY_FIRST'` -- bool. If True, a day is being found first. If False, a month is being found first. True by default.

For example:
```python
Datify('17_06_2021')  # ValueError  # Not works
Datify.config['SPLITTERS'].add('_')  # Adding new separator to the set
Datify('17_06_2021')  # <Datify object (17, 6, 2021)>  # Works!
```
Changing the order of a day and a month:
```python
Datify('10.12').month  # 12
Datify.config['DAY_FIRST'] = False
Datify('10.12').month  # 10
```

---

## Examples:
I'll use different date formats in every example to show that Datify can handle them all. Let's begin!
```python
from datify import Datify  # Importing our main class
```
1. Extracting date from string with a Datify object
```python
user_input = '06.07.2021'  # Imitating user input. Note that day is first!
val = Datify(user_input)
print(val)  # Output: <Datify object (6, 7, 2021)>
```
Any string can be processed this way.

2. Getting exact date parameters from Datify
```python
user_input = '06/07'
val = Datify(user_input)

date_day = val.day  # 6
date_month = val.month  # 7
date_year = val.year  # None
```

3. Getting date in **datetime** object
```python
user_input = '06-07-21'
date = Datify(user_input).date()  # 2021-07-06 00:00:00
```
If there is a possibility to get an incomplite date, datetime will raise TypeError:
```python
user_input = '06/07'
date = Datify(user_input).date()  # TypeError: an integer is required (got type NoneType)
```
Use the other examples instead, if there is a chanse to get incomplete date.

4. Getting output in a **tuple**:
Order of values: day, month, year
```python
user_input = '6th of July 2021'
Datify(user_input).tuple()  # (6, 7, 2021)

user_input = '6th of July'
Datify(user_input).tuple()  # (6, 7, None)
```

5. Getting alphapetic month without creating Datify object
```python
Datify.get_alpha_month('february')  # 2
```
7. Various checks for strings
```python
# Check for any date part
Datify.is_date_part('6')  # True (may be day or month)
Datify.is_date_part('31')  # True
Datify.is_date_part('june')  # True
Datify.is_date_part('jan')  # True
Datify.is_date_part('33')  # True (it might be year in `YY` spelling)
Datify.is_date_part('333')  # False
Datify.is_date_part('3131')  # False (it doesn't suit year format (from `10YY` to `21YY`))

# Check for date in General Date format
Datify.is_date('20210607')  # True

# Checks for particular date parts

# Year
Datify.is_year('2021')  # True
Datify.is_year('221')  # False

# Month
Datify.is_digit_month('11')  # True (0 < str <= 12)
Datify.is_alpha_month('June')  # True

# Day
Datify.is_day('13')  # True (0 < str <= 31)
```

8. Getting date in General Date format from any string
```python
user_input = 'created "20200120"'
Datify.find_date(user_input)  # '20200120'
```

9. Parameters of an existing Daitfy object can be modified this way
```python
res = Datify('6th of July, 2021')  # <Datify object (6, 7, 2021)>
res.set_year(2018)
print(res.date())  # 2018-07-06 00:00:00
```
Also exact parameters can be set during creating object:
```python
Datify('6th of July, 2021', year=2018, month=3)  # <Datify object (6, 3, 2018)>
```

*Datify is much more powerful than you may think.*
