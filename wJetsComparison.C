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

void wJetsComparison(){

  using namespace std;
  
  gStyle->SetOptStat(0);
  
  gStyle->SetPaintTextFormat("4.2f");
  //gStyle->SetTitleX(0.1f);gStyle->SetTitleW(0.8f);
  gStyle->SetTitleBorderSize(0);

  TCanvas *c1 = new TCanvas("c1","",1400,1000);
  c1->cd();
  
  
  TFile f_mbin("NTupleAnalyzer_Spring15MC_2015_08_16_14_24_53/SummaryFiles/WJetsAmcAtNLO.root","READ");
  TFile f_inc ("NTupleAnalyzer_Spring15MC_2015_08_16_14_24_53/SummaryFiles/WJetsMGMLM.root","READ");
  TFile f_sig ("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/LQuvjj800.root","READ");
  TFile f_jb2012("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsJBin.root","READ");
  TFile f_2012_mup("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsMatchUp.root","READ");
  TFile f_2012_mdown("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsMatchDown.root","READ");
  TFile f_2012_sup("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsScaleUp.root","READ");
  TFile f_2012_sdown("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsScaleDown.root","READ");
  TFile f_jb2012_sup("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsJBinScaleUp.root","READ");
  TFile f_jb2012_sdown("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsJBinScaleDown.root","READ");
  TFile f_jb2012_mup("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsJBinMatchUp.root","READ");
  TFile f_jb2012_mdown("~/work/leptoQuark/CMSSW_5_3_14_patch2_LQ/src/LQ2Analysis8TeV/NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/WJetsJBinMatchDown.root","READ");


  const int nFiles=3,nFilesTot=12;
  
  TTree* trees[nFilesTot]={(TTree*)f_mbin.Get("PhysicalVariables"),
			(TTree*)f_inc.Get("PhysicalVariables"),
			(TTree*)f_sig.Get("PhysicalVariables"),
			(TTree*)f_jb2012.Get("PhysicalVariables"),
			(TTree*)f_2012_mup.Get("PhysicalVariables"),
			(TTree*)f_2012_mdown.Get("PhysicalVariables"),
			(TTree*)f_2012_sup.Get("PhysicalVariables"),
			(TTree*)f_2012_sdown.Get("PhysicalVariables"),
			(TTree*)f_jb2012_sup.Get("PhysicalVariables"),
			(TTree*)f_jb2012_sdown.Get("PhysicalVariables"),
			(TTree*)f_jb2012_mup.Get("PhysicalVariables"),
			(TTree*)f_jb2012_mdown.Get("PhysicalVariables"),
  };
  
  const int nCuts=24;
  float L_int=5000.;
  TCut cuts[nCuts]={"(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>0)&&(St_uvjj>0)&&(M_uvjj>0)",//preselection
		    "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(MT_uv>0)&&(St_uvjj>0)&&(M_uvjj>0)",//object selection only
	  	    "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(MT_uv>50)&&(St_uvjj>300)&&(M_uvjj>0)",//preselection
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>155)&&(St_uvjj>455)&&(M_uvjj>125)",//300 GeV
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>180)&&(St_uvjj>540)&&(M_uvjj>150)",//350 GeV
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>205)&&(St_uvjj>625)&&(M_uvjj>175)",//etc.
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>225)&&(St_uvjj>715)&&(M_uvjj>200)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>245)&&(St_uvjj>800)&&(M_uvjj>225)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>260)&&(St_uvjj>890)&&(M_uvjj>250)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>275)&&(St_uvjj>980)&&(M_uvjj>280)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>290)&&(St_uvjj>1070)&&(M_uvjj>305)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>300)&&(St_uvjj>1160)&&(M_uvjj>330)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>310)&&(St_uvjj>1250)&&(M_uvjj>355)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>315)&&(St_uvjj>1345)&&(M_uvjj>380)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>320)&&(St_uvjj>1435)&&(M_uvjj>410)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>320)&&(St_uvjj>1530)&&(M_uvjj>435)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>325)&&(St_uvjj>1625)&&(M_uvjj>465)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>320)&&(St_uvjj>1720)&&(M_uvjj>490)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>320)&&(St_uvjj>1820)&&(M_uvjj>590)",//new1
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>320)&&(St_uvjj>1920)&&(M_uvjj>690)",//new2
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>320)&&(St_uvjj>2020)&&(M_uvjj>790)",//new3
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>320)&&(St_uvjj>2120)&&(M_uvjj>890)",//new4
		    "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>400)&&(St_uvjj>2500)&&(M_uvjj>1200)",//new5, newly optimized 2000gev
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2<45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(Pt_miss>55)&&(Pt_ele1<45.0)&&(DPhi_muon1met>0.8)&&(DPhi_jet1met>0.5)&&(St_uvjj>300)&&(MT_uv>50)&&(MT_uv>500)&&(St_uvjj>3500)&&(M_uvjj>1400)"};//new6, super high
  TCut MTuvCut = "(MT_uv>100)";TCut weightcutonly = "weight_central";
  TCut weightcut2 = "weight_central*5000.";TCut weightcut = weightcut2;//*MTuvCut;//*cuts[2];
  
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


  TH1F *h_MTuv[nFiles], *h_Muvjj[nFiles],*h_Muujj2[nFiles],*h_STuvjj[nFiles],*h_PTu1[nFiles],*h_PTu2[nFiles],*h_PTj1[nFiles],*h_PTj2[nFiles],*h_jetCount[nFiles];  
 
  bool doXsecs=1;//1 to scale by correct cross sections, 0 to scale arbitrarily for visual use
  for(int i=0;i<nFiles;i++){
    TString nam1 = "h_Muvjj";nam1+=i;
    TString nam2 = "h_Muujj2";nam2+=i;
    TString ptnam1 = "h_PTu1";ptnam1+=i;
    TString ptnam2 = "h_PTu2";ptnam2+=i;
    TString ptjnam1 = "h_PTj1";ptjnam1+=i;
    TString ptjnam2 = "h_PTj2";ptjnam2+=i;
    TString stNam ="h_STuvjj";stNam+=i;
    TString muuNam ="h_MTuv";muuNam+=i;
    TString jcNam ="h_jetCount";jcNam+=i;
    h_MTuv[i] = new TH1F(muuNam,"MT_{uv};MT_{uv};Arbitrary Units",50,0,5000);
    h_Muvjj[i] = new TH1F(nam1,"M_{uvjj};M_{uvjj};Arbitrary Units",50,0,5000);
    h_Muujj2[i] = new TH1F(nam2,"M_{uujj2};M_{uujj2};Arbitrary Units",50,0,5000);
    h_PTu1[i] = new TH1F(ptnam1,"P_{T}(muon1);P_{T}(muon1);Arbitrary Units",50,0,5000);
    h_PTu2[i] = new TH1F(ptnam2,"P_{T}(muon2);P_{T}(muon2);Arbitrary Units",50,0,5000);
    h_PTj1[i] = new TH1F(ptjnam1,"P_{T}(jet1);P_{T}(jet1);Arbitrary Units",50,0,5000);
    h_PTj2[i] = new TH1F(ptjnam2,"P_{T}(jet2);P_{T}(jet2);Arbitrary Units",50,0,5000);
    h_STuvjj[i] = new TH1F(stNam,"ST_{uvjj};ST_{uvjj};Arbitrary Units",50,0,10000);
    h_jetCount[i] = new TH1F(jcNam,"Jet Count;Jet Count;Arbitrary Units",50,0,50);
    h_MTuv[i]->Sumw2();h_Muvjj[i]->Sumw2();h_Muujj2[i]->Sumw2();h_STuvjj[i]->Sumw2();
    h_PTu1[i]->Sumw2();h_PTu2[i]->Sumw2();h_PTj1[i]->Sumw2();h_PTj1[i]->Sumw2();h_jetCount[i]->Sumw2();
    if(doXsecs){
      h_MTuv[i]->GetYaxis()->SetTitle("Events");
      h_Muvjj[i]->GetYaxis()->SetTitle("Events");
      h_Muujj2[i]->GetYaxis()->SetTitle("Events");
      h_PTu1[i]->GetYaxis()->SetTitle("Events");
      h_PTu2[i]->GetYaxis()->SetTitle("Events");
      h_PTj1[i]->GetYaxis()->SetTitle("Events");
      h_PTj2[i]->GetYaxis()->SetTitle("Events");
      h_STuvjj[i]->GetYaxis()->SetTitle("Events");
      h_jetCount[i]->GetYaxis()->SetTitle("Events");
      
      h_MTuv[i]->SetMarkerSize(0);
      h_Muvjj[i]->SetMarkerSize(0);
      h_Muujj2[i]->SetMarkerSize(0);
      h_PTu1[i]->SetMarkerSize(0);
      h_PTu2[i]->SetMarkerSize(0);
      h_PTj1[i]->SetMarkerSize(0);
      h_PTj2[i]->SetMarkerSize(0);
      h_STuvjj[i]->SetMarkerSize(0);
      h_jetCount[i]->SetMarkerSize(0);
      
      trees[i]->Project(muuNam,"MT_uv",weightcut);
      trees[i]->Project(nam1,"M_uvjj",weightcut);
      trees[i]->Project(nam2,"M_uujj2",weightcut);
      trees[i]->Project(ptnam1,"Pt_muon1",weightcut);
      trees[i]->Project(ptnam2,"Pt_muon2",weightcut);
      trees[i]->Project(ptjnam1,"Pt_jet1",weightcut);
      trees[i]->Project(ptjnam2,"Pt_jet2",weightcut);
      trees[i]->Project(stNam,"St_uujj",weightcut);
      trees[i]->Project(jcNam,"JetCount",weightcut);
    }
    else{
      trees[i]->Project(muuNam,"MT_uv","");
      trees[i]->Project(nam1,"M_uvjj","");
      trees[i]->Project(nam2,"M_uujj2","");
      trees[i]->Project(ptnam1,"Pt_muon1","");
      trees[i]->Project(ptnam2,"Pt_muon2","");
      trees[i]->Project(ptjnam1,"Pt_jet1","");
      trees[i]->Project(ptjnam2,"Pt_jet2","");
      trees[i]->Project(stNam,"St_uujj","");
      trees[i]->Project(jcNam,"JetCount","");
    }
  }
  if(doXsecs)c1->SetLogy(1);
  
  // cout<<"\nmt: "<<h_MTuv[0]->Integral(0,-1)<<"   jetCount: "<<h_jetCount[0]->Integral(0,-1)<<endl<<endl;

  for(int i=1;i<2;i++){
    float weight = h_MTuv[0]->Integral(0,-1)/h_MTuv[i]->Integral(0,-1);
    h_MTuv[i]->Scale(weight,"");
    h_Muvjj[i]->Scale(weight,"");
    h_Muujj2[i]->Scale(weight,"");
    h_PTu1[i]->Scale(weight,"");
    h_PTu2[i]->Scale(weight,"");
    h_PTj1[i]->Scale(weight,"");
    h_PTj2[i]->Scale(weight,"");
    h_STuvjj[i]->Scale(weight,"");
    h_jetCount[i]->Scale(weight,"");
}
  
  for(int j=0;j<nFilesTot;j++){
    TString histname="h_St";histname+=j;
    TH1F *h_St = new TH1F(histname,"",1,0,100000);
    trees[j]->Project(histname,"St_uujj","");
    float yield = h_St->Integral();
    h_yields->Fill(150+50*(j+1),100+50,yield);
    h_St->Delete();  
    for(int k=2;k<=nCuts;++k){
      histname+=k;
      //if(k==3)continue;
      TH1F *h_St2 = new TH1F(histname,"",1,0,100000);
      trees[j]->Project(histname,"St_uujj",cuts[k-1]);
      float yield = h_St2->Integral();
      h_yields->Fill(150+50*(j+1),100+k*50,yield);
      //cout<<"j:"<<j<<" k:"<<k<<" yield:"<<yield<<endl;
      h_St2->Delete();  
    }
  }
 

  float lowbound=0.;doXsecs?lowbound=.01:;
  h_MTuv[nFiles-1]->GetXaxis()->SetRangeUser(0,2200);
  h_MTuv[nFiles-1]->GetYaxis()->SetRangeUser(.0001,1000000);
  h_MTuv[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_MTuv[nFiles-1]->Draw("e");
  for(int i=0;i<nFiles-1;i++){
    h_MTuv[i]->SetLineColor(2**(i+1));
    h_MTuv[i]->Draw("esames");
    // i++;
  }
  leg = TLegend(0.4,0.55,0.86,0.82,"","brNDC");	
  leg.SetHeader("13 TeV (5 fb^{-1} ) W+Jets simulation");
  leg.AddEntry(h_MTuv[0],"amc@NLO inclusive","le");
  leg.AddEntry(h_MTuv[1],"MG LO HT binned * NLO/LO","le");
  leg.AddEntry(h_MTuv[2],"LQ LO M=800 GeV","le");
  //leg.AddEntry(h_MTuv[1],"MG LO inclusive","le");
  //leg.AddEntry(h_MTuv[3],"8TeV MG LO jet binned","le");
  leg.SetFillStyle(0);leg.SetBorderSize(0);
  leg.Draw();
  c1->Print("Plots/wJetsComp/MT_uv.pdf");
  
  h_Muvjj[nFiles-1]->GetXaxis()->SetRangeUser(0,3700);
  h_Muvjj[nFiles-1]->GetYaxis()->SetRangeUser(.01,800000);
  h_Muvjj[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muvjj[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i++){
    h_Muvjj[i]->SetLineColor(2**(i+1));
    h_Muvjj[i]->Draw("sames");
    // i++;
  }
  leg.Draw();
  c1->Print("Plots/wJetsComp/M_uvjj.pdf");
  
  h_Muujj2[nFiles-1]->GetXaxis()->SetRangeUser(0,3700);
  h_Muujj2[nFiles-1]->GetYaxis()->SetRangeUser(.0001,30000);
  h_Muujj2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_Muujj2[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i++){
    h_Muujj2[i]->SetLineColor(2**(i+1));
    h_Muujj2[i]->Draw("sames");
    // i++;
  }

  leg.Draw();
  //c1->Print("Plots/wJetsComp/M_uujj2.pdf");

  h_STuvjj[nFiles-1]->GetXaxis()->SetRangeUser(0,5500);
  h_STuvjj[nFiles-1]->GetYaxis()->SetRangeUser(lowbound,1000000);
  h_STuvjj[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_STuvjj[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i++){
    h_STuvjj[i]->SetLineColor(2**(i+1));
    h_STuvjj[i]->Draw("sames");
    // i++;
  }

  leg.Draw();
  c1->Print("Plots/wJetsComp/ST_uvjj.pdf");
  
  h_PTu1[nFiles-1]->GetXaxis()->SetRangeUser(0,2500);
  h_PTu1[nFiles-1]->GetYaxis()->SetRangeUser(2e-3,800000);
  h_PTu1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTu1[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i++){
    h_PTu1[i]->SetLineColor(2**(i+1));
    h_PTu1[i]->Draw("sames");
    // i++;
  }
  leg.Draw();
  c1->Print("Plots/wJetsComp/Pt_muon1.pdf");
  
  h_PTu2[nFiles-1]->GetXaxis()->SetRangeUser(0,2500);
  h_PTu2[nFiles-1]->GetYaxis()->SetRangeUser(2e-3,80000);
  h_PTu2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTu2[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i++){
    h_PTu2[i]->SetLineColor(2**(i+1));
    h_PTu2[i]->Draw("sames");
    // i++;
  }

  leg.Draw();
  //c1->Print("Plots/wJetsComp/Pt_muon2.pdf");
  
  h_PTj1[nFiles-1]->GetXaxis()->SetRangeUser(0,2000);
  h_PTj1[nFiles-1]->GetYaxis()->SetRangeUser(2e-1,800000);
  h_PTj1[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTj1[nFiles-1]->Draw();
  for(int i=0;i<nFiles-1;i++){
    h_PTj1[i]->SetLineColor(2**(i+1));
    h_PTj1[i]->Draw("sames");
    // i++;
  }
  leg.Draw();
  c1->Print("Plots/wJetsComp/Pt_jet1.pdf");
  
  h_PTj2[nFiles-1]->GetXaxis()->SetRangeUser(0,2000);
  h_PTj2[nFiles-1]->GetYaxis()->SetRangeUser(2e-1,800000);
  h_PTj2[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_PTj2[nFiles-1]->Draw("e");
  for(int i=0;i<nFiles-1;i++){
    h_PTj2[i]->SetLineColor(2**(i+1));
    h_PTj2[i]->Draw("esames");
    // i++;
  }

  leg.Draw();
  c1->Print("Plots/wJetsComp/Pt_jet2.pdf");
 
  c1->SetLogy(0);
  h_jetCount[nFiles-1]->GetXaxis()->SetRangeUser(0,20);
  h_jetCount[nFiles-1]->GetYaxis()->SetRangeUser(0,210000);
  h_jetCount[nFiles-1]->GetYaxis()->SetTitleOffset(1.3);
  h_jetCount[nFiles-1]->Draw("e");
  for(int i=0;i<nFiles-1;i++){
    h_jetCount[i]->SetLineColor(2**(i+1));
    h_jetCount[i]->Draw("esames");
    // i++;
  }

  leg.Draw();
  c1->Print("Plots/wJetsComp/jetCount.pdf");

  c1->SetLogy(0);
  int y=200;
  h_yields->SetTitle("W+Jets raw event counts");//h_yields->CenterTitle();
  int b=1;
  h_yields->GetXaxis()->SetBinLabel(b,"amc@NLO inclusive");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"LO HT binned");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"LQ LO uvjj M=800");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV LO jet binned");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV match up");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV match down");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV scale up");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV scale down");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV jet bin scale up");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV jet bin scale down");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV jet bin match up");b++;
  h_yields->GetXaxis()->SetBinLabel(b,"8TeV jet bin match down");b++;
  //h_yields->GetYaxis()->SetBinLabel(1,"#mu>42, jet>110 GeV");
  h_yields->GetYaxis()->SetBinLabel(1,"");
  h_yields->GetYaxis()->SetBinLabel(2,"+ #mu#nujj object selection");
  h_yields->GetYaxis()->SetBinLabel(3,"+ Preselection");
  for(int b=1;b<nCuts;b++){
    int j=b-17;
    stringstream ss;ss <<y;
    string str=ss.str();
    //h_yields->GetXaxis()->SetBinLabel(b,str.c_str());
    if(b<=3){//h_eff->GetXaxis()->SetBinLabel(b,str.c_str());
      //h_sOverSplusB->GetXaxis()->SetBinLabel(b,str.c_str());
    }
    if(b>=3 && b<18){
      h_yields->GetYaxis()->SetBinLabel(b+1,str.c_str());
      //h_eff->GetYaxis()->SetBinLabel(b+1,str.c_str());
      //h_sOverSplusB->GetYaxis()->SetBinLabel(b+1,str.c_str());
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
  // c1->Print("Plots/wJetsComp/efficiencyTable.png");
  // c1->Print("Plots/wJetsComp/efficiencyTable.pdf");
  
  h_sOverSplusB->GetYaxis()->SetTitleSize(0.05);
  h_sOverSplusB->GetZaxis()->SetRangeUser(.077,140);
  //c1->SetLogz(0);
   //  h_sOverSplusB->Draw("colztext");
  //c1->Print("Plots/wJetsComp/sOverSqrtSplusB.png");
  //c1->Print("Plots/wJetsComp/sOverSqrtSplusB.pdf");
  
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
  T1.DrawLatex(tlx,tly,"+ mt_{uv}>320 st>1820 m_{uvjj}>590");tly+=step;
  T1.DrawLatex(tlx,tly,"+ mt_{uv}>320 st>1920 m_{uvjj}>690");tly+=step;
  T1.DrawLatex(tlx,tly,"+ mt_{uv}>320 st>2020 m_{uvjj}>790");tly+=step;
  T1.DrawLatex(tlx,tly,"+ mt_{uv}>320 st>2120 m_{uvjj}>890");tly+=step;
  T1.DrawLatex(tlx,tly,"+ mt_{uv}>400 st>2500 m_{uvjj}>1200");tly+=step;
  T1.DrawLatex(tlx,tly,"+ mt_{uv}>500 st>3500 m_{uvjj}>1400");tly+=step;
  T1.SetTextSize(0.03);
  T1.DrawLatex(.258,.88,"13 TeV #leftarrow");T1.DrawLatex(.375,.88,"#rightarrow 8 TeV");T1.DrawLatex(.643,.88,"#rightarrow FastSim");
  TLatex T2;T2.SetNDC();T2.SetTextAngle(90);T2.SetTextSize(0.03);
  T2.DrawLatex(.12,.28,"2012 LQ2 optim. cut mass");
  T2.SetTextSize(0.023);T2.SetTextAngle(0);
  T2.DrawLatex(.02,.112,"#splitline{skim: #mu1>42, E_{T}^{miss}>35,}{jet1>110, jet2>40, ST>250}");
  TLine l;l.SetLineWidth(2);tlx=.363;l.DrawLineNDC(tlx,.13,tlx,.9);tlx=.633;l.DrawLineNDC(tlx,.13,tlx,.9);
  c1->Update();
  //c1->Print("Plots/wJetsComp/yields.png");
  c1->Print("Plots/wJetsComp/yields.pdf");
  
    
}
