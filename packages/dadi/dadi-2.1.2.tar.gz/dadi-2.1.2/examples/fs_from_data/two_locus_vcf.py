import collections
import numpy as np
import allel
import dadi

# PopFly ZI data indicates N as an alternate allele, not as missing data. To fix that, I used this sequence of bcftools commands
# bcftools norm -m- ZI_Chr2R_1_1000000.vcf | bcftools filter -e'ALT="N"' -S . | bcftools norm -m+ | bcftools norm -m- | bcftools view -e'ALT="N"' > ZI_Chr2R_1_1000000.fixed.vcf

Na_rho = 1e8

fid = open('genetic_map_comeron2012_dm6_chr2R.txt')
header = fid.readline()
genetic_map = []
for line in fid:
    _, pos, rate = line.split()
    genetic_map.append((int(pos), float(rate)))
genetic_map = np.array(genetic_map)
genetic_map[:,1] = np.cumsum(genetic_map[:,1])

callset = allel.read_vcf('ZI_Chr2R_4000000_5000000.fixed.vcf',
                         fields=['samples', 'calldata/GT', 'variants/AA',
                                 'variants/ALT', 'variants/REF', 'variants/numalt',
                                 'variants/is_snp', 'variants/CHROM', 'variants/POS'],
                         # types = {'variants/ALT':'S1', 'variants/REF':'S1', 'variants/AA':'S1'}
                         )

pos_to_rho = Na_rho*1e-8 * np.interp(callset['variants/POS'], genetic_map[:,0], genetic_map[:,1])

# Popfly data. How to handle 'N' alleles?

gt = allel.GenotypeArray(callset['calldata/GT'])
#gt = allel.HaplotypeArray(callset['calldata/GT'])
is_biallelic_snp = callset['variants/is_snp'] & (callset['variants/numalt'] == 1)
# Keep only biallelic SNPs
gt = gt.compress(is_biallelic_snp).to_haplotypes()

ref_all = callset['variants/REF'][is_biallelic_snp]
alt_all = callset['variants/ALT'][:, 0][is_biallelic_snp]
aa_all = callset['variants/AA'][is_biallelic_snp]
chr_all = callset['variants/CHROM'][is_biallelic_snp]
pos_all = callset['variants/POS'][is_biallelic_snp]

rho_bins = [0.001, 0.2]
hap_counts_by_bin = [collections.defaultdict(int) for _ in rho_bins]

for ii in range(10):#len(ref_all)):
    g1 = gt[ii]
    # Check that we have both derived and ancestral alleles at this site
    if not (np.any(g1==1) and np.any(g1==0)):
        continue

    next_bin_start = ii+1
    for bin_ii, bin_val in enumerate(rho_bins):
        next_bin_end = pos_to_rho.searchsorted(pos_to_rho[ii]+bin_val)
        for jj in range(next_bin_start, next_bin_end):
            if jj > 10+next_bin_start:
                break
            g2 = gt[jj]
            if not (np.any(g2==1) and np.any(g2==0)):
                continue
            # Clever way to count haplotypes, based on score
            # Using fact that missing values are assigned -1
            #   0:0 -> 0,   0:1 -> 1,   1:0 -> 3,  1:1 -> 4
            # -1:0 -> -3, -1:1 -> -2, 0:-1 -> -1, 1:-1 -> 2
            hap_score = 3*g1 + g2
            # Assumed order 0,0; 0,1;, 1,0; 1,1
            hap_counts = (np.count_nonzero(hap_score == 0),
                          np.count_nonzero(hap_score == 1),
                          np.count_nonzero(hap_score == 3),
                          np.count_nonzero(hap_score == 4))
            hap_counts_by_bin[bin_ii][hap_counts] += 1
        next_bin_start = next_bin_end


#hap_score = 3*g1 + g2
#hap_counts = {'0:0': np.count_nonzero(hap_score == 0),
#              '0:1': np.count_nonzero(hap_score == 1),
#              '1:0': np.count_nonzero(hap_score == 3),
#              '1:1': np.count_nonzero(hap_score == 4)}
#
