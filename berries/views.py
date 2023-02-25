from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .util import BerryData, fetch_all_berry_data


def all_berry_stats(request: HttpRequest) -> JsonResponse:
    """Return a JSON response containing statistics on all berries."""
    try:
        data: BerryData = fetch_all_berry_data()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(data.to_json(), safe=False)


def plot_growth_time_frequency(request: HttpRequest) -> HttpResponse:
    """Return an HTTP response containing a histogram of berry growth times."""
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

    return response
