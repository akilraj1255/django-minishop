from imaging.models import *
from imaging.forms import *
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import simplejson
from settings import MEDIA_ROOT
from django.core.files import File

# Create your views here.

def iframe_form(request):
  if request.method == 'POST':
    form = AjaxUploadForm(request.POST, request.FILES)
    if form.is_valid():
      name = form.cleaned_data['name']
      alt = form.cleaned_data['alt']
      title = form.cleaned_data['title']
      image_upl = request.FILES['image']
      new_image = form.save()
      id = new_image.pk
      img = new_image.get_admin_thumb_url()
      response_dict = { 'title':title, 'name':name[:25], 'id': id, 'image':img, 'alt':alt }
      form = AjaxUploadForm()
      return render_to_response('iframe_form.html',
          { 'form' : form, 'callback': simplejson.dumps(response_dict) },
          context_instance=RequestContext(request))
    else:
      return render_to_response('iframe_form.html',
          { 'form' : form },
          context_instance=RequestContext(request))
  else:
    form = AjaxUploadForm()
    return render_to_response('iframe_form.html',
        { 'form' : form },
        context_instance=RequestContext(request))
iframe_form = permission_required('imaging.upload_images')(iframe_form)
 
def ajax_image_removal(request):
  if request.method == 'POST':
    image_id = request.POST.get('id', '0')
    if image_id > 0:
      try:
        image = Image.objects.get(pk=image_id)
        image.delete()
      except:
        return HttpResponse("fail");
      return HttpResponse("ok");
    else:
      return HttpResponse("fail");
  else:
    return HttpResponse("fail");

ajax_image_removal = permission_required('imaging.ajax_delete_images')(ajax_image_removal)
