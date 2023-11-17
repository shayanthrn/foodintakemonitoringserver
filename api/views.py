from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import os
from .yolov5 import detect
import requests
from .resnet50 import resnet50_infer
import json

@method_decorator(csrf_exempt, name='dispatch')
class Analyze(View):
    def post(self,request):
        timestamp = int(timezone.now().timestamp())
        inputfilename = f'./sources/{timestamp}.jpg'
        os.makedirs(os.path.dirname(inputfilename), exist_ok=True)
        with open(inputfilename, 'wb') as f:
            f.write(request.FILES['pic'].file.read())
        cropped_bowl_dir = detect.run(data="api\yolov5\data\platebowl.yaml", weights="api\yolov5\last.pt",source=inputfilename,save_crop=True,project="sources",name="yoloD")
        if cropped_bowl_dir=="no_detect":
            category = resnet50_infer.run(weights="api\\resnet50\\resnet50model.pth",classes="api\\resnet50\\classes.txt",file=inputfilename)
        else:
            category = resnet50_infer.run(weights="api\\resnet50\\resnet50model.pth",classes="api\\resnet50\\classes.txt",file=str(cropped_bowl_dir))
        api_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'
        api_key = 'UpiCIow4X9djmkhaFquVi3C60KDysvaLrwfYse5D'
        category = category.replace("_"," ")
        response = requests.get(api_endpoint,
                            params={'api_key':api_key,'query':category,"dataType":"Survey (FNDDS)","pageSize":"5"})
        response_json=json.loads(response.text)
        print(f"This is detected category: {category}")
        if(response_json['totalHits']==0):
            response = requests.get(api_endpoint,
                            params={'api_key':api_key,'query':category,"pageSize":"5"})
            response_json=json.loads(response.text)
        print("This is response:")
        print(response_json)
        return JsonResponse({'detected_category':category,'response':response_json})