import collections
import numpy as np
import allel
import dadi

all_inds = set()
pops_to_inds = collections.defaultdict(set)
with open('1KG.YRI.CEU.popfile.txt') as popfile:
    for line in popfile:
        ind, pop = line.split()
        pops_to_inds[pop].add(ind)
        all_inds.add(ind)

callset = allel.read_vcf('1KG.YRI.CEU.biallelic.synonymous.snps.withanc.strict.subset.vcf.gz', 
                         fields=['samples', 'calldata/GT', 'variants/AA',
                                 'variants/ALT', 'variants/REF', 'variants/numalt',
                                 'variants/is_snp', 'variants/CHROM', 'variants/POS'],
                         #types = {'variants/ALT':'S1', 'variants/REF':'S1', 'variants/AA':'S1'}
                         )

# In PopFly ZI data, many times numalt > 1, but alt is N...
# And those N's are marked as a genotype allele

gt = allel.GenotypeArray(callset['calldata/GT'])
is_biallelic_snp = callset['variants/is_snp'] & (callset['variants/numalt'] == 1)
# Keep only biallelic SNPs
gt = gt.compress(is_biallelic_snp)

ref_all = callset['variants/REF'][is_biallelic_snp]
alt_all = callset['variants/ALT'][:,0][is_biallelic_snp]
aa_all = callset['variants/AA'][is_biallelic_snp]
chr_all = callset['variants/CHROM'][is_biallelic_snp]
pos_all = callset['variants/POS'][is_biallelic_snp]

pops_to_gts = {}
pops_to_counts = {}
for pop, samps in pops_to_inds.items():
    subset = [samp in pops_to_inds[pop] for samp in callset['samples']]
    gt_subset = gt.compress(subset, axis=1)
    # Could call to_haplotypes earlier to make sum a little simpler (and maybe faster?)
    ref_counts = (gt_subset == 0).sum(axis=(1,2))
    alt_counts = (gt_subset == 1).sum(axis=(1,2))
    pops_to_counts[pop] = ref_counts, alt_counts

dd = {}
for ii in range(len(ref_all)):
    data_this_snp = {}
    data_this_snp['outgroup_allele'] = aa_all[ii].upper()
    data_this_snp['segregating'] = ref_all[ii].upper(), alt_all[ii].upper()
    data_this_snp['calls'] = {}
    for pop, (ref_counts, alt_counts) in pops_to_counts.items():
        data_this_snp['calls'][pop] = (ref_counts[ii], alt_counts[ii])
    dd['{0:s}_{1}'.format(chr_all[ii], pos_all[ii])] = data_this_snp

pop_ids, ns = ['YRI','CEU'], [20,24]
fs = dadi.Spectrum.from_data_dict(dd, pop_ids, ns)

datafile = '1KG.YRI.CEU.biallelic.synonymous.snps.withanc.strict.subset.vcf.gz'
dd_old = dadi.Misc.make_data_dict_vcf(datafile, '1KG.YRI.CEU.popfile.txt')
fs_old = dadi.Spectrum.from_data_dict(dd, pop_ids, ns)