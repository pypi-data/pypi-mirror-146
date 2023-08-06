# %%

fid = open('ZI_Chr2R_4000000_5000000.vcf')

newlines = []
# Read through header
line = fid.readline()
while line.startswith('#'):
    newlines.append(line)
    line = fid.readline()

while line.strip():
    # Split fields
    spl = line.split('\t', 5)

    # Pull out alternate alleles
    alts = spl[4].split(',')
    try:
        # Find the N alelle
        Ngt = alts.index('N')+1
        # Replace the N genotypes with missing data symbols
        spl[-1] = spl[-1].replace(str(Ngt), '.')
        # Reduce the integer designation of all remaining alleles
        for ii in range(Ngt+1, len(alts)+1):
            spl[-1] = spl[-1].replace(str(ii), str(ii-1))
        # Remove N from alts list
        del alts[Ngt-1]
        # Put the fixed alts back into spl
        spl[4] = ','.join(alts)
    except ValueError:
        pass 
    newlines.append('\t'.join(spl))
    line = fid.readline()

fid.close()

fid = open('ZI_Chr2R_4000000_5000000.fixed.vcf', 'w')
fid.writelines(newlines)
fid.close()