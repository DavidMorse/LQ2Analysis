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

  Double_t lqmass[29] = {250.,350.,450.,550.,650.,750.,850.,950.,1050.,1150.,1250.,1350.,1450.,1550.,1650.,1750.,1850.,1950.,2050.,2150.,2250.,2350.,2450.,2550.,2650.,2750.,2850.,2950.,3050.};

  // total systematics - 06/29/2023
  Float_t SigSysts2016[28] = {2.54,2.53,2.64,2.81,3.02,3.33,3.74,4.27,5.03,5.81,6.99,8.34,9.76,11.67,13.95,15.94,18.6,21.15,24.03,27.08,29.37,32.27,35.02,37.77,40.32,42.96,45.62,47.95};
  Float_t BkgSysts2016[28] = {3.63,3.62,3.74,4.46,5.37,6.4,7.37,8.59,10.14,11.5,11.93,12.33,14.15,15.03,14.69,16.56,19.18,20.82,26.33,26.15,28.75,38.14,41.09,43.29,46.36,47.1,51.06,54.72};
  
  Float_t SigSysts2017[28] = {4.04,3.54,3.46,3.49,3.56,3.64,3.77,3.91,4.09,4.3,4.58,4.93,5.33,5.79,6.29,6.97,7.58,8.31,9.0,9.77,10.44,11.16,11.91,12.68,13.41,14.03,14.78,15.37};
  Float_t BkgSysts2017[28] = {4.94,4.97,5.2,5.6,6.11,7.21,8.72,10.15,11.33,12.76,14.17,14.18,14.91,17.39,17.26,20.45,20.77,24.17,33.73,30.81,34.52,43.58,44.52,45.03,45.95,46.58,49.63,54.31};
  
  Float_t SigSysts2018[28] = {3.07,2.88,2.92,3.07,3.27,3.55,3.88,4.29,4.71,5.27,5.84,6.46,7.08,7.8,8.64,9.36,10.12,10.9,11.79,12.54,13.29,14.0,14.77,15.48,16.19,16.86,17.56,18.25};
  Float_t BkgSysts2018[28] = {4.15,4.18,4.36,4.72,5.33,6.46,7.89,9.63,10.77,11.95,13.55,14.56,16.3,17.61,18.76,20.42,23.24,24.9,29.29,31.32,33.4,41.53,43.87,44.73,53.01,59.58,50.93,52.4};


  TH1F* h_sig2016 = new TH1F("h_sig2016",";M_{LQ} [GeV];Total Systematic (%)",28,lqmass);
  TH1F* h_bkg2016 = new TH1F("h_bkg2016",";M_{LQ} [GeV];Total Systematic (%)",28,lqmass);

  TH1F* h_sig2017 = new TH1F("h_sig2017",";M_{LQ} [GeV];Total Systematic (%)",28,lqmass);
  TH1F* h_bkg2017 = new TH1F("h_bkg2017",";M_{LQ} [GeV];Total Systematic (%)",28,lqmass);

  TH1F* h_sig2018 = new TH1F("h_sig2018",";M_{LQ} [GeV];Total Systematic (%)",28,lqmass);
  TH1F* h_bkg2018 = new TH1F("h_bkg2018",";M_{LQ} [GeV];Total Systematic (%)",28,lqmass);

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

  for(int i=0;i<28;i++){
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

  h_sig2018->GetYaxis()->SetRangeUser(0.0,15.0);
  h_sig2018->GetXaxis()->SetRangeUser(200.0,4500.0);

  leg->Draw();

  c1.Print("TotalSysVsLQMass.pdf");

  return;
}
