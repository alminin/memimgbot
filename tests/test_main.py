import unittest
from decouple import config

class EnvVarsTest(unittest.TestCase):

    def test_token(self):
        self.assertIsNotNone(config('TOKEN'))

    def test_images_dir(self):
        self.assertIsNotNone(config('IMAGES_DIR'))
        # self.assertEqual(config('IMAGES_DIR'), 'images/')
    
    def test_font(self):
        self.assertIsNotNone(config('FONT'))
    
    def test_repost_channel(self):
        self.assertIsNotNone(config('REPOST_CHANNEL'))


if __name__ == '__main__':
    unittest.main()