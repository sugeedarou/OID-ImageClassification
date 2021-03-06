import functools
import csv
import config

print('reading class ids')

class_ids = []
class_id_to_name = {}
with open(config.FILEPATH_CLASS_NAMES, encoding='utf-8') as f:
    next(f)
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        class_id = row[0]
        class_name = row[1].lower()
        class_ids.append(class_id)
        class_id_to_name[class_id] = class_name

print('reading class id to image ids mapping')

class_id_to_image_ids = {}
with open(config.FILEPATH_CLASS_ID_TO_IMAGE_IDS, encoding='utf-8') as f:
    for line in f:
        line_arr = line.rstrip().split(',')
        class_id = line_arr[0]
        image_ids = line_arr[1].split(';')
        class_id_to_image_ids[class_id] = image_ids


print('sorting classes by count')

def compare(x1, x2):
    return len(class_id_to_image_ids[x2]) - len(class_id_to_image_ids[x1])


class_ids = sorted(
    class_ids, key=functools.cmp_to_key(compare))

print('writing result to file')

if not config.DIRPATH_OUT.exists():
    config.DIRPATH_OUT.mkdir()

f = open(config.FILEPATH_CLASS_LIST_BY_IMAGE_COUNT, "w", encoding='utf-8', newline='')
writer = csv.writer(f)

for class_id in class_ids:
    class_name = class_id_to_name[class_id]
    # escape class names that include a comma
    if ',' in class_name:
        class_name = f'"{class_name}"'
    count = len(class_id_to_image_ids[class_id])
    writer.writerow([class_name, count])
f.close()

print('-------------- DONE --------------')