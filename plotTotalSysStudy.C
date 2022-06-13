#include "TCanvas.h"
#include "TH1.h"

void sysVsLQMass(){
  gStyle->SetOptStat(0);
  TCanvas c1("c1","c1",800,600);

  Double_t lqmass[31] = {250.,350.,450.,550.,650.,750.,850.,950.,1050.,1150.,1250.,1350.,1450.,1550.,1650.,1750.,1850.,1950.,2050.,2150.,2250.,2350.,2450.,2550.,2650.,2750.,2850.,2950.,3050.,3950.,4050.};

  Float_t SigSysts2016[30] = {2.17,2.18,2.25,2.38,2.53,2.82,3.24,3.6,4.57,5.27,6.68,7.95,9.36,11.26,13.57,15.66,18.29,23.7,26.79,28.77,31.77,34.53,37.21,39.81,42.62,45.04,47.48,59.14,70.43};
  Float_t BkgSysts2016[30] = {3.42,4.5,5.35,4.18,5.06,7.79,11.55,6.62,16.59,8.03,11.05,10.43,13.73,14.6,13.12,45.63,18.28,20.8,18.06,20.41,21.24,20.66,16.42,13.34,12.8,40.25,16.4,22.81,13.12,32.27};

  Float_t SigSysts2017[30] = {2.64,2.5,2.51,2.54,2.57,2.62,2.7,2.79,2.92,3.09,3.36,3.62,4.02,4.47,4.94,5.6,6.23,6.99,7.68,8.51,9.12,9.78,10.53,11.3,12.05,12.58,13.29,13.79,16.5,18.9};
  Float_t BkgSysts2017[30] = {3.64,3.29,4.83,4.49,7.32,8.77,10.45,8.15,9.05,7.55,8.64,11.33,15.12,9.02,17.07,15.1,10.48,20.92,15.4,16.4,20.63,20.83,13.29,5.97,16.37,16.48,13.99,14.84,19.11,19.74};

  Float_t SigSysts2018[30] = {2.77,2.63,2.62,2.62,2.65,2.69,2.75,2.85,3.01,3.2,3.46,3.72,4.15,4.58,5.1,5.64,6.33,6.96,7.72,8.39,8.96,9.58,10.24,10.79,11.51,12.1,12.66,13.06,15.49,17.55};
  Float_t BkgSysts2018[30] = {5.23,4.85,6.12,7.47,8.11,12.92,13.89,10.33,7.82,9.83,28.2,8.64,38.32,17.83,10.24,13.81,16.28,10.97,9.19,15.42,11.08,9.26,14.42,7.04,17.78,21.04,15.33,13.77,0.0,0.0};

  TH1F* h_sig2016 = new TH1F("h_sig2016",";M_{LQ} [GeV];Total Systematic (%)",30,lqmass);
  TH1F* h_bkg2016 = new TH1F("h_bkg2016",";M_{LQ} [GeV];Total Systematic (%)",30,lqmass);

  TH1F* h_sig2017 = new TH1F("h_sig2017",";M_{LQ} [GeV];Total Systematic (%)",30,lqmass);
  TH1F* h_bkg2017 = new TH1F("h_bkg2017",";M_{LQ} [GeV];Total Systematic (%)",30,lqmass);

  TH1F* h_sig2018 = new TH1F("h_sig2018",";M_{LQ} [GeV];Total Systematic (%)",30,lqmass);
  TH1F* h_bkg2018 = new TH1F("h_bkg2018",";M_{LQ} [GeV];Total Systematic (%)",30,lqmass);

  h_sig2016->SetLineColor(kBlack);
  h_sig2016->SetMarkerColor(kBlack);
  h_sig2016->SetMarkerStyle(8);

  h_bkg2016->SetLineColor(kBlack);
  h_bkg2016->SetMarkerColor(kBlack);
  h_bkg2016->SetMarkerStyle(22);

  h_sig2017->SetLineColor(kBlue);
  h_sig2017->SetMarkerColor(kBlue);
  h_sig2017->SetMarkerStyle(8);

  h_bkg2017->SetLineColor(kBlue);
  h_bkg2017->SetMarkerColor(kBlue);
  h_bkg2017->SetMarkerStyle(22);

  h_sig2018->SetLineColor(kRed);
  h_sig2018->SetMarkerColor(kRed);
  h_sig2018->SetMarkerStyle(8);

  h_bkg2018->SetLineColor(kRed);
  h_bkg2018->SetMarkerColor(kRed);
  h_bkg2018->SetMarkerStyle(22);

  auto leg = new TLegend(0.4,0.7,0.65,0.85);
  leg->AddEntry(h_sig2016,"2016 Signal","p");
  leg->AddEntry(h_bkg2016,"2016 Background","p");
  leg->AddEntry(h_sig2017,"2017 Signal","p");
  leg->AddEntry(h_bkg2017,"2017 Background","p");
  leg->AddEntry(h_sig2018,"2018 Signal","p");
  leg->AddEntry(h_bkg2018,"2018 Background","p");
  leg->SetBorderSize(0);

  for(int i=0;i<30;i++){
    h_sig2016->SetBinContent(i+1,SigSysts2016[i]);
    h_bkg2016->SetBinContent(i+1,BkgSysts2016[i]);
    h_sig2017->SetBinContent(i+1,SigSysts2017[i]);
    h_bkg2017->SetBinContent(i+1,BkgSysts2017[i]);
    h_sig2018->SetBinContent(i+1,SigSysts2018[i]);
    h_bkg2018->SetBinContent(i+1,BkgSysts2018[i]);
  }

  h_sig2016->Draw("p");
  h_bkg2016->Draw("psame");
  h_sig2017->Draw("psame");
  h_bkg2017->Draw("psame");
  h_sig2018->Draw("psame");
  h_bkg2018->Draw("psame");

  h_sig2018->GetYaxis()->SetRangeUser(0.0,40.0);
  h_sig2018->GetXaxis()->SetRangeUser(200.0,4500.0);

  leg->Draw();

  c1.Print("TotalSysVsLQMass.pdf");

  return;
}
