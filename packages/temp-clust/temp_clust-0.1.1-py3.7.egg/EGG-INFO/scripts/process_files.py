from temp_clust import aggregate_subject_files

def main():
    """ """
    recall_types = ['recalled_order', 'recalled_order_four']
    for recall_type in recall_types:
        df = aggregate_subject_files(recall_type=recall_type, subs=None)


if __name__ == '__main__':
    main()