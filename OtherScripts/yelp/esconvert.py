import json

def transform_for_elasticsearch_bulk():
    # Specifying the name of your DynamoDB formatted file.
    input_filename = 'yelp_data_dynamodb.json'
    
    # A default file name for the Elasticsearch Bulk Script in the same folder.
    output_filename = 'to_elasticsearch_bulk.json'
    
    # A container for our index and source documents in ES Bulk API required JSON Lines format.
    with open(input_filename, 'r') as infile:
        dynamodb_data = json.load(infile)
    
    with open(output_filename, 'w') as outfile:
        for item in dynamodb_data:
            meta_dict = {
                "index": {
                    "_index": "restaurants",
                    "_id": item['business_id']['S']
                }
            }
            es_document = {
                "RestaurantID": item['business_id']['S'],
                "cuisine": item['cuisine']['S']
            }
            outfile.write(json.dumps(meta_dict) + '\n' + json.dumps(es_document) + '\n')

# Just call the function. The DynamoDB formatted JSON file should be in the same folder.
transform_for_elasticsearch_bulk()
