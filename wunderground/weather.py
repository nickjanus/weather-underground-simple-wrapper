import datetime

from .service import call_restful_service

cached_weather_data = dict()

def get_temp_for_region(region_name):
    """Wrapper for getting weather data from the WeatherUnderground API service.
    This method will cache results so that additional calls to the weather service can be avoided
    when we have already retrieved weather data for the same region for another subscriber.

    Keyword arguments:
    region_name -- a string in the format of ST/CITY (where ST is the two-letter state code
                   and CITY is the city name) of the city whose weather we plan to look up.
                   Note that this city must be available in WeatherUnderground's store.
    """
    _now = datetime.datetime.now()
    if (region_name not in cached_weather_data or
        cached_weather_data[region_name]['dateretrieved'] < _now - datetime.timedelta(seconds=60)):
        _url_template='http://api.wunderground.com/api/3a506d8e3255df14/geolookup/conditions/almanac/q/{0}.json'
        _url_composed = _url_template.format(region_name)
        _parsed_json=call_restful_service(_url_composed)
        
        if not 'location' in _parsed_json: # handle case where we were passed a bad value
            return
        _location = _parsed_json['location']['city']
        _temp_f = _parsed_json['current_observation']['temp_f']
        _weather_description = _parsed_json['current_observation']['icon']
        _normal_high_f = float(_parsed_json['almanac']['temp_high']['normal']['F'])
        _normal_low_f = float(_parsed_json['almanac']['temp_low']['normal']['F'])
        _average_f = (_normal_high_f + _normal_low_f) / 2
        # can we do better than the icon field for description?  consider
        # "partlycloudy"
        # possibly a translation table
        _readable_string = "In " + _location + ", it's currently " + str(_temp_f) + \
        " degrees and " + _weather_description + ". "
        
        print("Current temperature in %s is: %s" % (_location, _temp_f))
        
        # keep as float because will need to do mathematical comparison.
        # Convert to string later as nec.
        cached_weather_data[region_name] = {
            'temp':_temp_f,
            'dateretrieved':datetime.datetime.now(),
            'average_temp':_average_f,
            'description': _weather_description,
            'readable_string':_readable_string
            }
        
    return cached_weather_data[region_name]


def is_good_weather(input_region):
    """Determine if the weather for a region is considered "good" by our defined parameters:
    Five degrees or more above average, or sunny means good.
    Five degrees or more below average, or rainy means bad.
    Otherwise, neither good nor bad.

    Keyword arguments:
    input_region -- A data structure containing the relevant weather data for a region
                    as returned by the web service and processed by our wrapper.
    """
    precipitation_descriptions = [
        "flurries",
        "sleet",
        "rain",
        "snow",
        "tstorms"
    ]
    if (input_region['temp'] - input_region['average_temp'] >= 5):
        # If we're 5 degrees above average temp
        return 1
    if input_region['description'] is 'clear': # or if it's sunny
        return 1
    # If we're 5 degrees below average temp
    if (input_region['temp'] - input_region['average_temp'] <= -5):
        return -1
    if precipitation_descriptions.count(input_region['description']) == 1:
        return -1
    return 0
