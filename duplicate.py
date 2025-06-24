seen = set()
duplicates = []
count = 0
dup   = 0
for i in [-0.16, -0.12, -0.08, -0.04, 0, 0.04, 0.08, 0.12, 0.16, 0.20]:
    for j in [-0.10, -0.08, -0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08, 0.10]:
        for k in [-0.30, -0.24, -0.18, -0.12, -0.06, 0, 0.06, 0.12, 0.18, 0.24, 0.30, 0.33]:
            for l in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
                for m in [-0.10, -0.08, -0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08, 0.10]:
                    for n in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
                        if ((abs(l) <= 0.1 and abs(n) <= 1.0) or 
                            (abs(l) <= 0.4 and abs(n) <= 0.9) or 
                            (abs(l) <= 0.6 and abs(n) <= 0.8) or 
                            (abs(l) <= 0.7 and abs(n) <= 0.7) or 
                            (abs(l) <= 0.9 and abs(n) <= 0.6) or 
                            (abs(l) <= 1.0 and abs(n) <= 0.5)
                            ): # 406560 w/o symmetrization
                            count += 1
                            if str([i,j,k,l,m,n]) in seen:
                                duplicates.append(str([i,j,k,l,m,n]))
                            else:
                                seen.add(str([i,j,k,l,m,n]))
                            if l != 0:
                                count += 1
                                if str([i,j,k,-l,m,n]) in seen:
                                    duplicates.append(str([i,j,k,-l,m,n]))
                                else:
                                    seen.add(str([i,j,k,-l,m,n]))
                            if m != 0 or n != 0:
                                count += 1
                                if str([i,j,k,l,-m,-n]) in seen:
                                    duplicates.append(str([i,j,k,l,-m,-n]))
                                else:
                                    seen.add(str([i,j,k,l,-m,-n]))
                            if l != 0 and (m != 0 or n != 0):
                                count += 1 # 1437480 with symmetrization
                                if str([i,j,k,-l,-m,-n]) in seen:
                                    duplicates.append(str([i,j,k,-l,-m,-n]))
                                else:
                                    seen.add(str([i,j,k,-l,-m,-n]))
                            print(count)
                            if l == 0 and n == 0 and m > 0:
                                dup += 1
print("Duplicates: ", dup)
for d in duplicates:
    print(d)
print("len(seen) = ", len(seen))
print("len(duplicates) = ", len(duplicates))
