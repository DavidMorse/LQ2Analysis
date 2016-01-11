#include <TCanvas.h>
#include <TH1.h>
#include <TH2.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TTree.h>
#include <TFile.h>
#include <THStack.h>
#include <sstream>
#include <string>
#include <vector>
#include <iostream>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TGraphAsymmErrors.h>
#include <TString.h>

void signalTest();

void signalTest(){

  using namespace std;
  
  gStyle->SetOptStat(0);
  
  gStyle->SetPaintTextFormat("4.2f");
  
  TCanvas *c1 = new TCanvas("c1","",1400,1000);
  c1->cd();
  
  
  TFile f_200("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj200.root","READ");
  TFile f_250("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj250.root","READ");
  TFile f_300("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj300.root","READ");
  TFile f_350("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj350.root","READ");
  TFile f_400("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj400.root","READ");
  TFile f_450("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj450.root","READ");
  TFile f_500("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj500.root","READ");
  TFile f_550("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj550.root","READ");
  TFile f_600("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj600.root","READ");
  TFile f_650("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj650.root","READ");
  TFile f_700("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj700.root","READ");
  TFile f_750("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj750.root","READ");
  TFile f_800("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj800.root","READ");
  TFile f_850("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj850.root","READ");
  TFile f_900("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj900.root","READ");
  TFile f_950("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj950.root","READ");
  TFile f_1000("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1000.root","READ");
  TFile f_1050("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1050.root","READ");
  TFile f_1100("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1100.root","READ");
  TFile f_1150("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1150.root","READ");
  TFile f_1200("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1200.root","READ");
  TFile f_1250("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1250.root","READ");
  TFile f_1300("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1300.root","READ");
  TFile f_1350("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1350.root","READ");
  TFile f_1400("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1400.root","READ");
  TFile f_1450("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1450.root","READ");
  TFile f_1500("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1500.root","READ");
  TFile f_1550("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1550.root","READ");
  TFile f_1600("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1600.root","READ");
  TFile f_1650("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1650.root","READ");
  TFile f_1700("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1700.root","READ");
  TFile f_1750("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1750.root","READ");
  TFile f_1800("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1800.root","READ");
  TFile f_1850("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1850.root","READ");
  TFile f_1900("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1900.root","READ");
  TFile f_1950("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj1950.root","READ");
  TFile f_2000("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuujj2000.root","READ");

  const int nFiles=37;
  
  TTree* trees[nFiles]={(TTree*)f_200.Get("PhysicalVariables"),
			(TTree*)f_250.Get("PhysicalVariables"),
			(TTree*)f_300.Get("PhysicalVariables"),
			(TTree*)f_350.Get("PhysicalVariables"),
			(TTree*)f_400.Get("PhysicalVariables"),
			(TTree*)f_450.Get("PhysicalVariables"),
			(TTree*)f_500.Get("PhysicalVariables"),
			(TTree*)f_550.Get("PhysicalVariables"),
			(TTree*)f_600.Get("PhysicalVariables"),
			(TTree*)f_650.Get("PhysicalVariables"),
			(TTree*)f_700.Get("PhysicalVariables"),
			(TTree*)f_750.Get("PhysicalVariables"),
			(TTree*)f_800.Get("PhysicalVariables"),
			(TTree*)f_850.Get("PhysicalVariables"),
			(TTree*)f_900.Get("PhysicalVariables"),
			(TTree*)f_950.Get("PhysicalVariables"),
			(TTree*)f_1000.Get("PhysicalVariables"),
			(TTree*)f_1050.Get("PhysicalVariables"),
			(TTree*)f_1100.Get("PhysicalVariables"),
			(TTree*)f_1150.Get("PhysicalVariables"),
			(TTree*)f_1200.Get("PhysicalVariables"),
			(TTree*)f_1250.Get("PhysicalVariables"),
			(TTree*)f_1300.Get("PhysicalVariables"),
			(TTree*)f_1350.Get("PhysicalVariables"),
			(TTree*)f_1400.Get("PhysicalVariables"),
			(TTree*)f_1450.Get("PhysicalVariables"),
			(TTree*)f_1500.Get("PhysicalVariables"),
			(TTree*)f_1550.Get("PhysicalVariables"),
			(TTree*)f_1600.Get("PhysicalVariables"),
			(TTree*)f_1650.Get("PhysicalVariables"),
			(TTree*)f_1700.Get("PhysicalVariables"),
			(TTree*)f_1750.Get("PhysicalVariables"),
			(TTree*)f_1800.Get("PhysicalVariables"),
			(TTree*)f_1850.Get("PhysicalVariables"),
			(TTree*)f_1900.Get("PhysicalVariables"),
			(TTree*)f_1950.Get("PhysicalVariables"),
			(TTree*)f_2000.Get("PhysicalVariables")
  };
  
  
  float L_int=3000.;
  
  TCut cuts[18]={"(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>0)&&(St_uujj>0)&&(M_uujj2>0)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>100)&&(St_uujj>0)&&(M_uujj2>0)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>100)&&(St_uujj>380)&&(M_uujj2>0)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>100)&&(St_uujj>380)&&(M_uujj2>115)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>115)&&(St_uujj>460)&&(M_uujj2>115)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>125)&&(St_uujj>540)&&(M_uujj2>120)",
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
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>245)&&(St_uujj>1210)&&(M_uujj2>690)"};
  
  const int nTrigCuts = 3;
  //TCut trigCuts[nTrigCuts]={"3000*weight_central","3000*weight_central*pass_HLTMu40_eta2p1","3000*weight_central*pass_HLTMu40_eta2p1*((abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>50)&&(Pt_muon2>50)&&(Pt_jet1>45)&&(Pt_jet2>45)&&(M_uu>0)&&(DR_muon1muon2>0.3)&&(M_uu>0)&&(St_uujj>0)&&(M_uujj2>0))"};
  TCut trigCuts[nTrigCuts]={"3000*weight_central","3000*weight_central*pass_HLTMu40_eta2p1","3000*weight_central*pass_HLTMu40_eta2p1*((abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(Pt_muon1>50)&&(Pt_muon2>50)&&(Pt_jet1>45)&&(Pt_jet2>45)&&(M_uu>0)&&(DR_muon1muon2>0.3)&&(M_uu>0)&&(St_uujj>0)&&(M_uujj2>0))"};
  //no cuts
  //trigger
  //trigger + object acceptance selection (no id)


  float bgs[18]={13952.41,
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
                 0.41};
  TH2F* h_eff = new TH2F("h_eff",";stop mass;LQ2 optimization cut mass",nFiles,200,2050,18,150,1050);
  TH2F* h_sOverSplusB = new TH2F("h_sOverSplusB",";stop mass;LQ2 optimization cut mass",nFiles,200,2050,18,150,1050);
  TH2F* h_yields = new TH2F("h_yields",";LQ mass;LQ2 optimization cut mass",nFiles,200,2050,18,150,1050);
  
  
  
  for(int j=0;j<nFiles;++j){
    
    trees[j]->Draw("weight_central");
    TH1F *h_w = (TH1F*)trees[j]->GetHistogram();
    float weight = h_w->GetMean(1)*L_int;
    h_w->Delete();
 

    trees[j]->Draw("St_uujj","","");
    TH1F *h_St = (TH1F*)trees[j]->GetHistogram();
    float yield = h_St->Integral(0,-1)*weight;
    
    float tot = yield*weight;
    h_yields->Fill(150+50*(j+1),100+50,yield);
    h_St->Delete();
    
    


  }
  //}
  float xsecs[nFiles]={60.6,20.3,8.04,3.59,1.74,.906,.496,.284,.169,.103,.0648,.0416,.0273,.0182,.0123,.00845,.00586,.00411,.00291,.00208,.00150,.00109,.000795,.000585,.000433,.000321,.000240,.000180,.000135,.000102,.0000774,.0000588,.0000448,.0000343,.0000262,.0000201,.0000155};
  float nEvents[nFiles]={50000,48352,49307,50000,50000,50000,50000,50000,50000,50000,47954,49163,50000,48906,50000,50000,50000,48569,50000,46916,49742,49072,49543,48560,50000,50000,49599,49400,48725,50000,50000,50000,50000,47520,47402,50000,49768};


  TH1F *h_Muujj1[nFiles],*h_Muujj2[nFiles],*h_STuujj[nFiles],*h_PTu1[nFiles],*h_PTu2[nFiles],*h_PTj1[nFiles],*h_PTj2[nFiles];  
  TH1F *htrig_Muujj1[nFiles][nTrigCuts],*htrig_Muujj2[nFiles][nTrigCuts],*htrig_STuujj[nFiles][nTrigCuts],*htrig_PTu1[nFiles][nTrigCuts],*htrig_PTu2[nFiles][nTrigCuts],*htrig_PTj1[nFiles][nTrigCuts],*htrig_PTj2[nFiles][nTrigCuts];  
  TGraphAsymmErrors *ttrig_Muujj1[nFiles][nTrigCuts],*ttrig_Muujj2[nFiles][nTrigCuts],*ttrig_STuujj[nFiles][nTrigCuts],*ttrig_PTu1[nFiles][nTrigCuts],*ttrig_PTu2[nFiles][nTrigCuts],*ttrig_PTj1[nFiles][nTrigCuts],*ttrig_PTj2[nFiles][nTrigCuts];  
  TH1F *h_trigEff = new TH1F("h_trigEff",";M_{LQ};Trigger Efficiency",37,175,2025);
  TH1F *h_trigEffAcc = new TH1F("h_trigEffAcc",";M_{LQ};Trigger + Selection Acceptance",37,175,2025);
  std::vector<Double_t> x,y,exl,exh,eyl,eyh,xacc,yacc,exlacc,exhacc,eylacc,eyhacc;

  bool doXsecs=0;//1 to scale by correct cross sections, 0 to scale arbitrarily for visual use
  for(int i=0;i<nFiles;i++){
    TString nam1 = "h_Muujj1";nam1+=i;
    TString nam2 = "h_Muujj2";nam2+=i;
    TString ptnam1 = "h_PTu1";ptnam1+=i;
    TString ptnam2 = "h_PTu2";ptnam2+=i;
    TString ptjnam1 = "h_PTj1";ptjnam1+=i;
    TString ptjnam2 = "h_PTj2";ptjnam2+=i;
    TString stNam ="h_STuujj";stNam+=i;
    h_Muujj1[i] = new TH1F(nam1,"M_{uujj1};M_{uujj1};Arbitrary Units",500,0,2500);
    h_Muujj2[i] = new TH1F(nam2,"M_{uujj2};M_{uujj2};Arbitrary Units",500,0,2500);
    h_PTu1[i] = new TH1F(ptnam1,"P_{T}(muon1);P_{T}(muon1);Arbitrary Units",500,0,2500);
    h_PTu2[i] = new TH1F(ptnam2,"P_{T}(muon2);P_{T}(muon2);Arbitrary Units",500,0,2500);
    h_PTj1[i] = new TH1F(ptjnam1,"P_{T}(jet1);P_{T}(jet1);Arbitrary Units",500,0,2500);
    h_PTj2[i] = new TH1F(ptjnam2,"P_{T}(jet2);P_{T}(jet2);Arbitrary Units",500,0,2500);
    h_STuujj[i] = new TH1F(stNam,"ST_{uujj};ST_{uujj};Arbitrary Units",500,0,10000);
    if(doXsecs){
      trees[i]->Project(nam1,"M_uujj1","weight_central");
      trees[i]->Project(nam2,"M_uujj2","weight_central");
      trees[i]->Project(ptnam1,"Pt_muon1","weight_central");
      trees[i]->Project(ptnam2,"Pt_muon2","weight_central");
      trees[i]->Project(ptjnam1,"Pt_jet1","weight_central");
      trees[i]->Project(ptjnam2,"Pt_jet2","weight_central");
      trees[i]->Project(stNam,"St_uujj","weight_central");
    }
    else{
      trees[i]->Project(nam1,"M_uujj1","");
      trees[i]->Project(nam2,"M_uujj2","");
      trees[i]->Project(ptnam1,"Pt_muon1","");
      trees[i]->Project(ptnam2,"Pt_muon2","");
      trees[i]->Project(ptjnam1,"Pt_jet1","");
      trees[i]->Project(ptjnam2,"Pt_jet2","");
      trees[i]->Project(stNam,"St_uujj","");
    }
  }
  //trigger study
  for(int i=0;i<nFiles;i++){
    for( int j=0; j<nTrigCuts; j++){
      TString nam1 = "htrig_Muujj1";nam1+=i;nam1+=j;
      TString nam2 = "htrig_Muujj2";nam2+=i;nam2+=j;
      TString ptnam1 = "htrig_PTu1";ptnam1+=i;ptnam1+=j;
      TString ptnam2 = "htrig_PTu2";ptnam2+=i;ptnam2+=j;
      TString ptjnam1 = "htrig_PTj1";ptjnam1+=i;ptjnam1+=j;
      TString ptjnam2 = "htrig_PTj2";ptjnam2+=i;ptjnam2+=j;
      TString stNam ="htrig_STuujj";stNam+=i;stNam+=j;
      htrig_Muujj1[i][j] = new TH1F(nam1,"trigM_{uujj1};M_{uujj1};Efficiency",1,0,2500);htrig_Muujj1[i][j]->Sumw2();//was 333
      htrig_Muujj2[i][j] = new TH1F(nam2,"trigM_{uujj2};M_{uujj2};Efficiency",1,0,2500);htrig_Muujj2[i][j]->Sumw2();
      htrig_PTu1[i][j] = new TH1F(ptnam1,"trigP_{T}(muon1);P_{T}(muon1);Efficiency",1,0,2500);htrig_PTu1[i][j]->Sumw2();
      htrig_PTu2[i][j] = new TH1F(ptnam2,"trigP_{T}(muon2);P_{T}(muon2);Efficiency",1,0,2500);htrig_PTu2[i][j]->Sumw2();
      htrig_PTj1[i][j] = new TH1F(ptjnam1,"trigP_{T}(jet1);P_{T}(jet1);Efficiency",1,0,2500);htrig_PTj1[i][j]->Sumw2();
      htrig_PTj2[i][j] = new TH1F(ptjnam2,"trigP_{T}(jet2);P_{T}(jet2);Efficiency",1,0,2500);htrig_PTj2[i][j]->Sumw2();
      htrig_STuujj[i][j] = new TH1F(stNam,"trigST_{uujj};ST_{uujj};Efficiency",1,0,10000);htrig_STuujj[i][j]->Sumw2();
      trees[i]->Project(nam1,"M_uujj1",trigCuts[j]);
      trees[i]->Project(nam2,"M_uujj2",trigCuts[j]);
      trees[i]->Project(ptnam1,"Pt_muon1",trigCuts[j]);
      trees[i]->Project(ptnam2,"Pt_muon2",trigCuts[j]);
      trees[i]->Project(ptjnam1,"Pt_jet1",trigCuts[j]);
      trees[i]->Project(ptjnam2,"Pt_jet2",trigCuts[j]);
      trees[i]->Project(stNam,"St_uujj",trigCuts[j]);
    }
    /*
    ttrig_Muujj1[i][j]=new TGraphAsymmErrors(htrig_Muujj1[i][j]);
    ttrig_Muujj2[i][j]=new TGraphAsymmErrors(htrig_Muujj2[i][j]);
    ttrig_PT1[i][j]=new TGraphAsymmErrors(htrig_PTu1[i][j]);
    ttrig_PTu2[i][j]=new TGraphAsymmErrors(htrig_PTu2[i][j]);
    ttrig_PTj1[i][j]=new TGraphAsymmErrors(htrig_PTj1[i][j]);
    ttrig_PTj2[i][j]=new TGraphAsymmErrors(htrig_PTj2[i][j]);
    ttrig_STuujj[i][j]=new TGraphAsymmErrors(htrig_STuujj[i][j]);
    */
    for( int j=1; j<nTrigCuts; j++){
      cout<<i<<" "<<j<<"    integrals: "<<htrig_Muujj1[i][0]->Integral()<<"  "<<htrig_Muujj1[i][j]->Integral()<<endl;
      ttrig_Muujj1[i][j] = new TGraphAsymmErrors(htrig_Muujj1[i][j],htrig_Muujj1[i][0]);
      ttrig_Muujj2[i][j] = new TGraphAsymmErrors(htrig_Muujj2[i][j],htrig_Muujj2[i][0]);
      ttrig_PTu1[i][j] = new TGraphAsymmErrors(htrig_PTu1[i][j],htrig_PTu1[i][0]);
      ttrig_PTu2[i][j] = new TGraphAsymmErrors(htrig_PTu2[i][j],htrig_PTu2[i][0]);
      ttrig_PTj1[i][j] = new TGraphAsymmErrors(htrig_PTj1[i][j],htrig_PTj1[i][0]);
      ttrig_PTj2[i][j] = new TGraphAsymmErrors(htrig_PTj2[i][j],htrig_PTj2[i][0]);
      ttrig_STuujj[i][j] = new TGraphAsymmErrors(htrig_STuujj[i][j],htrig_STuujj[i][0]);


    }
    //ttrig_PTu1[i][1]->Print();
    x.push_back(double((i*50.)+200.));y.push_back((double)ttrig_PTu1[i][1]->Eval(1));
    exl.push_back((double)((i*50.)+200.-25.));exh.push_back((double)((i*50.)+200.+25.));
    eyl.push_back((double)ttrig_PTu1[i][1]->GetErrorYlow(0));eyh.push_back((double)ttrig_PTu1[i][1]->GetErrorYhigh(0));

    xacc.push_back(double((i*50.)+200.));yacc.push_back((double)ttrig_PTu1[i][2]->Eval(1));
    exlacc.push_back((double)((i*50.)+200.-25.));exhacc.push_back((double)((i*50.)+200.+25.));
    eylacc.push_back((double)ttrig_PTu1[i][2]->GetErrorYlow(0));eyhacc.push_back((double)ttrig_PTu1[i][2]->GetErrorYhigh(0));

    cout<<"i: "<<i<<" x:"<<x[i]<<" y:"<<y[i]<<" exl:"<<exl[i]<<" exh:"<<exh[i]<<" eyl:"<<eyl[i]<<" eyh:"<<eyh[i]<<endl;
    cout<<"acc: "<<i<<" x:"<<xacc[i]<<" y:"<<yacc[i]<<" exl:"<<exlacc[i]<<" exh:"<<exhacc[i]<<" eyl:"<<eylacc[i]<<" eyh:"<<eyhacc[i]<<endl;


    h_trigEff->SetBinContent(i+1,y[i]);
    h_trigEff->SetBinError(i+1,eyl[i]>eyh[i]?eyl[i]:eyh[i]);

    h_trigEffAcc->SetBinContent(i+1,yacc[i]);
    h_trigEffAcc->SetBinError(i+1,eylacc[i]>eyhacc[i]?eylacc[i]:eyhacc[i]);


    TString filen = "Plots/trigEff_PT_u1_";filen+=(i*50)+200;filen+=".pdf";
    ttrig_PTu1[i][1]->Draw("AEP");
    c1->Print(filen);
    filen = "Plots/trigEffAcc_PT_u1_";filen+=(i*50)+200;filen+=".pdf";
    ttrig_PTu1[i][2]->Draw("AEP");
    c1->Print(filen);

    filen = "Plots/trigEff_PT_u2_";filen+=(i*50)+200;filen+=".pdf";
    ttrig_PTu2[i][1]->Draw("AEP");
    c1->Print(filen);
    filen = "Plots/trigEffAcc_PT_u2_";filen+=(i*50)+200;filen+=".pdf";
    ttrig_PTu2[i][2]->Draw("AEP");
    c1->Print(filen);

  }
  //int n=x.size();
  //TGraph *h_trigEff = new TGraphAsymmErrors(n,&x[0],&y[0]);//,&exl[0],&exh[0],&eyl[0],&eyh[0]);
  //TGraph *h_trigEffAcc = new TGraphAsymmErrors(n,xacc,yacc,exlacc,exhacc,eylacc,eyhacc);

  h_trigEff->GetYaxis()->SetRangeUser(0.94,1.0);
  h_trigEffAcc->GetYaxis()->SetRangeUser(0.4,0.9);

  h_trigEff->Draw("PE");
  c1->Print("Plots/triggerEff.pdf");
  h_trigEffAcc->Draw("PE");
  c1->Print("Plots/triggerAcc.pdf");

  
  if(doXsecs)c1->SetLogy(1);
  for(int i=0;i<nFiles;i++){
    float weight = 0.;
    doXsecs?weight=L_int:weight=3000./nEvents[i];
    h_Muujj1[i]->Scale(weight,"");
    h_Muujj2[i]->Scale(weight,"");
    h_PTu1[i]->Scale(weight,"");
    h_PTu2[i]->Scale(weight,"");
    h_STuujj[i]->Scale(weight,"");
    int reb = 20;
    /*  h_Muujj1[i]->Rebin(reb);
    h_Muujj2[i]->Rebin(reb);
    h_STuujj[i]->Rebin(reb);*/
 }
  float lowbound=0.;doXsecs?lowbound=.01:;
  h_Muujj1[nFiles-1]->GetXaxis()->SetRangeUser(lowbound,2400);
  h_Muujj1[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,3000);
  h_Muujj1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muujj1[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_Muujj1[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_Muujj1[i]->SetLineColor(9);
    if(2*(i+2)==18)h_Muujj1[i]->SetLineColor(17);

    h_Muujj1[i]->Draw("sames");
    // i+=2;
  }
  c1->Print("Plots/M_uujj1.pdf");
  
  h_Muujj2[nFiles-1]->GetXaxis()->SetRangeUser(lowbound,2400);
  h_Muujj2[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,2500);
  h_Muujj2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muujj2[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_Muujj2[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_Muujj2[i]->SetLineColor(9);
    if(2*(i+2)==18)h_Muujj2[i]->SetLineColor(17);
    h_Muujj2[i]->Draw("sames");
    // i+=2;
  }

  c1->Print("Plots/M_uujj2.pdf");

  h_STuujj[nFiles-1]->GetXaxis()->SetRangeUser(lowbound,5500);
  h_STuujj[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,2200);
  h_STuujj[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_STuujj[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_STuujj[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_STuujj[i]->SetLineColor(9);
    if(2*(i+2)==18)h_STuujj[i]->SetLineColor(17);
    h_STuujj[i]->Draw("sames");
    // i+=2;
  }

  c1->Print("Plots/ST_uujj.pdf");
  
  h_PTu1[nFiles-1]->GetXaxis()->SetRangeUser(lowbound,1700);
  h_PTu1[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,1400);
  h_PTu1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTu1[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_PTu1[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_PTu1[i]->SetLineColor(9);
    if(2*(i+2)==18)h_PTu1[i]->SetLineColor(17);

    h_PTu1[i]->Draw("sames");
    // i+=2;
  }
  c1->Print("Plots/Pt_muon1.pdf");
  
  h_PTu2[nFiles-1]->GetXaxis()->SetRangeUser(lowbound,1700);
  h_PTu2[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,1400);
  h_PTu2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTu2[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_PTu2[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_PTu2[i]->SetLineColor(9);
    if(2*(i+2)==18)h_PTu2[i]->SetLineColor(17);
    h_PTu2[i]->Draw("sames");
    // i+=2;
  }

  c1->Print("Plots/Pt_muon2.pdf");
  
  h_PTj1[nFiles-1]->GetXaxis()->SetRangeUser(lowbound,1700);
  h_PTj1[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,1400);
  h_PTj1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTj1[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_PTj1[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_PTj1[i]->SetLineColor(9);
    if(2*(i+2)==18)h_PTj1[i]->SetLineColor(17);

    h_PTj1[i]->Draw("sames");
    // i+=2;
  }
  c1->Print("Plots/Pt_jet1.pdf");
  
  h_PTj2[nFiles-1]->GetXaxis()->SetRangeUser(lowbound,1700);
  h_PTj2[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,1400);
  h_PTj2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTj2[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_PTj2[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_PTj2[i]->SetLineColor(9);
    if(2*(i+2)==18)h_PTj2[i]->SetLineColor(17);
    h_PTj2[i]->Draw("sames");
    // i+=2;
  }

  c1->Print("Plots/Pt_jet2.pdf");

  int y1=200;
  h_yields->GetYaxis()->SetBinLabel(1,"No Cuts");
  h_yields->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
  //h_eff->GetYaxis()->SetBinLabel(1,"Preselection");
  // h_eff->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
  //h_sOverSplusB->GetYaxis()->SetBinLabel(1,"Preselection");
  // h_sOverSplusB->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
  for(int b=1;b<=nFiles;b++){
    stringstream ss;ss <<y1;
    string str=ss.str();
    h_yields->GetXaxis()->SetBinLabel(b,str.c_str());
    h_eff->GetXaxis()->SetBinLabel(b,str.c_str());
    h_sOverSplusB->GetXaxis()->SetBinLabel(b,str.c_str());
    if(b>=3 && b<18){
      h_yields->GetYaxis()->SetBinLabel(b+1,str.c_str());
      h_eff->GetYaxis()->SetBinLabel(b+1,str.c_str());
      h_sOverSplusB->GetYaxis()->SetBinLabel(b+1,str.c_str());
    }
    y1+=50;
  }
  //h_eff->GetZaxis()->SetRangeUser(lowbound.,1.);
  h_eff->GetYaxis()->SetTitleSize(0.05);
  // h_eff->Draw("colztext");
  // c1->Print("Plots/efficiencyTable.png");
  // c1->Print("Plots/efficiencyTable.pdf");
  
  h_sOverSplusB->GetYaxis()->SetTitleSize(0.05);
  h_sOverSplusB->GetZaxis()->SetRangeUser(.077,140);
  gPad->SetLogz(1);
   //  h_sOverSplusB->Draw("colztext");
  //c1->Print("Plots/sOverSqrtSplusB.png");
  //c1->Print("Plots/sOverSqrtSplusB.pdf");
  
  gStyle->SetPaintTextFormat("4.0f");
  //gPad->SetLogz(0);
  h_yields->GetYaxis()->SetTitleSize(0.05);
  h_yields->GetZaxis()->SetRangeUser(20000,55000);
  h_yields->Draw("colztext45");
  //c1->Print("Plots/yields.png");
  c1->Print("Plots/yields.pdf");
  
  /*
  
  TH1F* h_xsecs = new TH1F("h_xsecs",";stop mass;#tilde{t}  #tilde{t}   #sigma [pb]",16,200,1000);
  float xsecs[34]={18.5245,.149147,
		   5.57596,.147529,
		   1.99608,.146905,
		   0.807323,.143597,
		   0.35683,.142848,
		   0.169668,.142368,
		   0.0855847,.149611,
		   0.0452067,.158177,
		   0.0248009,.166406,
		   0.0139566,.1756,
		   0.0081141,.184146,
		   0.00480639,.194088,
		   0.00289588,.20516,
		   0.00176742,.21836,
		   0.00109501,.239439,
		   0.000687022,.25834,
		   0.000435488,.276595};
  
  
  for(int i=0;i<17;i+=2){
    h_xsecs->SetBinContent(i+1,xsecs[2*i]);
    h_xsecs->SetBinError(i+1,xsecs[2*i]*xsecs[2*i+1]);
  }
  c1->SetLogy(1);
  h_xsecs->GetYaxis()->SetRangeUser(4.5e-4,30);
  h_xsecs->Draw("pe");
  h_xsecs->Draw("c hist sames");
  c1->Print("Plots/stopXsecs.png");
  c1->Print("Plots/stopXsecs.pdf");
  */
    
    
}
