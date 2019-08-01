#------------------------SIMULATED ANNEALING---------------------#


def obj_function_swap01(binsList , binDest , binSrc , objSrc):
	sommeCarre = 0
	for i in range(len(binsList)):
		if i == binDest:
			sommeCarre += (sum(binsList[i]) + binsList[binSrc][objSrc] )**2
		elif i== binSrc:
			sommeCarre += (sum(binsList[i]) - binsList[binSrc][objSrc] )**2
		else:
			sommeCarre+= (sum(binsList[i]))**2
	return sommeCarre

def obj_function_swap11(binsList , bin1 , bin2 , obj1,obj2):
	sommeCarre = 0
	for i in range(len(binsList)):
		if i == bin1:
			sommeCarre += (sum(binsList[i]) + binsList[bin2][obj2] - binsList[bin1][obj1] )**2
		elif i== bin2:
			sommeCarre += (sum(binsList[i])+ binsList[bin1][obj1] - binsList[bin2][obj2] )**2
		else:
			sommeCarre+= (sum(binsList[i]))**2
	return sommeCarre

def init_obj(binsList):
	sommeCarre =0
	for i in binsList:
		sommeCarre += (sum(i))**2
	return sommeCarre


def SA(temperature_init, temperature_target, cooling_factor,n,capacity,w):
    wbins , bins = FF(n,capacity,w)
    #print("sol init : " + str(len(bins)))
    #print(wbins)

    cost = init_obj(bins)

    temperature = temperature_init

    while temperature > temperature_target:

        #print("--------------------------------")
        #print("------------- new iter ----------------")
        bins_prim = copy.deepcopy(bins)
        wbins_prim = copy.deepcopy(wbins)
        #print(bins)
        #print("actual sol " + str(len(wbins_prim)))
        #print(wbins_prim)
        max_sol_indecator = list()
        bin_r1 = 0; bin_r2 = 0; obj_r1 = 0; obj_r2 = 0
        stop = False
        max_iter = 50
        while not stop :
            max_sol_indecator = list()
            rand_bins=sample(range(len(bins_prim)), 2)
            #print("rand_bins: "+str(rand_bins))
            #print(bins_prim[bin_r1])
            #print(bins_prim[bin_r2])
            bin_r1 = rand_bins[0]
            bin_r2 = rand_bins[1]
            obj_r1=sample(range(len(bins_prim[bin_r1])), 1)[0]
            obj_r2=sample(range(len(bins_prim[bin_r2])), 1)[0]


            if max_iter > 0 :
                max_iter -= 1
                if wbins_prim[bin_r1] >= bins_prim[bin_r2][obj_r2]:
                    #print(str(wbins_prim[bin_r1])+">"+str(bins_prim[bin_r2][obj_r2]))
                    max_sol_indecator.append(obj_function_swap01(bins_prim,bin_r1,bin_r2,obj_r2))
                    stop = True
                else :
                    max_sol_indecator.append(0)

                if wbins_prim[bin_r2]>=bins_prim[bin_r1][obj_r1]:
                    #print(str(wbins_prim[bin_r2])+">"+str(bins_prim[bin_r1][obj_r1]))
                    max_sol_indecator.append(obj_function_swap01(bins_prim,bin_r2,bin_r1,obj_r1))
                    stop = True
            else :
                if wbins_prim[bin_r1] >= bins_prim[bin_r2][obj_r2]:
                    #print(str(wbins_prim[bin_r1])+">"+str(bins_prim[bin_r2][obj_r2]))
                    max_sol_indecator.append(obj_function_swap01(bins_prim,bin_r1,bin_r2,obj_r2))
                    stop = True
                else :
                    max_sol_indecator.append(0)

                if wbins_prim[bin_r2]>=bins_prim[bin_r1][obj_r1]:
                    #print(str(wbins_prim[bin_r2])+">"+str(bins_prim[bin_r1][obj_r1]))
                    max_sol_indecator.append(obj_function_swap01(bins_prim,bin_r2,bin_r1,obj_r1))
                    stop = True
                else:
                    max_sol_indecator.append(0)

                if wbins_prim[bin_r2]+bins_prim[bin_r2][obj_r2]>=bins_prim[bin_r1][obj_r1] and wbins_prim[bin_r1]+bins_prim[bin_r1][obj_r1]>=bins_prim[bin_r2][obj_r2]:
                    #print(str(wbins_prim[bin_r1]-bins_prim[bin_r1][obj_r1])+">"+str(bins_prim[bin_r2][obj_r2]))
                    #print(str(wbins_prim[bin_r2]-bins_prim[bin_r2][obj_r2])+">"+str(bins_prim[bin_r1][obj_r1]))
                    max_sol_indecator.append(obj_function_swap11(bins_prim,bin_r1,bin_r2,obj_r1,obj_r2))
                    stop = True


        max_obj = max(max_sol_indecator)

        take_next = False
        proba = 1
        if (max_obj > cost) :
            take_next = True
        else :
            r = uniform(0, 1);
            try :
                proba = math.exp((max_obj - cost)/temperature)
            except OverflowError:
                proba = 0
            if (r < proba):
                take_next = True

        #print("Temp: " + str(temperature) + "; delta: " + str(max_obj - cost) + ";  random: " + str(r) + ";  proba: " + str(proba))
        if take_next :   
            indice_max = max_sol_indecator.index(max_obj)
            #print("swap : " + str(indice_max))
            if indice_max == 0 :
                bins_prim[bin_r1].append(bins_prim[bin_r2][obj_r2])
                wbins_prim[bin_r1] -= bins_prim[bin_r2][obj_r2]
                wbins_prim[bin_r2] += bins_prim[bin_r2][obj_r2]
                #print("before pop -- 1")
                #print(bins_prim[bin_r2])
                bins_prim[bin_r2].pop(obj_r2)
                #print("After pop")
                #print(bins_prim[bin_r2])
                if(wbins_prim[bin_r2] == capacity):
                    bins_prim.pop(bin_r2)
                    wbins_prim.pop(bin_r2)

            elif indice_max == 1:
                bins_prim[bin_r2].append(bins_prim[bin_r1][obj_r1])
                wbins_prim[bin_r2] -= bins_prim[bin_r1][obj_r1]
                wbins_prim[bin_r1] += bins_prim[bin_r1][obj_r1]
                #print("before pop -- 2")
                #print(bins_prim[bin_r1])
                bins_prim[bin_r1].pop(obj_r1)
                #print("After pop")
                #print(bins_prim[bin_r1])
                if(wbins_prim[bin_r1] == capacity):
                    bins_prim.pop(bin_r1)
                    wbins_prim.pop(bin_r1)

            else:
                bins_prim[bin_r2].append(bins_prim[bin_r1][obj_r1])
                wbins_prim[bin_r2] -= bins_prim[bin_r1][obj_r1]
                wbins_prim[bin_r2] += bins_prim[bin_r2][obj_r2]
                bins_prim[bin_r1].append(bins_prim[bin_r2][obj_r2])
                wbins_prim[bin_r1] -= bins_prim[bin_r2][obj_r2]
                wbins_prim[bin_r1] += bins_prim[bin_r1][obj_r1]
                #print("before pop --3")
                #print(bins_prim[bin_r2])
                #print(bins_prim[bin_r1])

                bins_prim[bin_r2].pop(obj_r2)
                bins_prim[bin_r1].pop(obj_r1)
                #print("After pop")
                #print(bins_prim[bin_r2])
                #print(bins_prim[bin_r1])

            #print("---- updated ---")
            bins = copy.deepcopy(bins_prim)
            wbins = copy.deepcopy(wbins_prim)
            cost = max_obj

        temperature *= cooling_factor

    #print("sol final : " + str(len(bins)))
    return bins
		
