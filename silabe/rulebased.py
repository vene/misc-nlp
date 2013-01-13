# coding=utf8
# Author: Octavia-Maria Sulea
# License: Simplified BSD

# test it!
#voc="aeiouy"
#cons="bcdfghjklmnprstvxz"
#liquid="lr"
#stop="bcdfghptv"
#cc_o=["ch", "gh", "gv", "cv", "sp", "sc", "st", "sf", "zb", "zg", "zd", "zv", "jg", "jd", "sm", "sn", "sl", "zm", "zl", "jn", "tr", "cl", "cr", "pl", "pr", "dr", "gl", "gr", "br", "bl", "fl", "fr", "vl", "vr", "hr", "hl", "ml", "mr"]
#ccc_o=["spl", "spr", "str", "jgh", "zdr", "scl", "scr", "zgl", "zgr", "sfr"]
#cc_e=["sc", "sf", "sl", "sp"]
#dif=["ea", "oa", "ia", "ua", "iu", "uu", "ie", "ii"]
#trif=["eoa", "eai", "eau", "iau"]
#hiat=["aa","au", "ae", "ie", "ai", "ee", "oe", "oo", "yu"]
voc = u"aeiouăîâ"
cons = u"bcdfghjklmnprsștțvxz"
liquid = u"lr"
stop = u"bcdfghptv"
cc_o = [
    u"ch",
    u"gh",
    u"sp",
    u"sc",
    u"st",
    u"sf",
    u"zb",
    u"zg",
    u"zd",
    u"zv",
    u"șk",
    u"șp",
    u"șt",
    u"șf",
    u"șv",
    u"jg",
    u"jd",
    u"sm",
    u"sn",
    u"sl",
    u"șm",
    u"șn",
    u"șl",
    u"zm",
    u"zl",
    u"jn",
    u"tr",
    u"cl",
    u"cr",
    u"pl",
    u"pr",
    u"dr",
    u"gl",
    u"gr",
    u"br",
    u"bl",
    u"fl",
    u"fr",
    u"vl",
    u"vr",
    u"hr",
    u"hl",
    u"ml",
    u"mr"
]
ccc_o = [
    u"spl",
    u"spr",
    u"șpl",
    u"șpr",
    u"str",
    u"ștr",
    u"jgh",
    u"zdr",
    u"scl",
    u"scr",
    u"zgl",
    u"zgr",
    u"sfr"
]
cc_e = [
    u"sc",
    u"sf",
    u"sl",
    u"sp"
]
dif = [
    u"ea",
    u"oa",
    u"ia",
    u"ua",
    u"uă",
    u"iu",
    u"uu",
    u"ie"
]
trif = [
    u"eoa",
    u"eai",
    u"eau",
    u"iau"
]
hiat = [
    u"aa",
    u"au",
    u"ae",
    u"ie",
    u"ai",
    u"ee",
    u"oe"
]


def ccv(cuv, i):
    if cuv[i] in stop and cuv[i+1] in liquid: #avem stop+liquid combo
        cuv=cuv[:i] + '-' + cuv[i:] #despartim -CCV
        #print cuv
        i=i+3 #trecem peste CC si '-'
    else: #nu avem decat C-CV
        cuv=cuv[:i+1] + '-' + cuv[i+1:] #despartim
        #print cuv
        i=i+3
    return cuv,i


def cccv(cuv, i):
    if cuv[i+1:i+3] in cc_o: #ultimele doua C sunt valid onset
        if cuv[i+1:i+3] in cc_e: #daca ultimele doua C sunt in exceptie
            cuv=cuv[:i+2] + '-' + cuv[i+2:] #despartim CC-C
            i=i+4
        else: #valid onset
            cuv=cuv[:i+1] + '-' + cuv[i+1:] #despartim C-CC
            #print cuv
            i=i+4 #sarim peste secventa
    else: #C-CC nu e valid
        cuv=cuv[:i+2] + '-' + cuv[i+2:] #despartim CC-C
        #print cuv
        i=i+4 #sarim peste secventa
    return cuv,i


def ccccv(cuv,i):
    if cuv[i+1:i+4] in ccc_o: #avem C-CCC
        cuv=cuv[:i+1] + '-' + cuv[i+1:]
        i=i+5
    elif cuv[i+2:i+4] in cc_o: #avem CC-CC
        cuv=cuv[:i+2] + '-' + cuv[i+2:]
        i=i+5
    else: #avem CCC-C
        cuv=cuv[:i+3] + '-' + cuv[i+3:]
        i=i+5
    return cuv, i


