#include "TROOT.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TH2F.h"
#include "TGraph.h"
#include "TF1.h"
#include "TLegend.h"
#include "TPolyLine.h"
#include "TPad.h"
#include "TLatex.h"
#include "TMath.h"
#include "stdio.h"
using namespace std;
void myStyle();
void setTDRStyle();
void makePlotsBOVector()
{

 // filename for the final plot (NB: changing the name extension changes the file format)
 string fileName2 = "BR_Sigma_MuMuVector.pdf";
 string fileName3 = "BR_Sigma_MuMuVector.png";
 string fileName1 = "BR_Sigma_MuMuVector.eps";

 // axes labels for the final plot
 string title = ";M_{LQ} (GeV);#sigma#times#beta^{2} (pb)";

 // integrated luminosity
 string lint = "19.7 fb^{-1}";


Double_t mTh[16] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 }; 
Double_t mData[16] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 }; 
Double_t MCx_shademasses[32] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 , 1800.0 , 1700.0 , 1600.0 , 1500.0 , 1400.0 , 1300.0 , 1200.0 , 1100.0 , 1000.0 , 900.0 , 800.0 , 700.0 , 600.0 , 500.0 , 400.0 , 300.0 }; 


Double_t YMxsTh[16] = {104.6,17.74,4.03,1.125,0.3519,0.1194,0.04373,0.01731,0.006853,0.002832,0.001203,0.0005089,0.0002236,9.675E-05,4.159E-05,1.794E-05};
Double_t MCxsTh[16] = {21.19,3.354,0.7378,0.2034,0.06362,0.02177,0.008059,0.003231,0.001298,0.0005442,0.0002344,0.0001006,4.478E-05,1.96E-05,8.518E-06,3.711E-06};
Double_t MMxsTh[16] = {2510,242.9,40.14,9.204,2.528,0.7827,0.2678,0.1006,0.03822,0.01528,0.006316,0.002614,0.001128,0.0004799,0.0002037,8.697E-05};
Double_t AMxsTh[16] = {20.06,2.956,0.5897,0.1458,0.04056,0.01228,0.004027,0.001431,0.0005108,0.0001909,7.373E-05,2.849E-05,1.148E-05,4.578E-06,1.829E-06,7.371E-07};



// Insert limit information below

Double_t MCxsUp_expected[16] = {0.01503839467 , 0.005022604938 , 0.0026718512128 , 0.0014719260672 , 0.000933003205 , 0.00056899140907 , 0.000338587876406 , 0.00024399135594 , 0.000232718338226 , 0.000229119960162 , 0.000224006546952 , 0.000221992709584 , 0.000222843742615 , 0.00021687167397 , 0.0002195750371 , 0.000219359066747 }; 
Double_t MCxsUp_observed[16] = {0.0224917017 , 0.005349569628 , 0.0021869255226 , 0.0014595127686 , 0.0006520964113 , 0.00083868485246 , 0.000501884629169 , 0.000195036287553 , 0.00018691863278 , 0.000182725857679 , 0.000179993854562 , 0.000177461132296 , 0.000178983363726 , 0.000174174610826 , 0.000175495107237 , 0.000175687111222 }; 
Double_t MCy_1sigma[32]={0.01088617179 , 0.003596775936 , 0.0019069591968 , 0.0010380362382 , 0.00065458000886 , 0.00038867248014 , 0.000218816855858 , 0.000146781635346 , 0.000139999957878 , 0.000137244373154 , 0.00013475906808 , 0.000133547565857 , 0.000134059542054 , 0.00013046682721 , 0.000131575486944 , 0.000131963207564 , 0.000378495244514 , 0.000378867898614 , 0.000377661204519 , 0.000388060976753 , 0.000383039501329 , 0.000390085897146 , 0.000395337282821 , 0.000405256656156 , 0.000420997277394 , 0.000541031769681 , 0.00085703049677 , 0.00135324912306 , 0.0020997122346 , 0.0037688122528 , 0.007084694448 , 0.0209728025 }; 
Double_t MCy_2sigma[32]={0.00813600645 , 0.002697685926 , 0.0014246394162 , 0.0007733361564 , 0.0004847242791 , 0.0002822730855 , 0.00015276132683 , 9.673875711e-05 , 9.2269189276e-05 , 8.99474842308e-05 , 8.8815094084e-05 , 8.80166412466e-05 , 8.8354059733e-05 , 8.59862297056e-05 , 8.70580727119e-05 , 8.69724430043e-05 , 0.000628716707198 , 0.000624822776581 , 0.000622046685798 , 0.000639176189857 , 0.00063170249431 , 0.000642511398021 , 0.000651983817184 , 0.000667499182966 , 0.000694301848524 , 0.000842567700513 , 0.00124928348881 , 0.00190390668898 , 0.0028886849694 , 0.0051130144996 , 0.0096115578 , 0.02803235695 }; 


