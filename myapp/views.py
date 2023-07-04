from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from .models import *
from django.db import transaction
from myapp.models import *
import json
from myapp.form import *
from django.shortcuts import redirect
def home(request):
    return render(request, 'myapp/home.html')


@transaction.atomic
def populate_colleges_and_branches(df):
  for _, row in df.iterrows():
    institute_name = row['Institute']
    academic_program_name = row['Academic Program Name'].split(" (")[0]
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
        name=academic_program_name        
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
    
    academic_program.institutes.set([institute])


def graph_view(request):
    # # Load the Excel file into a pandas DataFrame
    # df = pd.read_excel('myapp/data.xlsx')
    # Call the function with your DataFrame as an argument

    # populate_colleges_and_branches(df)
    insti_data = json.loads(request.session.get('insti_name'))
    gender_data = json.loads(request.session.get('gender_name'))
    seat_data = json.loads(request.session.get('seat_name'))
    round_no = request.session.get('round_no')
    year = request.session.get('year')

# Extract the specific values from the JSON
    insti_pk = insti_data['pk']
    gender_pk = gender_data['pk']
    seat_pk = seat_data['pk']

# Fetch the corresponding objects from the database
    seat_type = SeatType.objects.get(pk=seat_pk)
    gender = Gender.objects.get(pk=gender_pk)
    institute = Institute.objects.get(pk=insti_pk)

# Print the extracted values
    print(f"Seat Type: {seat_type}, Gender: {gender}, Round: {round_no}, Year: {year}")

# Fetch the corresponding program ranks from the database
    program_ranks = ProgramRank.objects.filter(
     seat_type=seat_type,
     gender=gender,
     round=round_no,
     institute=institute,
     year=year
     )

    sorted_ranks = sorted(program_ranks, key=lambda rank: (rank.opening_rank + rank.closing_rank) / 2)

    # Prepare the data for the graph
    opening_ranks = []
    closing_ranks = []
    labels = [[],[]]
    object = []
    
    for rank in sorted_ranks:
        opening_ranks.append(rank.opening_rank)
        closing_ranks.append(rank.closing_rank)
        labels[0].append(str(rank.academic_program))
        labels[1].append((str(rank.year)))
        object.append((rank.opening_rank,rank.closing_rank,rank.academic_program,rank.year))
    for data in labels:
        print(data)
    # Prepare the JSON response
    round_number = round_no
    gender_info = gender.name
    seat_type_info = seat_type.name
    data = {
        # 'object_data': object,
        'opening_ranks': opening_ranks,
        'closing_ranks': closing_ranks,
        'labels': labels,
        'round_number': round_number,
        'gender_info': gender_info,
        'seat_type_info': seat_type_info,
    }
    # data_json = json.dumps(data)
    context = {'data_json': data}
    return render(request, 'myapp/graph.html',context)


def front_choice(request):
    if request.method == 'POST':
        form = Choices_form(request.POST) 
        if form.is_valid():
            insti_name = form.cleaned_data['insti']
            gender_name = form.cleaned_data['gender']
            seat_name = form.cleaned_data['seat']
            round_no = form.cleaned_data['round_no']
            year = form.cleaned_data['year']
           
            insti_data = {
                'pk': insti_name.pk,
                'name': insti_name.name
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
            request.session['gender_name'] = json.dumps(gender_data)  # Serialize the data as JSON
            request.session['seat_name'] = json.dumps(seat_data)  # Serialize the data as JSON
            request.session['round_no'] = round_no
            request.session['year'] = year 

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
    