def vvv(cuv, i):
    if cuv[i:i+3] in trif: #e triftong (pleoape)
        i=i+3 #trec peste triftong
    elif cuv[i+1:i+3] in dif:
        cuv=cuv[:i+1] + '-' + cuv[i+1:] #despart V-VV
        i=i+4 #trec peste VVV si -
        #print cuv
    else: #caz ambiguu pe care il tratam ca triftong
        i=i+3 #sarim peste, fara sa despartim
    return cuv,i


def syll(cuv):
    i=0
    nucleu=0
    while i<len(cuv)-1:
        #print i, cuv[i]
        if cuv[i] in voc: #daca incepe cu vocala
            nucleu=1 #am dat peste nucleu
            if cuv[i+1] in voc: #avem VV
                if (i+2)<=len(cuv)-1: #exista cuv[i+2]
                    if cuv[i+2] in voc: #avem VVV (ploua, pleoape)
                        if (i+3)<=len(cuv)-1: #exista cuv(i+3)
                            if cuv[i+3] in voc: #avem VVVV
                                cuv=cuv[:i+2] + '-' + cuv[i+2:] #despartim VV-VV
                                i=i+5
                            else: #avem VVVC
                                cuv,i=vvv(cuv,i)
                        else: #suntem la sf si avem VVV
                            cuv,i=vvv(cuv,i)
                    else: #avem VVC
                        if cuv[i:i+2] in dif: #avem diftong
                            i=i+2 #trec peste diftong
                        elif cuv[i:i+2] in hiat: #avem hiat
                            cuv=cuv[:i+1] + '-' + cuv[i+1:] #despartim V-V
                            #print cuv
                            i=i+3 #trec peste cele 2 vocale si '-'
                        else: #e o secv VV pe care nu stim cum sa o tratam
                            i=i+2 #asa ca trecem peste fara sa o separam
                else: #suntem la sfarsit
                    i=i+2
            else: #avem VC
                i=i+1 #trec peste vocala de pe poz i
        else: #cuv[i] e consoana
            if nucleu == 0: #daca nu avem nucleu deja
                i=i+1 #suntem la inceputul cuv=> onset=> trecem peste
            else: #daca avem nucleu
                if cuv[i+1] in cons: #avem secventa CC
                    if (i+2) < (len(cuv)-1):#exista i+2 & nu suntem la sfarsit
                        if cuv[i+2] in cons: #avem secventa CCC
                            if (i+3) < (len(cuv)-1):#exista i+3
                                if cuv[i+3] in cons: #avem CCCC
                                    if (i+4) < (len(cuv)-1):
                                        if cuv[i+4] in cons: #avem CCCCC optsprezece
                                            cuv=cuv[:i+2] + '-' + cuv[i+2:]
                                            i=i+6
                                        else: #avem CCCCV
                                            cuv,i=ccccv(cuv,i)
                                    else:#suntem la sfarsit
                                        if cuv[i+4] in cons: #avem CCCCC la sfarsit
                                            i=i+5 #sarim la sfarsit
                                        else:#avem CCCCV
                                            cuv,i=ccccv(cuv,i)
                                else: #avem CCCV
                                    cuv,i=cccv(cuv,i)
                            else: #suntem la sfarsit
                                if cuv[i+3] in cons: #avem CCCC la sfarsit
                                    i=i+4
                                else: #avem CCCV la sfarsit
                                    cuv,i=cccv(cuv,i)
                        else: #avem CCV
                            cuv,i=ccv(cuv,i) #tratam secventa CCV
                    elif (i+2)==(len(cuv)-1): #suntem la sf cuv
                        if cuv[i+2] in voc: #CCV la sf. (problema cu CCi)
                            cuv,i=ccv(cuv,i) #tratam secventa CCV
                        else: # avem CCC la sf. ('stm' din 'astm')
                            i=i+3
                    else:#avem CC la sfarsit
                        break
                else: #avem secventa CV
                    cuv=cuv[:i] + '-' + cuv[i:] #despartim -CV (conform MOP)
                    #print cuv
                    i=i+2
    return cuv

#probleme (infara de ambiguitatile de diftong):
#copci vs. craci vs. citi (toate iau i drept vocala), orice vs. varice
#se rezolva folosind eticheta de functie sintactica
#i.e. verbele au i vocalic mai putin la -esti, iar restul au i semivocalic
#u-ul ambiguul
