from django.test import TestCase
from .models import WorldBorder


class TestIndexView(TestCase):
    def setUp(self):
        self.url = ""
        self.res = self.client.get(self.url)

    def test_view_returns_200_on_get_request(self):
        self.assertEqual(self.res.status_code, 200)

    def test_view_returns_correct_template_name(self):
        self.assertTemplateUsed(self.res, "world/indexpage.html")

    def test_view_does_not_support_post_request(self):
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, 405)


class TestHomePageView(TestCase):
    def setUp(self):
        self.url = "/world/homepage/"
        self.res = self.client.get(self.url)

    def test_view_returns_200_on_get_request(self):
        self.assertEqual(self.res.status_code, 200)

    def test_view_returns_correct_template_name(self):
        self.assertTemplateUsed(self.res, "world/homepage.html")

    def test_view_does_not_support_post_request(self):
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, 405)


class TestLocationDetailView(TestCase):
    def setUp(self):
        self.url = "/world/details/?latitude={}&longitude={}"

    def test_view_returns_200_for_weather_api_working(self):
        url = self.url.format("39.7456", "-97.0892")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_assert_correct_template_used(self):
        url = self.url.format("39.7456", "-97.0892")
        res = self.client.get(url)

        self.assertTemplateUsed(res, "world/detail.html")

    def test_msg_returned_when_weather_api_is_giving_404(self):
        msg = "Weather API is giving 404 for this latitude and longitude"
        url = self.url.format("36.7783", "119.4179")

        res = self.client.get(url)

        self.assertIn(msg, res.content.decode('utf-8'))

