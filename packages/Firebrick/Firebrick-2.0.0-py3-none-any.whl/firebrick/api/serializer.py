from firebrick.exceptions.api import BadRequest
import json


class Serializer:
    @classmethod
    def data(cls, request):
        '''
        Turns json object into object
        '''
        
        try:
            body = json.loads(request.body)
        except:
            raise BadRequest('Body is not valid json.')
        
        fields_data = {}
        
        for field in cls.Meta.fields:
            try:
                fields_data[field] = body[field]
            except KeyError:
                raise BadRequest(f'{field} is required.')
        try:
            return cls.Meta.model.objects.get_object_or_404(**fields_data, error_text='Object could not be found.')
        except ValueError:
            raise BadRequest('Not all arguments were the correct type.')
    
    @classmethod
    def parse(cls, object):
        '''
        Turns object into json data
        '''
        
        data = {}
        
        for field in cls.Meta.fields:
            # Get the fields value
            data[field] = eval(f'object.{field}')
        
        return data