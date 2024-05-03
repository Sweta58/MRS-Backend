from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from .projectLogic import *
from .cleaner import *
import json, os

from rest_framework.response import Response
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def landingPage(request):
    return render(request, 'index.html')

def aboutPage(request):
    return render(request, 'about.html')

@api_view(['POST'])
def webHandler(request):
    with open('MRS/logs/activities.txt', 'a') as file:
        file.write(f"[{timestamp}]\n")
        file.write('Processing image from web...\n')
        file.write('------------------------------------------------------------------------\n')

    extractedText = imageProcessor(request, timestamp)
    if '' == extractedText:
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write('Cannot extract text from the given image\n')
            file.write('Image processing aborted!\n')
            file.write('------------------------------------------------------------------------\n')
        return Response('Cannot extract text from the given image')
    else:
        if 'ERROR_400' == extractedText:
            return Response({'ERROR 400': 'Request method is not POST'})
        elif 'ERROR_406' == extractedText:
            return Response({'ERROR 406': 'Photo not received'})
        elif 'ERROR_500' == extractedText:
            with open('MRS/logs/activities.txt', 'a') as file:
                file.write('Image processing stopped!\n')
                file.write('------------------------------------------------------------------------\n')
            return Response({'ERROR 500': 'Internal server error'})
        else:
            drugs = identifyMedicines(extractedText)
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write('Processing successful!\n')
            file.write('------------------------------------------------------------------------\n\n')
        
        medicineInfo = {}
        medicineInfo = createWebResponse(drugs)
        medicineInfo['image_path'] = f'{timestamp}.jpg'
        return render(None, 'medicine.html', medicineInfo)

#mobileHandler is not complete..
@api_view(['POST'])
def mobileHandler(request):
    with open('MRS/logs/activities.txt', 'a') as file:
        file.write(f"[{timestamp}]\n")
        file.write('Processing image from mobile...\n')
        file.write('------------------------------------------------------------------------\n')

    extractedText = imageProcessor(request, timestamp)
    if '' == extractedText:
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write('Cannot extract text from the given image\n')
            file.write('Image processing aborted!\n')
            file.write('------------------------------------------------------------------------\n')
            #code below this line does not work
        return JsonResponse({'ERROR 500': 'Cannot extract text from the given image'})
    else:
        if 'ERROR_400' == extractedText:
            return JsonResponse({'ERROR 400': 'Request method is not POST'})
        elif 'ERROR_406' == extractedText:
            return JsonResponse({'ERROR 406': 'Photo not received'})
        elif 'ERROR_500' == extractedText:
            with open('MRS/logs/activities.txt', 'a') as file:
                file.write('Image processing stopped!\n')
                file.write('------------------------------------------------------------------------\n')
            return JsonResponse({'ERROR 500': 'Internal server error'})
        else:
            drugs = identifyMedicines(extractedText)
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write('Processing successful!\n')
            file.write('------------------------------------------------------------------------\n')
        return JsonResponse(extractedText)