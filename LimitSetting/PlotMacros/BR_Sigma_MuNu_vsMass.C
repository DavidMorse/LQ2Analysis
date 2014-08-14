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
Double_t xsTh[101] = {8.7,6.7,5.25,4.135,3.285,2.63,2.12,1.72,1.4,1.15,0.945,0.785,0.65,0.545,0.457,0.385,0.325,0.2755,0.2345,0.2,0.171,0.147,0.1265,0.109,0.094,0.0815,0.071,0.0615,0.0535,0.04685,0.041,0.03595,0.03155,0.02775,0.02445,0.02155,0.01905,0.01685,0.0149,0.01325,0.01175,0.01045,0.0093,0.0083,0.0074,0.0066,0.0059,0.0053,0.00473,0.00424,0.00381,0.00342,0.00307,0.00276,0.00248,0.00224,0.00202,0.00182,0.00165,0.00149,0.00135,0.00122,0.0011,0.001,0.00091,0.00082,0.00075,0.00068,0.00062,0.00056,0.00051,0.00046,0.00042,0.00038,0.00035,0.00032,0.00029,0.00026,0.00024,0.00022,0.0002,0.00018,0.00017,0.00015,0.00014,0.00013,0.00012,0.00011,0.0001,9e-05,8e-05,8e-05,7e-05,6e-05,6e-05,5e-05,5e-05,4e-05,4e-05,4e-05,3e-05};
Double_t x_pdf[202] = {200.0,210.0,220.0,230.0,240.0,250.0,260.0,270.0,280.0,290.0,300.0,310.0,320.0,330.0,340.0,350.0,360.0,370.0,380.0,390.0,400.0,410.0,420.0,430.0,440.0,450.0,460.0,470.0,480.0,490.0,500.0,510.0,520.0,530.0,540.0,550.0,560.0,570.0,580.0,590.0,600.0,610.0,620.0,630.0,640.0,650.0,660.0,670.0,680.0,690.0,700.0,710.0,720.0,730.0,740.0,750.0,760.0,770.0,780.0,790.0,800.0,810.0,820.0,830.0,840.0,850.0,860.0,870.0,880.0,890.0,900.0,910.0,920.0,930.0,940.0,950.0,960.0,970.0,980.0,990.0,1000.0,1010.0,1020.0,1030.0,1040.0,1050.0,1060.0,1070.0,1080.0,1090.0,1100.0,1110.0,1120.0,1130.0,1140.0,1150.0,1160.0,1170.0,1180.0,1190.0,1200.0,1200.0,1190.0,1180.0,1170.0,1160.0,1150.0,1140.0,1130.0,1120.0,1110.0,1100.0,1090.0,1080.0,1070.0,1060.0,1050.0,1040.0,1030.0,1020.0,1010.0,1000.0,990.0,980.0,970.0,960.0,950.0,940.0,930.0,920.0,910.0,900.0,890.0,880.0,870.0,860.0,850.0,840.0,830.0,820.0,810.0,800.0,790.0,780.0,770.0,760.0,750.0,740.0,730.0,720.0,710.0,700.0,690.0,680.0,670.0,660.0,650.0,640.0,630.0,620.0,610.0,600.0,590.0,580.0,570.0,560.0,550.0,540.0,530.0,520.0,510.0,500.0,490.0,480.0,470.0,460.0,450.0,440.0,430.0,420.0,410.0,400.0,390.0,380.0,370.0,360.0,350.0,340.0,330.0,320.0,310.0,300.0,290.0,280.0,270.0,260.0,250.0,240.0,230.0,220.0,210.0,200.0};
Double_t y_pdf[202] = {10.00648,7.732,6.06582,4.78163,3.80393,3.0482,2.45901,1.99987,1.6324,1.34144,1.10578,0.92054,0.76604,0.64259,0.53973,0.45504,0.38547,0.32772,0.2794,0.23878,0.20474,0.17609,0.15192,0.1313,0.11376,0.09862,0.08599,0.07477,0.0655,0.05722,0.05028,0.04416,0.0389,0.03428,0.03028,0.02677,0.0237,0.02103,0.01867,0.01662,0.0148,0.01317,0.01175,0.01052,0.00941,0.00842,0.00754,0.00678,0.00609,0.00546,0.00492,0.00443,0.00399,0.0036,0.00325,0.00293,0.00265,0.0024,0.00217,0.00197,0.00179,0.00162,0.00147,0.00134,0.00122,0.00111,0.00101,0.00092,0.00084,0.00076,0.00069,0.00063,0.00058,0.00053,0.00048,0.00044,0.0004,0.00037,0.00034,0.00031,0.00028,0.00026,0.00024,0.00022,0.0002,0.00018,0.00017,0.00015,0.00014,0.00013,0.00012,0.00011,0.0001,9e-05,9e-05,8e-05,7e-05,7e-05,6e-05,6e-05,5e-05,2e-05,2e-05,2e-05,2e-05,2e-05,3e-05,3e-05,3e-05,4e-05,4e-05,4e-05,5e-05,5e-05,6e-05,6e-05,7e-05,8e-05,9e-05,0.0001,0.00011,0.00012,0.00013,0.00014,0.00016,0.00017,0.00019,0.00021,0.00023,0.00026,0.00029,0.00032,0.00035,0.00039,0.00043,0.00048,0.00053,0.00059,0.00065,0.00072,0.0008,0.00089,0.00099,0.0011,0.00123,0.00137,0.00153,0.0017,0.0019,0.00212,0.00237,0.00266,0.00298,0.00334,0.00375,0.00421,0.00473,0.00531,0.006,0.00675,0.00763,0.0086,0.00975,0.011,0.01252,0.01418,0.01614,0.01837,0.02094,0.02389,0.02737,0.03132,0.03593,0.04126,0.04764,0.05511,0.06346,0.07362,0.08543,0.09948,0.1163,0.13595,0.15922,0.18757,0.22123,0.26175,0.31109,0.37069,0.44376,0.53396,0.64192,0.77663,0.94696,1.15977,1.42819,1.76486,2.19538,2.75357,3.47568,4.42127,5.668,7.3493};

 // filename for the final plot (NB: changing the name extension changes the file format)
 string fileName2 = "BR_Sigma_MuNu.pdf";
 string fileName3 = "BR_Sigma_MuNu.png";
 string fileName1 = "BR_Sigma_MuNu.eps";
  
 // axes labels for the final plot
 string title = ";M_{LQ} (GeV);#sigma#times2#beta(1-#beta) (pb)";

 // integrated luminosity
 string lint = "19.7 fb^{-1}";


// Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
// Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
// Double_t xsUp_expected[19] = {0.087696 , 0.0333025 , 0.0192033 , 0.01016305 , 0.0066133 , 0.004553515 , 0.0033793 , 0.0026862 , 0.0020771495 , 0.001761536 , 0.001301691 , 0.000944886 , 0.0007512885 , 0.0006863684 , 0.00069022125 , 0.00062368 , 0.000577137 , 0.00054423945 , 0.00050895 }; 
// Double_t xsUp_observed[19] = {0.1214325 , 0.0557865 , 0.032661 , 0.0143766 , 0.0096473 , 0.005540505 , 0.005058375 , 0.00365178 , 0.002980837 , 0.00206976 , 0.0016980625 , 0.001442052 , 0.0008207765 , 0.0009090926 , 0.00093872095 , 0.0008475136 , 0.0007841625 , 0.00074224295 , 0.0006950256 }; 
// Double_t y_1sigma[38]={0.0639765 , 0.0242935 , 0.014022 , 0.00734315 , 0.0047724 , 0.003312235 , 0.00245105 , 0.00196944 , 0.0014911795 , 0.001270976 , 0.0009179625 , 0.000651244 , 0.000503687 , 0.0004584771 , 0.0004613505 , 0.000415616 , 0.00038460675 , 0.0003648807 , 0.00034122444 , 0.00079093788 , 0.00084577615 , 0.0008923035 , 0.0009642496 , 0.0010671412 , 0.0010611892 , 0.0011555915 , 0.00141573 , 0.0018879765 , 0.002484832 , 0.0029302305 , 0.00371382 , 0.004687075 , 0.00634863 , 0.009143 , 0.01400985 , 0.026334 , 0.0456225 , 0.120204 }; 
// Double_t y_2sigma[38]={0.0482895 , 0.018326 , 0.0105849 , 0.00559905 , 0.0036285 , 0.002489025 , 0.001855325 , 0.0014949 , 0.001127802 , 0.000966784 , 0.0006839325 , 0.000477978 , 0.0003624385 , 0.0003284437 , 0.00033297035 , 0.0003008768 , 0.000278421 , 0.00026255125 , 0.00024552792 , 0.00119884956 , 0.00128197235 , 0.00134723325 , 0.001455872 , 0.00161119795 , 0.0016022448 , 0.0017245245 , 0.002047786 , 0.002656106 , 0.003393376 , 0.0040017185 , 0.00498432 , 0.006280375 , 0.00848639 , 0.0121852 , 0.01855755 , 0.0344736 , 0.0601755 , 0.157437 }; 



Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
Double_t xsUp_expected[19] = {0.091098 , 0.035112 , 0.0202122 , 0.0106928 , 0.0069741 , 0.004741 , 0.003425125 , 0.0026994 , 0.002063832 , 0.001752128 , 0.0012851475 , 0.000895768 , 0.0007462385 , 0.000670455 , 0.0006688279 , 0.0006052864 , 0.00055958925 , 0.0005302171 , 0.0004951866 }; 
Double_t xsUp_observed[19] = {0.125685 , 0.0578655 , 0.0337896 , 0.01480855 , 0.0099097 , 0.0056461 , 0.005112425 , 0.00366366 , 0.002983881 , 0.002065056 , 0.0016945655 , 0.001433032 , 0.000820625 , 0.0009095047 , 0.00093667585 , 0.0008462208 , 0.00078276 , 0.0007407931 , 0.00069386676 }; 
Double_t y_1sigma[38]={0.0664335 , 0.025641 , 0.0147573 , 0.0077914 , 0.0050799 , 0.00342645 , 0.002471025 , 0.0019734 , 0.0014805255 , 0.00126 , 0.0009055885 , 0.00061295 , 0.0005003035 , 0.0004478259 , 0.00044508995 , 0.0004028032 , 0.00037239675 , 0.00035284855 , 0.00032953512 , 0.0007734996 , 0.00082821745 , 0.00087409575 , 0.000945472 , 0.0010447253 , 0.0010472729 , 0.0011507435 , 0.001356362 , 0.001874123 , 0.002457504 , 0.0029112055 , 0.00372174 , 0.00474935 , 0.006574905 , 0.0096678 , 0.01474335 , 0.027702 , 0.048279 , 0.1248345 }; 
Double_t y_2sigma[38]={0.0501795 , 0.019327 , 0.0111321 , 0.005868 , 0.0038253 , 0.002583845 , 0.00188 , 0.00149226 , 0.001112582 , 0.000954688 , 0.0006702135 , 0.000446162 , 0.0003600145 , 0.0003208357 , 0.0003174316 , 0.0002872704 , 0.000265584 , 0.00025164795 , 0.0002350218 , 0.00117969216 , 0.00125089955 , 0.00132018975 , 0.0014279936 , 0.00159335345 , 0.0015817349 , 0.00172306 , 0.001981366 , 0.0026446735 , 0.0033656 , 0.0039758445 , 0.00500148 , 0.006364975 , 0.0087493 , 0.0128699 , 0.01953555 , 0.0362691 , 0.063602 , 0.163485 }; 

  // turn on/off batch mode
 gROOT->SetBatch(kTRUE);


 // set ROOT style
//  myStyle();
 setTDRStyle();
 gStyle->SetPadLeftMargin(0.14);
 gROOT->ForceStyle();
 
 TCanvas *c = new TCanvas("c","",800,800);
 c->cd();
 
 TH2F *bg = new TH2F("bg",title.c_str(), 500, 300., 1200., 500., 0.0001, 50.);
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
 Double_t y_shaded[5] = {0.0001,0.0001,50,50,0.0001};// CHANGED FOR LQ2

 Double_t x_shaded2[5] = {300,552,552,300,300};// CHANGED FOR LQ2
 Double_t y_shaded2[5] = {0.0001,0.0001,50,50,0.0001};// CHANGED FOR LQ2

 Double_t x_shaded3[5] = {650,obslim,obslim,650,650};// CHANGED FOR LQ2
 Double_t y_shaded3[5] = {0.0001,0.0001,50,50,0.0001};// CHANGED FOR LQ2







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
