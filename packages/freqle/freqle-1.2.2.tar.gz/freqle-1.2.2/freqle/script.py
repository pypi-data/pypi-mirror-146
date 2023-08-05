from freqle import cluster
import freqle as fr
import matplotlib.pyplot as plt
import numpy as np

pal = cluster(Nbh = 200, n_mus = 300, cluster_eta = 1e9)
pal.populate(v = True)
pal.build_mass_grid()
pal.emit_GW(v = True, maximum_det_freq = 2048)
pal.calc_freq_distr(remove_outliers = False, v = True, nbins = 64, norm_distr=False)
#pal.plot_freq_distr(mu = 1e-12)



freq = pal.get_freqs()[250]

#freq = freq[freq < 550]

bins, counts, bin_size = fr.hist_by_row(freq, binsize=0.01, normalize=False)

cond = counts[0] > 10
bins = bins [0, :-1]
counts = counts [0]
bin_size = bin_size[0]
'''counts = counts [ cond ]
bins = bins [cond]
bin_size =bin_size [cond]'''

plt.plot(bins, counts, 'o')
#plt.bar(bins[0, :-1], counts[0], width = bin_size[0], align = 'edge')
plt.yscale('log')
#plt.xscale('log')
#plt.axhline(y = 1)
plt.show()