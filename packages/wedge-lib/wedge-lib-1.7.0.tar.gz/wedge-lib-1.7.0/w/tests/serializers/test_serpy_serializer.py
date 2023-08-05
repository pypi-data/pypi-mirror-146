from django.contrib.auth.models import User

from w.data_test_factory.data_test_factory import DataTestFactory
from w.django.tests.django_testcase import DjangoTestCase
from w.drf.serializers.serpy_serializers import UserWithOneGroupSerializer
from w.tests.fixtures.datasets.django_app import dtf_recipes, dtf_models
from w.tests.fixtures.datasets.dtf_recipes import user_recipes
from w.tests.fixtures.datasets.serpy_serializer import serializers
from w.tests.helpers import orm_test_helper
from w.tests.mixins.serializer_mixin import SerializerMixin


class TestSerpySerializer(SerializerMixin, DjangoTestCase):
    _serializers = {
        "author": serializers.AuthorSerializer,
        "book": serializers.BookSerializer,
        "character": serializers.CharacterSerializer,
        "user": UserWithOneGroupSerializer,
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        dtf = DataTestFactory()
        dtf.build(dtf_recipes.books_series_recipe, nb=2)
        dtf.build(dtf_recipes.books_series_recipe, nb=3)
        dtf.build(dtf_recipes.books_series_recipe, nb=2)
        dtf.build(user_recipes.base_user, nb=2)
        dtf.build(user_recipes.user_with_one_group, nb=3)

    """
    get_optimized_queryset
    """

    def test_get_optimized_queryset_with_foreign_key_return_qs(self):
        """
        Ensure method succeed with foreign k optimizations

        qs = dtf_models.Author.objects.all().select_related(*["birth_city"])
        """
        qs = serializers.AuthorSerializer.get_optimized_queryset()
        with orm_test_helper.capture_nb_queries(1):
            self.assert_equals_resultset(self.serialize("author", qs, many=True))

    def test_get_optimized_queryset_with_many2many_return_qs(self):
        """
        Ensure method succeed with manyTomany optimizations

        qs = dtf_models.Character.objects.prefetch_related(
                 *[
                     Prefetch(
                         "books",
                         queryset=dtf_models.Book.objects.select_related(
                             *["author", "author__birth_city", "series"]
                         ).prefetch_related(*[Prefetch("departments")]),
                     )
                 ]
             )
        """

        with orm_test_helper.capture_nb_queries(3):
            qs = serializers.CharacterSerializer.get_optimized_queryset(
                dtf_models.Character.objects.all()
            )
            self.assert_equals_resultset(self.serialize("character", qs, many=True))

    def test_get_optimized_queryset_with_manual_prefetch_return_qs(self):
        """ Ensure we can define manual prefetch_related """
        with orm_test_helper.capture_nb_queries(2):
            qs = UserWithOneGroupSerializer.get_optimized_queryset(User.objects.all())
            self.assert_equals_resultset(self.serialize("user", qs, many=True))
