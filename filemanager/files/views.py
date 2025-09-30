import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.conf import settings
from .models import UploadedFile
from .forms import FileUploadForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def file_list(request):
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    return render(request, 'files/file_list.html', {'files': files})


def file_download(request, filename):
    try:
        # Убираем слеш в конце если есть
        if filename.endswith('/'):
            filename = filename[:-1]

        # Ищем файл по имени в базе данных
        uploaded_file = get_object_or_404(UploadedFile, file=f'uploads/{filename}')

        # Открываем файл и отдаем как ответ
        response = HttpResponse(uploaded_file.file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.original_name}"'
        return response

    except UploadedFile.DoesNotExist:
        raise Http404("File does not exist")
    except Exception as e:
        raise Http404("Error accessing file")


@login_required
@user_passes_test(is_admin)
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('file_list'))
    else:
        form = FileUploadForm()

    return render(request, 'files/file_upload.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def file_delete(request, pk):
    uploaded_file = get_object_or_404(UploadedFile, pk=pk)
    if request.method == 'POST':
        uploaded_file.delete()
        return HttpResponseRedirect(reverse('file_list'))

    return render(request, 'files/file_confirm_delete.html', {'file': uploaded_file})
