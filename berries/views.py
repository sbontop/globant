from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .util import BerryData, fetch_all_berry_data

berry_schema = {
    "type": "object",
    "properties": {
        "berry_names": {
            "type": "array",
            "items": {
                "type": "string",
            },
            "description": "List of all berry names",
        },
        "growth_times": {
            "type": "array",
            "items": {
                "type": "number",
            },
            "description": "List of all berry growth times",
        },
        "growth_statistics": {
            "type": "object",
            "properties": {
                "min_growth_time": {
                    "type": "number",
                    "description": "Minimum growth time",
                },
                "max_growth_time": {
                    "type": "number",
                    "description": "Maximum growth time",
                },
                "median_growth_time": {
                    "type": "number",
                    "description": "Median growth time",
                },
                "mean_growth_time": {
                    "type": "number",
                    "description": "Mean growth time",
                },
                "mode_growth_time": {
                    "type": "number",
                    "description": "Mode growth time",
                },
                "variance_growth_time": {
                    "type": "number",
                    "description": "Variance of growth times",
                },
                "standard_deviation_growth_time": {
                    "type": "number",
                    "description": "Standard deviation of growth times",
                },
            },
            "description": "Statistics of growth times",
        },
        "description": "A list of berries and their growth times with statistics",
    },
}


@extend_schema(
    description="Return a JSON response containing statistics on all berries.",
    responses={
        200: {
            "description": "OK",
            "content": {"application/json": {"schema": berry_schema}},
        },
        500: {
            "description": "Server Error",
            "content": {"application/json": {"schema": {"type": "string"}}},
        },
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def all_berry_stats(request: HttpRequest) -> JsonResponse:
    """Return a JSON response containing statistics on all berries."""
    data = cache.get("all_berry_stats_data")
    if data is None:
        try:
            data: BerryData = fetch_all_berry_data()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        cache.set("all_berry_stats_data", data, timeout=3600)

    return JsonResponse(data.to_json(), safe=False)


@extend_schema(
    description="Return an HTTP response containing a histogram of berry growth times.",
    responses={
        200: {
            "description": "OK",
            "content": {
                "image/png": {"schema": {"type": "string", "format": "binary"}}
            },
        },
        500: {
            "description": "Server Error",
            "content": {"text/html": {"schema": {"type": "string"}}},
        },
    },
)
@api_view(["GET"])
def plot_growth_time_frequency(request: HttpRequest) -> HttpResponse:
    data = cache.get("plot_growth_time_frequency_data")
    if data is None:
        try:
            data: BerryData = fetch_all_berry_data()
        except Exception as e:
            return render(request, "error.html", {"error": str(e)})
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.hist(data.growth_times, bins=10)
        ax.set_xlabel("Growth Time")
        ax.set_ylabel("Frequency")
        ax.set_title("Frequency of Berry Growth Times")
        response = HttpResponse(content_type="image/png")
        fig.savefig(response, format="png")
        cache.set("plot_growth_time_frequency_data", response, timeout=3600)
    else:
        response = data

    return response
