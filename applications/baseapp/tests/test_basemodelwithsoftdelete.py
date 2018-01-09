from django.test import TestCase

from .base_models import (
    Category,
    Post,
)


class BaseModelWithSoftDeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title='Python')
        cls.category = category
        cls.posts = [
            Post.objects.create(category=category, title='Python post 1'),
            Post.objects.create(category=category, title='Python post 2'),
        ]

    def test_basemodelwithsoftdelete_fields(self):
        self.assertEqual(self.category.pk, self.category.id)
        self.assertEqual(self.category.status, Post.STATUS_ONLINE)
        for post in self.posts:
            self.assertEqual(post.status, Post.STATUS_ONLINE)

    def test_basemodelwithsoftdelete_queryset(self):
        self.assertQuerysetEqual(self.category.posts.all().order_by('id'), [
            '<Post: Python post 1>',
            '<Post: Python post 2>'
        ])
        self.assertQuerysetEqual(Category.objects_bm.actives(), ['<Category: Python>'])
        self.assertQuerysetEqual(Category.objects_bm.offlines(), [])
        self.assertQuerysetEqual(Category.objects_bm.deleted(), [])
        self.assertQuerysetEqual(Category.objects_bm.drafts(), [])

    def test_softdelete(self):
        deleted_category = self.category.delete()
        self.assertEqual(deleted_category, (3, {'baseapp.Category': 1, 'baseapp.Post': 2}))
        self.assertQuerysetEqual(Category.objects_bm.deleted(), ['<Category: Python>'])
        self.assertQuerysetEqual(Category.objects.all(), ['<Category: Python>'])
        self.assertQuerysetEqual(Post.objects_bm.deleted().order_by('id'), [
            '<Post: Python post 1>',
            '<Post: Python post 2>'
        ])
