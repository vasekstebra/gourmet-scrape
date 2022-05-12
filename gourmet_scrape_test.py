#!/usr/bin/env python3

import unittest

from lxml import etree

from gourmet_scrape import process_menu_item, remove_alergens


class TestGourmetScrape(unittest.TestCase):

    def test_remove_alergens_single_alergen(self):
        menu_name = remove_alergens('Polévka *9')
        self.assertEqual('Polévka', menu_name)

    def test_remove_alergens_multiple_alergens(self):
        menu_name = remove_alergens('Menu 1 *1,3,7,10,11')
        self.assertEqual('Menu 1', menu_name)

    def test_process_menu(self):
        row = etree.Element('tr')

        menu_name = etree.SubElement(row, 'td')
        menu_name.text = 'Polévka *9'

        menu_content = etree.SubElement(row, 'td')
        menu_content.text = 'Uzená s bramborami / Vývar dle denní nabídky'

        menu_price = etree.SubElement(row, 'td')
        menu_price.text = '23 Kč'

        menu = process_menu_item(row)
        expected_menu = '**Polévka:** Uzená s bramborami / Vývar dle denní nabídky (23 Kč)\n\n'
        self.assertEqual(expected_menu, menu)
        

if __name__ == '__main__':
    unittest.main()

