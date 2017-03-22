#include "TCanvas.h"
#include "TH1.h"
#include "TH2.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TTree.h"
#include "TFile.h"
#include "THStack.h"
#include <sstream>
#include <string>
#include <vector>
//#include "pair.h"

void signalTest_betaHalf(){

  using namespace std;
  
  gStyle->SetOptStat(0);
  
  gStyle->SetPaintTextFormat("4.2f");
  
  TCanvas *c1 = new TCanvas("c1","",1400,1000);
  c1->cd();
  
  
  TFile f_200("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj200.root","READ");
  TFile f_250("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj250.root","READ");
  TFile f_300("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj300.root","READ");
  TFile f_350("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj350.root","READ");
  TFile f_400("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj400.root","READ");
  TFile f_450("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj450.root","READ");
  TFile f_500("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj500.root","READ");
  TFile f_550("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj550.root","READ");
  TFile f_600("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj600.root","READ");
  TFile f_650("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj650.root","READ");
  TFile f_700("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj700.root","READ");
  TFile f_750("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj750.root","READ");
  TFile f_800("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj800.root","READ");
  TFile f_850("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj850.root","READ");
  TFile f_900("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj900.root","READ");
  TFile f_950("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj950.root","READ");
  TFile f_1000("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1000.root","READ");
  TFile f_1050("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1050.root","READ");
  TFile f_1100("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1100.root","READ");
  TFile f_1150("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1150.root","READ");
  TFile f_1200("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1200.root","READ");
  TFile f_1250("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1250.root","READ");
  TFile f_1300("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1300.root","READ");
  TFile f_1350("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1350.root","READ");
  TFile f_1400("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1400.root","READ");
  TFile f_1450("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1450.root","READ");
  TFile f_1500("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1500.root","READ");
  TFile f_1550("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1550.root","READ");
  TFile f_1600("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1600.root","READ");
  TFile f_1650("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1650.root","READ");
  TFile f_1700("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1700.root","READ");
  TFile f_1750("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1750.root","READ");
  TFile f_1800("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1800.root","READ");
  TFile f_1850("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1850.root","READ");
  TFile f_1900("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1900.root","READ");
  TFile f_1950("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj1950.root","READ");
  TFile f_2000("/media/dataPlus/dmorse/lqNtuples/NTupleAnalyzer_Full2016_2016_10_18_15_14_53/SummaryFiles/LQuvjj2000.root","READ");

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
  
  
  float L_int=10000.;
  
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
    
    trees[j]->Draw("weight_nopu");
    TH1F *h_w = (TH1F*)trees[j]->GetHistogram();
    float weight = h_w->GetMean(1)*L_int;
    h_w->Delete();
    
    //for(int k=1;k<=nFiles;++k){
    //if(k==3)continue;
    //cout<<"j:"<<j<<" k:"<<k<<endl;
      //trees[j]->Draw("St_uujj",cuts[k-1],"");
      trees[j]->Draw("St_uvjj","","");
      TH1F *h_St = (TH1F*)trees[j]->GetHistogram();
      float yield = h_St->Integral(0,-1);
      
      /*if(j==0) h_eff->Fill(150+50*(j+1),100+50*k,yield/9500.);
	else if(j==6)h_eff->Fill(150+50*(j+1),100+50*k,yield/9480.);
	else h_eff->Fill(150+50*(j+1),100+50*k,yield/50.);*/
      //h_eff->Fill(150+50*(j+1),100+50*k,yield/30000.);
      
      float tot = yield*weight;
      //cout<<"xbin:"<<150+50*(j+1)<<"  ybin:"<<100+50*k<<"  tot:"<<tot<<"  bg:"<<bgs[k-1]<<endl;
      //h_sOverSplusB->Fill(150+50*(j+1),100+50*k,tot/sqrt(tot+bgs[k-1]));
      //h_yields->Fill(150+50*(j+1),100+50*k,tot);
      //h_yields->Fill(150+50*(j+1),100+50*k,yield);
      h_yields->Fill(150+50*(j+1),100+50,yield);
      h_St->Delete();
   


  }
  //}
  float xsecs[nFiles]={60.6,20.3,8.04,3.59,1.74,.906,.496,.284,.169,.103,.0648,.0416,.0273,.0182,.0123,.00845,.00586,.00411,.00291,.00208,.00150,.00109,.000795,.000585,.000433,.000321,.000240,.000180,.000135,.000102,.0000774,.0000588,.0000448,.0000343,.0000262,.0000201,.0000155};
  float nEvents[nFiles]={50000,48352,49307,50000,50000,50000,50000,50000,50000,50000,47954,49163,50000,48906,50000,50000,48471,48569,50000,40748,49742,49072,49543,48560,50000,50000,49599,49400,48725,50000,50000,50000,50000,47520,47402,50000,49768};


  TH1F *h_Muvjj1[nFiles],*h_Muvjj2[nFiles],*h_STuvjj[nFiles],*h_PTu1[nFiles],*h_PTu2[nFiles],*h_PTj1[nFiles],*h_PTj2[nFiles];  
 

  for(int i=0;i<nFiles;i++){
    TString nam1 = "h_Muvjj1";nam1+=i;
    TString nam2 = "h_Muvjj2";nam2+=i;
    TString ptnam1 = "h_PTu1";ptnam1+=i;
    TString ptnam2 = "h_PTu2";ptnam2+=i;
    TString ptjnam1 = "h_PTj1";ptjnam1+=i;
    TString ptjnam2 = "h_PTj2";ptjnam2+=i;
    TString stNam ="h_STuvjj";stNam+=i;
    h_Muvjj1[i] = new TH1F(nam1,"M_{uvjj};M_{uvjj};Events",500,0,2500);
    h_Muvjj2[i] = new TH1F(nam2,"MT_{uvjj2};MT_{uvjj2};Events",500,0,2500);
    h_PTu1[i] = new TH1F(ptnam1,"P_{T}(muon1);P_{T}(muon1);Events",500,0,2500);
    h_PTu2[i] = new TH1F(ptnam2,"P_{T}(muon2);P_{T}(muon2);Events",500,0,2500);
    h_PTj1[i] = new TH1F(ptjnam1,"P_{T}(jet1);P_{T}(jet1);Events",500,0,2500);
    h_PTj2[i] = new TH1F(ptjnam2,"P_{T}(jet2);P_{T}(jet2);Events",500,0,2500);
    h_STuvjj[i] = new TH1F(stNam,"ST_{uvjj};ST_{uvjj};Events",500,0,10000);
    trees[i]->Project(nam1,"M_uvjj","");
    trees[i]->Project(nam2,"MT_uvjj2","");
    trees[i]->Project(ptnam1,"Pt_muon1","");
    trees[i]->Project(ptnam2,"Pt_muon2","");
    trees[i]->Project(ptjnam1,"Pt_jet1","");
    trees[i]->Project(ptjnam2,"Pt_jet2","");
    trees[i]->Project(stNam,"St_uvjj","");
  }
  
  for(int i=0;i<nFiles;i++){
    //float weight = xsecs[i]*L_int/nEvents;
    float weight = 1./nEvents[i];
    h_Muvjj1[i]->Scale(weight,"");
    h_Muvjj2[i]->Scale(weight,"");
    h_PTu1[i]->Scale(weight,"");
    h_PTu2[i]->Scale(weight,"");
    h_STuvjj[i]->Scale(weight,"");
    int reb = 20;
    /*  h_Muvjj1[i]->Rebin(reb);
    h_Muvjj2[i]->Rebin(reb);
    h_STuvjj[i]->Rebin(reb);*/
 }
  
  h_Muvjj1[nFiles-1]->GetXaxis()->SetRangeUser(0,2400);
  h_Muvjj1[nFiles-1]->GetYaxis()->SetRangeUser(0,.06);
  h_Muvjj1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muvjj1[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_Muvjj1[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_Muvjj1[i]->SetLineColor(9);
    if(2*(i+2)==18)h_Muvjj1[i]->SetLineColor(17);

    h_Muvjj1[i]->Draw("sames");
    // i++;
  }
  c1->Print("Plots/M_uvjj.png");
  
  h_Muvjj2[nFiles-1]->GetXaxis()->SetRangeUser(0,2400);
  h_Muvjj2[nFiles-1]->GetYaxis()->SetRangeUser(0,1500);
  h_Muvjj2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muvjj2[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_Muvjj2[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_Muvjj2[i]->SetLineColor(9);
    if(2*(i+2)==18)h_Muvjj2[i]->SetLineColor(17);
    h_Muvjj2[i]->Draw("sames");
    // i++;
  }

  c1->Print("Plots/MT_uvjj2.pdf");

  h_STuvjj[nFiles-1]->GetXaxis()->SetRangeUser(0,5500);
  h_STuvjj[nFiles-1]->GetYaxis()->SetRangeUser(0,2200);
  h_STuvjj[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_STuvjj[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_STuvjj[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_STuvjj[i]->SetLineColor(9);
    if(2*(i+2)==18)h_STuvjj[i]->SetLineColor(17);
    h_STuvjj[i]->Draw("sames");
    // i++;
  }

  c1->Print("Plots/ST_uvjj.pdf");
  
  h_PTu1[nFiles-1]->GetXaxis()->SetRangeUser(0,1700);
  h_PTu1[nFiles-1]->GetYaxis()->SetRangeUser(0,1400);
  h_PTu1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTu1[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_PTu1[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_PTu1[i]->SetLineColor(9);
    if(2*(i+2)==18)h_PTu1[i]->SetLineColor(17);

    h_PTu1[i]->Draw("sames");
    // i++;
  }
  c1->Print("Plots/Pt_muon1_betaHalf.pdf");
  
  h_PTu2[nFiles-1]->GetXaxis()->SetRangeUser(0,1700);
  h_PTu2[nFiles-1]->GetYaxis()->SetRangeUser(0,1400);
  h_PTu2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTu2[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_PTu2[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_PTu2[i]->SetLineColor(9);
    if(2*(i+2)==18)h_PTu2[i]->SetLineColor(17);
    h_PTu2[i]->Draw("sames");
    // i++;
  }

  c1->Print("Plots/Pt_muon2_betaHalf.pdf");
  
  h_PTj1[nFiles-1]->GetXaxis()->SetRangeUser(0,1700);
  h_PTj1[nFiles-1]->GetYaxis()->SetRangeUser(0,1400);
  h_PTj1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTj1[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_PTj1[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_PTj1[i]->SetLineColor(9);
    if(2*(i+2)==18)h_PTj1[i]->SetLineColor(17);

    h_PTj1[i]->Draw("sames");
    // i++;
  }
  c1->Print("Plots/Pt_jet1_betaHalf.pdf");
  
  h_PTj2[nFiles-1]->GetXaxis()->SetRangeUser(0,1700);
  h_PTj2[nFiles-1]->GetYaxis()->SetRangeUser(0,1400);
  h_PTj2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTj2[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i+=2){
    h_PTj2[i]->SetLineColor(2*(i+2));
    if(2*(i+2)==10)h_PTj2[i]->SetLineColor(9);
    if(2*(i+2)==18)h_PTj2[i]->SetLineColor(17);
    h_PTj2[i]->Draw("sames");
    // i++;
  }

  c1->Print("Plots/Pt_jet2_betaHalf.pdf");

  int y=200;
  h_yields->GetYaxis()->SetBinLabel(1,"No Cuts");
  h_yields->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
  //h_eff->GetYaxis()->SetBinLabel(1,"Preselection");
  // h_eff->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
  //h_sOverSplusB->GetYaxis()->SetBinLabel(1,"Preselection");
  // h_sOverSplusB->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
  for(int b=1;b<=nFiles;b++){
    stringstream ss;ss <<y;
    string str=ss.str();
    h_yields->GetXaxis()->SetBinLabel(b,str.c_str());
    h_eff->GetXaxis()->SetBinLabel(b,str.c_str());
    h_sOverSplusB->GetXaxis()->SetBinLabel(b,str.c_str());
    if(b>=3 && b<18){
      h_yields->GetYaxis()->SetBinLabel(b+1,str.c_str());
      h_eff->GetYaxis()->SetBinLabel(b+1,str.c_str());
      h_sOverSplusB->GetYaxis()->SetBinLabel(b+1,str.c_str());
    }
    y+=50;
  }
  //h_eff->GetZaxis()->SetRangeUser(0.,1.);
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
  c1->Print("Plots/yields_betaHalf.pdf");
  
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
  
  
  for(int i=0;i<17;i++){
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