Double_t YMxsUp_observed[16] = {0.0246214802 , 0.00560520136 , 0.00226700799 , 0.001502821125 , 0.0006680832057 , 0.0008444280828 , 0.00050466505921 , 0.00019354260801 , 0.000185063366719 , 0.000181115224512 , 0.000179223347817 , 0.000180467267605 , 0.000176141854772 , 0.000175374453487 , 0.000175860340192 , 0.000173710210793 }; 
Double_t MMxsUp_observed[16] = {0.02081292 , 0.0050144276 , 0.00210080718 , 0.001408773444 , 0.00064701632 , 0.0008187018519 , 0.0004965724348 , 0.0001923861322 , 0.00018532579884 , 0.00018327907712 , 0.00017911174914 , 0.000177300854968 , 0.000176156230488 , 0.000175184522979 , 0.000175274344543 , 0.000175298392083 }; 
Double_t AMxsUp_observed[16] = {0.0221659991 , 0.00519256872 , 0.0021462951183 , 0.0014349675366 , 0.0006444718332 , 0.0008197058412 , 0.000498776915022 , 0.000193865896989 , 0.00018776264786 , 0.000182337121321 , 0.000179475959276 , 0.000178213586259 , 0.000178298192531 , 0.000176073975401 , 0.00017971543089 , 0.00017788406583 }; 



  // turn on/off batch mode
 gROOT->SetBatch(kTRUE);


 // set ROOT style
//  myStyle();
 setTDRStyle();
 gStyle->SetPadLeftMargin(0.14);
 gROOT->ForceStyle();
 
 TCanvas *c = new TCanvas("c","",800,800);
 c->cd();
 
 TH2F *bg = new TH2F("bg",title.c_str(), 500, 300., 1800., 500., 0.0000005, 6000.);
 bg->GetXaxis()->CenterTitle();
 bg->GetYaxis()->CenterTitle();
 bg->SetStats(kFALSE);
 bg->SetTitleOffset(1.,"X");
 bg->SetTitleOffset(1.15,"Y");
 
 bg->Draw();



TGraph *MCxsTh_vs_m = new TGraph(16, mTh, MCxsTh);
MCxsTh_vs_m->SetLineWidth(3);
MCxsTh_vs_m->SetLineColor(2);
MCxsTh_vs_m->SetLineStyle(5);
MCxsTh_vs_m->SetFillColor(0);
MCxsTh_vs_m->SetMarkerSize(0.00001);
MCxsTh_vs_m->SetMarkerStyle(22);
MCxsTh_vs_m->SetMarkerColor(kBlue);

TGraph *MMxsTh_vs_m = new TGraph(16, mTh, MMxsTh);
MMxsTh_vs_m->SetLineWidth(3);
MMxsTh_vs_m->SetLineColor(4);
MMxsTh_vs_m->SetLineStyle(2);
MMxsTh_vs_m->SetFillColor(0);
MMxsTh_vs_m->SetMarkerSize(0.00001);
MMxsTh_vs_m->SetMarkerStyle(22);
MMxsTh_vs_m->SetMarkerColor(kBlue);

TGraph *YMxsTh_vs_m = new TGraph(16, mTh, YMxsTh);
YMxsTh_vs_m->SetLineWidth(3);
YMxsTh_vs_m->SetLineColor(6);
YMxsTh_vs_m->SetLineStyle(3);
YMxsTh_vs_m->SetFillColor(0);
YMxsTh_vs_m->SetMarkerSize(0.00001);
YMxsTh_vs_m->SetMarkerStyle(22);
YMxsTh_vs_m->SetMarkerColor(kBlue);

