from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import os
from .yolov5 import detect
from .resnet50 import resnet50_infer

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
        return JsonResponse({'foo':category})