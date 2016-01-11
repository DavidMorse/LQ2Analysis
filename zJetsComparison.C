#include <TCanvas>
#include <TH1>
#include <TH2>
#include <TH1F>
#include <TH2F>
#include <TTree>
#include <TFile>
#include <THStack>
#include <sstream>
#include <string>
#include <vector>
#include <pair>
#include <TLatex>
#include <TMathText>

void zJetsComparison(){

  using namespace std;
  
  gStyle->SetOptStat(0);
  
  gStyle->SetPaintTextFormat("4.2f");
  //gStyle->SetTitleX(0.1f);gStyle->SetTitleW(0.8f);
  gStyle->SetTitleBorderSize(0);
  TCanvas *c1 = new TCanvas("c1","",1400,1000);
  c1->cd();
  
  
  //TFile f_mbin("NTupleAnalyzer_Spring15MC_2015_08_19_11_32_18/SummaryFiles/DYJetsToLL_Mbin.root","READ");
  //TFile f_mbin("NTupleAnalyzer_Spring15_Zjets_Mbin_new_2015_09_18_09_53_55/SummaryFiles/DYJetsToLL_Mbin.root","READ");
  TFile f_mbin("NTupleAnalyzer_Spring2015_noskimZjets_2015_09_21_12_13_08/SummaryFiles/DYJetsToLL_Mbin.root","READ");
  TFile f_inc ("NTupleAnalyzer_Spring15MC_2015_08_16_13_36_43/SummaryFiles/ZJets.root","READ");
  TFile f_ht  ("NTupleAnalyzer_Spring15MC_2015_08_16_13_36_43/SummaryFiles/ZJetsHT.root","READ");
  TFile f_sig  ("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1000.root","READ");
  TFile f_jb2012("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/ZJetsJBin.root","READ");
  TFile f_2012_mup("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/ZJetsMatchUp.root","READ");
  TFile f_2012_mdown("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/ZJetsMatchDown.root","READ");
  TFile f_2012_sup("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/ZJetsScaleUp.root","READ");
  TFile f_2012_sdown("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/ZJetsScaleDown.root","READ");
  TFile f_jb2012_sup("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/ZJetsJBinScaleUp.root","READ");
  TFile f_jb2012_sdown("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/ZJetsJBinScaleDown.root","READ");


  const int nFiles=4,nFilesTot=11;
  
  TTree* trees[nFilesTot]={(TTree*)f_mbin.Get("PhysicalVariables"),
			(TTree*)f_inc.Get("PhysicalVariables"),
			(TTree*)f_ht.Get("PhysicalVariables"),
			(TTree*)f_sig.Get("PhysicalVariables"),
			(TTree*)f_jb2012.Get("PhysicalVariables"),
			(TTree*)f_2012_mup.Get("PhysicalVariables"),
			(TTree*)f_2012_mdown.Get("PhysicalVariables"),
			(TTree*)f_2012_sup.Get("PhysicalVariables"),
			(TTree*)f_2012_sdown.Get("PhysicalVariables"),
			(TTree*)f_jb2012_sup.Get("PhysicalVariables"),
			(TTree*)f_jb2012_sdown.Get("PhysicalVariables"),
  };
  
  TString junk = "junk.root";
  TFile f(junk,"RECREATE");
  TTree* weightZjets = (TTree*)trees[0]->CopyTree("weight_amcNLO");

  const int nCuts=24;
  float L_int=3000.;
  TCut cuts[nCuts]={"(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>0)&&(St_uujj>0)&&(M_uujj2>0)",//preselection
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(DR_muon1muon2>0.3)&&(M_uu>0)&&(St_uujj>0)&&(M_uujj2>0)",//object selection only
		 "((abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>50)&&(St_uujj>300)&&(M_uujj2>0))",//preselection
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>100)&&(St_uujj>380)&&(M_uujj2>115)",//300 GeV
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>115)&&(St_uujj>460)&&(M_uujj2>115)",//350 GeV
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>125)&&(St_uujj>540)&&(M_uujj2>120)",//etc.
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>140)&&(St_uujj>615)&&(M_uujj2>135)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>150)&&(St_uujj>685)&&(M_uujj2>155)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>165)&&(St_uujj>755)&&(M_uujj2>180)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>175)&&(St_uujj>820)&&(M_uujj2>210)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>185)&&(St_uujj>880)&&(M_uujj2>250)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>195)&&(St_uujj>935)&&(M_uujj2>295)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>205)&&(St_uujj>990)&&(M_uujj2>345)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>215)&&(St_uujj>1040)&&(M_uujj2>400)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>220)&&(St_uujj>1090)&&(M_uujj2>465)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>230)&&(St_uujj>1135)&&(M_uujj2>535)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>235)&&(St_uujj>1175)&&(M_uujj2>610)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>245)&&(St_uujj>1210)&&(M_uujj2>690)",
		    "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>245)&&(St_uujj>1310)&&(M_uujj2>790)",//new1
		    "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>245)&&(St_uujj>1410)&&(M_uujj2>890)",//new2
		    "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>245)&&(St_uujj>1510)&&(M_uujj2>990)",//new3
		    "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>245)&&(St_uujj>1610)&&(M_uujj2>1090)",//new4
		    "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>275)&&(St_uujj>2500)&&(M_uujj2>1300)",//new5, newly optimized 2000gev
		    "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>1200)&&(St_uujj>3000)&&(M_uujj2>1400)"};//new6, super high
  TCut MuuCut = "(M_uu>100)";TCut weightcutonly = "weight_central";
  TCut amcElse = "(M_uu>100)*3000"; TCut amcElsePlusPre = amcElse*cuts[2]*MuuCut;
  TCut amc = "weight_amcNLO";
  TCut amcAll = "weight_amcNLO*3000*(M_uu>100)";
  TCut weightcut2 = "weight_central*3000.";TCut weightcut = weightcut2*MuuCut*cuts[2];TCut weightcutAMC = weightcut2*MuuCut*cuts[2]*amc;

  float bgs[nCuts]={13952.41,
		    2783.1,
		    0.,
		    1583.,
		    819.,
		    434.3,
		    234.7,
		    142.6,
		    77.,
		    47.4,
		    31.,
		    20.3,
		    10.18,
		    5.7,
		    2.71,
		    1.38,
		    0.87,
		    0.41,
		    0.,
		    0.};
  TH2F* h_eff = new TH2F("h_eff",";stop mass;LQ2 optimized cut mass",nFiles,200,2050,nCuts,150,150+nCuts*50);
  TH2F* h_sOverSplusB = new TH2F("h_sOverSplusB",";stop mass;LQ2 optimization cut mass",nFiles,200,2050,nCuts,150,150+nCuts*50);
  TH2F* h_yields = new TH2F("h_yields",";;",nFilesTot,200,200+nFilesTot*50,nCuts,150,150+nCuts*50);//2012 LQ2 optim. cut mass
  
  
 
  //}
 float xsecs[37]={60.6,20.3,8.04,3.59,1.74,.906,.496,.284,.169,.103,.0648,.0416,.0273,.0182,.0123,.00845,.00586,.00411,.00291,.00208,.00150,.00109,.000795,.000585,.000433,.000321,.000240,.000180,.000135,.000102,.0000774,.0000588,.0000448,.0000343,.0000262,.0000201,.0000155};
  float nEvents[37]={50000,48352,49307,50000,50000,50000,50000,50000,50000,50000,47954,49163,50000,48906,50000,50000,50000,48569,50000,46916,49742,49072,49543,48560,50000,50000,49599,49400,48725,50000,50000,50000,50000,47520,47402,50000,49768};


  TH1F *h_Muu[nFiles], *h_Muujj1[nFiles],*h_Muujj2[nFiles],*h_STuujj[nFiles],*h_PTu1[nFiles],*h_PTu2[nFiles],*h_PTj1[nFiles],*h_PTj2[nFiles],*h_jetCount[nFiles];  
 
  bool doXsecs=1;//1 to scale by correct cross sections, 0 to scale arbitrarily for visual use
  for(int i=0;i<nFiles;i++){
    TString nam1 = "h_Muujj1";nam1+=i;
    TString nam2 = "h_Muujj2";nam2+=i;
    TString ptnam1 = "h_PTu1";ptnam1+=i;
    TString ptnam2 = "h_PTu2";ptnam2+=i;
    TString ptjnam1 = "h_PTj1";ptjnam1+=i;
    TString ptjnam2 = "h_PTj2";ptjnam2+=i;
    TString stNam ="h_STuujj";stNam+=i;
    TString muuNam ="h_Muu";muuNam+=i;
    TString jcNam ="h_jetCount";jcNam+=i;
    h_Muu[i] = new TH1F(muuNam,"M_{uu};M_{uu};Arbitrary Units",100,0,5000);
    h_Muujj1[i] = new TH1F(nam1,"M_{uujj1};M_{uujj1};Arbitrary Units",100,0,5000);
    h_Muujj2[i] = new TH1F(nam2,"M_{uujj2};M_{uujj2};Arbitrary Units",100,0,5000);
    h_PTu1[i] = new TH1F(ptnam1,"P_{T}(muon1);P_{T}(muon1);Arbitrary Units",100,0,5000);
    h_PTu2[i] = new TH1F(ptnam2,"P_{T}(muon2);P_{T}(muon2);Arbitrary Units",100,0,5000);
    h_PTj1[i] = new TH1F(ptjnam1,"P_{T}(jet1);P_{T}(jet1);Arbitrary Units",100,0,5000);
    h_PTj2[i] = new TH1F(ptjnam2,"P_{T}(jet2);P_{T}(jet2);Arbitrary Units",100,0,5000);
    h_STuujj[i] = new TH1F(stNam,"ST_{uujj};ST_{uujj};Arbitrary Units",100,0,10000);
    h_jetCount[i] = new TH1F(jcNam,"Jet Count;Jet Count;Arbitrary Units",50,0,50);
    h_Muu[i]->Sumw2();h_Muujj1[i]->Sumw2();h_Muujj2[i]->Sumw2();h_STuujj[i]->Sumw2();
    h_PTu1[i]->Sumw2();h_PTu2[i]->Sumw2();h_PTj1[i]->Sumw2();h_PTj1[i]->Sumw2();h_jetCount[i]->Sumw2();
    if(doXsecs){
      h_Muu[i]->GetYaxis()->SetTitle("Events");
      h_Muujj1[i]->GetYaxis()->SetTitle("Events");
      h_Muujj2[i]->GetYaxis()->SetTitle("Events");
      h_PTu1[i]->GetYaxis()->SetTitle("Events");
      h_PTu2[i]->GetYaxis()->SetTitle("Events");
      h_PTj1[i]->GetYaxis()->SetTitle("Events");
      h_PTj2[i]->GetYaxis()->SetTitle("Events");
      h_STuujj[i]->GetYaxis()->SetTitle("Events");
      h_jetCount[i]->GetYaxis()->SetTitle("Events");
      
      h_Muu[i]->SetMarkerSize(0);
      h_Muujj1[i]->SetMarkerSize(0);
      h_Muujj2[i]->SetMarkerSize(0);
      h_PTu1[i]->SetMarkerSize(0);
      h_PTu2[i]->SetMarkerSize(0);
      h_PTj1[i]->SetMarkerSize(0);
      h_PTj2[i]->SetMarkerSize(0);
      h_STuujj[i]->SetMarkerSize(0);
      h_jetCount[i]->SetMarkerSize(0);
      
      trees[i]->Project(muuNam,"M_uu",weightcut);
      trees[i]->Project(nam1,"M_uujj1",weightcut);
      trees[i]->Project(nam2,"M_uujj2",weightcut);
      trees[i]->Project(ptnam1,"Pt_muon1",weightcut);
      trees[i]->Project(ptnam2,"Pt_muon2",weightcut);
      trees[i]->Project(ptjnam1,"Pt_jet1",weightcut);
      trees[i]->Project(ptjnam2,"Pt_jet2",weightcut);
      trees[i]->Project(stNam,"St_uujj",weightcut);
      trees[i]->Project(jcNam,"JetCount",weightcut);
    }
    else{
      trees[i]->Project(muuNam,"M_uu","");
      trees[i]->Project(nam1,"M_uujj1","");
      trees[i]->Project(nam2,"M_uujj2","");
      trees[i]->Project(ptnam1,"Pt_muon1","");
      trees[i]->Project(ptnam2,"Pt_muon2","");
      trees[i]->Project(ptjnam1,"Pt_jet1","");
      trees[i]->Project(ptjnam2,"Pt_jet2","");
      trees[i]->Project(stNam,"St_uujj","");
      trees[i]->Project(jcNam,"JetCount","");
    }
  }

  h_weightAMC = new TH1F("h_weightAMC","weight_amcNLO*weight_amcNLO;weight_amcNLO;Events",250,-10,10);h_weightAMC->Sumw2();
  h_PTu1w = new TH1F("h_PTu1w","P_{T}(muon1)*weight_amcNLO;P_{T}(muon1);Events",100,0,5000);h_PTu1w->Sumw2();
  h_PTu1x = new TH1F("h_PTu1x","P_{T}(muon1);P_{T}(muon1);Events",100,0,5000);h_PTu1x->Sumw2();
  weightZjets->Project("h_PTu1w","Pt_muon1",amcElsePlusPre);
  weightZjets->Project("h_weightAMC","weight_amcNLO",amcElsePlusPre);
  h_PTu1w->SetMarkerSize(0);std::cout<<"h_PTu1w events: "<<h_PTu1w->Integral()<<std::endl;
  trees[0]->Project("h_PTu1x","Pt_muon1",weightcutonly);


  if(doXsecs)c1->SetLogy(1);

  //cout<<"\nm_uu: "<<h_Muu[0]->Integral(0,-1)<<"   jetCount: "<<h_jetCount[0]->Integral(0,-1)<<endl<<endl;
  //cout<<"\nm_uu: "<<h_Muu[1]->Integral(0,-1)<<"   jetCount: "<<h_jetCount[1]->Integral(0,-1)<<endl<<endl;

  for(int i=1;i<3;i++){
    float weight = h_Muu[0]->Integral(0,-1)/h_Muu[i]->Integral(0,-1);
    h_Muu[i]->Scale(weight,"");
    h_Muujj1[i]->Scale(weight,"");
    h_Muujj2[i]->Scale(weight,"");
    h_PTu1[i]->Scale(weight,"");
    h_PTu2[i]->Scale(weight,"");
    h_PTj1[i]->Scale(weight,"");
    h_PTj2[i]->Scale(weight,"");
    h_STuujj[i]->Scale(weight,"");
    h_jetCount[i]->Scale(weight,"");
}


  /*
  for(int j=0;j<nFiles;j++){
    trees[j]->Draw("","St_uujj","(M_uu>0)");
    TH1F *h_St = (TH1F*)trees[j]->GetHistogram();
    float yield = h_St->Integral();
    h_yields->Fill(150+50*(j+1),100+50,yield);
    h_St->Delete();  
    for(int k=2;k<=18;++k){
      //cout<<"j:"<<j<<" k:"<<k<<endl;
      trees[j]->Draw("St_uujj","St_uujj",cuts[k-1]);
      TH1F *h_St2 = (TH1F*)trees[j]->GetHistogram();
      yield = h_St2->Integral();
      h_yields->Fill(150+50*(j+1),100+k*50,yield);
      h_St2->Delete();  
    }
  }
  */
  for(int j=0;j<nFilesTot;j++){
    TString histname="h_St";histname+=j;
    TH1F *h_St = new TH1F(histname,"",1,0,100000);
    if(j==0)trees[j]->Project(histname,"St_uujj",amc);
    else trees[j]->Project(histname,"St_uujj","");
    float yield = h_St->Integral();
    h_yields->Fill(150+50*(j+1),100+50,yield);
    h_St->Delete();  
    for(int k=2;k<=nCuts;++k){
      histname+=k;
      //if(k==3)continue;
      TH1F *h_St2 = new TH1F(histname,"",1,0,100000);
      if(j==0)trees[j]->Project(histname,"St_uujj",cuts[k-1]*amc);
      else trees[j]->Project(histname,"St_uujj",cuts[k-1]);
      float yield = h_St2->Integral();
      h_yields->Fill(150+50*(j+1),100+k*50,yield);
      //cout<<"j:"<<j<<" k:"<<k<<" yield:"<<yield<<endl;
      h_St2->Delete();  
    }
  }
  


  float lowbound=0.;doXsecs?lowbound=.01:;
  h_Muu[nFiles-1]->GetXaxis()->SetRangeUser(0,3500);
  h_Muu[nFiles-1]->GetYaxis()->SetRangeUser(.0001,3000);
  h_Muu[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muu[nFiles-1]->Draw("e");
  h_Muu[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_Muu[i]->SetLineColor(2**(i+1));
    h_Muu[i]->Draw("esames");
    // i++;
  }
  leg = TLegend(0.4,0.55,0.86,0.82,"","brNDC");	
  leg.SetHeader("13 TeV (3 fb^{-1} ) DY+Jets sim., M_{ll}>100");
  leg.AddEntry(h_Muu[0],"amc@NLO Z-mass binned","le");
  leg.AddEntry(h_Muu[2],"MG LO HT binned * NLO/LO","le");
  leg.AddEntry(h_Muu[1],"MG LO inclusive * NLO/LO","le");
  leg.AddEntry(h_Muu[3],"LQ LO M=1000 GeV","le");
  //leg.AddEntry(h_Muu[3],"8TeV MG LO jet binned","le");
  leg.SetFillStyle(0);leg.SetBorderSize(0);
  leg.Draw();
  c1->Print("Plots/zJetsComp/M_uu.pdf");
  
  h_Muujj1[nFiles-1]->GetXaxis()->SetRangeUser(0,3700);
  h_Muujj1[nFiles-1]->GetYaxis()->SetRangeUser(.0001,3000);
  h_Muujj1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muujj1[nFiles-1]->Draw();
  h_Muujj1[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_Muujj1[i]->SetLineColor(2**(i+1));
    h_Muujj1[i]->Draw("sames");
    // i++;
  }
  leg.Draw();
  c1->Print("Plots/zJetsComp/M_uujj1.pdf");
  
  h_Muujj2[nFiles-1]->GetXaxis()->SetRangeUser(0,3700);
  h_Muujj2[nFiles-1]->GetYaxis()->SetRangeUser(.0001,3000);
  h_Muujj2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muujj2[nFiles-1]->Draw();
  h_Muujj2[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_Muujj2[i]->SetLineColor(2**(i+1));
    h_Muujj2[i]->Draw("sames");
    // i++;
  }

  leg.Draw();
  c1->Print("Plots/zJetsComp/M_uujj2.pdf");

  h_STuujj[nFiles-1]->GetXaxis()->SetRangeUser(0,5500);
  h_STuujj[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,3000);
  h_STuujj[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_STuujj[nFiles-1]->Draw();
  h_STuujj[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_STuujj[i]->SetLineColor(2**(i+1));
    h_STuujj[i]->Draw("sames");
    // i++;
  }

  leg.Draw();
  c1->Print("Plots/zJetsComp/ST_uujj.pdf");
  
  for(int i=0;i<nFiles-1;i++){
    //h_PTu1[i]->Rebin(100);
  }

  h_PTu1w->SetLineColor(kYellow);

  h_PTu1[nFiles-1]->GetXaxis()->SetRangeUser(0,2000);
  h_PTu1[nFiles-1]->GetYaxis()->SetRangeUser(2e-3,3000);
  h_PTu1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTu1[nFiles-1]->Draw();
  h_PTu1[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_PTu1[i]->SetLineColor(2**(i+1));
    h_PTu1[i]->Draw("sames");
    // i++;
  }
  h_PTu1[0]->Draw("sames");
  h_PTu1w->Draw("SAMES");
  leg.Draw();
  c1->Print("Plots/zJetsComp/Pt_muon1.pdf");
  
  h_PTu1w->Draw("");
  c1->Print("Plots/zJetsComp/Pt_muon1_preweight.pdf");

  h_weightAMC->Draw();
  c1->Print("Plots/zJetsComp/amctimsamc.pdf");

  std::cout<<"pt integral: "<<h_PTu1w->Integral()<<"  amc wieght int: "<<h_weightAMC->Integral()<<std::endl;

  h_PTu2[nFiles-1]->GetXaxis()->SetRangeUser(0,2000);
  h_PTu2[nFiles-1]->GetYaxis()->SetRangeUser(2e-3,3000);
  h_PTu2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTu2[nFiles-1]->Draw();
  h_PTu2[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_PTu2[i]->SetLineColor(2**(i+1));
    h_PTu2[i]->Draw("sames");
    // i++;
  }

  leg.Draw();
  c1->Print("Plots/zJetsComp/Pt_muon2.pdf");
  
  h_PTj1[nFiles-1]->GetXaxis()->SetRangeUser(0,2000);
  h_PTj1[nFiles-1]->GetYaxis()->SetRangeUser(2e-3,3000);
  h_PTj1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTj1[nFiles-1]->Draw();
  h_PTj1[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_PTj1[i]->SetLineColor(2**(i+1));
    h_PTj1[i]->Draw("sames");
    // i++;
  }
  leg.Draw();
  c1->Print("Plots/zJetsComp/Pt_jet1.pdf");
  
  h_PTj2[nFiles-1]->GetXaxis()->SetRangeUser(0,2000);
  h_PTj2[nFiles-1]->GetYaxis()->SetRangeUser(2e-3,3000);
  h_PTj2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTj2[nFiles-1]->Draw("e");
  h_PTj2[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_PTj2[i]->SetLineColor(2**(i+1));
    h_PTj2[i]->Draw("esames");
    // i++;
  }

  leg.Draw();
  c1->Print("Plots/zJetsComp/Pt_jet2.pdf");
 
  c1->SetLogy(0);
  h_jetCount[nFiles-1]->GetXaxis()->SetRangeUser(0,20);
  h_jetCount[nFiles-1]->GetYaxis()->SetRangeUser(0,500);
  h_jetCount[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_jetCount[nFiles-1]->Draw("e");
  h_jetCount[nFiles-1]->SetLineColor(kBlack);
  for(int i=0;i<nFiles-1;i++){
    h_jetCount[i]->SetLineColor(2**(i+1));
    h_jetCount[i]->Draw("esames");
    // i++;
  }

  leg.Draw();
  c1->Print("Plots/zJetsComp/jetCount.pdf");

  c1->SetLogy(0);
  int y=200;
  h_yields->SetTitle("DY+Jets raw event counts");//h_yields->SetTitleBorderSize(0);
  int b=1;
  h_yields->GetXaxis()->SetBinLabel(b,"amc@NLO Z-mass binned");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"LO inclusive");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"LO HT binned");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"LQ LO M=1000");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV LO jet binned");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV match up");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV match down");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV scale up");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV scale down");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV jet bin scale up");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV jet bin scale down");b++;
  //h_yields->GetYaxis()->SetBinLabel(1,"#mu>42, jet>110 GeV");
  h_yields->GetYaxis()->SetBinLabel(1,"");
  h_yields->GetYaxis()->SetBinLabel(2,"+ #mu#mujj object selection");
  h_yields->GetYaxis()->SetBinLabel(3,"+ Preselection");
  //h_eff->GetYaxis()->SetBinLabel(1,"Preselection");
  // h_eff->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
  //h_sOverSplusB->GetYaxis()->SetBinLabel(1,"Preselection");
  // h_sOverSplusB->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
  for(int b=1;b<nCuts;b++){
    int j=b-17;
    stringstream ss;ss <<y;
    string str=ss.str();
    //h_yields->GetXaxis()->SetBinLabel(b,str.c_str());
    if(b<=3){h_eff->GetXaxis()->SetBinLabel(b,str.c_str());
      h_sOverSplusB->GetXaxis()->SetBinLabel(b,str.c_str());}
    if(b>=3 && b<18){
      h_yields->GetYaxis()->SetBinLabel(b+1,str.c_str());
      h_eff->GetYaxis()->SetBinLabel(b+1,str.c_str());
      h_sOverSplusB->GetYaxis()->SetBinLabel(b+1,str.c_str());
    }
    if(b>=18){
      TString str2="new";str2+=j;
      h_yields->GetYaxis()->SetBinLabel(b+1,"");
      //j++;
    }
    
    y+=50;
  }
  //h_eff->GetZaxis()->SetRangeUser(lowbound.,1.);
  h_eff->GetYaxis()->SetTitleSize(0.05);
  // h_eff->Draw("colztext");
  // c1->Print("Plots/zJetsComp/efficiencyTable.png");
  // c1->Print("Plots/zJetsComp/efficiencyTable.pdf");
  
  h_sOverSplusB->GetYaxis()->SetTitleSize(0.05);
  h_sOverSplusB->GetZaxis()->SetRangeUser(.077,140);
  //c1->SetLogz(0);
   //  h_sOverSplusB->Draw("colztext");
  //c1->Print("Plots/zJetsComp/sOverSqrtSplusB.png");
  //c1->Print("Plots/zJetsComp/sOverSqrtSplusB.pdf");
  
  gStyle->SetPaintTextFormat("4.0f");
  c1->SetLogz(1);
  h_yields->GetYaxis()->SetTitleSize(0.05);
  h_yields->GetYaxis()->SetLabelSize(0.044);
  h_yields->GetXaxis()->SetLabelSize(0.04);
  h_yields->GetZaxis()->SetRangeUser(0,100000);
  h_yields->Draw("colztext");
  TLatex T1;T1.SetNDC();
  T1.SetTextAlign(12);
  T1.SetTextSize(0.021);
  float tlx =0.0,tly=.68,step=.0325;
  T1.DrawLatex(tlx,tly,"+ m_{uu}>245 st>1310 m_{uj2}>790");tly+=step;
  T1.DrawLatex(tlx,tly,"+ m_{uu}>245 st>1410 m_{uj2}>890");tly+=step;
  T1.DrawLatex(tlx,tly,"+ m_{uu}>245 st>1510 m_{uj2}>990");tly+=step;
  T1.DrawLatex(tlx,tly,"+ m_{uu}>245 st>1610 m_{uj2}>1090");tly+=step;
  T1.DrawLatex(tlx,tly,"+ m_{uu}>275 st>2500 m_{uj2}>1300");tly+=step;
  T1.DrawLatex(tlx,tly,"+ m_{uu}>1200 st>3000 m_{uj2}>1400");tly+=step;
  T1.SetTextSize(0.03);
  T1.DrawLatex(.3349,.88,"13 TeV #leftarrow");T1.DrawLatex(.446,.88,"#rightarrow 8 TeV");T1.DrawLatex(.7425,.88,"#rightarrow FastSim");
  TLatex T2;T2.SetNDC();T2.SetTextAngle(90);T2.SetTextSize(0.03);
  T2.DrawLatex(.12,.28,"2012 LQ2 optim. cut mass");
  T2.SetTextSize(0.023);T2.SetTextAngle(0);
  T2.DrawLatex(.02,.12,"#splitline{skim: #mu1>42, #mu2>42,}{jet1>110, jet2>40, ST>250}");
  TLine l;l.SetLineWidth(2);l.DrawLineNDC(.436,.13,.436,.9);tlx=.7325;l.DrawLineNDC(tlx,.13,tlx,.9);
  c1->Update();
  //c1->Print("Plots/zJetsComp/yields.png");
  c1->Print("Plots/zJetsComp/yields.pdf");
  
    
}