TGraph *AMxsTh_vs_m = new TGraph(16, mTh, AMxsTh);
AMxsTh_vs_m->SetLineWidth(3);
AMxsTh_vs_m->SetLineColor(8);
AMxsTh_vs_m->SetLineStyle(4);
AMxsTh_vs_m->SetFillColor(0);
AMxsTh_vs_m->SetMarkerSize(0.00001);
AMxsTh_vs_m->SetMarkerStyle(22);
AMxsTh_vs_m->SetMarkerColor(kBlue);


TGraph *MCxsData_vs_m_expected = new TGraph(16, mData, MCxsUp_expected);
MCxsData_vs_m_expected->SetMarkerStyle(0);
MCxsData_vs_m_expected->SetMarkerColor(kBlack);
MCxsData_vs_m_expected->SetLineColor(kBlack);
MCxsData_vs_m_expected->SetLineWidth(2);
MCxsData_vs_m_expected->SetLineStyle(7);
MCxsData_vs_m_expected->SetMarkerSize(0.001);

TGraph *MCxsData_vs_m_observed = new TGraph(16, mData, MCxsUp_observed);
MCxsData_vs_m_observed->SetMarkerStyle(21);
MCxsData_vs_m_observed->SetMarkerColor(kBlack);
MCxsData_vs_m_observed->SetLineColor(kBlack);
MCxsData_vs_m_observed->SetLineWidth(2);
MCxsData_vs_m_observed->SetLineStyle(1);
MCxsData_vs_m_observed->SetMarkerSize(1);


 TGraph *MCexshade1 = new TGraph(32,MCx_shademasses,MCy_1sigma);
 MCexshade1->SetFillColor(kGreen);
 TGraph *MCexshade2 = new TGraph(32,MCx_shademasses,MCy_2sigma);
 MCexshade2->SetFillColor(kYellow);



TGraph *YMxsData_vs_m_observed = new TGraph(16, mData, YMxsUp_observed);
YMxsData_vs_m_observed->SetMarkerStyle(5);
YMxsData_vs_m_observed->SetMarkerColor(6);
YMxsData_vs_m_observed->SetLineColor(6);
YMxsData_vs_m_observed->SetLineWidth(2);
YMxsData_vs_m_observed->SetLineStyle(1);
YMxsData_vs_m_observed->SetMarkerSize(2);


TGraph *AMxsData_vs_m_observed = new TGraph(16, mData, AMxsUp_observed);
AMxsData_vs_m_observed->SetMarkerStyle(5);
AMxsData_vs_m_observed->SetMarkerColor(8);
AMxsData_vs_m_observed->SetLineColor(8);
AMxsData_vs_m_observed->SetLineWidth(2);
AMxsData_vs_m_observed->SetLineStyle(1);
AMxsData_vs_m_observed->SetMarkerSize(2);

TGraph *MMxsData_vs_m_observed = new TGraph(16, mData, MMxsUp_observed);
MMxsData_vs_m_observed->SetMarkerStyle(5);
MMxsData_vs_m_observed->SetMarkerColor(4);
MMxsData_vs_m_observed->SetLineColor(4);
MMxsData_vs_m_observed->SetLineWidth(2);
MMxsData_vs_m_observed->SetLineStyle(1);
MMxsData_vs_m_observed->SetMarkerSize(2);





 MCexshade2->Draw("f");
 MCexshade1->Draw("f");

 gPad->RedrawAxis();


 setTDRStyle();
 gStyle->SetPadLeftMargin(0.14);
 gROOT->ForceStyle();


 
 MCxsTh_vs_m->Draw("L");
 MMxsTh_vs_m->Draw("L");
 YMxsTh_vs_m->Draw("L");
 AMxsTh_vs_m->Draw("L");
 

 MCxsData_vs_m_expected->Draw("LP");
 MCxsData_vs_m_observed->Draw("LP");

 AMxsData_vs_m_observed->Draw("LP");
 YMxsData_vs_m_observed->Draw("LP");
 MMxsData_vs_m_observed->Draw("LP");

 
 // grshade->SetFillStyle(1001); 


 TLegend *legend = new TLegend(.5,.57,.92,.88);
 legend->SetBorderSize(1);
 legend->SetFillColor(0);
 //legend->SetFillStyle(0);
 legend->SetTextFont(42);
 legend->SetTextSize(.035);
 legend->SetMargin(0.15);
 legend->SetHeader("LQ #bar{LQ} #rightarrow #mu#mujj");
 // legend->AddEntry(p2,"ATLAS exclusion (1.03 fb^{-1}, 7 TeV)","f");
 // legend->AddEntry(pl,"CMS exclusion (5.0 fb^{-1}, 7TeV)","f");
 // legend->AddEntry(p3,"CMS exclusion (19.7 fb^{-1}, 8 TeV)","f");

