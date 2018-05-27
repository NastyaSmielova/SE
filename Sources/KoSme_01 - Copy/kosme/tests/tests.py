from django.test import TestCase

import datetime
import django.utils.timezone as timezone



from  kosme.models import *

class TestLecture(TestCase):

    def createLecture(self, name = "firstone",link="http://127.0.0.1:8800/firstOne" ):
        return Lecture.objects.create(name=name, link=link, date= timezone.now())

    def testwLectureCreation(self):
        lecture = self.createLecture()
        print("huihuhuihiuhiuh")
        self.assertTrue(isinstance(lecture, Lecture))
        self.assertEqual(lecture.__str__(), lecture.name)
