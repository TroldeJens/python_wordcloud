import unittest
import create_wordcloud
  
class UnitTests(unittest.TestCase):

    def test_capitalize_first_letter(self):
        testInputAndExpectedResult = {
            "McDonald": "McDonald",
            "mcDonald": "McDonald",
            "old mcDonald": "Old mcDonald",
            "Old McDonald": "Old McDonald",
            "old mcDonald": "Old mcDonald",
            "22bicycles": "22bicycles",
            "22 bicycles": "22 bicycles",
            "now, there's a bugger": "Now, there's a bugger",
        }

        for input, expectedResult in testInputAndExpectedResult.items():
            actualResult = create_wordcloud.capitalize_first_letter(input)
            self.assertEqual(actualResult, expectedResult)

    def test_capitalize_first_letter_of_every_word(self):
        testInputAndExpectedResult = {
            "McDonald": "McDonald",
            "mcDonald": "McDonald",
            "old mcDonald": "Old McDonald",
            "Old McDonald": "Old McDonald",
            "22bicycles": "22bicycles",
            "22 bicycles": "22 Bicycles",
            "now, there's a bugger": "Now, There's A Bugger",
        }

        for input, expectedResult in testInputAndExpectedResult.items():
            actualResult = create_wordcloud.capitalize_first_letter_of_every_word(input)
            self.assertEqual(actualResult, expectedResult)
  
if __name__ == '__main__':
    unittest.main()