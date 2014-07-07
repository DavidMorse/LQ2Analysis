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
 string lint = "19.6 fb^{-1}";



// Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
// Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
// Double_t xsUp_expected[19] = {0.1363635 , 0.0466235 , 0.0232218 , 0.0114752 , 0.0071545 , 0.004773325 , 0.0032007 , 0.00241626 , 0.0019614775 , 0.001677984 , 0.001431887 , 0.000993922 , 0.00087668 , 0.0007442526 , 0.00071247675 , 0.000644096 , 0.00059968425 , 0.00057116065 , 0.00053554764 }; 
// Double_t xsUp_observed[19] = {0.156492 , 0.055979 , 0.031977 , 0.0153872 , 0.009512 , 0.005967195 , 0.00474465 , 0.0034089 , 0.002903976 , 0.002397472 , 0.002038213 , 0.001399002 , 0.001110899 , 0.0011344479 , 0.001189366 , 0.001074624 , 0.0010066815 , 0.0009586665 , 0.00090357504 }; 
// Double_t y_1sigma[38]={0.0983745 , 0.033649 , 0.016758 , 0.0082804 , 0.0051619 , 0.003445845 , 0.00231005 , 0.00174372 , 0.00141546 , 0.001210944 , 0.0010333635 , 0.000717336 , 0.000632664 , 0.0005371248 , 0.00051418225 , 0.000464832 , 0.0004327785 , 0.0004121961 , 0.00038649228 , 0.00074387436 , 0.00079334615 , 0.00083296125 , 0.000894656 , 0.0009896279 , 0.0010337687 , 0.0012177065 , 0.001380552 , 0.0019888515 , 0.00233072 , 0.00272438 , 0.0033561 , 0.0044462 , 0.006630935 , 0.0099343 , 0.01593325 , 0.0322677 , 0.064757 , 0.189378 }; 
// Double_t y_2sigma[38]={0.0739935 , 0.0252945 , 0.0126027 , 0.0062266 , 0.0038827 , 0.00259031 , 0.00173665 , 0.00131076 , 0.0010642585 , 0.000910336 , 0.000776872 , 0.000539232 , 0.0004756595 , 0.0004037946 , 0.00038654395 , 0.0003494528 , 0.00032535525 , 0.0003098827 , 0.0002905626 , 0.0009883374 , 0.0010540677 , 0.00110669625 , 0.001188672 , 0.00131485895 , 0.0013735293 , 0.0016178685 , 0.001834258 , 0.0026425215 , 0.003096576 , 0.003620077 , 0.00445896 , 0.0059079 , 0.00880964 , 0.013202 , 0.0211737 , 0.0428526 , 0.086009 , 0.2516535 }; 


Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
Double_t xsUp_expected[19] = {0.1373085 , 0.0470085 , 0.0233586 , 0.01151595 , 0.0071504 , 0.004760395 , 0.00319835 , 0.00241494 , 0.00195577 , 0.001671264 , 0.0014266415 , 0.000988264 , 0.000863954 , 0.0007399414 , 0.0007084066 , 0.0006422528 , 0.0005981085 , 0.00056788645 , 0.00053013276 }; 
Double_t xsUp_observed[19] = {0.1575315 , 0.056364 , 0.0320796 , 0.01541165 , 0.0094997 , 0.00594349 , 0.0047141 , 0.00337788 , 0.0028685895 , 0.002370816 , 0.002009699 , 0.00138211 , 0.001094436 , 0.0011151109 , 0.00115465945 , 0.0010432512 , 0.00097443225 , 0.0009235491 , 0.00086238924 }; 
Double_t y_1sigma[38]={0.0991305 , 0.0339185 , 0.0168606 , 0.00830485 , 0.0051578 , 0.00343507 , 0.002308875 , 0.00174306 , 0.001411655 , 0.001206016 , 0.0010295975 , 0.000713154 , 0.0006235235 , 0.0005339865 , 0.0005112349 , 0.0004635008 , 0.00043164 , 0.0004098314 , 0.00038258424 , 0.00073635756 , 0.00078879865 , 0.000830775 , 0.0008920832 , 0.0009839738 , 0.0010277774 , 0.0012000315 , 0.00137268 , 0.0019815885 , 0.002321312 , 0.00271677 , 0.00335478 , 0.004442675 , 0.006613695 , 0.0099302 , 0.0159903 , 0.0324387 , 0.065296 , 0.190701 }; 
Double_t y_2sigma[38]={0.074466 , 0.025487 , 0.0126711 , 0.0062429 , 0.0038786 , 0.002583845 , 0.001735475 , 0.0013101 , 0.0010612145 , 0.000906752 , 0.0007740475 , 0.000536198 , 0.000468741 , 0.0004014488 , 0.00038433845 , 0.0003484544 , 0.0003245055 , 0.0003081065 , 0.00028762548 , 0.00097834632 , 0.0010480222 , 0.00110379225 , 0.0011852544 , 0.00130736025 , 0.0013655092 , 0.0015944365 , 0.001823762 , 0.0026328375 , 0.003084256 , 0.0036098035 , 0.00445698 , 0.0059032 , 0.008785935 , 0.0131938 , 0.02124705 , 0.043092 , 0.0867405 , 0.253449 }; 


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
 legend->AddEntry(p3,"CMS exclusion (19.6 fb^{-1}, 8 TeV)","f");
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

 l1.DrawLatex(0.14,0.93,"CMS Preliminary          #sqrt{s} = 8 TeV         19.6 fb^{-1}");


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
