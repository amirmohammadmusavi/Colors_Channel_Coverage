from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from django.http import HttpResponse,JsonResponse
import os
import time
from Color_Calculate.Channel_Coverage import Channel_Coverage

@csrf_exempt
def cmyk_calculate(request):
    path = 'image_inputs/'
    filename=False
    if not os.path.exists(path):
        os.makedirs(path)
    # get the file from request and save it
    if 'file' in request.FILES:
        filename = request.FILES['file'].name
        rf = request.FILES['file']
        with open(f'{path}file.pdf', 'wb+') as f:
            for chunk in rf.chunks():
                f.write(chunk)

    PART_CALCULATE=request.GET.get('part_cal')
    TAK = request.GET.get('tak')
    PROJECT_NAME = filename
    TAK_SIZE = request.GET.get('coverage')
    CHANGE_N=request.GET.get('change_n')
    if not PROJECT_NAME:
        return "ValError"
    response = Channel_Coverage(IPATH=path,NAME=PROJECT_NAME if PROJECT_NAME else False,CHANGE_N=True if CHANGE_N else False,PART_CALCULATE=True if PART_CALCULATE else False,TAK=True if TAK else False,TAK_SIZE=TAK_SIZE if TAK_SIZE else False)
     
    return JsonResponse(response,safe=False)





