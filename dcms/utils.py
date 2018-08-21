# For unit testing, get the actual results when using API pagination
def get_results(data):
    if 'results' in data:
        return data['results']
    return data
