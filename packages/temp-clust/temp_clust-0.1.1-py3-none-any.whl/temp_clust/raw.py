#!/usr/bin/env python

from glob import glob
import os
import pandas as pd
import numpy as np
from psifr import fr

# data location (not public)
data_dir = 'data/ind_data'

# unique category variable per list - i.e., 12 scrambled, 3 serial, 3 structured
sub_cat_var = np.hstack([np.tile(np.arange(12), 8),  # scambled
                         np.tile(np.tile([1, 2, 3], 4), 8),  # serial
                         np.tile(np.repeat([1, 2, 3], 4), 8)])  # structured

# category mappings for items
item_category_mapping = pd.read_csv('data/item_category_mapping.csv')


def get_subs_num():
    """ """
    subs = [3, 5, 6, 11, 13, 14, 17, 18, 20, 21,
            22, 23, 24, 25, 26, 27, 28, 29, 31, 33,
            36, 38, 40, 41, 42, 43, 44, 46, 47, 48,
            50, 52, 53, 54, 55, 56, 57, 58, 60, 61,
            62, 63, 65, 67, 68, 69, 70, 71, 73, 75,
            76, 77, 79, 80, 81, 82, 84, 85, 86, 87,
            88, 89, 90, 92, 93, 94, 95, 97, 99]
    return subs


def generate_list_type_single(r):
    ''' '''
    if (r['list'] <= 8):
        list_type = 'scrambled'

    elif 9 <= r['list'] <= 16:
        list_type = 'serial'

    elif r['list'] > 16:
        list_type = 'structured'

    else:
        list_type = 'unknown'
    return list_type


def generate_list_type_four(r):
    ''' '''
    if r['list'] <= 2:
        list_type = 'scrambled'

    elif 3 <= r['list'] <= 4:
        list_type = 'serial'

    elif 5 <= r['list'] <= 6:
        list_type = 'structured'

    else:
        list_type = 'unknown'
    return list_type


def generate_four_list(r):
    """ """
    if r['position'] == 999.0:
        return np.nan
    else:
        if r['list'] <= 4:
            list_num = 1

        elif 5 <= r['list'] <= 8:
            list_num = 2

        elif 9 <= r['list'] <= 12:
            list_num = 3

        elif 13 <= r['list'] <= 16:
            list_num = 4

        elif 17 <= r['list'] <= 20:
            list_num = 5

        elif 21 <= r['list'] <= 24:
            list_num = 6

        else:
            list_num = 9

        return list_num


def get_subs_files(subs_num):
    """ """
    files = list()
    for sub_num in subs_num:
        # check existence - this confirms all data is there before proceeding.
        file = check_file(sub_num)
        files.append(file)
    return files


def check_file(sub_num):
    """ """
    file_name = os.path.join(data_dir, 'include', f'sub_{sub_num:03d}_stimuli_lists_GRADED.csv')
    file_path = glob(file_name)
    if len(file_path) != 1:
        raise IOError(f'Problem finding subject file for {sub_num:03d}')
    return file_path[0]