legend->AddEntry(MMxsTh_vs_m,"MM, #sigma_{theory}#times#beta^{2}, (#beta=1)","lf");
legend->AddEntry(MCxsTh_vs_m,"MC, #sigma_{theory}#times#beta^{2}, (#beta=1)","lf");
legend->AddEntry(YMxsTh_vs_m,"YM, #sigma_{theory}#times#beta^{2}, (#beta=1)","lf");
legend->AddEntry(AMxsTh_vs_m,"AM, #sigma_{theory}#times#beta^{2}, (#beta=1)","lf");

 legend->AddEntry(MCxsData_vs_m_expected, "Exp. 95% CL upper limit","lp");
 legend->AddEntry(MCxsData_vs_m_observed, "Obs. 95% CL upper limit","lp");
 legend->Draw();

 TLatex l1;
 l1.SetTextAlign(12);
 l1.SetTextFont(42);
 l1.SetNDC();
 l1.SetTextSize(0.04);
// double stamp_x = 0.76;
//  double stamp_y = 0.58;

 // l1.DrawLatex(stamp_x,stamp_y - 0.00,"CMS 2012");	   
 // l1.DrawLatex(stamp_x,stamp_y - 0.05,"#sqrt{s} = 8 TeV");
  //l1.DrawLatex(0.70,0.53,"CMS 2011");
 //l1.DrawLatex(0.70,0.48,"#sqrt{s} = 7 TeV");

 l1.DrawLatex(0.14,0.93,"CMS #it{Preliminary}          #sqrt{s} = 8 TeV         19.7 fb^{-1}");


 TLatex l1b;
 l1b.SetTextAlign(12);
 l1b.SetTextFont(42);
 l1b.SetNDC();
 l1b.SetTextSize(0.025);
 l1b.DrawLatex(.17,.215,"The limits are computed with the MC vector sample.");
 l1b.DrawLatex(.17,.19,"X markers indicate observed limits using other vector samples.");
 l1b.DrawLatex(.17,.165,"X markers would be removed for publication.");
 // l1.DrawLatex(0.14,0.93,"CMS Work In Progres       #sqrt{s} = 8 TeV         19.6 fb^{-1}");
 // l1.DrawLatex(0.76,0.53,"Preliminary");
 // l1.DrawLatex(0.76,0.48,"#sqrt{s} = 8 TeV");
 // l1.DrawLatex(0.76,0.43,"19.6 fb^{-1}");
 
//  TLatex l2;
//  l2.SetTextAlign(12);
//  l2.SetTextSize(0.037);
//  l2.SetTextFont(42);
//  l2.SetNDC();
//  l2.DrawLatex(0.4,0.485,"EXO-10-005 scaled to #sqrt{s} = 7 TeV");

 c->SetGridx();
 c->SetGridy();
 c->RedrawAxis();
 legend->Draw();

 c->SetLogy();
 c->SaveAs((fileName1).c_str());
 c->SaveAs((fileName2).c_str());
 c->SaveAs((fileName3).c_str());

 // delete pl;
 // delete xsTh_vs_m;
 // delete bg;
 // delete c;
}


void myStyle()
{
 gStyle->Reset("Default");
 gStyle->SetCanvasColor(0);
 gStyle->SetPadColor(0);
 gStyle->SetTitleFillColor(10);
 gStyle->SetCanvasBorderMode(0);
 gStyle->SetStatColor(0);
 gStyle->SetPadBorderMode(0);
 gStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
 gStyle->SetPadTickY(1);
 gStyle->SetFrameBorderMode(0);
 gStyle->SetPalette(1);

   //gStyle->SetOptStat(kFALSE);
 gStyle->SetOptStat(111110);
 gStyle->SetOptFit(0);
 gStyle->SetStatFont(42);
 gStyle->SetPadLeftMargin(0.13);
 gStyle->SetPadRightMargin(0.07);
 gStyle->SetStatY(.9);
}

