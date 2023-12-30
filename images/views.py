# import redis
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from actions.utils import create_action
from django.conf import settings

#Connect To Redis
# r = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB
# )

# Create your views here.
@login_required
def image_create(request):
    form = ImageCreateForm()
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        
        if form.is_valid():
            cleanData = form.cleaned_data
            new_image =form.save(commit=False)

            # the item is assigned to the current user
            new_image.user = request.user
            new_image.save()

            # Added the create action shortcut
            create_action(request.user, 'Bookmarked Image', new_image)

            messages.success(request, 'Image Added Successfully')

            return redirect(new_image.get_absolute_url())

        else:
            form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {
        'section':'images',
        'form':form
    })


def image_detail(request , id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)

    #increment total views by 1
    # total_views = r.incr(f'image:{image.id}:views')
    # 'total_views':total_views

    return render(request, 'images/image/detail.html', 
                  {'section':'images','image':image})



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

                create_action(request.user, 'Liked', image)

            else:
                image.users_like.remove(request.user)

            return JsonResponse({'status': 'ok'})

        except Image.DoesNotExist:
            pass
    
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    
    except PageNotAnInteger:
        images = paginator.page(1)

    except EmptyPage:
        if images_only:
            return HttpResponse('')
        
        images = paginator.page(paginator.num_pages)
    
    context = {'section':'images', 'images':images}

    if images_only:
        return render(request, 'images/image/list_images.html', context)
    
    return render(request, 'images/image/list.html', context)

