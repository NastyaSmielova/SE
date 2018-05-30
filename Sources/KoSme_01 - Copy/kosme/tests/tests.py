from django.test import TestCase

import datetime
import django.utils.timezone as timezone



from  kosme.models import *
import requests




from coverage import Coverage

cov = Coverage()
cov.start()


class TestLecture(TestCase):

    def createLecture(self, name = "firstone",link="http://127.0.0.1:8800/firstOne" ):
        return Lecture.objects.create(name=name, link=link, date= timezone.now())

    def testwLectureCreation(self):
        lecture = self.createLecture()
        self.assertTrue(isinstance(lecture, Lecture))
        self.assertEqual(lecture.__str__(), lecture.name)

    def testServer(self):
        link = "http://127.0.0.1:8800/test01"
        dataToSend ="some text"

        requests.put(url=link, data=dataToSend)
        data = requests.get(url=link).text
        print(dataToSend,data)
        self.assertEqual(dataToSend, data)

    # i def
    #
    # def test_whatever_list_view(self):
    #     w = self.create_whatever()
    #     url = reverse("whatever.views.whatever")
    #     resp = self.client.get(url)
    #
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn(w.ttle, resp.content)

cov.stop()
cov.html_report(directory='covhtml')

