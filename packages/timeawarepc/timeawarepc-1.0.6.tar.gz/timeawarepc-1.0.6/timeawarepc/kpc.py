def kpc(suffStat, indepTest, alpha, labels, u2pd = 'relaxed', skelmethod = 'stable'):
    p = len(labels)
    skel = estimate_skeleton(indepTest, data_matrix, alpha)
    wanpdag = udag2wanpdag(gInput = skel, )
    return wanpdag
def udag2wanpdag(gInput, suffStat, indepTest='kernelCItest',alpha=0.05):
    
