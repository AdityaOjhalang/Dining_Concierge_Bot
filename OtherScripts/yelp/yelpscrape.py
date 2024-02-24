import requests
import json
import datetime

# Your updated API key
API_KEY = "ruPwsYp_ThA3MLodequF46pXchlXVrHeH9wIF2j-wbPK_VCNBkELMJEt1YE0vMvYsI9bTlBNi3_Hs1S-Cyl6HQcWveOGOnhniAobe1Zs4UNt5jBY-qy7-bQPeAjVZXYx"
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
DEFAULT_LOCATION = 'Manhattan'
SEARCH_LIMIT = 50

def search(api_key, term, location, offset):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': offset
    }
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    url = f'{API_HOST}{SEARCH_PATH}'
    response = requests.get(url, headers=headers, params=url_params)

    return response.json()

def format_for_dynamodb(item):
    """Converts item to DynamoDB format."""
    return {
        'business_id': {'S': item['id']},
        'insertedAtTimestamp': {'S': str(datetime.datetime.now())},
        'name': {'S': item['name']},
        'address': {'S': ', '.join(item['location']['display_address'])},
        'coordinates': {'S': f"{item['coordinates']['latitude']},{item['coordinates']['longitude']}"},
        'number_of_reviews': {'N': str(item['review_count'])},
        'rating': {'N': str(item['rating'])},
        'zip_code': {'S': item['location']['zip_code']},
        'cuisine': {'S': item['cuisine']}
    }

def scrape_yelp():
    cuisines = ['Chinese', 'Indian', 'Italian']
    all_items = []
    for cuisine in cuisines:
        print(f"Scraping {cuisine} cuisine")
        cuisine_term = cuisine + ' restaurant'
        offset = 0
        res_id = []
        while len(res_id) < 50:  # Update the condition to collect only 50 restaurants
            res = search(API_KEY, cuisine_term, DEFAULT_LOCATION, offset)
            if not res.get('businesses'):
                print(f"No more {cuisine} cuisine found")
                break
            for x in res['businesses']:
                if x['id'] in res_id:
                    continue
                x['cuisine'] = cuisine  # Add cuisine type to each item
                res_id.append(x['id'])
                if len(res_id) >= 50:  # Stop once we have 50 restaurants for the cuisine
                    break
                formatted_item = format_for_dynamodb(x)
                all_items.append(formatted_item)
            if len(res_id) < 50:
                offset += SEARCH_LIMIT
        print(f"{cuisine} cuisine has {len(res_id)} rows")

    with open('yelp_data_dynamodb.json', 'w') as outfile:
        json.dump(all_items, outfile, indent=4)

def main():
    scrape_yelp()

if __name__ == '__main__':
    main()
