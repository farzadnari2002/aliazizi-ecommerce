from django_filters import rest_framework as filters
from .models import Product, CategoryProduct
from django.contrib.postgres.search import SearchVector, TrigramSimilarity, SearchRank, SearchQuery
from django.db.models.functions import Greatest


class ProductFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=('price', 'favorites_count', 'avg_rating', 'name', 'comments_count', 'created_at')
        )
    price = filters.RangeFilter()
    category = filters.CharFilter(method='filter_by_category')
    search = filters.CharFilter(method='filter_by_search')


    def filter_by_category(self, queryset, name, value):
        try:
            category = CategoryProduct.objects.get(slug=value)
            descendants = category.get_descendants(include_self=True)
            return queryset.filter(category__in=descendants)
        except CategoryProduct.DoesNotExist:
            return queryset.none()

    class Meta:
        model = Product
        fields = ['order_by', 'price', 'category']


    def filter_by_search(self, queryset, name, value):
        query_input = SearchQuery(value)
        search_vector = SearchVector('category__name', 'name', 'tags__name')
        trigram_similarity = Greatest(
            TrigramSimilarity('name', value),
            TrigramSimilarity('category__name', value),
            TrigramSimilarity('tags__name', value),
        )
        search_rank = SearchRank(search_vector, query_input)
        results = queryset.annotate(
            trigram_similarity=trigram_similarity,
            rank=search_rank).filter(trigram_similarity__gt=0.4).order_by('-rank')
        return results

                                                                        
        

