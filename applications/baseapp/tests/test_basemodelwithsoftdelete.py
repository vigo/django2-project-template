from django.db import connections
from django.test import TestCase

from ..utils import console
from .base_models import Category, Member, Person, Post

console = console(source=__name__)


class BaseModelWithSoftDeleteTestCase(TestCase):
    """Unit tests of BaseModelWithSoftDelete"""

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        with connections['default'].schema_editor() as schema_editor:
            schema_editor.create_model(Category)
            schema_editor.create_model(Post)
            schema_editor.create_model(Person)
            schema_editor.create_model(Member)

        cls.category = Category.objects.create(title='Python')
        cls.posts = [
            Post.objects.create(category=cls.category, title='Python post 1'),
            Post.objects.create(category=cls.category, title='Python post 2'),
        ]
        cls.people = [Person.objects.create(name='Person 1'), Person.objects.create(name='Person 2')]
        cls.member = Member.objects.create(title='Membership')
        cls.member.members.add(*cls.people)

    def test_softdelete_for_many_to_many(self):
        deleted_member = self.member.delete()
        self.assertEqual(deleted_member, (3, {'baseapp.Member': 1, 'baseapp.Member_members': 2}))
        self.assertQuerysetEqual(Member.objects.all(), [])
        self.assertQuerysetEqual(Member.objects.actives(), [])
        self.assertQuerysetEqual(Member.objects.deleted(), ['<Member: Membership>'])
        self.assertQuerysetEqual(self.member.members.all(), [])

    def test_basemodelwithsoftdelete_fields(self):
        """Test fields"""

        self.assertEqual(self.category.pk, self.category.id)
        self.assertEqual(self.category.status, Post.STATUS_ONLINE)
        for post in self.posts:
            self.assertEqual(post.status, Post.STATUS_ONLINE)

    def test_basemodelwithsoftdelete_queryset(self):
        """Test queryset"""

        self.assertQuerysetEqual(
            self.category.posts.all().order_by('id'), ['<Post: Python post 1>', '<Post: Python post 2>']
        )
        self.assertQuerysetEqual(Category.objects.actives(), ['<Category: Python>'])
        self.assertQuerysetEqual(Category.objects.offlines(), [])
        self.assertQuerysetEqual(Category.objects.deleted(), [])
        self.assertQuerysetEqual(Category.objects.drafts(), [])

    def test_soft_deletetion(self):
        """Test soft deletion"""

        deleted_category = self.category.delete()
        self.assertEqual(deleted_category, (3, {'baseapp.Category': 1, 'baseapp.Post': 2}))
        self.assertQuerysetEqual(Category.objects.deleted(), ['<Category: Python>'])
        self.assertQuerysetEqual(
            Post.objects.deleted().order_by('id'), ['<Post: Python post 1>', '<Post: Python post 2>']
        )

    def test_softdelete_undelete(self):
        """Test undelete feature"""
        deleted_category = self.category.delete()
        self.assertEqual(deleted_category, (3, {'baseapp.Category': 1, 'baseapp.Post': 2}))
        undeleted_items = self.category.undelete()
        self.assertEqual(undeleted_items, (3, {'baseapp.Category': 1, 'baseapp.Post': 2}))
        self.assertQuerysetEqual(Post.objects.deleted(), [])

    def test_softdelete_all(self):
        deleted_posts = Post.objects.delete()
        self.assertEqual(deleted_posts, (2, {'baseapp.Post': 2}))
