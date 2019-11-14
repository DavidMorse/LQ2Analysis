#include "TCanvas.h"
#include "TH1.h"

void zplot(){
  gStyle->SetOptStat(0);
  TCanvas c1("c1","c1",800,600);c1.cd();

  Double_t bins[]={300,500,750,1250,2000};
  Double_t binsMuujj2[]={0,250,750,2000};
  Double_t binsMuNu[]={300,500,750,2000};
  TH1F* mujmin = new TH1F("mujmin",";[GeV];#mu#mu Scale Factors",3,binsMuujj2);
  TH1F* munuW = new TH1F("munuW",";S_{T} [GeV];#mu#nujj SF",3,binsMuNu);
  TH1F* munuTT = new TH1F("munuTT",";S_{T} [GeV];#mu#nujj Scale Factors",3,binsMuNu);
  TH1F* pt = new TH1F("pt",";S_{T} [GeV];Z+Jets SF (Pt-binned)",4,bins);


  Double_t Znom = 0.956;
  Double_t ZnomErr = 0.006;
  Double_t Wnom_uvjj = 0.926;
  Double_t WnomErr_uvjj = 0.01;
  Double_t TTnom_uvjj = 1.022;
  Double_t TTnomErr_uvjj = 0.008;


  Float_t Sts_uujj[4]={0.978,0.924,0.904,0.905};
  Float_t StErrs_uujj[4]={0.007,0.01,0.016,0.048};
  Float_t Mujs_uujj[3]={0.969,0.92,0.82};
  Float_t MujErrs_uujj[3]={.007,.01,.102};
  Float_t Ws_uvjj[3]={0.929,0.92,.903};
  Float_t WErrs_uvjj[3]={.011,.022,.06};
  Float_t TTs_uvjj[3]={1.017,1.048,1.095};
  Float_t TTErrs_uvjj[3]={0.009,.025,.089};



  //corrected vjets xsecs
  pt->SetBinContent(1,Sts_uujj[0]);
  pt->SetBinError(1,StErrs_uujj[0]);
  pt->SetBinContent(2,Sts_uujj[1]);
  pt->SetBinError(2,StErrs_uujj[1]);
  pt->SetBinContent(3,Sts_uujj[2]);
  pt->SetBinError(3,StErrs_uujj[2]);
  pt->SetBinContent(4,Sts_uujj[3]);
  pt->SetBinError(4,StErrs_uujj[3]);

  mujmin->SetBinContent(1,Mujs_uujj[0]);
  mujmin->SetBinError(1,MujErrs_uujj[0]);
  mujmin->SetBinContent(2,Mujs_uujj[1]);
  mujmin->SetBinError(2,MujErrs_uujj[1]);
  mujmin->SetBinContent(3,Mujs_uujj[2]);
  mujmin->SetBinError(3,MujErrs_uujj[2]);

  munuW->SetBinContent(1,Ws_uvjj[0]);
  munuW->SetBinError(1,WErrs_uvjj[0]);
  munuW->SetBinContent(2,Ws_uvjj[1]);
  munuW->SetBinError(2,WErrs_uvjj[1]);
  munuW->SetBinContent(3,Ws_uvjj[2]);
  munuW->SetBinError(3,WErrs_uvjj[2]);

  munuTT->SetBinContent(1,TTs_uvjj[0]);
  munuTT->SetBinError(1,TTErrs_uvjj[0]);
  munuTT->SetBinContent(2,TTs_uvjj[1]);
  munuTT->SetBinError(2,TTErrs_uvjj[1]);
  munuTT->SetBinContent(3,TTs_uvjj[2]);
  munuTT->SetBinError(3,TTErrs_uvjj[2]);

  TLine l,l1;
  l.SetLineColor(kBlue);l1.SetLineColor(kRed);
  munuW->SetLineColor(kBlue);munuW->SetMarkerColor(kBlue);
  munuTT->SetLineColor(kRed);munuTT->SetMarkerColor(kRed);
  pt->SetLineColor(kBlue);pt->SetMarkerColor(kBlue);
  mujmin->SetLineColor(kRed);mujmin->SetMarkerColor(kRed);

  munuW->GetYaxis()->SetRangeUser(.8,1.2);
  munuTT->GetYaxis()->SetRangeUser(.8,1.2);
  mujmin->GetYaxis()->SetRangeUser(.7,1.);

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



return;
}
