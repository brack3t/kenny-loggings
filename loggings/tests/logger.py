from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase

from loggings.logger import Logger


def get_user():
    user = User(username="test")
    user.id = 1
    return user


class Blog(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()


class NotBlog(models.Model):
    title = models.CharField(max_length=255)


class SomeObj(object):
    pass


class LoggerTests(TestCase):
    def test_logger_success(self):
        blog = Blog(title="test", body="testing")
        blog.pk = 1

        prev = Blog(title="old test", body="old testing")
        prev.pk = 1

        log = Logger(1, blog, previous_obj=prev, user=get_user(),
            extras=["title"])

        self.assertIsInstance(log, Logger)

    def test_logger_failures(self):
        blog = Blog(title="test", body="testing")
        blog.pk = 1

        not_blog = NotBlog(title="not it")
        not_blog.id = 1

        some_obj = SomeObj()

        with self.assertRaises(ValueError) as ex:
            Logger("fail", blog)

        self.assertEqual(ex.exception.message, "Action must be an integer.")
        ex = None

        with self.assertRaises(Exception) as ex:
            Logger(100, blog)

        self.assertEqual(ex.exception.message,
            "Action must be an integer in %s" % str(Logger.actions))
        ex = None

        with self.assertRaises(TypeError) as ex:
            Logger(1, some_obj)

        self.assertEqual(ex.exception.message,
            "current_obj must be a Django model instance.")
        ex = None

        with self.assertRaises(TypeError) as ex:
            Logger(1, blog, previous_obj=some_obj)

        self.assertEqual(ex.exception.message,
            "previous_obj must be a Django model instance.")
        ex = None

        with self.assertRaises(Exception) as ex:
            Logger(1, blog, previous_obj=get_user())

        self.assertEqual(ex.exception.message,
            "current_obj and previous_obj must be from the same Django app.")
        ex = None

        with self.assertRaises(Exception) as ex:
            Logger(1, blog, previous_obj=not_blog)

        self.assertEqual(ex.exception.message,
            "current_obj and previous_obj must be instances of the same "
            "Django model.")
        ex = None

        with self.assertRaises(TypeError) as ex:
            Logger(1, blog, extras="fail")

        self.assertEqual(ex.exception.message, "extras must be a list.")
        ex = None

        with self.assertRaises(Exception) as ex:
            Logger(1, blog, extras=["fail__fail"])

        self.assertEqual(ex.exception.message,
            "'fail' in fail__fail is not a valid attribute.")
        ex = None

        with self.assertRaises(Exception) as ex:
            Logger(1, blog, extras=["fail"])

        self.assertEqual(ex.exception.message,
            "The attribute 'fail' does not exist on the current instance.")
        ex = None

        with self.assertRaises(Exception) as ex:
            Logger(1, blog, extras=["title__fail"])

        self.assertEqual(ex.exception.message,
            "'title' in title__fail is not a subclass of "
            "django.db.models.Model.")
        ex = None
