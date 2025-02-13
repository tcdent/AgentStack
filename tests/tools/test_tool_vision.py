import os
from pathlib import Path
import unittest
from agentstack._tools import ToolConfig


TEST_IMAGE_PATH: Path = Path(__file__).parent.parent / 'fixtures/test_image.jpg'


class VisionToolTest(unittest.TestCase):
    def setUp(self):
        tool = ToolConfig.from_tool_name('vision')
        for dependency in tool.dependencies:
            os.system(f"pip install {dependency}")

    def test_get_media_type(self):
        from agentstack._tools.vision import _get_media_type

        self.assertEqual(_get_media_type("image.jpg"), "image/jpeg")
        self.assertEqual(_get_media_type("image.jpeg"), "image/jpeg")
        self.assertEqual(_get_media_type("http://google.com/image.png"), "image/png")
        self.assertEqual(_get_media_type("/foo/bar/image.gif"), "image/gif")
        self.assertEqual(_get_media_type("image.webp"), "image/webp")
        self.assertEqual(_get_media_type("document.pdf"), None)

    def test_encode_image(self):
        from agentstack._tools.vision import _encode_image

        with open(TEST_IMAGE_PATH, "rb") as image_file:
            encoded_image = _encode_image(image_file)
            print(encoded_image[:200])
            self.assertTrue(isinstance(encoded_image, str))

    def test_analyze_image_web_live(self):
        from agentstack._tools.vision import analyze_image

        if not os.environ.get('ANTHROPIC_API_KEY'):
            self.skipTest("ANTHROPIC_API_KEY not set")

        image_url = "https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png"
        result = analyze_image(image_url)
        self.assertTrue(isinstance(result, str))

    def test_analyze_image_local_live(self):
        from agentstack._tools.vision import analyze_image

        if not os.environ.get('ANTHROPIC_API_KEY'):
            self.skipTest("ANTHROPIC_API_KEY not set")

        result = analyze_image(str(TEST_IMAGE_PATH))
        self.assertTrue(isinstance(result, str))
