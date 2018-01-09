from django.test import TestCase

from .base_models import BasicPost


class BaseModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = BasicPost.objects.create(title='Test Post 1')
        cls.post_status_deleted = BasicPost.objects.create(title='Test Post 2', status=BasicPost.STATUS_DELETED)
        cls.post_status_offline = BasicPost.objects.create(title='Test Post 3', status=BasicPost.STATUS_OFFLINE)
        cls.post_status_draft = BasicPost.objects.create(title='Test Post 4', status=BasicPost.STATUS_DRAFT)

    def test_basemodel_fields(self):
        self.assertEqual(self.post.pk, self.post.id)
        self.assertEqual(self.post.status, BasicPost.STATUS_ONLINE)

    def test_basemodel_queryset(self):
        self.assertQuerysetEqual(BasicPost.objects_bm.all().order_by('id'), [
            '<BasicPost: Test Post 1>',
            '<BasicPost: Test Post 2>',
            '<BasicPost: Test Post 3>',
            '<BasicPost: Test Post 4>'
        ])
        self.assertQuerysetEqual(BasicPost.objects_bm.actives().order_by('id'), ['<BasicPost: Test Post 1>'])
        self.assertQuerysetEqual(BasicPost.objects_bm.offlines(), ['<BasicPost: Test Post 3>'])
        self.assertQuerysetEqual(BasicPost.objects_bm.deleted(), ['<BasicPost: Test Post 2>'])
        self.assertQuerysetEqual(BasicPost.objects_bm.drafts(), ['<BasicPost: Test Post 4>'])
