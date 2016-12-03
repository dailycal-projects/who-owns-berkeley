import json
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from bakery.views import BuildableTemplateView, BuildableDetailView
from parcels.models import *

class Main(BuildableTemplateView):
    """
    The landing page.
    """
    template_name = "main.html"
    build_path = "index.html"

# APIs

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class BuildableJSONView(JSONResponseMixin, BuildableTemplateView):
    # Nothing more than standard bakery configuration here
    build_path = 'jsonview.json'

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_content(self):
        """
        Overrides an internal trick of buildable views so that bakery
        can render the HttpResponse substituted above for the typical Django
        template by the JSONResponseMixin
        """
        return self.get(self.request).content


class ParcelsJson(BuildableJSONView):
    """
    
    """
    build_path = "api/parcels.json"

    def get_context_data(self, **kwargs):
        parcels = Parcel.objects.all()[:1000]
        features = []
        for parcel in parcels:
            as_dict = {
                "type": "Feature",
                "geometry": json.loads(parcel.geom.geojson),
                "properties": {
                    "id": parcel.id,
                }
            }
            features.append(as_dict)
        objects = {
            "type": "FeatureCollection",
            "features": features,
        }
        return objects