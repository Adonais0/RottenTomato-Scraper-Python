# Final Project of SI 507
 * Target: Scrape 2000 movie information from [Rotten Tomato](https://www.rottentomatoes.com/browse/dvd-streaming-all/)
 * __Please download the [Cache File](https://drive.google.com/a/umich.edu/file/d/182RyW3mWL1yeghIf4r4tB3R5ZslDu_CT/view?usp=sharing) first!__

##Please run files following this sequence:
1. __Download the cache file__ (or you will have to wait for around 1 hour to get the data)
2. `pip3 install -r requirements.txt`
2. Run `SI507F17_finalproject.py`
3. Create a database named `chuyao_507finalproject`
3. Run `database_setup.py` to setup database
4. Run `database_insert_and_query.py` to insert data and make queries
5. Create a `plotlyconfig.py` and fill in with your own Plotly config.(You can refer to `plotlyconfig_example.py`)
6. Run `draw.py`
7. Run `SI507F17_finalproject_test.py`

## Project Description
### Run SI507F17_finalproject.py:
1. Cache 2000 urls of movies from [this page]('https://www.rottentomatoes.com/browse/dvd-streaming-all') into `url.csv`. Since the page is written with javascript, I used `PhantomJS` to fake-click the `show more` button.  

2. Use `url.csv` to scrape 2000 pages of movie's information. Cache the json data into `cache_contents.json`

3. Create a class: `Movie()` , a Movie instance includes following attributes:

  * Movie Name
  * Genre
  * Director
  * Date in Theatre
  * Box Office
  * Tomato Meter
  * Tomato Meter Number
  * Audience Score
  * Audience Number

4. Store the 2000 movie information into `data.csv`

### Run database_setup.py:
 * Includes 2 tables
     * `basic_info_of_movie`
         * `name (PRIMARY KEY)`
         * `genre`
         * `director`
         * `time_in_theatre`
         * `boxoffice`
     * `tomato_meter`
         * `movie_id (PRIMARY KEY)`
         * `name (FOREIGN KEY)`
         * `tomato_meter`
         * `tomato_num`
         * `audience_score`
         * `audience_num`
 * `database_insert_and_query.py`   
        *  insert 2000 data into two tables

### Run draw.py:

Use [Plotly](https://plot.ly/) to visualize the scatter relation between the tomato meter and audience score, and the relation between the tomato meter and genre.

![Image of Scatter](https://github.com/Adonais0/SI507-F17-FinalProject/blob/master/images/new_scatter.png?raw=true)

![Image of Box](https://github.com/Adonais0/SI507-F17-FinalProject/blob/master/images/newplot.png?raw=true)
