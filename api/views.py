from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import os

@method_decorator(csrf_exempt, name='dispatch')
class Analyze(View):
    def post(self,request):
        timestamp = int(timezone.now().timestamp())
        inputfilename = f'./sources/{timestamp}.jpg'
        os.makedirs(os.path.dirname(inputfilename), exist_ok=True)
        file = open(inputfilename, 'wb')
        file.write(request.FILES['pic'].file.read())
        return JsonResponse({'foo':'bar'})