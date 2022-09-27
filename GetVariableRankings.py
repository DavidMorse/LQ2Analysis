from argparse import ArgumentParser
import json
import os 

parser = ArgumentParser()
parser.add_argument("-d", "--dir", dest="directory", help="directory where BDT training outputs are stored", metavar="DIRECTORY")
options = parser.parse_args()
bdtDir = str(options.directory)

outFiles = [bdtDir+'/'+ff.replace('\n','') for ff in os.popen('ls '+bdtDir+"| grep \".out\"").readlines()]

checkStr = "Ranking input variables (method specific)..."
checkVars = "Using variable"
rankingDict = {}

for outFile in outFiles:
    mass = outFile.split("__M")[-1].split('_')[0]
    rankingDict[mass] = []
    with open(outFile,'r') as f:
        l = 0
        startLine = -1
        nVars = 0
        for line in f:
            if checkVars in line:
                nVars += 1
            if checkStr in line:
                startLine = l+6
            l+=1
            if startLine > 0:
                if l in range(startLine, startLine+nVars):
                    rankingDict[mass].append(line.strip())

with open("BDTVariableRankings.json",'w') as outJSON:
    json.dump(rankingDict, outJSON, indent = 4)

with open("BDTVariableRankings.json",'r') as inJSON:
    rankings = json.load(inJSON)

strToLatexMath = {
    "M_uujj2": r"$M_{{\mu j}_2}$",
    "M_uujj1": r"$M_{{\mu j}_1}$",
    "M_uu": r"$M_{\mu\mu}$",
    "DR_dimuonjet1": r"$\Delta R\,(\mu_1+\mu_2, j_1)$",
    "Pt_miss": r"$\vec{p}_T^{miss}$",
    "St_uujj": r"$S_T$",
    "Pt_muon1": r"$p_T\,(\mu_1)$",
    "M_uujj": r"$M_{\mu\mu jj}$",
    "Pt_muon2": r"$p_T\,(\mu_2)$",
    "Pt_jet1": r"$p_T\,(j_1)$",
    "Pt_jet2": r"$p_T\,(j_2)$"
}

latexStr = ""
for key in sorted(rankings, key = int):
    mass = str(key)
    print "Formatting for LaTeX mass =",mass,"GeV"
    latexStr += r"\b"+"egin{table}[htb]\n"
    latexStr += "\t\caption{A ranking of input variables by their importance in training a BDT with a $M_{\mathrm{LQ}}="+mass+"$~GeV signal sample.}\n"
    latexStr += "\t"+r"\b"+"egin{center}\n"
    latexStr += "\t\t"+r"\b"+"egin{tabular}{lll} \hline \hline\n"
    latexStr += "\t\t\tRank & Variable & Importance "+r" \\"+" \hline\n"
    length = len(rankings[key])
    i = 0
    for line in rankings[key]:
        i += 1
        rank = line.split(":")[1].strip()+"."
        var = line.split(":")[2].strip()
        latexVar = strToLatexMath[var]
        importance = line.split(":")[-1].strip()
        lineStr = "\t\t\t"+rank+" & "+latexVar+" & "+importance+r" \\"
        if i == length:
            lineStr += " \hline \hline\n"
        else:
            lineStr += "\n"
        latexStr += lineStr
    latexStr += "\t\t\end{tabular}\n"
    latexStr += "\t\t\label{tab:bdtRank"+mass+"}\n"
    latexStr += "\t\end{center}\n"
    latexStr += "\end{table}\n"
    latexStr += "\n"

with open("BDTVariableRankingsTables.txt",'w') as outTxt:
    outTxt.write(latexStr)


    

    
