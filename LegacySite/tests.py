
from django.test import TestCase , Client
from LegacySite.models import Card
# Create your tests here.

class MyTest(TestCase):
    # Django's test run with an empty database. We can populate it with
    # data by using a fixture. You can create the fixture by running:
    #    mkdir LegacySite/fixtures
    #   python manage.py dumpdata LegacySite > LegacySite/fixtures/testdata.json
    # You can read more about fixtures here:
    #    https://docs.djangoproject.com/en/4.0/topics/testing/tools/#fixture-loading
    fixtures = ["testdata.json"]

    # Assuming that your database had at least one Card in it, this
    # test should pass.
    def test_get_card(self):
        allcards = Card.objects.all()
        self.assertNotEqual(len(allcards), 0)

    def setUp(self):
        self.client = Client()


    def test_xss(self):
        response = self.client.get('/gift', {'director' : '<script>alert</script>'})
        self.assertEqual('<script>alert("12"</script>' in response.context['director'],False)
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        self.client = Client(enforce_csrf_checks = True)
        response = self.client.get('/gift.html')
        self.assertContains(response, 'csrfmiddlewaretoken')
        response = self.client.post('/gift.html', {'amount': 95, 'username': 'user2'})
        self.assertEqual(response.status_code, 403)
    
    def test_SQL_Injection(self):
        self.client.login(username="user1", password="user1")
        with open("part1/sqla.gftcrd") as act:
            response = self.client.post("/use", {"card_data": act, "card_supplied": True, "card_fname": "sqlcard"})
            adminpass= "000000000000000000000000000078d2$18821d89de11ab18488fdc0a01f1ddf4d290e198b0f80cd4974fc031dc2615a3"
            self.assertNotIn(adminpass, response.content.decode("UTF-8"))

