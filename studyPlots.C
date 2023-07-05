#include "TCanvas.h"
#include "TH1.h"

void studyPlots(){
  gStyle->SetOptStat(0);gStyle->SetLegendBorderSize(0);gStyle->SetLegendFillColor(0);
  TCanvas c1("c1","c1",800,600);c1.cd();

  Double_t bins[]={300,400,650,900,2000};
  Double_t binsMuujj2[]={0,250,750,2000};
  Double_t binsMuNu[]={300,500,750,2000};
  Double_t binsJetPt[]={50,100,200,400,750};
  Double_t binsMuonPt[]={50,85,100,160,200,500};
  Double_t binsZPt[]={0,100,200,400,1000};
  Double_t binsNJet[]={2,3,4,5,6,7};
  TH1F* mujmin = new TH1F("mujmin",";[GeV];#mu#mu SFs",3,binsMuujj2);
  TH1F* munuW = new TH1F("munuW",";S_{T} [GeV];#mu#nujj SF",3,binsMuNu);
  TH1F* munuTT = new TH1F("munuTT",";S_{T} [GeV];#mu#nujj SFs",3,binsMuNu);
  TH1F* pt = new TH1F("pt",";S_{T} [GeV];Z+Jets SF (Pt-binned)",4,bins);
  TH1F* pt_jet = new TH1F("pt_jet",";Leading Jet Pt [GeV];Z / tt Normalization SF",4,binsJetPt);
  TH1F* pt_jet_TT = new TH1F("pt_jet_TT",";Leading Jet Pt [GeV];Z / tt Normalization SF",4,binsJetPt);
  TH1F* njet = new TH1F("njet",";Number of Jets;Z / tt Normalization SF",5,binsNJet);
  TH1F* njet_TT = new TH1F("njet_TT",";Number ofJets;Z / tt Normalization SF",5,binsNJet);
  TH1F* pt_jet2 = new TH1F("pt_jet2",";Traiing Jet Pt [GeV];Z / tt Normalization SF",4,binsJetPt);
  TH1F* pt_jet2_TT = new TH1F("pt_jet2_TT",";Trailing Jet Pt [GeV];Z / tt Normalization SF",4,binsJetPt);
  TH1F* pt_mu = new TH1F("pt_mu",";Leading Muon Pt [GeV];Z / tt Normalization SF",5,binsMuonPt);
  TH1F* pt_mu_TT = new TH1F("pt_mu_TT",";Leading Muon Pt [GeV];Z / tt Normalization SF",5,binsMuonPt);
  TH1F* pt_mu2 = new TH1F("pt_mu2",";Trailing Muon Pt [GeV];Z / tt Normalization SF",5,binsMuonPt);
  TH1F* pt_mu2_TT = new TH1F("pt_mu2_TT",";Trailing Muon Pt [GeV];Z / tt Normalization SF",5,binsMuonPt);
  TH1F* st = new TH1F("st",";S_T [GeV];Z / tt Normalization SF",4,bins);
  TH1F* st_TT = new TH1F("st_TT",";S_T [GeV];Z / tt Normalization SF",4,bins);
  TH1F* muj1 = new TH1F("muj1",";m_{#muj1} [GeV];Z / tt Normalization SF",4,bins);
  TH1F* muj1_TT = new TH1F("muj1_TT",";m_{#muj1} [GeV];Z / tt Normalization SF",4,bins);
  TH1F* muj2 = new TH1F("muj2",";m_{#muj2} [GeV];Z / tt Normalization SF",4,bins);
  TH1F* muj2_TT = new TH1F("muj2_TT",";m_{#muj2} [GeV];Z / tt Normalization SF",4,bins);
  TH1F* zpt = new TH1F("zpt",";RECO Z pt [GeV];Z / tt Normalization SF",4,binsZPt);
  TH1F* zpt_TT = new TH1F("zpt_TT",";RECO Z Pt [GeV];Z / tt Normalization SF",4,binsZPt);
  TString year = "2016";


  Double_t Wnom_uvjj = 0.926;
  Double_t WnomErr_uvjj = 0.01;
  Double_t TTnom_uvjj = 1.022;
  Double_t TTnomErr_uvjj = 0.008; 
  Float_t Mujs_uujj[3]={0.969,0.92,0.82};
  Float_t MujErrs_uujj[3]={.007,.01,.102};
  Float_t Ws_uvjj[3]={0.929,0.92,.903};
  Float_t WErrs_uvjj[3]={.011,.022,.06};
  Float_t TTs_uvjj[3]={1.017,1.048,1.095};
  Float_t TTErrs_uvjj[3]={0.009,.025,.089};

  //2016
  
  Double_t Znom = 1.022;
  Double_t ZnomErr = 0.017;
  Double_t TTnom = 0.989;
  Double_t TTnomErr = 0.014; 
  //inclusive
  //Double_t Zpt_Z[4]={1.12855070957,1.0223233817,1.00785512305,0.979400743118};Double_t ZptErr_Z[4]={0.09596,0.02018,0.02477,0.06789};
  //Double_t Zpt_TT[4]={0.982838477246,0.997277977577,1.05695167819,0.291053062213};Double_t ZptErr_TT[4]={0.01552,0.02573,0.11993,1.50623};
  //2 jet
  //Double_t Zpt_Z[4]={1.10790435733,1.02376545112,0.992045187409,1.03050690914};Double_t ZptErr_Z[4]={0.14301,0.02812,0.02985,0.11796};
  //Double_t Zpt_TT[4]={0.950352819227,1.01360094346,0.848498833096,-0.582657586753};Double_t ZptErr_TT[4]={0.02369,0.04302,0.28688,1.70868};
  //3 jet
  //Double_t Zpt_Z[4]={1.10348023313,0.944443961267,0.981348229962,0.683684292497};Double_t ZptErr_Z[4]={0.23014,0.03897,0.05089,0.12294};
  //Double_t Zpt_TT[4]={1.04469173839,0.995147213158,1.41349428898,3.12693341441};Double_t ZptErr_TT[4]={0.02903,0.04047,0.24494,2.44644000001};
  //4 jet
  Double_t Zpt_Z[4]={32.5556936862,1.11479309077,1.03804104416,1.31187164477};Double_t ZptErr_Z[4]={31.556499999,0.13647,0.10781,0.22001};
  Double_t Zpt_TT[4]={0.726000424409,1.02772645722,1.12966486841,-4.10440303856};Double_t ZptErr_TT[4]={0.27989,0.07735,0.31383,4.24722000001};
  //5 jet
  //Double_t Zpt_Z[4]={0.836960439277,1.90942894477,1.1759546514,1.62075617194};Double_t ZptErr_Z[4]={0.822229999999,0.32205,0.1938,0.36297};
  //Double_t Zpt_TT[4]={1.11255718483,0.979258677492,0.587590153017,-14.1388699125};Double_t ZptErr_TT[4]={0.1235,0.18973,0.35755,18.2702199995};
  //6 jet
  //Double_t Zpt_Z[4]={-0.342549285149,2.34104989328,1.9029131752,3.18352928945};Double_t ZptErr_Z[4]={0.22703,1.03623,0.65851,1.88058};
  //Double_t Zpt_TT[4]={0.884799691495,1.05140926549,0.550367286654,55.3561219724};Double_t ZptErr_TT[4]={0.3115,0.43196,0.39923,61.5333400083};
  
  Float_t Sts[4]={.974,1.046,1.068,1.037};
  Float_t StErrs[4]={.028,.025,.052,.059};
  Float_t Sts_TT[4]={.944,.994,.886,.844};
  Float_t StErrs_TT[4]={.02,.023,.06,.124};
  Float_t PtJet_Z[4]={.996,1.0,1.055,1.112};Float_t PtJetErr_Z[4]={.048,.024,.026,.059};
  Float_t PtJet_TT[4]={.907,.983,.979,.782};Float_t PtJetErr_TT[4]={.026,.018,.041,.096};
  Float_t PtMu_Z[5]={1.059,.984,.99,1.078,1.045};Float_t PtMuErr_Z[5]={.043,.036,.027,.046,.038};
  Float_t PtMu_TT[5]={.989,.956,.957,.949,.786};Float_t PtMuErr_TT[5]={.028,.023,.023,.057,.119};
  Float_t nJet_Z[5]={};Float_t nJetErr_Z[5]={};
  Float_t nJet_TT[5]={};Float_t nJetErr_TT[5]={};
  Float_t PtJet2_Z[4]={};Float_t PtJet2Err_Z[4]={};
  Float_t PtJet2_TT[4]={};Float_t PtJet2Err_TT[4]={};
  Float_t PtMu2_Z[5]={};Float_t PtMu2Err_Z[5]={};
  Float_t PtMu2_TT[5]={};Float_t PtMu2Err_TT[5]={};
  Float_t muj1s_Z[4]={};Float_t muj1Errs_Z[4]={};
  Float_t muj1s_TT[4]={};Float_t muj1Errs_TT[4]={};
  Float_t muj2s_Z[4]={};Float_t muj2Errs_Z[4]={};
  Float_t muj2s_TT[4]={};Float_t muj2Errs_TT[4]={};
 
  //2017
  /*
  Double_t Znom = 1.372;
  Double_t ZnomErr = 0.0207;
  Double_t TTnom = 1.061;
  Double_t TTnomErr = 0.0122;
  Float_t Sts[4]={1.3476205016,1.37604304814,1.42676607397,1.41914813299};Float_t StErrs[4]={0.03636,0.03069,0.04432,0.07019};
  Float_t Sts_TT[4]={1.07523724898,1.04804241503,1.00616389533,0.952093897372};Float_t StErrs_TT[4]={0.0158,0.01747,0.0615,0.16237};
  Float_t PtJet_Z[4]={1.36209780585,1.3539979262,1.41288056705,1.39077279237};Float_t PtJetErr_Z[4]={0.05231,0.02367,0.03651,0.09197};
  Float_t PtJet_TT[4]={1.05219069427,1.07433711988,1.0303306525,0.991486989738};Float_t PtJetErr_TT[4]={0.02631,0.01641,0.03251,0.11082};
  Float_t PtMu_Z[5]={1.32053674298,1.33115517154,1.38805508914,1.40718514849,1.46385042475};Float_t PtMuErr_Z[5]={0.04622,0.03337,0.03645,0.05281,0.0525};
  Float_t PtMu_TT[5]={1.08998793594,1.09061745996,1.01657855366,1.03605087677,0.833578597181};Float_t PtMuErr_TT[5]={0.02189,0.01871,0.02172,0.06969,0.1375};
  */
  //2018
  /*
  Double_t Znom = 1.302;
  Double_t ZnomErr = 0.0166;
  Double_t TTnom = 0.98;
  Double_t TTnomErr = 0.0097;
  Float_t Sts[4]={1.32016372637,1.2779543503,1.30896020658,1.32867206093};Float_t StErrs[4]={0.02623,0.0237,0.04609,0.06156};
  Float_t Sts_TT[4]={0.966736770207,0.98803260802,1.10633238344,0.834144173491};Float_t StErrs_TT[4]={0.01507,0.0134,0.06159,0.11592};
  Float_t PtJet_Z[4]={1.39961825267,1.29270888196,1.28535771553,1.27753090463};Float_t PtJetErr_Z[4]={0.04893,0.02607,0.02913,0.06363};
  Float_t PtJet_TT[4]={0.935571392342,0.991526772008,0.999020889745,0.960138599137};Float_t PtJetErr_TT[4]={0.02048,0.01407,0.02419,0.08341};
  Float_t PtMu_Z[5]={1.27477666325,1.26484376884,1.28698618107,1.36085756515,1.39492732949};Float_t PtMuErr_Z[5]={0.04249,0.02829,0.02947,0.05607,0.04301};
  Float_t PtMu_TT[5]={1.02074905189,0.972355703983,0.96020647631,0.939497670007,1.02671644728};Float_t PtMuErr_TT[5]={0.01574,0.01702,0.01506,0.05722,0.10724};
  */
  //2016-2018 combination
  /*
  Double_t Znom = 1.242;
  Double_t ZnomErr = 0.0104;
  Double_t TTnom = 0.999;
  Double_t TTnomErr = 0.0068;
  Float_t Sts[4]={1.22963848497,1.24012734697,1.28175899733,1.26373582279};Float_t StErrs[4]={0.01655,0.0166,0.03072,0.03827};
  Float_t Sts_TT[4]={0.991401743248,1.00925352533,1.01409589638,0.858003877204};Float_t StErrs_TT[4]={0.0094,0.01155,0.03855,0.07649};
  Float_t PtJet_Z[4]={1.27440907726,1.22529750163,1.25854693949,1.25967075061};Float_t PtJetErr_Z[4]={0.03122,0.01273,0.01985,0.03993};
  Float_t PtJet_TT[4]={0.963850034663,1.0123882319,1.00002590793,0.929382567501};Float_t PtJetErr_TT[4]={0.01561,0.00861,0.01951,0.04504};
  Float_t PtMu_Z[5]={1.22710094175,1.20625688051,1.23341991423,1.2923519005,1.31810593919};Float_t PtMuErr_Z[5]={0.03036,0.02097,0.01844,0.03039,0.02821};
  Float_t PtMu_TT[5]={1.03425341839,1.00228191734,0.977044017319,0.967189462567,0.89801563345};Float_t PtMuErr_TT[5]={0.01268,0.0121,0.01025,0.03261,0.06965};
  */
  //2016-2018 combination
  /*
  Double_t Znom = 1.239;
  Double_t ZnomErr = 0.01;
  Double_t TTnom = 1.014;
  Double_t TTnomErr = 0.007;
  
  Float_t Sts[4]={1.22872629996,1.23331793004,1.28328859643,1.26750545166};Float_t StErrs[4]={0.01628,0.01554,0.02858,0.03932};
  Float_t Sts_TT[4]={1.00158332126,1.03326745995,1.04824955485,0.862485393573};Float_t StErrs_TT[4]={0.00963,0.01079,0.03887,0.07953};
  Float_t PtJet_Z[4]={1.27427964077,1.21971225506,1.24852683306,1.25364521022};Float_t PtJetErr_Z[4]={0.02918,0.01531,0.01839,0.04205};
  Float_t PtJet_TT[4]={0.969414485254,1.03055334008,1.02704776951,0.945917546825};Float_t PtJetErr_TT[4]={0.01276,0.00954,0.01748,0.0445};
  Float_t PtJet2_Z[4]={1.23706350654,1.24616094209,1.22811881923,1.25376457639};Float_t PtJet2Err_Z[4]={0.01136,0.02141,0.04564,0.11046};
  Float_t PtJet2_TT[4]={1.00893294929,1.02455340094,1.05433717167,2.05029777319};Float_t PtJet2Err_TT[4]={0.00845,0.01349,0.04822,0.55261};
  Float_t PtMu_Z[5]={1.22163971983,1.20475271579,1.22650931872,1.29077660862,1.31010740014};Float_t PtMuErr_Z[5]={0.02603,0.02157,0.01789,0.03034,0.02766};
  Float_t PtMu_TT[5]={1.04171593441,1.01262682863,0.996377282804,0.992393991485,0.926262530832};Float_t PtMuErr_TT[5]={0.01388,0.01274,0.01302,0.02936,0.06934};
  Float_t PtMu2_Z[5]={1.21958529064,1.25613852386,1.3758469996,1.18311034703,1.4884402017};Float_t PtMu2Err_Z[5]={0.01392,0.02123,0.03257,0.06705,0.14522};
  Float_t PtMu2_TT[5]={1.01808377568,1.00892699954,0.82946147465,1.72850231174,0.0138942953687};Float_t PtMu2Err_TT[5]={0.00607,0.01816,0.05615,0.775549999999,3.27672000001};
  Float_t muj1s_Z[4]={1.07679116642,1.21013057717,1.26171552888,1.36314570817};Float_t muj1Errs_Z[4]={0.08522,0.01376,0.01712,0.03345};
  Float_t muj1s_TT[4]={0.973680038735,1.03723454135,1.11316566103,1.0499287926};Float_t muj1Errs_TT[4]={0.00907,0.01061,0.02651,0.07692};
  Float_t muj2s_Z[4]={1.17368028567,1.2430343114,1.3223695078,1.45259831538};Float_t muj2Errs_Z[4]={0.02332,0.01341,0.02648,0.07236};
  Float_t muj2s_TT[4]={0.998679935505,1.05024316735,1.09629618089,0.718226154429};Float_t muj2Errs_TT[4]={0.00797,0.01366,0.07604,0.8230799};
  //comb 
  Float_t nJet_Z[5]={1.14616082875,1.30423711661,1.74615424473,2.26588402715,2.73379262824};Float_t nJetErr_Z[5]={0.0111,0.01883,0.059,0.1532,0.46306};
  Float_t nJet_TT[5]={1.00466693692,1.02925347697,1.0282330842,1.01271460077,0.954888063384};Float_t nJetErr_TT[5]={0.00996,0.01268,0.02145,0.05155,0.093};
  //2016
  //Float_t nJet_Z[5]={1.02509863258,0.949477848189,1.15219056899,1.47038986577,1.81713227943};Float_t nJetErr_Z[5]={0.01745,0.03161,0.07716,0.15961,0.44171};
  //Float_t nJet_TT[5]={0.963993354845,1.04371644007,0.979171389929,1.01020592434,0.917019133968};Float_t nJetErr_TT[5]={0.01823,0.02579,0.0498,0.09303,0.18131};
  //2017
  //Float_t nJet_Z[5]={1.23573233897,1.50288534347,2.0495211109,2.81468045202,7.79556258861};Float_t nJetErr_Z[5]={0.02079,0.04078,0.127,0.3503,2.76612000001};
  //Float_t nJet_TT[5]={1.10691859839,1.06213932449,1.15166159754,0.87731007865,0.937361239629};Float_t nJetErr_TT[5]={0.01464,0.01933,0.04243,0.07664,0.23774};
  //2018
  //Float_t nJet_Z[5]={1.16447448248,1.43658072629,2.02253025598,2.80350954739,2.50909075739};Float_t nJetErr_Z[5]={0.01744,0.04016,0.11312,0.33523,0.66039};
  //Float_t nJet_TT[5]={0.961146485003,1.00040298761,0.987927025219,1.09362206399,0.887102119887};Float_t nJetErr_TT[5]={0.01258,0.02036,0.03301,0.07419,0.12933};
  */

  for (int i=0;i<pt_jet->GetNbinsX();i++){
    pt_jet->SetBinContent(i+1,PtJet_Z[i]);pt_jet->SetBinError(i+1,PtJetErr_Z[i]);
    pt_jet_TT->SetBinContent(i+1,PtJet_TT[i]);pt_jet_TT->SetBinError(i+1,PtJetErr_TT[i]);
  }
  for (int i=0;i<njet->GetNbinsX();i++){
    njet->SetBinContent(i+1,nJet_Z[i]);njet->SetBinError(i+1,nJetErr_Z[i]);
    njet_TT->SetBinContent(i+1,nJet_TT[i]);njet_TT->SetBinError(i+1,nJetErr_TT[i]);
  }
  
  zpt->SetBinContent(1,Zpt_Z[0]);zpt->SetBinError(1,ZptErr_Z[0]);
  zpt->SetBinContent(2,Zpt_Z[1]);zpt->SetBinError(2,ZptErr_Z[1]);
  zpt->SetBinContent(3,Zpt_Z[2]);zpt->SetBinError(3,ZptErr_Z[2]);
  zpt->SetBinContent(4,Zpt_Z[3]);zpt->SetBinError(4,ZptErr_Z[3]);

  zpt_TT->SetBinContent(1,Zpt_TT[0]);zpt_TT->SetBinError(1,ZptErr_TT[0]);
  zpt_TT->SetBinContent(2,Zpt_TT[1]);zpt_TT->SetBinError(2,ZptErr_TT[1]);
  zpt_TT->SetBinContent(3,Zpt_TT[2]);zpt_TT->SetBinError(3,ZptErr_TT[2]);
  zpt_TT->SetBinContent(4,Zpt_TT[3]);zpt_TT->SetBinError(4,ZptErr_TT[3]);
  
  pt_jet2->SetBinContent(1,PtJet2_Z[0]);pt_jet2->SetBinError(1,PtJet2Err_Z[0]);
  pt_jet2->SetBinContent(2,PtJet2_Z[1]);pt_jet2->SetBinError(2,PtJet2Err_Z[1]);
  pt_jet2->SetBinContent(3,PtJet2_Z[2]);pt_jet2->SetBinError(3,PtJet2Err_Z[2]);
  pt_jet2->SetBinContent(4,PtJet2_Z[3]);pt_jet2->SetBinError(4,PtJet2Err_Z[3]);

  pt_jet2_TT->SetBinContent(1,PtJet2_TT[0]);pt_jet2_TT->SetBinError(1,PtJet2Err_TT[0]);
  pt_jet2_TT->SetBinContent(2,PtJet2_TT[1]);pt_jet2_TT->SetBinError(2,PtJet2Err_TT[1]);
  pt_jet2_TT->SetBinContent(3,PtJet2_TT[2]);pt_jet2_TT->SetBinError(3,PtJet2Err_TT[2]);
  pt_jet2_TT->SetBinContent(4,PtJet2_TT[3]);pt_jet2_TT->SetBinError(4,PtJet2Err_TT[3]);

  pt_mu->SetBinContent(1,PtMu_Z[0]);pt_mu->SetBinError(1,PtMuErr_Z[0]);
  pt_mu->SetBinContent(2,PtMu_Z[1]);pt_mu->SetBinError(2,PtMuErr_Z[1]);
  pt_mu->SetBinContent(3,PtMu_Z[2]);pt_mu->SetBinError(3,PtMuErr_Z[2]);
  pt_mu->SetBinContent(4,PtMu_Z[3]);pt_mu->SetBinError(4,PtMuErr_Z[3]);
  pt_mu->SetBinContent(5,PtMu_Z[4]);pt_mu->SetBinError(5,PtMuErr_Z[4]);
  pt_mu_TT->SetBinContent(1,PtMu_TT[0]);pt_mu_TT->SetBinError(1,PtMuErr_TT[0]);
  pt_mu_TT->SetBinContent(2,PtMu_TT[1]);pt_mu_TT->SetBinError(2,PtMuErr_TT[1]);
  pt_mu_TT->SetBinContent(3,PtMu_TT[2]);pt_mu_TT->SetBinError(3,PtMuErr_TT[2]);
  pt_mu_TT->SetBinContent(4,PtMu_TT[3]);pt_mu_TT->SetBinError(4,PtMuErr_TT[3]);
  pt_mu_TT->SetBinContent(5,PtMu_TT[4]);pt_mu_TT->SetBinError(5,PtMuErr_TT[4]);

  pt_mu2->SetBinContent(1,PtMu2_Z[0]);pt_mu2->SetBinError(1,PtMu2Err_Z[0]);
  pt_mu2->SetBinContent(2,PtMu2_Z[1]);pt_mu2->SetBinError(2,PtMu2Err_Z[1]);
  pt_mu2->SetBinContent(3,PtMu2_Z[2]);pt_mu2->SetBinError(3,PtMu2Err_Z[2]);
  pt_mu2->SetBinContent(4,PtMu2_Z[3]);pt_mu2->SetBinError(4,PtMu2Err_Z[3]);
  pt_mu2->SetBinContent(5,PtMu2_Z[4]);pt_mu2->SetBinError(5,PtMu2Err_Z[4]);
  pt_mu2_TT->SetBinContent(1,PtMu2_TT[0]);pt_mu2_TT->SetBinError(1,PtMu2Err_TT[0]);
  pt_mu2_TT->SetBinContent(2,PtMu2_TT[1]);pt_mu2_TT->SetBinError(2,PtMu2Err_TT[1]);
  pt_mu2_TT->SetBinContent(3,PtMu2_TT[2]);pt_mu2_TT->SetBinError(3,PtMu2Err_TT[2]);
  pt_mu2_TT->SetBinContent(4,PtMu2_TT[3]);pt_mu2_TT->SetBinError(4,PtMu2Err_TT[3]);
  pt_mu2_TT->SetBinContent(5,PtMu2_TT[4]);pt_mu2_TT->SetBinError(5,PtMu2Err_TT[4]);

  st->SetBinContent(1,Sts[0]);st->SetBinError(1,StErrs[0]);
  st->SetBinContent(2,Sts[1]);st->SetBinError(2,StErrs[1]);
  st->SetBinContent(3,Sts[2]);st->SetBinError(3,StErrs[2]);
  st->SetBinContent(4,Sts[3]);st->SetBinError(4,StErrs[3]);
  st_TT->SetBinContent(1,Sts_TT[0]);st_TT->SetBinError(1,StErrs_TT[0]);
  st_TT->SetBinContent(2,Sts_TT[1]);st_TT->SetBinError(2,StErrs_TT[1]);
  st_TT->SetBinContent(3,Sts_TT[2]);st_TT->SetBinError(3,StErrs_TT[2]);
  st_TT->SetBinContent(4,Sts_TT[3]);st_TT->SetBinError(4,StErrs_TT[3]);

  mujmin->SetBinContent(1,Mujs_uujj[0]);mujmin->SetBinError(1,MujErrs_uujj[0]);
  mujmin->SetBinContent(2,Mujs_uujj[1]);mujmin->SetBinError(2,MujErrs_uujj[1]);
  mujmin->SetBinContent(3,Mujs_uujj[2]);mujmin->SetBinError(3,MujErrs_uujj[2]);

  munuW->SetBinContent(1,Ws_uvjj[0]);munuW->SetBinError(1,WErrs_uvjj[0]);
  munuW->SetBinContent(2,Ws_uvjj[1]);munuW->SetBinError(2,WErrs_uvjj[1]);
  munuW->SetBinContent(3,Ws_uvjj[2]);munuW->SetBinError(3,WErrs_uvjj[2]);

  munuTT->SetBinContent(1,TTs_uvjj[0]);munuTT->SetBinError(1,TTErrs_uvjj[0]);
  munuTT->SetBinContent(2,TTs_uvjj[1]);munuTT->SetBinError(2,TTErrs_uvjj[1]);
  munuTT->SetBinContent(3,TTs_uvjj[2]);munuTT->SetBinError(3,TTErrs_uvjj[2]);

  muj1->SetBinContent(1,muj1s_Z[0]);muj1->SetBinError(1,muj1Errs_Z[0]);
  muj1->SetBinContent(2,muj1s_Z[1]);muj1->SetBinError(2,muj1Errs_Z[1]);
  muj1->SetBinContent(3,muj1s_Z[2]);muj1->SetBinError(3,muj1Errs_Z[2]);
  muj1->SetBinContent(4,muj1s_Z[3]);muj1->SetBinError(4,muj1Errs_Z[3]);
  muj1_TT->SetBinContent(1,muj1s_TT[0]);muj1_TT->SetBinError(1,muj1Errs_TT[0]);
  muj1_TT->SetBinContent(2,muj1s_TT[1]);muj1_TT->SetBinError(2,muj1Errs_TT[1]);
  muj1_TT->SetBinContent(3,muj1s_TT[2]);muj1_TT->SetBinError(3,muj1Errs_TT[2]);
  muj1_TT->SetBinContent(4,muj1s_TT[3]);muj1_TT->SetBinError(4,muj1Errs_TT[3]);


  muj2->SetBinContent(1,muj2s_Z[0]);muj2->SetBinError(1,muj2Errs_Z[0]);
  muj2->SetBinContent(2,muj2s_Z[1]);muj2->SetBinError(2,muj2Errs_Z[1]);
  muj2->SetBinContent(3,muj2s_Z[2]);muj2->SetBinError(3,muj2Errs_Z[2]);
  muj2->SetBinContent(4,muj2s_Z[3]);muj2->SetBinError(4,muj2Errs_Z[3]);
  muj2_TT->SetBinContent(1,muj2s_TT[0]);muj2_TT->SetBinError(1,muj2Errs_TT[0]);
  muj2_TT->SetBinContent(2,muj2s_TT[1]);muj2_TT->SetBinError(2,muj2Errs_TT[1]);
  muj2_TT->SetBinContent(3,muj2s_TT[2]);muj2_TT->SetBinError(3,muj2Errs_TT[2]);
  muj2_TT->SetBinContent(4,muj2s_TT[3]);muj2_TT->SetBinError(4,muj2Errs_TT[3]);


  TLine l,l1;
  l.SetLineColor(kBlue);l1.SetLineColor(kRed);//l.SetLineWidth(2);l1.SetLineWidth(2);
  munuW->SetLineColor(kBlue);munuW->SetMarkerColor(kBlue);
  munuTT->SetLineColor(kRed);munuTT->SetMarkerColor(kRed);
  pt->SetLineColor(kBlue);pt->SetMarkerColor(kBlue);
  mujmin->SetLineColor(kRed);mujmin->SetMarkerColor(kRed);

  munuW->GetYaxis()->SetRangeUser(.8,1.2);
  munuTT->GetYaxis()->SetRangeUser(.8,1.2);
  mujmin->GetYaxis()->SetRangeUser(.7,1.);
  /*
  munuW->Draw("pe");
  munuTT->Draw("pesames");
  l.DrawLine(300,Wnom_uvjj,2000,Wnom_uvjj);
  l.SetLineStyle(7);
  l.DrawLine(300,Wnom_uvjj+WnomErr_uvjj,2000,Wnom_uvjj+WnomErr_uvjj);
  l.DrawLine(300,Wnom_uvjj-WnomErr_uvjj,2000,Wnom_uvjj-WnomErr_uvjj);
  l1.DrawLine(300,TTnom_uvjj,2000,TTnom_uvjj);
  l1.SetLineStyle(7);
  l1.DrawLine(300,TTnom_uvjj+TTnomErr_uvjj,2000,TTnom_uvjj+TTnomErr_uvjj);
  l1.DrawLine(300,TTnom_uvjj-TTnomErr_uvjj,2000,TTnom_uvjj-TTnomErr_uvjj);
  c1.Print("Results_Testing_v236_Vpt_19Sep/munuScaleFactors.pdf");
  */
  /*
  mujmin->Draw("pe");
  pt->Draw("pesames");
  //l.DrawLine(300,1.092,2000,1.092);//pt-bin only
  l.SetLineColor(kBlack);
  l.SetLineStyle(0);
  l.DrawLine(0,Znom,2000,Znom);//stitched
  l.SetLineStyle(7);
  l.DrawLine(0,Znom+ZnomErr,2000,Znom+ZnomErr);
  l.DrawLine(0,Znom-ZnomErr,2000,Znom-ZnomErr);
  c1.Print("Results_Testing_v236_Vpt_19Sep/mumuScaleFactors.pdf");
  */
  
  pt_jet->SetLineColor(kBlue);pt_jet->SetMarkerColor(kBlue);pt_jet_TT->SetLineColor(kRed);pt_jet_TT->SetMarkerColor(kRed);
  if(year=="2016"){pt_jet->GetXaxis()->SetRangeUser(50,750);pt_jet->GetYaxis()->SetRangeUser(0.75,1.3);}
  else {pt_jet->GetXaxis()->SetRangeUser(50,750);pt_jet->GetYaxis()->SetRangeUser(0.75,1.5);}
  pt_jet->Draw("pe");pt_jet_TT->Draw("pesames");
  l.DrawLine(50,Znom,750,Znom);
  l.SetLineStyle(7);l.DrawLine(50,Znom-ZnomErr,750,Znom-ZnomErr);l.DrawLine(50,Znom+ZnomErr,750,Znom+ZnomErr);
  l1.DrawLine(50,TTnom,750,TTnom);
  l1.SetLineStyle(7);l1.DrawLine(50,TTnom-TTnomErr,750,TTnom-TTnomErr);l1.DrawLine(50,TTnom+TTnomErr,750,TTnom+TTnomErr);
  TLegend *leg = new TLegend(.6,.6,.9,.85);leg->SetFillStyle(0);
  leg->SetHeader(year);leg->AddEntry(pt_jet,"Z","l");leg->AddEntry(pt_jet_TT,"Jet-binned SF","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_jet1Pt.pdf");
  
  zpt->SetLineColor(kBlue);zpt->SetMarkerColor(kBlue);zpt_TT->SetLineColor(kRed);zpt_TT->SetMarkerColor(kRed);
  zpt->GetXaxis()->SetRangeUser(50,750);zpt->GetYaxis()->SetRangeUser(0.5,1.5);
  zpt->Draw("pe");//zpt_TT->Draw("pesames");
  l.DrawLine(0,Znom,1000,Znom);
  l.SetLineStyle(7);l.DrawLine(0,Znom-ZnomErr,1000,Znom-ZnomErr);l.DrawLine(0,Znom+ZnomErr,1000,Znom+ZnomErr);
  l1.DrawLine(0,1.152,1000,1.152);
  l1.SetLineStyle(7);l1.DrawLine(0,1.08,1000,1.08);l1.DrawLine(0,1.23,1000,1.23);
  //TLegend *leg = new TLegend(.7,.6,.9,.85);leg->SetFillStyle(0);
  //leg->SetHeader(year);leg->AddEntry(zpt,"Z","l");leg->AddEntry(zpt_TT,"tt","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_zPtReco4j.pdf");
  
  pt_jet2->SetLineColor(kBlue);pt_jet2->SetMarkerColor(kBlue);pt_jet2_TT->SetLineColor(kRed);pt_jet2_TT->SetMarkerColor(kRed);
  if(year=="2016"){pt_jet2->GetXaxis()->SetRangeUser(50,750);pt_jet2->GetYaxis()->SetRangeUser(0.75,1.3);}
  else {pt_jet2->GetXaxis()->SetRangeUser(50,750);pt_jet2->GetYaxis()->SetRangeUser(0.75,1.5);}
  pt_jet2->Draw("pe");pt_jet2_TT->Draw("pesames");
  l.DrawLine(50,Znom,750,Znom);
  l.SetLineStyle(7);l.DrawLine(50,Znom-ZnomErr,750,Znom-ZnomErr);l.DrawLine(50,Znom+ZnomErr,750,Znom+ZnomErr);
  l1.DrawLine(50,TTnom,750,TTnom);
  l1.SetLineStyle(7);l1.DrawLine(50,TTnom-TTnomErr,750,TTnom-TTnomErr);l1.DrawLine(50,TTnom+TTnomErr,750,TTnom+TTnomErr);
  //TLegend *leg = new TLegend(.7,.6,.9,.85);leg->SetFillStyle(0);
  //leg->SetHeader(year);leg->AddEntry(pt_jet2,"Z","l");leg->AddEntry(pt_jet2_TT,"tt","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_jet2Pt.pdf");
 
  pt_mu->SetLineColor(kBlue);pt_mu->SetMarkerColor(kBlue);pt_mu_TT->SetLineColor(kRed);pt_mu_TT->SetMarkerColor(kRed);
  if(year=="2016"){pt_mu->GetXaxis()->SetRangeUser(50,500);pt_mu->GetYaxis()->SetRangeUser(0.75,1.3);}
  else {pt_mu->GetXaxis()->SetRangeUser(50,500);pt_mu->GetYaxis()->SetRangeUser(0.75,1.5);}
  pt_mu->Draw("pe");pt_mu_TT->Draw("pesames");
  l.SetLineStyle(1);l.DrawLine(50,Znom,500,Znom);
  l.SetLineStyle(7);l.DrawLine(50,Znom-ZnomErr,500,Znom-ZnomErr);l.DrawLine(50,Znom+ZnomErr,500,Znom+ZnomErr);
  l1.SetLineStyle(1);l1.DrawLine(50,TTnom,500,TTnom);
  l1.SetLineStyle(7);l1.DrawLine(50,TTnom-TTnomErr,500,TTnom-TTnomErr);l1.DrawLine(50,TTnom+TTnomErr,500,TTnom+TTnomErr);
  //leg->AddEntry(pt_mu,"Z","l");leg->AddEntry(pt_mu_TT,"tt","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_mu1Pt.pdf");
  
  pt_mu2->SetLineColor(kBlue);pt_mu2->SetMarkerColor(kBlue);pt_mu2_TT->SetLineColor(kRed);pt_mu2_TT->SetMarkerColor(kRed);
  if(year=="2016"){pt_mu2->GetXaxis()->SetRangeUser(50,500);pt_mu2->GetYaxis()->SetRangeUser(0.5,1.3);}
  else {pt_mu2->GetXaxis()->SetRangeUser(50,500);pt_mu2->GetYaxis()->SetRangeUser(0.6,1.7);}
  pt_mu2->Draw("pe");pt_mu2_TT->Draw("pesames");
  l.SetLineStyle(1);l.DrawLine(50,Znom,500,Znom);
  l.SetLineStyle(7);l.DrawLine(50,Znom-ZnomErr,500,Znom-ZnomErr);l.DrawLine(50,Znom+ZnomErr,500,Znom+ZnomErr);
  l1.SetLineStyle(1);l1.DrawLine(50,TTnom,500,TTnom);
  l1.SetLineStyle(7);l1.DrawLine(50,TTnom-TTnomErr,500,TTnom-TTnomErr);l1.DrawLine(50,TTnom+TTnomErr,500,TTnom+TTnomErr);
  //leg->AddEntry(pt_mu,"Z","l");leg->AddEntry(pt_mu_TT,"tt","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_mu2Pt.pdf");

  st->SetLineColor(kBlue);st->SetMarkerColor(kBlue);st_TT->SetLineColor(kRed);st_TT->SetMarkerColor(kRed);
  if(year=="2016"){st->GetXaxis()->SetRangeUser(300,2000);st->GetYaxis()->SetRangeUser(0.75,1.3);}
  else {st->GetXaxis()->SetRangeUser(300,2000);st->GetYaxis()->SetRangeUser(0.75,1.5);}
  st->Draw("pe");st_TT->Draw("pesames");
  l.SetLineStyle(1);l.DrawLine(300,Znom,2000,Znom);
  l.SetLineStyle(7);l.DrawLine(300,Znom-ZnomErr,2000,Znom-ZnomErr);l.DrawLine(300,Znom+ZnomErr,2000,Znom+ZnomErr);
  l1.SetLineStyle(1);l1.DrawLine(300,TTnom,2000,TTnom);
  l1.SetLineStyle(7);l1.DrawLine(300,TTnom-TTnomErr,2000,TTnom-TTnomErr);l1.DrawLine(300,TTnom+TTnomErr,2000,TTnom+TTnomErr);
  //leg->AddEntry(st,"Z","l");leg->AddEntry(st_TT,"tt","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_ST.pdf");

  muj1->SetLineColor(kBlue);muj1->SetMarkerColor(kBlue);muj1_TT->SetLineColor(kRed);muj1_TT->SetMarkerColor(kRed);
  if(year=="2016"){muj1->GetXaxis()->SetRangeUser(300,2000);muj1->GetYaxis()->SetRangeUser(0.75,1.3);}
  else {muj1->GetXaxis()->SetRangeUser(300,2000);muj1->GetYaxis()->SetRangeUser(0.7,1.6);}
  muj1->Draw("pe");muj1_TT->Draw("pesames");muj1->Draw("pesames");
  l.SetLineStyle(1);l.DrawLine(300,Znom,2000,Znom);
  l.SetLineStyle(7);l.DrawLine(300,Znom-ZnomErr,2000,Znom-ZnomErr);l.DrawLine(300,Znom+ZnomErr,2000,Znom+ZnomErr);
  l1.SetLineStyle(1);l1.DrawLine(300,TTnom,2000,TTnom);
  l1.SetLineStyle(7);l1.DrawLine(300,TTnom-TTnomErr,2000,TTnom-TTnomErr);l1.DrawLine(300,TTnom+TTnomErr,2000,TTnom+TTnomErr);
  //leg->AddEntry(st,"Z","l");leg->AddEntry(st_TT,"tt","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_Muj1.pdf");

  muj2->SetLineColor(kBlue);muj2->SetMarkerColor(kBlue);muj2_TT->SetLineColor(kRed);muj2_TT->SetMarkerColor(kRed);
  if(year=="2016"){muj2->GetXaxis()->SetRangeUser(300,2000);muj2->GetYaxis()->SetRangeUser(0.75,1.3);}
  else {muj2->GetXaxis()->SetRangeUser(300,2000);muj2->GetYaxis()->SetRangeUser(0.7,1.6);}
  muj2->Draw("pe");muj2_TT->Draw("pesames");muj2->Draw("pesames");
  l.SetLineStyle(1);l.DrawLine(300,Znom,2000,Znom);
  l.SetLineStyle(7);l.DrawLine(300,Znom-ZnomErr,2000,Znom-ZnomErr);l.DrawLine(300,Znom+ZnomErr,2000,Znom+ZnomErr);
  l1.SetLineStyle(1);l1.DrawLine(300,TTnom,2000,TTnom);
  l1.SetLineStyle(7);l1.DrawLine(300,TTnom-TTnomErr,2000,TTnom-TTnomErr);l1.DrawLine(300,TTnom+TTnomErr,2000,TTnom+TTnomErr);
  //leg->AddEntry(st,"Z","l");leg->AddEntry(st_TT,"tt","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_Muj2.pdf");

  njet->SetLineColor(kBlue);njet->SetMarkerColor(kBlue);njet_TT->SetLineColor(kRed);njet_TT->SetMarkerColor(kRed);
  //njet->GetXaxis()->SetRangeUser(2,7);
  njet->GetYaxis()->SetRangeUser(0.8,3.3);
  njet->Draw("pe");njet_TT->Draw("pesames");njet->Draw("pesames");
  l.SetLineStyle(1);l.DrawLine(2,Znom,7,Znom);
  l.SetLineStyle(7);l.DrawLine(2,Znom-ZnomErr,7,Znom-ZnomErr);l.DrawLine(2,Znom+ZnomErr,7,Znom+ZnomErr);
  l1.SetLineStyle(1);l1.DrawLine(2,TTnom,7,TTnom);
  l1.SetLineStyle(7);l1.DrawLine(2,TTnom-TTnomErr,7,TTnom-TTnomErr);l1.DrawLine(2,TTnom+TTnomErr,7,TTnom+TTnomErr);
  //leg->AddEntry(st,"Z","l");leg->AddEntry(st_TT,"tt","l");
  leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_JetCount.pdf");
  
  /*
  TH1F* uujjSyst = new TH1F("uujjSyst","#mu#mu jj Systematics;M_{LQ};Total Systematic (%)",37,200,2100);
  TH1F* uvjjSyst = new TH1F("uvjjSyst","#mu#nu jj Systematics;M_{LQ};Total Systematic (%)",37,200,2100);

  float uujjSysts[37]={4.03,4.17,4.53,5.3,5.74,6.81,8.66,9.07,11.13,11.5,17.18,12.67,15.05,13.45,13.08,16.11,15.39,16.73,16.34,16.45,25.61,21.39,25.3,22.5,14.99,11.82,16.59,16.59,16.59,16.59,16.59,16.59,16.59,16.59,16.59,16.59,16.59};
  float uvjjSysts[37]={8.24,9.85,11.04,11.03,14.36,18.49,21.29,28.62,17.52,25.24,27.27,32.79,43.02,60.32,69.85,61.11,58.86,54.05,55.27,72.33,67.25,70.23,72.44,92.24,81.97,75.48,61.8,59.36,59.15,57.46,60.86,60.83,60.62,60.75,59.91,59.75,75.03};

  for(int i=0;i<37;i++){
    uujjSyst->SetBinContent(i,uujjSysts[i]);
    uvjjSyst->SetBinContent(i,uvjjSysts[i]);
  }

  uujjSyst->Draw("p");
  c1.Print("Results_Testing_v236_Vpt_19Sep/mumujjSysts.pdf");


  uvjjSyst->Draw("p");
  c1.Print("Results_Testing_v236_Vpt_19Sep/munujjSysts.pdf");
  */


return;
}
