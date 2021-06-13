# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from typing import List
import requests
import os


def parse_channel_page_member_files():
    names = read_and_clean('slack_names_and_faces/slack_real_names_swe.txt')
    pref_names = read_and_clean('slack_names_and_faces/slack_pref_name_swe.txt')
    image_urls = read_and_clean('slack_names_and_faces/slack_image_swe.txt')
    image_urls = [image_url.replace('-48', '-193') for image_url in image_urls]  # get a bigger image 512x512

    print('Finished reading from files')
    # dedup
    nameDedupDict = {}
    for i, name in enumerate(names):
        # remove [ ] or other parsing artifact
        if len(name) < 5:
            continue

        if 'http' not in image_urls[i]:
            continue

        if name in nameDedupDict:
            continue
        else:
            nameDedupDict[name] = i

    print('Finished dedup')
    print(f'{len(nameDedupDict.keys())} items to process')

    full_names_clean = []
    pref_names_clean = []
    image_urls_clean = []
    for i in nameDedupDict.values():
        full_names_clean.append(names[i])
        pref_names_clean.append(pref_names[i])
        image_urls_clean.append(image_urls[i])

    download_images_if_needed(image_urls_clean)

    full_info = []
    for i, full_name in enumerate(full_names_clean):
        full_info.append((full_name, pref_names_clean[i],  os.path.basename(image_urls_clean[i])))

    print(full_info[:5])
    export_to_file('slack_output_swe.txt', full_info)


def download_images_if_needed(image_urls_clean):
    for i, image_url in enumerate(image_urls_clean):
        basename = os.path.basename(image_url)
        image_url_local = f'slack_names_and_faces/images/{basename}'
        if not os.path.isfile(image_url_local):
            res = requests.get(image_url)
            f = open(image_url_local, 'wb')
            f.write(res.content)
            f.close()


def parse_members_page_files():
    names = read_and_clean('slack_names_and_faces/slack_names.txt')
    titles = read_and_clean('slack_names_and_faces/slack_titles.txt')
    image_urls = read_and_clean('slack_names_and_faces/slack_images.txt')
    image_urls = [image_url.replace('-192', '-193') for image_url in image_urls]  # get a bigger image 512x512

    full_info = []

    for i, image_url in enumerate(image_urls):
        if 'http' not in image_url:
            print(f'warning: invalid url {image_url} on line {i}')
            continue

        basename = os.path.basename(image_url)
        image_url_local = f'slack_names_and_faces/images/{basename}'
        if not os.path.isfile(image_url_local):
            res = requests.get(image_url)
            f = open(image_url_local, 'wb')
            f.write(res.content)
            f.close()

        full_info.append((names[i], titles[i], basename))

    print(full_info[:5])
    export_to_file('slack_output.txt', full_info)


def export_to_file(output_file, info):
    with open(output_file, 'w') as f:
        for person in info:
            f.write(','.join(person))
            f.write('\n')


def read_and_clean(file_path: str) -> List[str]:
    with open(file_path) as f:
        output_raw = f.readlines()
    return [x.strip().replace('\"', '').replace(',', '') for x in output_raw]


def main():
    parse_channel_page_member_files()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
