from collections import Counter

from django.shortcuts import render_to_response

counter_show = Counter()
counter_click = Counter()


def index(request):
    from_landing = request.GET.get('from-landing')
    if from_landing == 'original':
        counter_click['original'] += 1
        return render_to_response('index.html')
    elif from_landing == 'test':
        counter_click['test'] += 1
        return render_to_response('index.html')
    elif not from_landing:
        return render_to_response('index.html')


def landing(request):
    ab_test_arg = request.GET.get('ab-test-arg')
    if ab_test_arg == 'original':
        counter_show['original'] += 1
        return render_to_response('landing.html')
    elif ab_test_arg == 'test':
        counter_show['test'] += 1
        return render_to_response('landing_alternate.html')


def stats(request):
    test_conversion = counter_click['test'] / counter_show['test']
    original_conversion = counter_click['original'] / counter_show['original']
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
