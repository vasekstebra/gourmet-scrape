#!/usr/bin/env python3

import unittest

import lxml.html

from gourmet_scrape import process_menu_item, remove_alergens


class TestGourmetScrape(unittest.TestCase):

    def test_remove_alergens_single_alergen(self):
        menu_name = remove_alergens('Polévka *9')
        self.assertEqual('Polévka', menu_name)

    def test_remove_alergens_multiple_alergens(self):
        menu_name = remove_alergens('Menu 1 *1,3,7,10,11')
        self.assertEqual('Menu 1', menu_name)

    def test_process_menu(self):
        row = lxml.html.fromstring('''
            <tr>
                <td>Polévka *9</td>
                <td>Uzená s bramborami / Vývar dle denní nabídky</td>
                <td>23 Kč</td>
            </tr>
        ''')

        menu = process_menu_item(row)
        expected_menu = '**Polévka:** Uzená s bramborami / Vývar dle denní nabídky (23 Kč)\n\n'
        self.assertEqual(expected_menu, menu)
        

if __name__ == '__main__':
    unittest.main()

