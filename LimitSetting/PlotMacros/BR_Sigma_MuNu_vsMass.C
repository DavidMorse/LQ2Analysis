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
void makePlotsBH()
{
Double_t mTh[101] = {200.0,210.0,220.0,230.0,240.0,250.0,260.0,270.0,280.0,290.0,300.0,310.0,320.0,330.0,340.0,350.0,360.0,370.0,380.0,390.0,400.0,410.0,420.0,430.0,440.0,450.0,460.0,470.0,480.0,490.0,500.0,510.0,520.0,530.0,540.0,550.0,560.0,570.0,580.0,590.0,600.0,610.0,620.0,630.0,640.0,650.0,660.0,670.0,680.0,690.0,700.0,710.0,720.0,730.0,740.0,750.0,760.0,770.0,780.0,790.0,800.0,810.0,820.0,830.0,840.0,850.0,860.0,870.0,880.0,890.0,900.0,910.0,920.0,930.0,940.0,950.0,960.0,970.0,980.0,990.0,1000.0,1010.0,1020.0,1030.0,1040.0,1050.0,1060.0,1070.0,1080.0,1090.0,1100.0,1110.0,1120.0,1130.0,1140.0,1150.0,1160.0,1170.0,1180.0,1190.0,1200.0};
Double_t x_pdf[202] = {200.0,210.0,220.0,230.0,240.0,250.0,260.0,270.0,280.0,290.0,300.0,310.0,320.0,330.0,340.0,350.0,360.0,370.0,380.0,390.0,400.0,410.0,420.0,430.0,440.0,450.0,460.0,470.0,480.0,490.0,500.0,510.0,520.0,530.0,540.0,550.0,560.0,570.0,580.0,590.0,600.0,610.0,620.0,630.0,640.0,650.0,660.0,670.0,680.0,690.0,700.0,710.0,720.0,730.0,740.0,750.0,760.0,770.0,780.0,790.0,800.0,810.0,820.0,830.0,840.0,850.0,860.0,870.0,880.0,890.0,900.0,910.0,920.0,930.0,940.0,950.0,960.0,970.0,980.0,990.0,1000.0,1010.0,1020.0,1030.0,1040.0,1050.0,1060.0,1070.0,1080.0,1090.0,1100.0,1110.0,1120.0,1130.0,1140.0,1150.0,1160.0,1170.0,1180.0,1190.0,1200.0,1200.0,1190.0,1180.0,1170.0,1160.0,1150.0,1140.0,1130.0,1120.0,1110.0,1100.0,1090.0,1080.0,1070.0,1060.0,1050.0,1040.0,1030.0,1020.0,1010.0,1000.0,990.0,980.0,970.0,960.0,950.0,940.0,930.0,920.0,910.0,900.0,890.0,880.0,870.0,860.0,850.0,840.0,830.0,820.0,810.0,800.0,790.0,780.0,770.0,760.0,750.0,740.0,730.0,720.0,710.0,700.0,690.0,680.0,670.0,660.0,650.0,640.0,630.0,620.0,610.0,600.0,590.0,580.0,570.0,560.0,550.0,540.0,530.0,520.0,510.0,500.0,490.0,480.0,470.0,460.0,450.0,440.0,430.0,420.0,410.0,400.0,390.0,380.0,370.0,360.0,350.0,340.0,330.0,320.0,310.0,300.0,290.0,280.0,270.0,260.0,250.0,240.0,230.0,220.0,210.0,200.0};
Double_t xsTh[101] = {8.7,6.7,5.25,4.135,3.285,2.63,2.12,1.72,1.4,1.15,0.945,0.785,0.65,0.545,0.457,0.385,0.325,0.2755,0.2345,0.2,0.171,0.147,0.1265,0.109,0.094,0.0815,0.071,0.0615,0.0535,0.04685,0.041,0.03595,0.03155,0.02775,0.02445,0.02155,0.01905,0.01685,0.0149,0.01325,0.01175,0.01045,0.0093,0.0083,0.0074,0.0066,0.0059,0.0053,0.00473,0.00424,0.003805,0.003415,0.00307,0.00276,0.002485,0.00224,0.00202,0.00182,0.001645,0.001485,0.001345,0.001215,0.0011,0.000995,0.000905,0.00082,0.000745,0.000675,0.000615,0.000555,0.000505,0.000461,0.0004195,0.000382,0.000348,0.000317,0.000289,0.0002635,0.0002405,0.0002195,0.0002005,0.000183,0.0001675,0.000153,0.00014,0.000128,0.000117,0.000107,9.8e-05,9e-05,8.25e-05,7.55e-05,6.9e-05,6.35e-05,5.8e-05,5.35e-05,4.9e-05,4.495e-05,4.125e-05,3.79e-05,3.48e-05};
Double_t y_pdf[202] = {10.006483831,7.732000484,6.06581922,4.781628951,3.803931836,3.048201208,2.4590059,1.999873186,1.632398365,1.341441897,1.105776242,0.920544273,0.766043095,0.642590983,0.539734515,0.455035705,0.385471502,0.327716496,0.279400696,0.238783018,0.204737961,0.176088185,0.15192189,0.131300504,0.11376082,0.098623376,0.085992415,0.074772245,0.065502604,0.057223644,0.050277527,0.044160512,0.03890136,0.034284906,0.030281243,0.026767876,0.023702174,0.021026374,0.018668955,0.016617005,0.014795078,0.01317068,0.011751474,0.010523533,0.009413237,0.008420604,0.007541371,0.006775847,0.006085148,0.005460912,0.004916407,0.004425792,0.003989198,0.003596436,0.003247709,0.002933542,0.002653127,0.002401808,0.002173691,0.001968104,0.001786192,0.00161949,0.001470088,0.001335413,0.001216077,0.001105539,0.001007309,0.000915477,0.000835057,0.000759774,0.000692089,0.000633325,0.000577811,0.000527782,0.000482366,0.000440597,0.000402941,0.00036872,0.000337644,0.000309038,0.000283074,0.000259722,0.000238198,0.000218317,0.000200407,0.000183664,0.000168582,0.000154854,0.000142244,0.000130825,0.000120352,0.000110522,0.000101588,9.3637e-05,8.6034e-05,7.9368e-05,7.3049e-05,6.7291e-05,6.1948e-05,5.7112e-05,5.2637e-05,1.6789e-05,1.8497e-05,2.0343e-05,2.2429e-05,2.4689e-05,2.7271e-05,2.9785e-05,3.3033e-05,3.6076e-05,3.9978e-05,4.4146e-05,4.8495e-05,5.3242e-05,5.8624e-05,6.4725e-05,7.1456e-05,7.872e-05,8.68e-05,9.5728e-05,0.000105379,0.000116653,0.0001285,0.000141885,0.000156615,0.000173188,0.000191142,0.000211177,0.000233353,0.000258111,0.000285546,0.000315181,0.000348631,0.000389058,0.000428517,0.000476614,0.000528354,0.000585674,0.000648364,0.000721628,0.000799985,0.000891073,0.000989027,0.001103415,0.001225189,0.001369116,0.00152647,0.001702057,0.001900858,0.002123467,0.002374267,0.002656425,0.002979187,0.003338939,0.003754798,0.004210592,0.004730615,0.005311789,0.006001827,0.006748584,0.007628281,0.008601588,0.009753684,0.010999035,0.012515014,0.01418351,0.016142716,0.018371275,0.020937878,0.02388906,0.02736979,0.031319995,0.035929835,0.0412598,0.047638092,0.055109043,0.06345949,0.073616428,0.085434931,0.099481071,0.116301914,0.135953602,0.159218601,0.187573755,0.221226963,0.261748103,0.311086199,0.370686617,0.443762655,0.533956905,0.641918729,0.776628387,0.946960595,1.159773024,1.428188417,1.764859183,2.19538264,2.753572441,3.475679137,4.421274472,5.667999516,7.34929648};


 // filename for the final plot (NB: changing the name extension changes the file format)
 string fileName2 = "BR_Sigma_MuNu.pdf";
 string fileName3 = "BR_Sigma_MuNu.png";
 string fileName1 = "BR_Sigma_MuNu.eps";
  
 // axes labels for the final plot
 string title = ";M_{LQ} (GeV);#sigma#times2#beta(1-#beta) (pb)";

 // integrated luminosity
 string lint = "19.7 fb^{-1}";


Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
Double_t xsUp_expected[19] = {0.09107813799 , 0.035043277885 , 0.020131798023 , 0.010737183107 , 0.006976974059 , 0.0047389464143 , 0.00342351140775 , 0.002695204941 , 0.00205932059033 , 0.00175304332672 , 0.00128503046348 , 0.00089961663966 , 0.000745859955535 , 0.000670974077356 , 0.000668636674729 , 0.000605106567424 , 0.000559427161177 , 0.000529540079114 , 0.000496202109136 }; 
Double_t xsUp_observed[19] = {0.12573803151 , 0.05784480933 , 0.033743537046 , 0.0148114586535 , 0.009908428057 , 0.00564290876825 , 0.00511129973775 , 0.0036634270134 , 0.00298354786464 , 0.00206494458688 , 0.00169441242959 , 0.00143305054676 , 0.000820617412375 , 0.00090948531545 , 0.000936672902249 , 0.000846219274368 , 0.000782764985887 , 0.000740795093142 , 0.000693868694706 }; 
Double_t y_1sigma[38]={0.066572814735 , 0.02553224828 , 0.014738826357 , 0.0077473322165 , 0.00508336696 , 0.00342477394875 , 0.0024702085395 , 0.0019732046466 , 0.00147964955856 , 0.00126066864 , 0.000905517428855 , 0.00061341427334 , 0.000501568530555 , 0.000448184576624 , 0.000444960287051 , 0.00040268264768 , 0.00037228418469 , 0.000352395106309 , 0.00033020957793 , 0.000775083565535 , 0.000827158574576 , 0.000873843147787 , 0.00094519586176 , 0.00104443186544 , 0.00104808301854 , 0.00115316506994 , 0.00135502725156 , 0.00187408189142 , 0.00245880153568 , 0.00290480011734 , 0.0037265523108 , 0.0047471990685 , 0.00657124152155 , 0.009674594274 , 0.014803075808 , 0.027755189037 , 0.04831325807 , 0.12484097892 }; 
Double_t y_2sigma[38]={0.050342016375 , 0.019232736215 , 0.011166857289 , 0.005892867932 , 0.003829159658 , 0.0025823555502 , 0.0018789193055 , 0.0014949965118 , 0.00111412455841 , 0.00095527166336 , 0.000670123292195 , 0.0004445371126 , 0.00035981917004 , 0.000321071575262 , 0.000317341224224 , 0.000287189239552 , 0.000265509384855 , 0.000251324680798 , 0.000235502177251 , 0.00117064476472 , 0.00125541393757 , 0.00131980582239 , 0.00142757312013 , 0.0015929038895 , 0.00158296844495 , 0.00172367317453 , 0.00198599341416 , 0.00264459078116 , 0.00336750350944 , 0.00396706864039 , 0.0050009645466 , 0.00636209590925 , 0.008745395571 , 0.012830436188 , 0.019613435149 , 0.036251568909 , 0.0635579098 , 0.16346375829 }; 



  // turn on/off batch mode
 gROOT->SetBatch(kTRUE);


 // set ROOT style
//  myStyle();
 setTDRStyle();
 gStyle->SetPadLeftMargin(0.14);
 gROOT->ForceStyle();
 
 TCanvas *c = new TCanvas("c","",800,800);
 c->cd();
 
 TH2F *bg = new TH2F("bg",title.c_str(), 500, 300., 1200., 500., 0.00001, 50.);
  bg->GetXaxis()->CenterTitle();
 bg->GetYaxis()->CenterTitle();
 bg->SetStats(kFALSE);
 bg->SetTitleOffset(1.,"X");
 bg->SetTitleOffset(1.15,"Y");
 
 bg->Draw();


 TGraph *xsTh_vs_m = new TGraph(101, mTh, xsTh);
 xsTh_vs_m->SetLineWidth(2);
 xsTh_vs_m->SetLineColor(kBlue);
 xsTh_vs_m->SetFillColor(kCyan-6);
 xsTh_vs_m->SetMarkerSize(0.00001);
 xsTh_vs_m->SetMarkerStyle(22);
 xsTh_vs_m->SetMarkerColor(kBlue);

 TGraph *xsData_vs_m_expected = new TGraph(19, mData, xsUp_expected);
 xsData_vs_m_expected->SetMarkerStyle(0);
 xsData_vs_m_expected->SetMarkerColor(kBlack);
 xsData_vs_m_expected->SetLineColor(kBlack);
 xsData_vs_m_expected->SetLineWidth(2);
 xsData_vs_m_expected->SetLineStyle(7);
 xsData_vs_m_expected->SetMarkerSize(0.001);

 TGraph *xsData_vs_m_observed = new TGraph(19, mData, xsUp_observed);
 xsData_vs_m_observed->SetMarkerStyle(21);
 xsData_vs_m_observed->SetMarkerColor(kBlack);
 xsData_vs_m_observed->SetLineColor(kBlack);
 xsData_vs_m_observed->SetLineWidth(2);
 xsData_vs_m_observed->SetLineStyle(1);
 xsData_vs_m_observed->SetMarkerSize(1);
 
 Double_t xsUp_observed_logY[19], xsUp_expected_logY[19], xsTh_logY[101];
 for (int ii = 0; ii<19; ++ii) xsUp_observed_logY[ii] = log10(xsUp_observed[ii]);
 for (int ii = 0; ii<19; ++ii) xsUp_expected_logY[ii] = log10(xsUp_expected[ii]);
 for (int ii = 0; ii<101; ++ii) xsTh_logY[ii] = log10(xsTh[ii]);
 TGraph *xsTh_vs_m_log = new TGraph(101, mTh, xsTh_logY);
 TGraph *xsData_vs_m_expected_log = new TGraph(19, mData, xsUp_expected_logY);
 TGraph *xsData_vs_m_observed_log = new TGraph(19, mData, xsUp_observed_logY);
 


 double obslim = 0.0;
 double exlim = 0.0;
 for (Double_t mtest=300.10; mtest<1199.90; mtest = mtest+0.10){
   if(( pow(10.0,xsData_vs_m_expected_log->Eval(mtest))/pow(10.0,xsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,xsData_vs_m_expected_log->Eval(mtest+0.1))/pow(10.0,xsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) exlim = mtest;
   if(( pow(10.0,xsData_vs_m_observed_log->Eval(mtest))/pow(10.0,xsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,xsData_vs_m_observed_log->Eval(mtest+0.1))/pow(10.0,xsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) obslim =mtest;
  }
  

  std::cout<<"## LVJJ expected limit: "<<exlim<<" GeV"<<std::endl;
  std::cout<<"## LVJJ observed limit: "<<obslim<<" GeV"<<std::endl;



 // region excluded by Tevatron limits
 Double_t x_shaded[5] = {552,650,650,552,552};// CHANGED FOR LQ2
 Double_t y_shaded[5] = {0.00001,0.00001,50,50,0.00001};// CHANGED FOR LQ2

 Double_t x_shaded2[5] = {300,552,552,300,300};// CHANGED FOR LQ2
 Double_t y_shaded2[5] = {0.00001,0.00001,50,50,0.00001};// CHANGED FOR LQ2

 Double_t x_shaded3[5] = {650,obslim,obslim,650,650};// CHANGED FOR LQ2
 Double_t y_shaded3[5] = {0.00001,0.00001,50,50,0.00001};// CHANGED FOR LQ2







 TPolyLine *p2 = new TPolyLine(5,x_shaded2,y_shaded2,"");
//  pl->SetFillStyle(3001);
 p2->SetFillColor(8);
 p2->SetFillStyle(3345);
 p2->SetLineColor(8);   // CHANGED FOR LQ2
 p2->Draw();
 p2->Draw("F");


 TPolyLine *pl = new TPolyLine(5,x_shaded,y_shaded,"");
//  pl->SetFillStyle(3001);
 pl->SetLineColor(14);
 pl->SetFillColor(14);
 pl->SetFillStyle(3344);
 pl->Draw();
 pl->Draw("F");
 
 

 TPolyLine *p3 = new TPolyLine(5,x_shaded3,y_shaded3,"");
 p3->SetLineColor(46);
 p3->SetFillColor(46);
 p3->SetFillStyle(3354);
 p3->Draw();
 p3->Draw("F");



 TGraph *exshade1 = new TGraph(38,x_shademasses,y_1sigma);
 exshade1->SetFillColor(kGreen);
 TGraph *exshade2 = new TGraph(38,x_shademasses,y_2sigma);
 exshade2->SetFillColor(kYellow);

 exshade2->Draw("f");
 exshade1->Draw("f");

 gPad->RedrawAxis();


 TGraph *grshade = new TGraph(202,x_pdf,y_pdf);
 grshade->SetFillColor(kCyan-6);
 grshade->SetFillStyle(3001);
 grshade->Draw("f");



 // set ROOT style
//  myStyle();
 setTDRStyle();
 gStyle->SetPadLeftMargin(0.14);
 gROOT->ForceStyle();


 
  grshade->SetFillStyle(1001); 

 xsTh_vs_m->Draw("L");
 xsData_vs_m_expected->Draw("LP");
 xsData_vs_m_observed->Draw("LP");




 TLegend *legend = new TLegend(.37,.62,.92,.88);
 
  legend->SetBorderSize(1);
 legend->SetFillColor(0);
 //legend->SetFillStyle(0);
 legend->SetTextFont(42);
 legend->SetMargin(0.15);
 legend->SetHeader("LQ #bar{LQ} #rightarrow #mu#nujj");
 legend->AddEntry(p2,"ATLAS exclusion (1.03 fb^{-1}, 7 TeV)","f");
 legend->AddEntry(pl,"CMS exclusion (5.0 fb^{-1}, 7TeV)","f");
 legend->AddEntry(p3,"CMS exclusion (19.7 fb^{-1}, 8 TeV)","f");
 legend->AddEntry(xsTh_vs_m,"#sigma_{theory}#times2#beta(1-#beta) with unc., (#beta=1/2)","lf");
 legend->AddEntry(xsData_vs_m_expected, "Expected 95% CL upper limit","lp");
 legend->AddEntry(xsData_vs_m_observed, "Observed 95% CL upper limit","lp");
 legend->Draw();

 TLatex l1;
  l1.SetTextAlign(12);
 l1.SetTextFont(42);
 l1.SetNDC();
 l1.SetTextSize(0.04);
 
 double stamp_x = 0.76;
 double stamp_y = 0.58;

 // l1.DrawLatex(stamp_x,stamp_y - 0.00,"CMS 2012");	   
 // l1.DrawLatex(stamp_x,stamp_y - 0.05,"#sqrt{s} = 8 TeV");
 
 //l1.DrawLatex(0.7,0.53,"CMS 2011");

 //l1.DrawLatex(0.7,0.48,"#sqrt{s} = 7 TeV");

 l1.DrawLatex(0.14,0.93,"CMS #it{Preliminary}          #sqrt{s} = 8 TeV         19.7 fb^{-1}");


 // l1.DrawLatex(0.76,0.58,"CMS 2012");
 // l1.DrawLatex(0.76,0.53,"Preliminary");
 // l1.DrawLatex(0.76,0.48,"#sqrt{s} = 8 TeV");
 // l1.DrawLatex(0.76,0.43,"19.6 fb^{-1}");

//  TLatex l2;
//  l2.SetTextAlign(12);
//  l2.SetTextSize(0.037);
//  l2.SetTextFont(42);
//  l2.SetNDC();
//  l2.DrawLatex(0.4,0.485,"EXO-10-005 scaled to #sqrt{s} = 7 TeV");

 c->RedrawAxis();
 legend->Draw();
 c->SetGridx();
 c->SetGridy();


 c->SetLogy();
 c->SaveAs((fileName1).c_str());
 c->SaveAs((fileName2).c_str());
 c->SaveAs((fileName3).c_str());

 delete pl;
 delete xsTh_vs_m;
 delete bg;
 delete c;
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
//    gStyle->SetTitleFont(42);
//    gStyle->SetTitleFont(42, "XYZ");
//    gStyle->SetLabelFont(42, "XYZ");
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
