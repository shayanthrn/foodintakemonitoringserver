from django.views import View
from django.http import JsonResponse

class Analyze(View):

    def get(self,request):
        return JsonResponse({'foo':'bar'})