import csv

RAW_DATASET = 'raw_school_sites.csv'
TOS_DATASET = 'District Schools Terms of Service.csv'
PREPARED_DATASET = 'scraping-sites.csv'


def main():
    '''This script sanitizes and prepares the dataset for scraping'''

    allowed_district_names = filter_district_tos()
    sanitized_district_names = sanitize_names(allowed_district_names)
    print('Sanitized names: ', sanitized_district_names)

def filter_district_tos():
    '''Filter out districts that don't allow scraping.

    Returns:
        list (string): array of district name that allow scraping
    '''
    allowed_district_arr = []
    with open(TOS_DATASET) as tos_f:
        reader = csv.reader(tos_f, delimiter=',')
        count = 0
        for line in reader:
            if (count == 0) or (line[2] == 'no'):
                count += 1
                continue
            allowed_district_arr.append(line[0])
            count += 1
    print(f'Processed a total of {count} districts')
    print(f'{len(allowed_district_arr)} districts allow web scraping')
    return allowed_district_arr


def sanitize_names(district_name_arr):
    sanitized_list = []
    error_list = []
    for name in district_name_arr:
        name = name.lower()
        idx = name.find('county')
        if idx == -1:
            idx = name.find('school')
        if idx != -1:
            sanitized_name = name[:idx]
            # Remove 'district' keyword
            district_idx = sanitized_name.find('district')
            if district_idx != -1:
                sanitized_name = sanitized_name[:district_idx]
            sanitized_list.append(sanitized_name.strip())
        else:
            error_list.append(name)
    if len(error_list) > 0:
        print(f'Unable to sanitize name for: {error_list}')
    return sanitized_list


if __name__ == "__main__":
    main()
