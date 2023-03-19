"""Photo app generic views"""
import json
from copy import copy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDict
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PhotoModelForm
from .models import Photo, CnTaggedItem, CnTag


class PhotoListView(ListView):
    model = Photo

    template_name = 'photoapp/photo-list.html'

    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    template_name = 'photoapp/photo-tag-list.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag_name = None

    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        queryset = self.model.objects.filter(tags__slug=self.get_tag())
        self.tag_name = CnTag.objects.get(slug=self.get_tag())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag_name
        return context


class TagListView(ListView):
    model = CnTag
    template_name = 'photoapp/tag-list.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        queryset = CnTag.objects.prefetch_related('taggit_taggeditem_items')
        context = super().get_context_data(**kwargs)
        tags = []

        for tag in queryset:
            if tag.slug == 'shi' or tag.slug == 'fou':
                continue
            if tag.taggit_taggeditem_items.exists():
                object_id = tag.taggit_taggeditem_items.first().object_id
                yes_tag = Photo.objects.get(id=object_id).tags.filter(slug='shi').exists()
                no_tag = Photo.objects.get(id=object_id).tags.filter(slug='fou').exists()
                if yes_tag:
                    yn_tag = CnTag.objects.get(slug='shi')
                elif no_tag:
                    yn_tag = CnTag.objects.get(slug='fou')
                else:
                    yn_tag = ''
                tags.append({
                    'tag': tag,
                    'yes_no_tag': yn_tag,
                })

        context['tags'] = tags
        return context


class TaggedTagListView(TagListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = []
        for tag_info in context['tags']:
            if self.kwargs['flag'] == 'yes' and tag_info['yes_no_tag'] != '':
                tags.append(tag_info)
            elif self.kwargs['flag'] == 'no' and tag_info['yes_no_tag'] == '':
                tags.append(tag_info)

        context['tags'] = tags
        return context



class PhotoDetailView(DetailView):
    model = Photo

    template_name = 'photoapp/detail.html'

    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoModelForm
    template_name = 'photoapp/create.html'
    success_url = reverse_lazy('photo:tags')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None
        self.new_request = None

    def post(self, request, *args, **kwargs):
        for img in self.request.FILES.getlist('image'):
            new_files = MultiValueDict()
            new_files['image'] = img
            new_request = copy(request)
            new_request.photos = new_files
            self.new_request = new_request
            super().post(new_request, *args, **kwargs)

        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        request = self.new_request if self.new_request else self.request

        if request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': request.POST,
                'files': request.photos,
            })

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        self.object = form.save()


class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'photoapp/update.html'

    model = Photo

    fields = ['title', 'description', 'tags']

    success_url = reverse_lazy('photo:tags')


@csrf_exempt
def yes_no_tag(request):
    data = json.loads(request.POST['data'])
    tag = CnTag.objects.get(slug=data['tag'])
    yes_tag = CnTag.objects.get(slug='shi')
    no_tag = CnTag.objects.get(slug='fou')
    photos = Photo.objects.filter(id__in=data['photos'])
    for photo in photos:
        photo.tags.remove(yes_tag, no_tag)
        photo.tags.add(tag)

    return HttpResponse()


class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photoapp/delete.html'

    model = Photo

    success_url = reverse_lazy('photo:tags')
