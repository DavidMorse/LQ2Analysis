import json

with open("AllSystematics.json") as inJson:
    sysDict = json.load(inJson)

massesToSort = []
sysDictsToSort = []

for mass in sysDict:
    intMass = int(mass)
    massesToSort.append(intMass)
#    sysDictsToSort.append(sysDict[mass])
sortedMasses = sorted(massesToSort)
#sortedMasses, sortedSysDicts = zip(*sorted(zip(massesToSort, sysDictsToSort)))

tableStr = ""
tableStr += r"\begin{table}[htbp]" + "\n"
tableStr += r"\begin{center}" + "\n"
tableStr += r"\caption{Muon scale systematic uncertainties estimated with the Generalized Endpoint method and their effect on signal and background in 2016 for each final selection cut. All uncertainties are symmetric.}" + "\n"
tableStr += r"\begin{tabular}{llcc}" + "\n"
tableStr += r"\hline \hline" + "\n"
tableStr += r"LQ Mass [GeV] & BDT Threshold & Sys. Signal [\%] & Sys. Background [\%] \\ \hline" + "\n"
for m in sortedMasses:
    mass = str(m)
    cut = str(round(float(sysDict[mass]["Cut"].split(")*")[0].split(">")[-1]),3))
    SysSig = str(round(float(sysDict[mass]["Systematic"]["Signal"]),2))
    SysBkg = str(round(float(sysDict[mass]["Systematic"]["Background"]),2))
    if mass == "4000":
        tableStr += mass + " & " + cut + " & " + SysSig + " & " + SysBkg + r" \\ \hline\hline" + "\n"
    else:
        tableStr += mass + " & " + cut + " & " + SysSig + " & " + SysBkg + r" \\" + "\n"

tableStr += r"\end{tabular}" + "\n"
#tableStr += r"\label{tab:GESysUncertainties_2016_uubj}" + "\n"
tableStr += r"\end{center}" + "\n"
tableStr += r"\end{table}" + "\n"

print tableStr