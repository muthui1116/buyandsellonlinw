from django.shortcuts import render

# Create your views here.
def vprofile(request):
    return render(request, 'home/vendor/vprofile.html')