import datetime

from service import call_restful_service

class WeatherService:

    _cached_weather_data = dict()
    def __init__(self, apiKey):
        self.apiKey=apiKey

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
        if (region_name not in _cached_weather_data or
            _cached_weather_data[region_name]['dateretrieved'] < _now - datetime.timedelta(seconds=60)):
            _url_template='http://api.wunderground.com/api/{0}/geolookup/conditions/almanac/q/{1}.json'
            _url_composed = _url_template.format(self.apiKey,region_name)
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
            _cached_weather_data[region_name] = {
                'temp':_temp_f,
                'dateretrieved':datetime.datetime.now(),
                'average_temp':_average_f,
                'description': _weather_description,
                'readable_string':_readable_string
                }
        
        return _cached_weather_data[region_name]