def process_file(sub_num, file, recall_type='recalled_order', v=0):
    """
    Description: Processes recall/study file to setup
        for the psfir data format. Recall type can be
        either 'recalled_order' (default), which is 24
        lists of 12 words or 'recalled_order_four',
        which is 6 lists with 48 words per list. This
        occurred after a participant recalled 4, 12
        item lists in a row.

    Input:
        file - absolute filepath (str)
        recall_type - 'recalled_order' or 'recalled_
            order_four'

    Output:
        dataframe - pandas dataframe in a format to
            be merged with other subjects with the
            psfir package

    """
    # sub_num = subs_num[0]
    # file = files[0]
    # recall_type = 'recalled_order'
    # v = 1

    if v: print(sub_num, file)

    columns = ['trial', recall_type, 'item', 'word_location_in_list', 'list']

    # load file
    p = pd.read_csv(file).reset_index().rename(columns={'index': 'trial'})

    # some renaming so plotting looks a little better
    p.columns = p.columns.str.strip('s')
    p = p.rename(columns={'words_shuffled': 'item',
                          'word_shuffled': 'item',
                          'list_number': 'list',
                          'recalled_four_list': 'recalled_order_four',
                          'recalled_list_four': 'recalled_order_four'
                          })

    # strip
    p['item'] = p['item'].str.strip()

    # replace ' ' with nans
    p[recall_type].replace({' ': np.nan}, inplace=True)
    p = p[columns]

    # maps semantic category to word
    p = p.merge(item_category_mapping, how='left')

    # separate out study section
    study = p[['item', 'list', 'word_location_in_list', 'category']].copy()
    study = study[(~study['word_location_in_list'].isnull())]
    study.rename(columns={'word_location_in_list': 'position'}, inplace=True)
    assert len(study) == 288

    # meta
    study['trial_type'] = 'study'
    if recall_type == 'recalled_order_four':
        study['position'] = np.tile(np.arange(1, 49), 6)
        study['list four'] = study.apply(generate_four_list, axis=1)
        study['list_type'] = study.apply(generate_list_type_four, axis=1)
        study.drop(columns=['list'], inplace=True)
        study.rename(columns={'list four': 'list'}, inplace=True)
    else:
        study['list_type'] = study.apply(generate_list_type_single, axis=1)

    # recall
    # get recalled words
    r = p[~p[recall_type].isnull()]

    # merge on item to get the associated list
    recall = r[[recall_type, 'item', 'list']]
    recall.rename({recall_type: 'position'}, axis=1, inplace=True)
    recall['trial_type'] = 'recall'
    recall = recall.merge(item_category_mapping, how='left')
    if recall_type == 'recalled_order_four':
        recall['list_type'] = recall.apply(generate_list_type_four, axis=1)

    else:
        recall['list_type'] = recall.apply(generate_list_type_single, axis=1)

    # merge
    pdf = pd.concat([study, recall]).reset_index(drop=True)
    pdf['subject'] = sub_num
    pdf['position'] = pd.to_numeric(pdf['position'], errors='coerce')
    pdf = pdf[['subject', 'list', 'position', 'item', 'list_type', 'trial_type', 'category']].sort_values(
        ['subject', 'list', 'position'])

    # hack after the fact to test checking order numbers
    pdf.rename({'list': 'list_number'}, axis=1, inplace=True)
    pdf = pdf[pdf.item.isnull()==False]
    return pdf


def get_bad_positions(pdf):
    """


    """
    # sorts to make sure position is in order from low to high
    sorted_pdf = pdf.sort_values(['trial_type', 'list_number', 'position'])

    # gets order errors
    list_order_errors = sorted_pdf.groupby(['subject', 'trial_type', 'list_number']).apply(
        lambda x: any(np.diff(x.position) != 1.))\
        .reset_index()\
        .rename({0: 'order_error'}, axis=1)

    # merge
    sorted_pdf_errors = sorted_pdf.merge(list_order_errors, on=['subject', 'trial_type', 'list_number'], how='left')

    return sorted_pdf_errors


def aggregate_subject_files(recall_type='recalled_order', subs=None, v=0):
    """ """
    if subs is None:
        subs_num = get_subs_num()

    n_subs = len(subs_num)
    files = get_subs_files(subs_num)
    full_sample = list()
    error_list = list()
    for sub_num, file in zip(subs_num, files):
        pdf = process_file(sub_num, file, recall_type=recall_type, v=v)
        epdf = get_bad_positions(pdf)
        full_sample.append(epdf)

    df = pd.concat(full_sample)

    # gets the data into psifr format.
    df.to_csv(f"data/temp_clust_{recall_type}_n-{n_subs:02d}.csv", index=None)
    print(f"Saved file: 'data/temp_clust_{recall_type}_n-{n_subs:02d}.csv'")
    return df


def main():
    """ """
    recall_types = ['recalled_order', 'recalled_order_four']
    for recall_type in recall_types:
        df = aggregate_subject_files(recall_type=recall_type, subs=None)


if __name__ == '__main__':
    main()
