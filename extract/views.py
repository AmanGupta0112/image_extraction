from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import FileManager, Document
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import datetime
import os
import pytesseract
from django.conf import settings
from .constants import start_words
import re

def generateFile():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
    return formatted_datetime

def process_file(file_name):
    image = Image.open(f"{settings.BASE_DIR}/static/media/{file_name}.png")
    text = pytesseract.image_to_string(image).lower()
    integers = []
    for line in text.split("\n"):
        integer = []
        for txt in start_words:
            if txt in line:
                integer = re.findall(r"\b\d+\b", line)
        integers.extend(integer)
    integers = list(map(int,integers))
    print(integers)
    return max(integers)

@api_view(['POST'])
def upload_file(request):
    request_body = request.data
    image_file = request_body["image"].read()
    approved_amount = float(request_body["approved_amount"])
    try:
        image = Image.open(BytesIO(image_file))
        image.verify()
    except Exception as e:
        return JsonResponse({'error': 'Invalid image file'}, status=400)
    file_manager = FileManager()
    file_name = generateFile()
    file_manager.file.save(f"{file_name}.png", ContentFile(image_file))
    extracted_amount = float(process_file(file_name))
    if extracted_amount <= approved_amount:
        status = True
    else:
        status = False
    document = Document()
    document.file_name = file_manager
    document.extracted_amount = extracted_amount
    document.status = status
    document.approved_amount = approved_amount
    document.save()

    return JsonResponse(
        {
            "success": True,
            "file": f"{file_name}.jpg",
            "approved_amount": approved_amount,
            "extarcted_amount": extracted_amount,
            "approve_status": "Approved!!" if status else "Not Approved!!",
        }
    )
