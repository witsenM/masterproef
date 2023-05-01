from meta import Meta
from analysis import Analysis
import image

prev_ab = None

with open('data.csv', 'w') as data_file:
    data_file.write('name\tavg_a\tstd_a\tavg_b\tstd_b\n')
    for meta in Meta.find_all():
        print(f"Processing {meta.name()}")
        analysis = Analysis(meta.name())
        my_ab = None

        if not analysis.rgb_mask_is_valid(1):
            print("\tCreating RGB mask")
            analysis.save_blank_rgb_mask()

        if analysis.rgb_mask_is_valid(2):
            my_ab = analysis.mask_ab()
            print('\tLoaded AB from file')
        elif prev_ab is not None:
            if analysis.size_matches_with(prev_ab):
                print('\tReusing AB from previous image')
                my_ab = prev_ab
            else:
                print('\tCould not reuse AB: size mismatch')

        if my_ab is None:
            print(f"\tSkipping {meta.name()}: no AB was found")
            continue

        image.save(f"tmp/{meta.name()}_a.png", analysis.masked_orig(my_ab[0]))
        image.save(f"tmp/{meta.name()}_b.png", analysis.masked_orig(my_ab[1]))

        (stats_a, stats_b) = analysis.compute_stats(my_ab)
        data_file.write(f"{meta.name()}\t{stats_a[0]}\t{stats_a[1]}\t{stats_b[0]}\t{stats_b[1]}\n")

        prev_ab = my_ab
