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
  TH1F* mujmin = new TH1F("mujmin",";[GeV];#mu#mu SFs",3,binsMuujj2);
  TH1F* munuW = new TH1F("munuW",";S_{T} [GeV];#mu#nujj SF",3,binsMuNu);
  TH1F* munuTT = new TH1F("munuTT",";S_{T} [GeV];#mu#nujj SFs",3,binsMuNu);
  TH1F* pt = new TH1F("pt",";S_{T} [GeV];Z+Jets SF (Pt-binned)",4,bins);
  TH1F* pt_jet = new TH1F("pt_jet",";Leading Jet Pt [GeV];Z / tt Normalization SF",4,binsJetPt);
  TH1F* pt_jet_TT = new TH1F("pt_jet_TT",";Leading Jet Pt [GeV];Z / tt Normalization SF",4,binsJetPt);
  TH1F* pt_mu = new TH1F("pt_mu",";Leading Muon Pt [GeV];Z / tt Normalization SF",5,binsMuonPt);
  TH1F* pt_mu_TT = new TH1F("pt_mu_TT",";Leading Muon Pt [GeV];Z / tt Normalization SF",5,binsMuonPt);
  TH1F* st = new TH1F("st",";S_T [GeV];Z / tt Normalization SF",4,bins);
  TH1F* st_TT = new TH1F("st_TT",";S_T [GeV];Z / tt Normalization SF",4,bins);
  TString year = "2016-2018_ttReweight";


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
  /*
  Double_t Znom = 1.02;
  Double_t ZnomErr = 0.017;
  Double_t TTnom = 0.961;
  Double_t TTnomErr = 0.014; 
  Float_t Sts[4]={.974,1.046,1.068,1.037};
  Float_t StErrs[4]={.028,.025,.052,.059};
  Float_t Sts_TT[4]={.944,.994,.886,.844};
  Float_t StErrs_TT[4]={.02,.023,.06,.124};
  Float_t PtJet_Z[4]={.996,1.0,1.055,1.112};Float_t PtJetErr_Z[4]={.048,.024,.026,.059};
  Float_t PtJet_TT[4]={.907,.983,.979,.782};Float_t PtJetErr_TT[4]={.026,.018,.041,.096};
  Float_t PtMu_Z[5]={1.059,.984,.99,1.078,1.045};Float_t PtMuErr_Z[5]={.043,.036,.027,.046,.038};
  Float_t PtMu_TT[5]={.989,.956,.957,.949,.786};Float_t PtMuErr_TT[5]={.028,.023,.023,.057,.119};
  */
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
  //2016-2018 combination, TTBar pt Reweighting
  Double_t Znom = 1.241;
  Double_t ZnomErr = 0.0102;
  Double_t TTnom = 1.034;
  Double_t TTnomErr = 0.007;
  Float_t Sts[4]={1.22838967805,1.24124977737,1.28090142115,1.26891982969};Float_t StErrs[4]={0.01514,0.01666,0.02721,0.04184};
  Float_t Sts_TT[4]={1.01952899021,1.05366814854,1.06376510379,0.92708767826};Float_t StErrs_TT[4]={0.00785,0.01147,0.04274,0.08344};
  Float_t PtJet_Z[4]={1.27209290362,1.22253389771,1.25399669577,1.25538280632};Float_t PtJetErr_Z[4]={0.03444,0.0152,0.01855,0.04485};
  Float_t PtJet_TT[4]={0.987463457348,1.04813692128,1.04896967437,0.974053335592};Float_t PtJetErr_TT[4]={0.01477,0.00902,0.01684,0.05499};
  Float_t PtMu_Z[5]={1.22429724,1.20838160849,1.23057433049,1.29437076004,1.31436698107};Float_t PtMuErr_Z[5]={0.02128,0.01673,0.01562,0.0276,0.03032};
  Float_t PtMu_TT[5]={1.06186983501,1.03225472236,1.01536557067,1.01262441084,0.961561449663};Float_t PtMuErr_TT[5]={0.01222,0.01051,0.01354,0.03322,0.07606};
  

  pt_jet->SetBinContent(1,PtJet_Z[0]);pt_jet->SetBinError(1,PtJetErr_Z[0]);
  pt_jet->SetBinContent(2,PtJet_Z[1]);pt_jet->SetBinError(2,PtJetErr_Z[1]);
  pt_jet->SetBinContent(3,PtJet_Z[2]);pt_jet->SetBinError(3,PtJetErr_Z[2]);
  pt_jet->SetBinContent(4,PtJet_Z[3]);pt_jet->SetBinError(4,PtJetErr_Z[3]);

  pt_jet_TT->SetBinContent(1,PtJet_TT[0]);pt_jet_TT->SetBinError(1,PtJetErr_TT[0]);
  pt_jet_TT->SetBinContent(2,PtJet_TT[1]);pt_jet_TT->SetBinError(2,PtJetErr_TT[1]);
  pt_jet_TT->SetBinContent(3,PtJet_TT[2]);pt_jet_TT->SetBinError(3,PtJetErr_TT[2]);
  pt_jet_TT->SetBinContent(4,PtJet_TT[3]);pt_jet_TT->SetBinError(4,PtJetErr_TT[3]);

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
  TLegend *leg = new TLegend(.7,.6,.9,.85);leg->SetFillStyle(0);
  leg->SetHeader(year);leg->AddEntry(pt_jet,"Z","l");leg->AddEntry(pt_jet_TT,"tt","l");leg->Draw();
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_jetPt.pdf");
 
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
  c1.Print("Results_SFstudyPlots/"+year+"/mumuScaleFactors_muPt.pdf");

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
