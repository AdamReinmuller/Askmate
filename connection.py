import csv


def import_csv(filename):
    with open(filename) as file:
        csv_content = list(csv.DictReader(file))
    return csv_content


def export_csv(filename, content_dict):
    import util
    """
    :param filename:
    :param content_dict: is a list of ordered dicts
    Beware: it deletes the content
    """
    fieldnames = util.get_headers(filename)
    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(content_dict)


# a = import_csv('data/question.csv')
# fn = a[0].keys()
# print(fn)
# export_csv('data/try.csv', a, fn)
# print(import_csv('data/try.csv'))
