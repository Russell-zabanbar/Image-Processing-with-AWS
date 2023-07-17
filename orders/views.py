import base64
import io
import os
import random

import boto3
from PIL import Image
from django import views
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv

from orders.forms import ImageUploadForm, CardSelectionForm
from .models import Order, single_order
from orders.utils import CreateOrderUtils
from django.shortcuts import HttpResponseRedirect, HttpResponse, reverse


class DetectFaceView(views.View):
    template_name = 'orders/queue.html'
    form_class = ImageUploadForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name)

    def post(self, request):
        print('start request')
        image_text = request.POST.get('image')
        if image_text.startswith('data:image/png;base64,'):
            image_data = image_text[len('data:image/png;base64,'):]
        elif image_text.startswith('data:image/jpeg;base64,'):
            image_data = image_text[len('data:image/jpeg;base64,'):]

        image_bytes = base64.b64decode(image_data)

        collectionid = 'merese'
        bucket_name = 'testamirbucket'
        load_dotenv()
        session = boto3.Session(
            aws_access_key_id=os.getenv('ACCESS_KEY'),
            aws_secret_access_key=os.getenv('SECRET_KEY')
        )
        s3 = session.resource('s3')
        bucket = s3.Bucket(bucket_name)
        client = session.client('rekognition', region_name='ap-northeast-2')

        response = client.search_faces_by_image(CollectionId=collectionid,
                                                Image={'Bytes': image_bytes},
                                                FaceMatchThreshold=0.9,
                                                MaxFaces=1)
        if len(response['FaceMatches']) > 0:
            face_match = response['FaceMatches'][0]
            random_code = face_match['Face']['ExternalImageId']
            try:
                orders = Order.objects.filter(random_code=random_code)[0]
            except IndexError:
                orders = None
            try:
                single = single_order.objects.filter(random_code=random_code)[0]
            except IndexError:
                single = None

            if orders is not None:
                messages.warning(request, f"{orders.waiting_time}شما قبلا یک سفارش ثبت شده دارید زمان انتظار شما",'warning')
                return JsonResponse({'url': reverse('detect:available_order')})

            if single is not None:
                return JsonResponse({'url': reverse('detect:available_order')})

            else:
                return JsonResponse({'url': reverse('detect:available_order')})

        else:
            rancode = str(random.randint(1, 10000))
            file_path = f"/tmp/{rancode}.jpg"  # create a file path to save the image
            with open(file_path, 'wb') as f:
                f.write(image_bytes)  # write the image bytes to the file
            bucket.upload_file(file_path, rancode)  # upload the file to S3
            os.remove(file_path)  # delete the file from the local filesystem
            request.session['random_code'] = {
                'code': rancode
            }
            return JsonResponse({'url': reverse('detect:add_order')})


class AddOrderView(views.View):
    def get(self, request):
        form = CardSelectionForm
        return render(request, 'orders/bread_quantity.html', {'form': form})

    def post(self, request):
        form = CardSelectionForm(request.POST)
        if form.is_valid():
            bread_number = int(form.cleaned_data['card_number'])
            random_code = request.session['random_code']['code']
            collectionid = 'merese'
            session = boto3.Session(
                aws_access_key_id=os.getenv('ACCESS_KEY'),
                aws_secret_access_key=os.getenv('SECRET_KEY')
            )
            client = session.client('rekognition', region_name='ap-northeast-2')
            s3 = session.resource('s3')
            bucket = s3.Bucket('testamirbucket')
            response = client.index_faces(
                CollectionId='merese',
                Image={'S3Object': {'Bucket': 'testamirbucket', 'Name': random_code }},
                ExternalImageId=random_code,
                MaxFaces=1,
                QualityFilter="AUTO",
                DetectionAttributes=['ALL']
            )

            CreateOrderUtils(request, bread_number, random_code)

        return render(request, 'orders/bread_quantity.html', {'form': form})


class AvailableOrderView(views.View):
    form_class = CardSelectionForm

    def get(self, request):
        return render(request, 'orders/orderـavailable.html')
    #
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         bread_number = int(form.cleaned_data['card_number'])
    #         random_code = None
    #         CreateOrderUtils(request, bread_number, random_code)
    #
    #     return render(request, 'orders/succes_order.html', {'form': form})
