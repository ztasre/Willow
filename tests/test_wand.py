import unittest
import io
import imghdr

from willow.backends import wand as wand_backend


class TestWandOperations(unittest.TestCase):
    def setUp(self):
        with open('tests/images/transparent.png', 'rb') as f:
            self.image = wand_backend.WandBackend.from_file(f)

    def test_get_size(self):
        width, height = self.image.get_size()
        self.assertEqual(width, 200)
        self.assertEqual(height, 150)

    def test_resize(self):
        self.image.resize((100, 75))
        self.assertEqual(self.image.image.size, (100, 75))

    def test_crop(self):
        self.image.crop((10, 10, 100, 100))
        self.assertEqual(self.image.image.size, (90, 90))

    def test_save_as_jpeg(self):
        output = io.BytesIO()
        self.image.save_as_jpeg(output)
        output.seek(0)

        self.assertEqual(imghdr.what(output), 'jpeg')

    def test_save_as_png(self):
        output = io.BytesIO()
        self.image.save_as_png(output)
        output.seek(0)

        self.assertEqual(imghdr.what(output), 'png')

    def test_save_as_gif(self):
        output = io.BytesIO()
        self.image.save_as_gif(output)
        output.seek(0)

        self.assertEqual(imghdr.what(output), 'gif')

    def test_has_alpha(self):
        has_alpha = self.image.has_alpha()
        self.assertTrue(has_alpha)

    def test_has_animation(self):
        has_animation = self.image.has_animation()
        self.assertFalse(has_animation)

    def test_transparent_gif(self):
        with open('tests/images/transparent.gif', 'rb') as f:
            image = wand_backend.WandBackend.from_file(f)

        self.assertTrue(image.has_alpha())
        self.assertFalse(image.has_animation())

        # Check that the alpha of pixel 1,1 is 0
        self.assertEqual(image.image[1][1].alpha, 0)

    def test_resize_transparent_gif(self):
        with open('tests/images/transparent.gif', 'rb') as f:
            image = wand_backend.WandBackend.from_file(f)

        image.resize((100, 75))

        self.assertTrue(image.has_alpha())
        self.assertFalse(image.has_animation())

        # Check that the alpha of pixel 1,1 is 0
        self.assertAlmostEqual(image.image[1][1].alpha, 0, places=6)

    def test_animated_gif(self):
        with open('tests/images/newtons_cradle.gif', 'rb') as f:
            image = wand_backend.WandBackend.from_file(f)

        self.assertTrue(image.has_animation())

    def test_resize_animated_gif(self):
        with open('tests/images/newtons_cradle.gif', 'rb') as f:
            image = wand_backend.WandBackend.from_file(f)

        image.resize((100, 75))

        self.assertTrue(image.has_animation())
