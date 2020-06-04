import csv
from school import School

RAW_DATASET = 'raw_school_sites.csv'
TOS_DATASET = 'District Schools Terms of Service.csv'
PREPARED_DATASET = 'scraping-sites.csv'
MISSING_DISTRICTS = 'DistrictsMissing.txt'


def main():
    '''This script sanitizes and prepares the dataset for scraping'''

    allowed_district_names = filter_district_tos()
    allowed_district_names = sanitize_names(allowed_district_names)
    raw_sites_list = read_raw_dataset()
    filtered_sites_list = filter_by_tos(raw_sites_list, allowed_district_names)
    filtered_sites_list = filter_by_missing(filtered_sites_list)
    write_prepared_dataset(filtered_sites_list)


def filter_by_tos(raw_school_sites, allowed_district_names):
    '''Filters out schools which don't allow scraping
    Returns
    list: fitered school sites, 
    '''
    non_matching_districts = set()
    filtered_sites = []
    allowed_set = set(allowed_district_names)
    allowed_set.update(
        ['dade', 'fau lab sch', 'uf lab sch', 'fsu lab sch', 'famu lab sch'])
    for site in raw_school_sites:
        raw_district_name = site[1].lower()
        if raw_district_name in allowed_set:
            filtered_sites.append(site)
        else:
            non_matching_districts.add(raw_district_name)
    print('non matching districts', non_matching_districts)
    return filtered_sites


def filter_by_missing(school_sites):
    '''Filters out school entries who sent their records (3 districts left for testing)'''
    missing_set = set()
    non_missing = set()
    filtered_sites = []
    with open(MISSING_DISTRICTS, mode='r') as missing_f:
        for missing_district in missing_f:
            missing_set.add(missing_district.lower().strip())
    missing_set.add('dade')
    # print("Missing districts ==>", missing_set)
    
    for site in school_sites:
        district_name = site[1].lower()
        if district_name in missing_set:
            filtered_sites.append(site)
        else:
            non_missing.add(district_name)
    # print('Non-missing districts: ', non_missing)
    return filtered_sites

def write_prepared_dataset(sites_list):
    with open(PREPARED_DATASET, mode='w') as prepared_f:
        writer = csv.writer(prepared_f, delimiter=',')
        writer.writerow(['district', 'district_name', 'school',
                         'school_name', 'year', 'website', 'has sro (0/1)'])
        writer.writerows(sites_list)
    print(
        f'Wrote {len(sites_list)} school sites in scraping-sites.csv after filtering')


def read_raw_dataset():
    '''Reads raw dataset csv file only parsing single instances of each school
    and ignoring entries with missing websites
    '''
    raw_sites_list = []
    school_names_set = set()
    with open(RAW_DATASET) as raw_f:
        reader = csv.reader(raw_f, delimiter=',')
        count = 0
        for line in reader:
            if (count == 0):
                count += 1
                continue
            elif (len(line[5]) == 0 or line[5].isspace()):
                continue
            elif (line[3] in school_names_set):
                continue
            else:
                line[5] = line[5].strip()
                line[4] = '2019'  # Currently defaulting to latest year
                school_names_set.add(line[3])
                raw_sites_list.append(line)
                count += 1
    print(f'Parsed total {count - 1} school sites from raw dataset')
    return raw_sites_list


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
    '''Normalize district names for easy processing 
    For eg: Broward County Public Schools -> broward
    '''
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
    sanitized_list.remove('gulf')
    sanitized_list.remove('okeechobee')
    return sanitized_list


if __name__ == "__main__":
    main()
