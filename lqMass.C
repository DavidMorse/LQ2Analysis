#include <TCanvas>
#include <TH1>
#include <TF1>
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

void lqMass(){

  using namespace std;

  gStyle->SetOptStat(0);

  gStyle->SetPaintTextFormat("4.2f");
 
  TCanvas *c2 = new TCanvas("c2","",800,600);
  TCanvas *c1 = new TCanvas("c1","",1600,1400);
  c1->Divide(1,2);c1->cd(1);

  TFile _f("test13TeV/LQToCMu_M-1150_BetaOne_TuneCUETP8M1_13TeV-pythia8_tree.root","READ");
  //TFile _f("test13TeV/test13TeV__LQ2_M650_10kEvents_tree.root","READ");
  //TFile _f("test13TeV/test13TeV__file_CMu_M650_10kEvents_tree.root","READ");
  
  TTree* _t=(TTree*)_f.Get("PhysicalVariables");

  const int low=200,high=1500;const int nBins=high-low;

  TH1F* uujj1 = new TH1F("uujj1",";M_uujj1;",nBins,low,high);
  TH1F* uujj1_rel = new TH1F("uujj1_rel",";M_uujj1;",nBins,low,high);

  TH1F* uujj13 = new TH1F("uujj13",";M_uujj1;",nBins,low,high);
  TH1F* uujj13_rel = new TH1F("uujj13_rel",";M_uujj1;",nBins,low,high);

  TH1F* uujj2 = new TH1F("uujj2",";M_uujj2;",nBins,low,high);
  TH1F* uujj2_rel = new TH1F("uujj2_rel",";M_uujj2;",nBins,low,high);

  TH1F* uujj23 = new TH1F("uujj23",";M_uujj2;",nBins,low,high);
  TH1F* uujj23_rel = new TH1F("uujj23_rel",";M_uujj2;",nBins,low,high);

  TH1F* uujj1_gm = new TH1F("uujj1_gm",";M_uujj1;",nBins,low,high);
  TH1F* uujj2_gm = new TH1F("uujj2_gm",";M_uujj2;",nBins,low,high);

  uujj1->SetLineWidth(2);uujj13->SetLineWidth(2);uujj1_rel->SetLineWidth(2);uujj13_rel->SetLineWidth(2);uujj1_gm->SetLineWidth(2);
  uujj2->SetLineWidth(2);uujj23->SetLineWidth(2);uujj2_rel->SetLineWidth(2);uujj23_rel->SetLineWidth(2);uujj2_gm->SetLineWidth(2);
  uujj1->SetMarkerSize(1.5);uujj13->SetMarkerSize(1.5);uujj1_rel->SetMarkerSize(1.5);uujj13_rel->SetMarkerSize(1.5);uujj1_gm->SetMarkerSize(1.5);
  uujj2->SetMarkerSize(1.5);uujj23->SetMarkerSize(1.5);uujj2_rel->SetMarkerSize(1.5);uujj23_rel->SetMarkerSize(1.5);uujj2_gm->SetMarkerSize(1.5);

  //uujj1->SetLineColor(kBlue);uujj13->SetLineColor(kBlue);uujj1_rel->SetLineColor(kBlue);uujj13_rel->SetLineColor(kBlue);uujj1_gm->SetLineColor(kBlue);
  //uujj2->SetLineColor(kBlue);uujj23->SetLineColor(kBlue);uujj2_rel->SetLineColor(kBlue);uujj23_rel->SetLineColor(kBlue);uujj2_gm->SetLineColor(kBlue);

  TCut cut1 = "Pt_muon1>45";
  TCut cut2 = "Pt_muon2>45";
  TCut cut3 = "Pt_jet1>125";
  TCut cut4 = "Pt_jet2>45";
  TCut cut5 = "St_uujj>300";
  TCut cut6 = "M_uu>50";
  TCut cut7 = "abs(Eta_muon1)<2.1";
  TCut cut8 = "abs(Eta_muon2)<2.1";
  TCut cut9 = "DR_muon1muon2>0.3";
  TCut cut10= "abs(Eta_jet1)<2.4";
  TCut cut11= "abs(Eta_jet2)<2.4";
  TCut cuts = cut1 && cut2 && cut3 && cut4 && cut5 && cut6 && cut7 && cut8 && cut9 && cut10 && cut11;

  _t->Draw("M_uujj1>>uujj1",cuts);  
  _t->Draw("M_uujj2>>uujj2",cuts); 
  _t->Draw("M_uujj1_genMatched>>uujj1_gm",cuts);   
  _t->Draw("M_uujj2_genMatched>>uujj2_gm",cuts); 
  _t->Draw("M_uujj1_3jet>>uujj13",cuts);   
  _t->Draw("M_uujj2_3jet>>uujj23",cuts); 
  _t->Draw("M_uujj1_rel>>uujj1_rel",cuts);   
  _t->Draw("M_uujj2_rel>>uujj2_rel",cuts); 
  _t->Draw("M_uujj1_3jet_rel>>uujj13_rel",cuts);   
  _t->Draw("M_uujj2_3jet_rel>>uujj23_rel",cuts); 

  uujj1_gm->SetLineColor(kRed);uujj1->SetLineColor(kBlue);uujj1_rel->SetLineColor(kOrange);uujj13->SetLineColor(kGreen);uujj13_rel->SetLineColor(kViolet);
  uujj1_gm->SetMarkerColor(kRed);uujj1->SetMarkerColor(kBlue);uujj1_rel->SetMarkerColor(kOrange);uujj13->SetMarkerColor(kGreen);uujj13_rel->SetMarkerColor(kViolet);

  const int rebin=(high-low)/50;
  uujj1_gm->Rebin(rebin);uujj1->Rebin(rebin);uujj1_rel->Rebin(rebin);uujj13->Rebin(rebin);uujj13_rel->Rebin(rebin);
    
  int binlow = uujj1_gm->FindBin(1100.01),binhigh = uujj1_gm->FindBin(1999.9);

  std::cout<<"gm      : "<<uujj1_gm->Integral(binlow,binhigh)<<"  "<<uujj1_gm->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh)<<"%"<<std::endl
	   <<"normal  : "<<uujj1->Integral(binlow,binhigh)<<"  "<<uujj1->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh)<<"%"<<std::endl
	   <<"norm rel: "<<uujj1_rel->Integral(binlow,binhigh)<<"  "<<uujj1_rel->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh)<<"%"<<std::endl
	   <<"3jet    : "<<uujj13->Integral(binlow,binhigh)<<"  "<<uujj13->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh)<<"%"<<std::endl
	   <<"3jet rel: "<<uujj13_rel->Integral(binlow,binhigh)<<"  "<<uujj13_rel->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh)<<"%"<<std::endl;
  
  /*
  Double_t par[9];
  TF1 *g1    = new TF1("g1","gaus",0,550);
  TF1 *g2    = new TF1("g2","gaus",400,1000);
  TF1 *total = new TF1("total","gaus(0)+gaus(3)",0,1000);

  uujj13_rel->Fit(g1,"R");
  uujj13_rel->Fit(g2,"R+");
  g1->GetParameters(&par[0]);
  g2->GetParameters(&par[3]);
  total->SetParameters(par);
  uujj13_rel->Fit(total,"R+");
  */
  //uujj1_rel->Fit("gaus");

  c1->cd(1);
  uujj1_gm->Draw();
  uujj1->Draw("SAMES");
  uujj1_rel->Draw("SAMES");
  uujj13->Draw("SAMES");uujj13_rel->Draw("SAMES");

  leg = new TLegend(.23,.5,.53,.8);
  leg->SetFillStyle(0);leg->SetBorderSize(0);
  leg->AddEntry(uujj1_gm,"genMatched","l");
  leg->AddEntry(uujj1,"2 jet","l");
  leg->AddEntry(uujj1_rel,"2 jet, relative","l");
  leg->AddEntry(uujj13,"3 jet","l");
  leg->AddEntry(uujj13_rel,"3 jet, relative","l");
  leg->Draw();


  //c1->Print("uujj1_genMatched_vs_normal.pdf");

  c1->cd(2);

  TH1F* h_uujj1_gm = (TH1F*)uujj1_gm->Clone();
  TH1F* h_uujj1 = (TH1F*)uujj1->Clone();
  TH1F* h_uujj1_rel = (TH1F*)uujj1_rel->Clone();
  TH1F* h_uujj13 = (TH1F*)uujj13->Clone();
  TH1F* h_uujj13_rel = (TH1F*)uujj13_rel->Clone();


  h_uujj1_gm->Sumw2();
  h_uujj1->Sumw2();
  h_uujj1_rel->Sumw2();
  h_uujj13->Sumw2();
  h_uujj13_rel->Sumw2();
  
  h_uujj1->GetYaxis()->SetRangeUser(-0.5,8);
  /*
  h_uujj1_gm->Rebin(nBins/rebin);
  h_uujj1->Rebin(nBins/rebin);
  h_uujj1_rel->Rebin(nBins/rebin);
  h_uujj13->Rebin(nBins/rebin);
  h_uujj13_rel->Rebin(nBins/rebin);
  */
  h_uujj1->Divide(h_uujj1_gm);
  h_uujj1_rel->Divide(h_uujj1_gm);
  h_uujj13->Divide(h_uujj1_gm);
  h_uujj13_rel->Divide(h_uujj1_gm);
  h_uujj1->Draw("P");h_uujj1_rel->Draw("PSAMES");h_uujj13->Draw("PSAMES");h_uujj13_rel->Draw("PSAMES");

  leg2 = new TLegend(.47,.5,.77,.8);
  leg2->SetFillStyle(0);leg2->SetBorderSize(0);
  leg2->AddEntry(h_uujj1,"2 jet","l");
  leg2->AddEntry(h_uujj1_rel,"2 jet, relative","l");
  leg2->AddEntry(h_uujj13,"3 jet","l");
  leg2->AddEntry(h_uujj13_rel,"3 jet, relative","l");

  leg2->Draw();
  //c1->Print("uujj1_genMatched_vs_normal_ratio.pdf");


  const char* str[5] = {"genMatched","2 Jet","2 Jet, relative","3 Jet","3 Jet, relative"};
  TH1F* rats = new TH1F("rats","Ratio to genMatched with 550<M_{LQ}<750 and preselection cuts;;ratio",5,0,5);
  rats->GetXaxis()->SetBinLabel(1,str[0]);
  rats->GetXaxis()->SetBinLabel(2,str[1]);
  rats->GetXaxis()->SetBinLabel(3,str[2]);
  rats->GetXaxis()->SetBinLabel(4,str[3]);
  rats->GetXaxis()->SetBinLabel(5,str[4]);
  rats->SetBinContent(1,1);rats->SetBinError(1,0);
  float theint = uujj1->Integral(binlow,binhigh);float err = theint/uujj1_gm->Integral(binlow,binhigh) * sqrt(1./theint + 1./uujj1_gm->Integral(binlow,binhigh));
  std::cout<<"here: "<<uujj1_rel->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh)<<std::endl;
  rats->SetBinContent(2,uujj1->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh));rats->SetBinError(2,err);
  theint = uujj1_rel->Integral(binlow,binhigh);err = theint/uujj1_gm->Integral(binlow,binhigh) * sqrt(1./theint + 1./uujj1_gm->Integral(binlow,binhigh));
  rats->SetBinContent(3,uujj1_rel->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh));rats->SetBinError(3,err);
  theint = uujj13->Integral(binlow,binhigh);err = theint/uujj1_gm->Integral(binlow,binhigh) * sqrt(1./theint + 1./uujj1_gm->Integral(binlow,binhigh));
  rats->SetBinContent(4,uujj13->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh));rats->SetBinError(4,err);
  theint = uujj13_rel->Integral(binlow,binhigh);err = theint/uujj1_gm->Integral(binlow,binhigh) * sqrt(1./theint + 1./uujj1_gm->Integral(binlow,binhigh));
  rats->SetBinContent(5,uujj13_rel->Integral(binlow,binhigh)/uujj1_gm->Integral(binlow,binhigh));rats->SetBinError(5,err);
  
  //rats->GetYaxis()->SetRangeUser(0.4,1.05);
  rats->Draw();//leg2->Draw();
  c1->Print("uujj1_genMatched_vs_normal_ratio.pdf");

  c2->cd();

  const int ind=7;
  TH1F* muI = new TH1F("muI",";Index;",ind,0,ind);
  TH1F* jetI = new TH1F("jetI",";Index;",ind,0,ind);
  TH1F* muI2 = new TH1F("muI2",";Index;",ind,0,ind);
  TH1F* jetI2 = new TH1F("jetI2",";Index;",ind,0,ind);

  muI->SetLineWidth(2);muI2->SetLineWidth(2);
  jetI->SetLineWidth(2);jetI2->SetLineWidth(2);
  muI->SetLineColor(kRed);muI2->SetLineColor(kBlue);
  jetI->SetLineColor(kGreen);jetI2->SetLineColor(kOrange);

  _t->Draw("muonIndex1>>muI",cuts);  
  _t->Draw("jetIndex1>>jetI",cuts);  
  _t->Draw("muonIndex2>>muI2",cuts);  
  _t->Draw("jetIndex2>>jetI2",cuts);  

  //c2->SetLogy(1);
  muI2->Draw();
  muI->Draw("SAMES");
  jetI->Draw("SAMES");
  jetI2->Draw("SAMES");

  leg3 = new TLegend(.47,.5,.77,.8);
  leg3->SetFillStyle(0);leg3->SetBorderSize(0);
  leg3->AddEntry(muI,"muon1 index","l");
  leg3->AddEntry(muI2,"muon2 index","l");
  leg3->AddEntry(jetI,"jet1 index","l");
  leg3->AddEntry(jetI2,"jet2 index","l");
  leg3->Draw();
  c2->Print("indices.pdf");
  return;

}
