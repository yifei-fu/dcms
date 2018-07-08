from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.reverse import reverse

CONTENTTYPES_PARAMS_URL = r'(?P<content_type>\d+)/(?P<object_id>\d+)'


class ContenttypesParamsMixin(GenericAPIView):
    '''
    Add the content_type and object_id parameters to the view and the serializer context.
    '''

    # called before method handler, add attributes of the object being commented on from URL parameters
    def initial(self, request, *args, **kwargs):
        self.content_type = get_object_or_404(ContentType, id=self.kwargs['content_type'])
        self.obj = get_object_or_404(self.content_type.model_class(), id=self.kwargs['object_id'])
        super().initial(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'content_type': self.content_type,
                'obj': self.obj, 'object_id': self.obj.id,
                'request': self.request}

    def filter_generic_queryset(self, queryset):
        return queryset.filter(content_type=self.content_type, object_id=self.obj.id)


# Get the reversed url from a view whose URL contains contenttypes parameters
def reverse_contenttypes_url(view_name, obj, request):
    url_kwargs = {
        'content_type': ContentType.objects.get_for_model(obj).id,
        'object_id': obj.id
    }
    return reverse(view_name, kwargs=url_kwargs, request=request)


# add fields in context for deserialization
def add_contenttypes_info_from_context(attrs, context):
    attrs['content_type'] = context['content_type']
    obj = context.get('obj')
    object_id = obj.id if obj else context['object_id']
    attrs['object_id'] = object_id
