import requests
from django.http import JsonResponse
from .models import Plant
from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

# Helper functions to fetch data from Trefle and OpenFarm
def fetch_from_trefle(plant_name):
    trefle_api_key = settings.TREFLE_API_KEY
    url = f"https://trefle.io/api/v1/plants/search?token={trefle_api_key}&q={plant_name}"
    response = requests.get(url)
    print("Trefle response status:", response.status_code)
    print("Trefle response body:", response.text)  # Log the full response for debugging
    if response.status_code == 200 and response.json().get('data'):
        return response.json()['data'][0]  # First matching result
    return None

def fetch_from_openfarm(plant_name):
    url = f"https://openfarm.cc/api/v1/crops?filter={plant_name}"
    response = requests.get(url)
    print("OpenFarm response status:", response.status_code)
    print("OpenFarm response body:", response.text)  # Log the full response for debugging
    if response.status_code == 200 and response.json().get('data'):
        return response.json()['data'][0]  # First matching result
    return None

# Main view to handle plant data requests
def get_plant_data(request, plant_name):
    try:
        # Check if plant is already in the database
        plant = Plant.objects.get(name=plant_name)
        return JsonResponse({
            'name': plant.name,
            'origin': plant.origin or "",
            'lifespan': plant.lifespan or "",
            'ideal_conditions': plant.ideal_conditions or "",
            'home_remedies': plant.home_remedies or "Provide water regularly, keep in sunlight.",
            'image_url': plant.image_url or "",
            'description': plant.description or "",
            'binomial_name': plant.binomial_name or "",
            'taxon': plant.taxon or "",
            'companions': plant.companions or "",
            'sun_requirements': plant.sun_requirements or "",
            'growing_degree_days': plant.growing_degree_days or "",
            'sowing_method': plant.sowing_method or "",
            'spread': plant.spread or "",
            'row_spacing': plant.row_spacing or "",
            'height': plant.height or ""
        })
    except Plant.DoesNotExist:
        # Fetch data from APIs
        trefle_data = fetch_from_trefle(plant_name)
        openfarm_data = fetch_from_openfarm(plant_name)
        
        # Initialize plant data with defaults
        plant_data = {
            'name': plant_name,
            'origin': None,
            'lifespan': None,
            'ideal_conditions': None,
            'home_remedies': "Provide water regularly, keep in sunlight.",  # Placeholder
            'binomial_name': "",
            'taxon': "",
            'companions': "",
            'sun_requirements': "",
            'growing_degree_days': "",
            'sowing_method': "",
            'spread': "",
            'row_spacing': "",
            'height': ""
        }

        # Extract data from Trefle if available
        if trefle_data:
            plant_data['name'] = trefle_data.get('common_name', plant_name)
            plant_data['origin'] = trefle_data.get('distribution', {}).get('native', None)
           

        # Extract data from OpenFarm if available
        if openfarm_data:
            plant_data['name'] = openfarm_data.get('name', plant_name)
            plant_data['lifespan'] = openfarm_data.get('attributes', {}).get('lifespan', None)
            plant_data['ideal_conditions'] = openfarm_data.get('attributes', {}).get('sun_requirements', None)
            # Extract and assign new fields from OpenFarm response
            plant_data['binomial_name'] = openfarm_data.get('binomial_name', "")
            plant_data['taxon'] = openfarm_data.get('taxon', "")
            plant_data['companions'] = openfarm_data.get('companions', "")
            plant_data['sun_requirements'] = openfarm_data.get('attributes', {}).get('sun_requirements', "")
            plant_data['growing_degree_days'] = openfarm_data.get('attributes', {}).get('growing_degree_days', "")
            plant_data['sowing_method'] = openfarm_data.get('attributes', {}).get('sowing_method', "")
            plant_data['spread'] = openfarm_data.get('attributes', {}).get('spread', "")
            plant_data['row_spacing'] = openfarm_data.get('attributes', {}).get('row_spacing', "")
            plant_data['height'] = openfarm_data.get('attributes', {}).get('height', "")

        # If data is found, save to database and return the response
        if trefle_data or openfarm_data:
            # Save the fetched data to the database
            plant = Plant.objects.create(**plant_data)
            return JsonResponse(plant_data)

        # If no data found in APIs, return a 404 error
        return JsonResponse({'error': 'Plant not found in external APIs'}, status=404)
