import time
import logging


def filter_item_type(items):
    return list(filter(lambda item: item['type'] == 'item', items))


def filter_viewed_items(items, viewed_ids):
    ids = []
    not_viewed_items = []
    for item in items:
        if item['value']['id'] not in viewed_ids:
            not_viewed_items.append(item)
            ids.append(item['value']['id'])

    if not viewed_ids:
        viewed_ids += ids
        return []

    if len(viewed_ids) > 500:
        viewed_ids = viewed_ids[100:]

    viewed_ids += ids

    return not_viewed_items


def filter_ignore_list(items, ignore_list):
    try:
        allowed_items = []
        for item in items:
            if 'sellerInfo' in item['value'].keys():
                if item['value']['sellerInfo']['userKey'] not in ignore_list:
                    allowed_items.append(item)
            else:
                logging.debug('Items without sellerInfo')
                logging.debug(items)
                allowed_items.append(item)

        return allowed_items

    except Exception as exception:
        logging.error(f'Error in filter_ignore_list')
        logging.error(exception)
        logging.error(items)
        return items


def filter_old_time_items(items):
    unix_time = time.time()
    return list(filter(lambda item: item['value']['time'] > (unix_time - 7200), items))


def filter_by_region(items, region):
    return list(filter(lambda item: item['value']['uri_mweb'].find(region) != -1, items))