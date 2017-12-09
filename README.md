# Final Project of SI 507
 * Target: Scrape 2000 movie information from https://www.rottentomatoes.com/browse/dvd-streaming-all/
## Class movie
### A Movie instance includes following:
     * Movie Name
     * Genre
     * Director
     * Date in Theatre
     * Box Office
     * Tomato Meter
         * Including how many people review
     * Audience Score
         * Including how many people review
## Database tables
 * Including 2 tables
     * basic_info_of_movie
         * name (PRIMARY KEY)
         * genre
         * director
         * time_in_theatre
         * boxoffice
     * tomato_meter
         * movie_id (PRIMARY KEY)
         * name (FOREIGN KEY)
         * tomato_meter
         * tomato_num
         * audience_score
         * audience_num
 * Need to uncomment the setup_database() in the first time
## Visual
