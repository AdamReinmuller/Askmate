import connection

def get_id(file):
    file_all = connection.import_csv(file)
    new_id = int(file_all[-1]['id']) + 1
    return new_id

def get_headers(file):
    file_all = connection.import_csv(file)
    headers = list(file_all[0].keys())
    return headers


#print(get_headers('data/question.csv'))
