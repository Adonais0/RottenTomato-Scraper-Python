import unittest
from SI507F17_finalproject import *

class Cache(unittest.TestCase):
    def setUp(self):
        self.url = open("url.csv")
        self.data = open("data.csv")
        self.js = open("cache_contents.json")

    def test_files_exist(self):
        self.assertTrue(self.url.read())
        self.assertTrue(self.data.read())
        self.assertTrue(self.js.read())

    def tearDown(self):
        self.url.close()
        self.data.close()
        self.js.close()

class Movie(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.rottentomatoes.com/m/keplers_dream'
        self.data = CACHE_DICTION[self.url]#return html
        self.soup_movie_inst = BeautifulSoup(self.data, 'html.parser')
        self.sample_inst = Movie(self.soup_movie_inst)

    def test_movie_constructor(self):
        self.assertIsInstance(self.sample_inst.name,"str")
        self.assertIsInstance(self.sample_inst.genre, "str")
        self.assertIsInstance(self.sample_inst.director, str)
        self.assertIsInstance(self.sample_inst.data, str)
        self.assertIsInstance(self.sample_inst.tomato_meter, int)
        self.assertIsInstance(self.sample_inst.tomato_num, int)
        self.assertIsInstance(self.sample_inst.audience_score, int or None)
        self.assertIsInstance(self.sample_inst.audience_num, int or None)
        self.assertIsInstance(self.sample_inst.genre, boxoffice, int or None)

    def test_movie_string(self):
        self.assertEqual(self.sample_inst.__str__(),"\nMovie Name: Kepler's Dream(2017)\n Meter: 50")
    def test_movie_repr(self):
        self.assertEqual(self.sample_inst.__repr__(),"\nMovie Name: Kepler's Dream(2017)")
    def test_movie_contain(self):
        self.assertTrue("le" in self.sample_inst)
        self.assertTrue("50" not in self.sample_inst)

class movieList(unittest.TestCase):
    def setUp(self):
        pass
    def test_list_movies(self):
        self.assertIsInstance(movie_list,list)
    def test_list_elem_types(self):
        print(type(movie_list[1]))
        self.assertIsInstance(movie_list[1],Movie)

if __name__ == '__main__':
    unittest.main(verbosity=2)