void setTDRStyle() {
  TStyle *tdrStyle = new TStyle("tdrStyle","Style for P-TDR");

  // For the canvas:
  tdrStyle->SetCanvasBorderMode(0);
  tdrStyle->SetCanvasColor(kWhite);
  tdrStyle->SetCanvasDefH(600); //Height of canvas
  tdrStyle->SetCanvasDefW(600); //Width of canvas
  tdrStyle->SetCanvasDefX(0);   //POsition on screen
  tdrStyle->SetCanvasDefY(0);

  // For the Pad:
  tdrStyle->SetPadBorderMode(0);
  // tdrStyle->SetPadBorderSize(Width_t size = 1);
  tdrStyle->SetPadColor(kWhite);
  tdrStyle->SetPadGridX(false);
  tdrStyle->SetPadGridY(false);
  tdrStyle->SetGridColor(0);
  tdrStyle->SetGridStyle(3);
  tdrStyle->SetGridWidth(1);

  // For the frame:
  tdrStyle->SetFrameBorderMode(0);
  tdrStyle->SetFrameBorderSize(1);
  tdrStyle->SetFrameFillColor(0);
  tdrStyle->SetFrameFillStyle(0);
  tdrStyle->SetFrameLineColor(1);
  tdrStyle->SetFrameLineStyle(1);
  tdrStyle->SetFrameLineWidth(1);

  // For the histo:
  tdrStyle->SetHistFillColor(63);
  // tdrStyle->SetHistFillStyle(0);
  tdrStyle->SetHistLineColor(1);
  tdrStyle->SetHistLineStyle(0);
  tdrStyle->SetHistLineWidth(1);


  tdrStyle->SetMarkerStyle(20);

  //For the fit/function:
  tdrStyle->SetOptFit(1);
  tdrStyle->SetFitFormat("5.4g");
  tdrStyle->SetFuncColor(2);
  tdrStyle->SetFuncStyle(1);
  tdrStyle->SetFuncWidth(1);

  //For the date:
  tdrStyle->SetOptDate(0);

  // For the statistics box:
  tdrStyle->SetOptFile(0);
  tdrStyle->SetOptStat(0); // To display the mean and RMS:   SetOptStat("mr");
  tdrStyle->SetStatColor(kWhite);
  tdrStyle->SetStatFont(42);
  tdrStyle->SetStatFontSize(0.025);
  tdrStyle->SetStatTextColor(1);
  tdrStyle->SetStatFormat("6.4g");
  tdrStyle->SetStatBorderSize(1);
  tdrStyle->SetStatH(0.1);
  tdrStyle->SetStatW(0.15);


  // Margins:
  tdrStyle->SetPadTopMargin(0.1);
  tdrStyle->SetPadBottomMargin(0.13);
  tdrStyle->SetPadLeftMargin(0.13);
  tdrStyle->SetPadRightMargin(0.05);

  // For the Global title:

  //  tdrStyle->SetOptTitle(0);
  tdrStyle->SetTitleFont(42);
  tdrStyle->SetTitleColor(1);
  tdrStyle->SetTitleTextColor(1);
  tdrStyle->SetTitleFillColor(10);
  tdrStyle->SetTitleFontSize(0.05);

  // For the axis titles:

  tdrStyle->SetTitleColor(1, "XYZ");
  tdrStyle->SetTitleFont(42, "XYZ");
  tdrStyle->SetTitleSize(0.06, "XYZ");
  tdrStyle->SetTitleXOffset(0.9);
  tdrStyle->SetTitleYOffset(1.05);

  // For the axis labels:

  tdrStyle->SetLabelColor(1, "XYZ");
  tdrStyle->SetLabelFont(42, "XYZ");
  tdrStyle->SetLabelOffset(0.007, "XYZ");
  tdrStyle->SetLabelSize(0.04, "XYZ");

  // For the axis:

  tdrStyle->SetAxisColor(1, "XYZ");
  tdrStyle->SetStripDecimals(kTRUE);
  tdrStyle->SetTickLength(0.03, "XYZ");
  tdrStyle->SetNdivisions(510, "XYZ");
  tdrStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
  tdrStyle->SetPadTickY(1);

  // Change for log plots:
  tdrStyle->SetOptLogx(0);
  tdrStyle->SetOptLogy(0);
  tdrStyle->SetOptLogz(0);
  
  tdrStyle->cd();
}
