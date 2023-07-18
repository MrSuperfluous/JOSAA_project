from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from .models import *
from django.db import transaction
from myapp.models import *
import json
from myapp.form import *
from django.shortcuts import redirect
from django.db.models import Q
from django.http import JsonResponse
import razorpay
from django.views.decorators.csrf import csrf_exempt

def pay(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

        client = razorpay.Client(
            auth=("rzp_test_ggd2QsI33BOUVO", "6g2xJgEhYuyZEs1PA3bNCV8S"))

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '0'})
    return render(request, 'myapp/payment_2.html')

@csrf_exempt
def success(request):
    return render(request, "myapp/payment_3.html")

def get_academic_programs(request):
    institute_id = request.GET.get("institute_id")
    academic_programs = AcademicProgram.objects.filter(institute_name_id=institute_id)
    academic_programs_data = [
        {"pk": acad.pk, "name": acad.name} for acad in academic_programs
    ]   
    print(f"{academic_programs_data} this is important")
    return JsonResponse(academic_programs_data, safe=False)

def home(request):
    return render(request, 'myapp/home.html')
def populate(request):
  df = pd.read_excel('myapp/data.xlsx')
    # Call the function with your DataFrame as an argument 
  for _, row in df.iterrows():
    institute_name = row['Institute']
    academic_program_name = row['Academic Program Name']
    seat_type_name = row['Seat Type']
    gender_name = row['Gender']
    opening_rank = row['Opening Rank']
    closing_rank = row['Closing Rank']
    year = row['Year']
    round = row['Round']
    print(f'{institute_name} {year} {seat_type_name} {gender_name} {opening_rank} {closing_rank} {year} {round}')
    # Get or create the related objects
    institute, _ = Institute.objects.get_or_create(name=institute_name)
    seat_type, _ = SeatType.objects.get_or_create(name=seat_type_name)
    gender , _ = Gender.objects.get_or_create(name = gender_name)
   

    academic_program, _ = AcademicProgram.objects.get_or_create(
        name=academic_program_name , 
        institute_name = institute      
    )
    try:
        opening_rank = int(opening_rank)
        closing_rank = int(closing_rank)
    except (ValueError, TypeError):
        # Handle the exception here (e.g., raise an exception or skip saving the record)
        # raise Exception("Opening rank or closing rank is not a valid integer.")
        continue
        
    # Create the ProgramRank instance
    ProgramRank.objects.create(
        institute=institute,
        academic_program=academic_program,
        year=year,
        seat_type = seat_type,
        gender = gender,
        round = round,
        opening_rank=opening_rank,
        closing_rank=closing_rank
    )
    
    # academic_program.institutes.set([institute])


def graph_view(request):
    # # Load the Excel file into a pandas DataFrame
    
    insti_data = json.loads(request.session.get('insti_name'))
    acad_data = json.loads(request.session.get('acad_name'))
    gender_data = json.loads(request.session.get('gender_name'))
    seat_data = json.loads(request.session.get('seat_name'))
    round_no = json.loads(request.session.get('round_no'))
    year = json.loads(request.session.get('year'))
    print(f" This is {acad_data } ")
# Extract the specific values from the JSON
    insti_pk = insti_data['pk']
    acad_pk = acad_data['pk']
    gender_pk = gender_data['pk']
    seat_pk = seat_data['pk']

# Fetch the corresponding objects from the database
    
    seat_type = SeatType.objects.get(pk=seat_pk)
    gender = Gender.objects.get(pk=gender_pk)
    institute = Institute.objects.get(pk=insti_pk)
    acad = AcademicProgram.objects.get(pk=acad_pk)
    print(f"this is acad pk :{acad}")

# Print the extracted values
    print(f"Seat Type: {seat_type}, Gender: {gender}, Round: {round_no}, Year: {year}")
    
# Define the base query
    query = Q()

# Add filters conditionally
    if seat_type:
       query &= Q(seat_type=seat_type)
    if gender:
       query &= Q(gender=gender)
    if round_no:
       query &= Q(round=round_no)
    if institute:
       query &= Q(institute=institute)
    if acad:
       query &= Q(academic_program=acad)
    if year:
       query &= Q(year=year)
# Fetch the corresponding program ranks from the database
    program_ranks = ProgramRank.objects.filter(query)

    sorted_ranks = sorted(program_ranks, key=lambda rank: (rank.opening_rank + rank.closing_rank) / 2)
    print(f" This is {sorted_ranks} ")
    # Prepare the data for the graph
    opening_ranks = []
    closing_ranks = []
    round_ar = []
    labels = [[],[]]
    object = []
    
    for rank in sorted_ranks:
        opening_ranks.append(rank.opening_rank)
        closing_ranks.append(rank.closing_rank)
        labels[0].append(str(rank.academic_program))
        labels[1].append((str(rank.year)))
        round_ar.append((str(rank.round)))
    for data in labels:
        print(data)
    # Prepare the JSON response
    round_number = round_no
    gender_info = gender.name
    seat_type_info = seat_type.name
    data = {
        # 'object_data': object,
        'iit_name' : insti_data['name'],
        'opening_ranks': opening_ranks,
        'closing_ranks': closing_ranks,
        'labels': labels,
        'round_ar': round_ar,
        'round_number': round_number,
        'gender_info': gender_info,
        'seat_type_info': seat_type_info,
    }
    data_json = json.dumps(data)
    context = {'data_json': data}
    print("yup going to graph.html")
    return render(request, 'myapp/graph.html',context)


def front_choice(request):
    if request.method == 'POST':
        form = Choices_form(request.POST) 
        if form.is_valid():
            insti_name = form.cleaned_data['insti']
            acad_name = form.cleaned_data['acad']
            gender_name = form.cleaned_data['gender']
            seat_name = form.cleaned_data['seat']
            round_no = form.cleaned_data['round_no']
            year = form.cleaned_data['year']
            print(f" this is academic data :{acad_name}")
            
            insti_data = {
                'pk': insti_name.pk,
                'name': insti_name.name
            }
            acad_data = {
                'pk': acad_name,
                # 'name': acad_name.name
            }
            gender_data = {
                'pk': gender_name.pk,
                'name': gender_name.name
            }
            seat_data = {
                'pk': seat_name.pk,
                'name': seat_name.name
            }
            # Store the serialized institute data in the session
            request.session['insti_name'] = json.dumps(insti_data)
            request.session['gender_name'] = json.dumps(gender_data)
            request.session['acad_name'] = json.dumps(acad_data)                                                              # Serialize the data as JSON
            request.session['seat_name'] = json.dumps(seat_data)  # Serialize the data as JSON
            request.session['round_no'] = json.dumps(round_no)
            request.session['year'] = json.dumps(year) 

            print("going to graph view")    
            return redirect('graph')  # Use redirect to call the graph_view function
        else:
            # Form is not valid, print the errors
            print("Form is not valid")
            print(form.errors)
    else:
        print("something")
        form = Choices_form()
        
    return render(request, 'myapp/frontpage.html', {'form': form})

def branch_list(request):
    if request.method == 'POST':
        form = Branch_form(request.POST) 
    form = Branch_form()    
    return render(request, 'myapp/branch.html',{'form':form})

def get_branch(request):
    institute_id = request.GET.get("institute_id")
    try:
        institute = Institute.objects.get(id=institute_id)
        academic_programs = AcademicProgram.objects.filter(institute_name=institute)
        academic_programs_data = [program.name for program in academic_programs]
        return JsonResponse(academic_programs_data, safe=False)
    except Institute.DoesNotExist:
        return JsonResponse([], safe=False)
    