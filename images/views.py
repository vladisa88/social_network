from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse


from .forms import ImageCreateForm
from .models import Image


class ImageCreate(generic.View):
    def get(self, request):
        form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html',
                      {'section': 'images', 'form': form})

    def post(self, request):
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print('------------------------!!!!!!!!!!!!!!')
            new_item = form.save(commit=False)
            print('--------!!!!!!!!!!----------------')
            new_item.user = request.user
            new_item.save()
            print('------------------------')
            messages.success(request, 'Image added successfully!')
            print(new_item.get_absolute_url())
            return redirect(new_item.get_absolute_url())


class ImageDetailView(generic.View):
    def get(self, request, id, slug):
        image = get_object_or_404(Image, id=id, slug=slug)
        return render(request, 'images/image/detail.html',
                      {'section': 'images', 'image': image})


@login_required
def image_create(request):
    if request.method == 'POST':
        # Форма отправлена.
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Данные формы валидны.
            cd = form.cleaned_data
            print('-----------------------!!!!!!!!!!-')
            new_item = form.save(commit=False)
            print('------!!!!!!!!!!!!!----------------')
            # Добавляем пользователя к созданному объекту.
            new_item.user = request.user
            new_item.save()
            print('------------------------')
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            print(new_item.get_absolute_url())
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму данными из GET-запроса.
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html',
                  {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images', 'image': image})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        finally:
            pass
    return JsonResponse({'status': 'ok'})
