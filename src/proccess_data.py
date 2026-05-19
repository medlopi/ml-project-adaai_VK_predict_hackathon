import pandas as pd

def get_sample_data(path, part_size):
    df = pd.read_csv(f'../{path}')
    zero_class = df[df['target'] == 0]
    one_class = df[df['target'] == 1]

    n_zero = len(zero_class)
    n_one = len(one_class)

    zero_sample = zero_class.sample(int(n_zero * part_size), random_state=42)

    res_sample = pd.concat([zero_sample, one_class], ignore_index=True)
    save_path = '../data/small_sample.csv'
    res_sample.to_csv(save_path)

    return res_sample


