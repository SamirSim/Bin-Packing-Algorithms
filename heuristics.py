#------------------------HEURISTICS---------------------#


#First-Fit-Decreasing
def FFD(n, c, w):
    if n == 0:
        return 0

    wSorted = w.copy()
    wSorted.sort(reverse = True)
    return FF(n, c, wSorted)

#Max-Rest
def MR(n, c, w):
    Bins = [c]

    for i in range(len(w)):
        k = np.argmax(Bins)
        if w[i] <= Bins[k]:
            Bins[k] -= w[i]
        else:
            Bins.append(c)
            Bins[len(Bins)-1] -= w[i]
    return len(Bins)

#Next-Fit
def NF(n, c, w):
    if n == 0:
        return 0

    curBin = c
    nBins = 1
    for i in range(len(w)):
        if w[i] <= curBin:
            curBin -= w[i]
        else:
            curBin = c-w[i]
            nBins += 1
    return nBins

#Next-Fit-Decreasing
def NFD(n, c, w):
    if n == 0:
        return 0

    wSorted = w.copy()
    wSorted.sort(reverse = True)
    return NF(n, c, wSorted)

#Best-Fit
def BF(n, c, w):
    if n == 0:
        return 0

    Bins = [c]
    for i in range(len(w)):
        RC = []
        RCind = []
        for j in range(len(Bins)):
            if w[i] <= Bins[j]:
                RC.append(Bins[j] - w[i])
                RCind.append(j)
        if len(RC) > 0:
            Bins[RCind[np.argmin(RC)]] -= w[i]
        else:
            Bins.append(c)
            Bins[len(Bins)-1] -= w[i]
            
    return len(Bins)
  #First-Fit
def FF(n, c, w):
    if n == 0:
        return 0

    Bins = [c]
    result = [[]]
    for i in range(len(w)):
        nFit = False
        for j in range(len(Bins)):
            if w[i] <= Bins[j]:
                Bins[j] = Bins[j] - w[i]
                result[j].append(w[i])

                break
            if j == len(Bins)-1:
                nFit = True

        if nFit is True:
            Bins.append(c)
            result.append([])
            result[-1].append(w[i])
            Bins[len(Bins)-1] -= w[i]
    return (Bins,result)

