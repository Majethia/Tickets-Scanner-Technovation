from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Tickets
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == 'POST':
        data = request.POST['result']
        if data.startswith("DSAII"):
            Id = data.split('-')[-2]
            try:
                t = Tickets.objects.get(Id=Id)
                messages.error(request, f'Team ID: {Id}, This Ticket has alredy been used')
            except:
                t = Tickets(Id=Id, Attended='Y')
                messages.info(request, f'Team ID: {Id}, Verified you can enter')
                t.save()
        else:
            messages.error(request, 'Thats not a valid ticket.')
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'index.html')