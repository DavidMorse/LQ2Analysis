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
void makePlotsBO()
{

Double_t mTh[101] = {200.0,210.0,220.0,230.0,240.0,250.0,260.0,270.0,280.0,290.0,300.0,310.0,320.0,330.0,340.0,350.0,360.0,370.0,380.0,390.0,400.0,410.0,420.0,430.0,440.0,450.0,460.0,470.0,480.0,490.0,500.0,510.0,520.0,530.0,540.0,550.0,560.0,570.0,580.0,590.0,600.0,610.0,620.0,630.0,640.0,650.0,660.0,670.0,680.0,690.0,700.0,710.0,720.0,730.0,740.0,750.0,760.0,770.0,780.0,790.0,800.0,810.0,820.0,830.0,840.0,850.0,860.0,870.0,880.0,890.0,900.0,910.0,920.0,930.0,940.0,950.0,960.0,970.0,980.0,990.0,1000.0,1010.0,1020.0,1030.0,1040.0,1050.0,1060.0,1070.0,1080.0,1090.0,1100.0,1110.0,1120.0,1130.0,1140.0,1150.0,1160.0,1170.0,1180.0,1190.0,1200.0};
Double_t xsTh[101] = {17.4,13.4,10.5,8.27,6.57,5.26,4.24,3.44,2.8,2.3,1.89,1.57,1.3,1.09,0.914,0.77,0.65,0.551,0.469,0.4,0.342,0.294,0.253,0.218,0.188,0.163,0.142,0.123,0.107,0.0937,0.082,0.0719,0.0631,0.0555,0.0489,0.0431,0.0381,0.0337,0.0298,0.0265,0.0235,0.0209,0.0186,0.0166,0.0148,0.0132,0.0118,0.0106,0.00946,0.00848,0.00761,0.00683,0.00614,0.00552,0.00497,0.00448,0.00404,0.00364,0.00329,0.00297,0.00269,0.00243,0.0022,0.00199,0.00181,0.00164,0.00149,0.00135,0.00123,0.00111,0.00101,0.00092,0.00084,0.00076,0.0007,0.00063,0.00058,0.00053,0.00048,0.00044,0.0004,0.00037,0.00034,0.00031,0.00028,0.00026,0.00023,0.00021,0.0002,0.00018,0.00017,0.00015,0.00014,0.00013,0.00012,0.00011,0.0001,9e-05,8e-05,8e-05,7e-05};
Double_t x_pdf[202] = {200.0,210.0,220.0,230.0,240.0,250.0,260.0,270.0,280.0,290.0,300.0,310.0,320.0,330.0,340.0,350.0,360.0,370.0,380.0,390.0,400.0,410.0,420.0,430.0,440.0,450.0,460.0,470.0,480.0,490.0,500.0,510.0,520.0,530.0,540.0,550.0,560.0,570.0,580.0,590.0,600.0,610.0,620.0,630.0,640.0,650.0,660.0,670.0,680.0,690.0,700.0,710.0,720.0,730.0,740.0,750.0,760.0,770.0,780.0,790.0,800.0,810.0,820.0,830.0,840.0,850.0,860.0,870.0,880.0,890.0,900.0,910.0,920.0,930.0,940.0,950.0,960.0,970.0,980.0,990.0,1000.0,1010.0,1020.0,1030.0,1040.0,1050.0,1060.0,1070.0,1080.0,1090.0,1100.0,1110.0,1120.0,1130.0,1140.0,1150.0,1160.0,1170.0,1180.0,1190.0,1200.0,1200.0,1190.0,1180.0,1170.0,1160.0,1150.0,1140.0,1130.0,1120.0,1110.0,1100.0,1090.0,1080.0,1070.0,1060.0,1050.0,1040.0,1030.0,1020.0,1010.0,1000.0,990.0,980.0,970.0,960.0,950.0,940.0,930.0,920.0,910.0,900.0,890.0,880.0,870.0,860.0,850.0,840.0,830.0,820.0,810.0,800.0,790.0,780.0,770.0,760.0,750.0,740.0,730.0,720.0,710.0,700.0,690.0,680.0,670.0,660.0,650.0,640.0,630.0,620.0,610.0,600.0,590.0,580.0,570.0,560.0,550.0,540.0,530.0,520.0,510.0,500.0,490.0,480.0,470.0,460.0,450.0,440.0,430.0,420.0,410.0,400.0,390.0,380.0,370.0,360.0,350.0,340.0,330.0,320.0,310.0,300.0,290.0,280.0,270.0,260.0,250.0,240.0,230.0,220.0,210.0,200.0};
Double_t y_pdf[202] = {20.01297,15.464,12.13164,9.56326,7.60786,6.0964,4.91801,3.99975,3.2648,2.68288,2.21155,1.84109,1.53209,1.28518,1.07947,0.91007,0.77094,0.65543,0.5588,0.47757,0.40948,0.35218,0.30384,0.2626,0.22752,0.19725,0.17198,0.14954,0.13101,0.11445,0.10056,0.08832,0.0778,0.06857,0.06056,0.05354,0.0474,0.04205,0.03734,0.03323,0.02959,0.02634,0.0235,0.02105,0.01883,0.01684,0.01508,0.01355,0.01217,0.01092,0.00983,0.00885,0.00798,0.00719,0.0065,0.00587,0.00531,0.0048,0.00435,0.00394,0.00357,0.00324,0.00294,0.00267,0.00243,0.00221,0.00201,0.00183,0.00167,0.00152,0.00138,0.00127,0.00116,0.00106,0.00096,0.00088,0.00081,0.00074,0.00068,0.00062,0.00057,0.00052,0.00048,0.00044,0.0004,0.00037,0.00034,0.00031,0.00028,0.00026,0.00024,0.00022,0.0002,0.00019,0.00017,0.00016,0.00015,0.00013,0.00012,0.00011,0.00011,3e-05,4e-05,4e-05,4e-05,5e-05,5e-05,6e-05,7e-05,7e-05,8e-05,9e-05,0.0001,0.00011,0.00012,0.00013,0.00014,0.00016,0.00017,0.00019,0.00021,0.00023,0.00026,0.00028,0.00031,0.00035,0.00038,0.00042,0.00047,0.00052,0.00057,0.00063,0.0007,0.00078,0.00086,0.00095,0.00106,0.00117,0.0013,0.00144,0.0016,0.00178,0.00198,0.00221,0.00245,0.00274,0.00305,0.0034,0.0038,0.00425,0.00475,0.00531,0.00596,0.00668,0.00751,0.00842,0.00946,0.01062,0.012,0.0135,0.01526,0.0172,0.01951,0.022,0.02503,0.02837,0.03229,0.03674,0.04188,0.04778,0.05474,0.06264,0.07186,0.08252,0.09528,0.11022,0.12692,0.14723,0.17087,0.19896,0.2326,0.27191,0.31844,0.37515,0.44245,0.5235,0.62217,0.74137,0.88753,1.06791,1.28384,1.55326,1.89392,2.31955,2.85638,3.52972,4.39077,5.50714,6.95136,8.84255,11.336,14.69859};

 // filename for the final plot (NB: changing the name extension changes the file format)
 string fileName2 = "BR_Sigma_MuMu.pdf";
 string fileName3 = "BR_Sigma_MuMu.png";
 string fileName1 = "BR_Sigma_MuMu.eps";

 // axes labels for the final plot
 string title = ";M_{LQ} (GeV);#sigma#times#beta^{2} (pb)";

 // integrated luminosity
 string lint = "19.6 fb^{-1}";


// Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
// Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
// Double_t xsUp_expected[19] = {0.016065 , 0.008008 , 0.00513 , 0.003586 , 0.0027634 , 0.0019826 , 0.0015745 , 0.00121572 , 0.00101974 , 0.000758016 , 0.000678149 , 0.000551532 , 0.000407535 , 0.000338239 , 0.0002866749 , 0.000276224 , 0.0002662605 , 0.0002593894 , 0.00025655256 }; 
// Double_t xsUp_observed[19] = {0.019845 , 0.006622 , 0.0057456 , 0.0038957 , 0.0032144 , 0.00249118 , 0.0015228 , 0.00095832 , 0.000789157 , 0.000898688 , 0.000893887 , 0.000648948 , 0.000578023 , 0.0003601754 , 0.000229372 , 0.0002208768 , 0.0002130645 , 0.0002070236 , 0.00020501376 }; 
// Double_t y_1sigma[38]={0.011718 , 0.005775 , 0.0036936 , 0.0025917 , 0.0019926 , 0.00143092 , 0.0011374 , 0.0008778 , 0.000735887 , 0.000547008 , 0.000489311 , 0.000398028 , 0.000294112 , 0.00024409 , 0.0002068759 , 0.0001993472 , 0.0001921425 , 0.0001871965 , 0.00018514296 , 0.00035634504 , 0.0003602904 , 0.000369831 , 0.0003836672 , 0.000398193 , 0.000469794 , 0.000566105 , 0.000766044 , 0.000941769 , 0.0010528 , 0.001416221 , 0.0016896 , 0.00218785 , 0.00275409 , 0.0038376 , 0.0049878 , 0.0071478 , 0.011088 , 0.022491 }; 
// Double_t y_2sigma[38]={0.008694 , 0.004312 , 0.0028044 , 0.0019397 , 0.0015006 , 0.0010775 , 0.0008554 , 0.00066 , 0.000553247 , 0.000411264 , 0.000367992 , 0.000299136 , 0.000221089 , 0.0001834796 , 0.0001555479 , 0.0001498624 , 0.0001444575 , 0.0001407264 , 0.00013919304 , 0.000473454 , 0.0004786859 , 0.00049137 , 0.0005097728 , 0.0005290794 , 0.000624173 , 0.000752046 , 0.001017784 , 0.001251388 , 0.001398656 , 0.001881192 , 0.002244 , 0.00290695 , 0.00365919 , 0.0051004 , 0.0066178 , 0.0094734 , 0.014707 , 0.029862 }; 


Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
Double_t xsUp_expected[19] = {0.016443 , 0.008085 , 0.0051984 , 0.003586 , 0.0027552 , 0.00196536 , 0.0015557 , 0.00119328 , 0.001001476 , 0.000749504 , 0.00066981 , 0.00054448 , 0.000405414 , 0.0003338644 , 0.0002829055 , 0.0002711808 , 0.000261195 , 0.0002528517 , 0.00025016328 }; 
Double_t xsUp_observed[19] = {0.020601 , 0.007007 , 0.0058824 , 0.0038957 , 0.0032226 , 0.00248256 , 0.00151105 , 0.00094776 , 0.000778503 , 0.000886144 , 0.00088232 , 0.000639928 , 0.000571054 , 0.000355674 , 0.0002267655 , 0.0002176768 , 0.0002093355 , 0.0002029041 , 0.00020031576 }; 
Double_t y_1sigma[38]={0.011718 , 0.005852 , 0.0037278 , 0.0025917 , 0.0019844 , 0.00141799 , 0.0011233 , 0.00086196 , 0.00072295 , 0.000541184 , 0.000483393 , 0.000392944 , 0.000292597 , 0.00024092 , 0.0002041892 , 0.000195712 , 0.000188496 , 0.0001824778 , 0.00018053544 , 0.00034747104 , 0.0003512168 , 0.0003627855 , 0.0003766528 , 0.00039298 , 0.0004637076 , 0.000563176 , 0.000756368 , 0.000930471 , 0.001041152 , 0.001391108 , 0.00165792 , 0.00215965 , 0.00273254 , 0.0038212 , 0.0049715 , 0.0072162 , 0.011242 , 0.02268 }; 
Double_t y_2sigma[38]={0.008883 , 0.004389 , 0.0028044 , 0.0019397 , 0.0014924 , 0.00106888 , 0.00084365 , 0.00064812 , 0.000543354 , 0.000406784 , 0.000363419 , 0.000295364 , 0.000219978 , 0.0001811338 , 0.0001535028 , 0.0001471232 , 0.000141702 , 0.0001371847 , 0.00013572696 , 0.00046166376 , 0.0004666377 , 0.0004820145 , 0.0005004544 , 0.0005221421 , 0.0006161212 , 0.000748208 , 0.001004992 , 0.001236324 , 0.001383424 , 0.001847708 , 0.00220308 , 0.00286935 , 0.00362902 , 0.005084 , 0.0066178 , 0.009576 , 0.014938 , 0.03024 }; 




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
   if(( pow(10.0,xsData_vs_m_observed_log->Eval(mtest))/pow(10.0,xsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,xsData_vs_m_observed_log->Eval(mtest+0.1))/pow(10.0,xsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) obslim = mtest; 
  }
  std::cout<<"## LLJJ expected limit: "<<exlim<<" GeV"<<std::endl;
  std::cout<<"## LLJJ observed limit: "<<obslim<<" GeV"<<std::endl;

 // region excluded by Tevatron limits
 Double_t x_shaded[5] = {675,840,840,675,675};// CHANGED FOR LQ2
 Double_t y_shaded[5] = {0.0001,0.0001,50,50,0.0001};// CHANGED FOR LQ2

 Double_t x_shaded2[5] = {300,675,675,300,300};// CHANGED FOR LQ2
 Double_t y_shaded2[5] = {0.0001,0.0001,50,50,0.0001};// CHANGED FOR LQ2

 Double_t x_shaded3[5] = {840,obslim,obslim,840,840};// CHANGED FOR LQ2
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


 
 xsTh_vs_m->Draw("L");
 xsData_vs_m_expected->Draw("LP");
 xsData_vs_m_observed->Draw("LP");


 
 grshade->SetFillStyle(1001); 


 TLegend *legend = new TLegend(.37,.62,.92,.88);
 legend->SetBorderSize(1);
 legend->SetFillColor(0);
 //legend->SetFillStyle(0);
 legend->SetTextFont(42);
 legend->SetMargin(0.15);
 legend->SetHeader("LQ #bar{LQ} #rightarrow #mu#mujj");
 legend->AddEntry(p2,"ATLAS exclusion (1.03 fb^{-1}, 7 TeV)","f");
 legend->AddEntry(pl,"CMS exclusion (5.0 fb^{-1}, 7TeV)","f");
 legend->AddEntry(p3,"CMS exclusion (19.6 fb^{-1}, 8 TeV)","f");

 legend->AddEntry(xsTh_vs_m,"#sigma_{theory}#times#beta^{2}  with unc., (#beta=1)","lf");
 legend->AddEntry(xsData_vs_m_expected, "Expected 95% CL upper limit","lp");
 legend->AddEntry(xsData_vs_m_observed, "Observed 95% CL upper limit","lp");
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

 l1.DrawLatex(0.14,0.93,"CMS Preliminary          #sqrt{s} = 8 TeV         19.6 fb^{-1}");
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
