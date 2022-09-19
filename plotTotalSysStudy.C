#include "TCanvas.h"
#include "TH1.h"

// To run:
// root -l
// gROOT->ProcessLine(".L plotTotalSysStudy.C");
// gROOT->ProcessLine("sysVsLQMass()");
// output is: TotalSysVsLQMass.pdf

void sysVsLQMass(){
  gStyle->SetOptStat(0);
  TCanvas c1("c1","c1",800,600);

  Double_t lqmass[31] = {250.,350.,450.,550.,650.,750.,850.,950.,1050.,1150.,1250.,1350.,1450.,1550.,1650.,1750.,1850.,1950.,2050.,2150.,2250.,2350.,2450.,2550.,2650.,2750.,2850.,2950.,3050.,3950.,4050.};

  // systematics copied from SystematicsAllYears.json (created in SysTableCombine.py)

  Float_t SigSysts2016[30] = {3.47,3.52,4.63,4.73,4.86,5.06,5.34,5.82,6.4,7.02,8.01,9.21,10.49,12.29,14.45,16.37,18.97,21.46,24.31,27.31,29.58,32.46,35.19,37.91,40.43,43.05,45.67,47.96,59.58,71.14};
  Float_t BkgSysts2016[30] = {6.4,6.27,7.08,8.99,11.68,10.14,8.55,6.07,9.5,9.79,13.54,9.38,16.02,14.99,15.66,22.76,16.59,20.11,28.08,18.16,20.58,20.33,27.14,37.53,30.5,33.3,34.63,36.89,0.0,50.61};

  Float_t SigSysts2017[30] = {4.68,4.31,5.14,5.17,5.21,5.27,5.36,5.56,5.68,5.83,6.04,6.28,6.58,6.94,7.34,7.91,8.44,9.08,9.72,10.42,11.03,11.69,12.37,13.07,13.72,14.25,14.93,15.42,18.07,20.49};
  Float_t BkgSysts2017[30] = {8.61,9.41,10.74,10.53,9.5,11.24,10.87,13.67,13.25,12.39,18.73,16.42,25.42,20.36,22.23,22.88,21.85,25.84,25.29,25.12,37.05,38.32,17.59,30.24,48.98,30.81,29.97,11.46,50.9,30.09};

  Float_t SigSysts2018[30] = {3.88,3.78,4.8,4.89,5.02,5.21,5.44,5.83,6.15,6.58,7.03,7.54,8.06,8.69,9.43,10.08,10.78,11.5,12.34,13.06,13.76,14.43,15.14,15.8,16.45,17.05,17.68,18.28,21.0,23.41};
  Float_t BkgSysts2018[30] = {7.69,6.82,6.79,6.85,7.81,7.59,9.18,15.41,10.19,9.33,15.84,11.88,10.55,16.13,16.11,16.76,37.59,18.42,27.04,0.0,0.0,49.64,30.4,31.86,0.0,0.0,0.0,22.92,29.55,61.24};

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
