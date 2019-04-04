from django.db import connections
from django.test import TestCase

from .base_models import BasicPost


class BaseModelTestCase(TestCase):
    """Unit tests of BaseModel"""

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        with connections['default'].schema_editor() as schema_editor:
            schema_editor.create_model(BasicPost)

            cls.post = BasicPost.objects.create(title='Test Post 1')
            cls.post_status_deleted = BasicPost.objects.create(title='Test Post 2', status=BasicPost.STATUS_DELETED)
            cls.post_status_offline = BasicPost.objects.create(title='Test Post 3', status=BasicPost.STATUS_OFFLINE)
            cls.post_status_draft = BasicPost.objects.create(title='Test Post 4', status=BasicPost.STATUS_DRAFT)

    def test_basemodel_fields(self):
        """Test fields"""

        self.assertEqual(self.post.pk, self.post.id)
        self.assertEqual(self.post.status, BasicPost.STATUS_ONLINE)

    def test_basemodel_queryset(self):
        """Test queryset"""

        self.assertQuerysetEqual(
            BasicPost.objects.all().order_by('id'),
            [
                '<BasicPost: Test Post 1>',
                '<BasicPost: Test Post 2>',
                '<BasicPost: Test Post 3>',
                '<BasicPost: Test Post 4>',
            ],
        )
        self.assertQuerysetEqual(BasicPost.objects.actives().order_by('id'), ['<BasicPost: Test Post 1>'])
        self.assertQuerysetEqual(BasicPost.objects.offlines(), ['<BasicPost: Test Post 3>'])
        self.assertQuerysetEqual(BasicPost.objects.deleted(), ['<BasicPost: Test Post 2>'])
        self.assertQuerysetEqual(BasicPost.objects.drafts(), ['<BasicPost: Test Post 4>'])
