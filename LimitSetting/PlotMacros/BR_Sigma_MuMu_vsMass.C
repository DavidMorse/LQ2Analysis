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
 string lint = "19.7 fb^{-1}";


// Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
// Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
// Double_t xsUp_expected[19] = {0.015876 , 0.007777 , 0.0049932 , 0.0035045 , 0.0026978 , 0.00195674 , 0.00146875 , 0.00115104 , 0.000954294 , 0.00071456 , 0.000588572 , 0.00048052 , 0.000356126 , 0.0003123084 , 0.0002609307 , 0.0002503936 , 0.000241032 , 0.0002336559 , 0.00023130168 }; 
// Double_t xsUp_observed[19] = {0.023247 , 0.006468 , 0.0053694 , 0.0034067 , 0.002296 , 0.00243946 , 0.0014476 , 0.00083028 , 0.000674246 , 0.000772352 , 0.0008608 , 0.000660756 , 0.000526513 , 0.0003273342 , 0.000209723 , 0.0002012672 , 0.0001937265 , 0.0001873784 , 0.00018526824 }; 
// Double_t y_1sigma[38]={0.01134 , 0.005698 , 0.0036594 , 0.0024939 , 0.0019598 , 0.00140506 , 0.00104105 , 0.00080916 , 0.000671202 , 0.00049056 , 0.000402962 , 0.000325704 , 0.000230583 , 0.0001973008 , 0.0001569915 , 0.0001506304 , 0.000145002 , 0.0001405659 , 0.00013914432 , 0.00039909336 , 0.0004068996 , 0.0004197435 , 0.0004360448 , 0.0004544132 , 0.0005140472 , 0.000574791 , 0.00073144 , 0.000882051 , 0.001053696 , 0.001384259 , 0.00165924 , 0.00211265 , 0.00278426 , 0.0038376 , 0.0049063 , 0.0070452 , 0.011011 , 0.022491 }; 
// Double_t y_2sigma[38]={0.008505 , 0.004158 , 0.0026334 , 0.0018093 , 0.0014514 , 0.00105595 , 0.00076845 , 0.00059796 , 0.000495411 , 0.000358848 , 0.00029321 , 0.000237472 , 0.000161398 , 0.0001360564 , 0.000103458 , 9.92768e-05 , 9.5568e-05 , 9.26406e-05 , 9.170496e-05 , 0.00066293304 , 0.0006701945 , 0.00069135 , 0.000718208 , 0.0007484665 , 0.0008169724 , 0.000888396 , 0.001082072 , 0.001282861 , 0.001512448 , 0.001947399 , 0.00231396 , 0.00293045 , 0.00383159 , 0.0052316 , 0.0067482 , 0.0097128 , 0.015169 , 0.029862 }; 


Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
Double_t xsUp_expected[19] = {0.016065 , 0.007777 , 0.0049932 , 0.0034719 , 0.002706 , 0.00195674 , 0.00149695 , 0.00116028 , 0.000961143 , 0.000716352 , 0.00057566 , 0.000471992 , 0.000351884 , 0.000312245 , 0.0002600084 , 0.0002513664 , 0.0002403225 , 0.000233153 , 0.0002295756 }; 
Double_t xsUp_observed[19] = {0.024381 , 0.006776 , 0.0054036 , 0.003423 , 0.0022222 , 0.00242222 , 0.0014852 , 0.00081972 , 0.00066968 , 0.000764288 , 0.000848157 , 0.000655016 , 0.000522574 , 0.000326193 , 0.0002089611 , 0.0002004992 , 0.000193017 , 0.0001866829 , 0.0001845792 }; 
Double_t y_1sigma[38]={0.01134 , 0.005775 , 0.0036594 , 0.0025265 , 0.001968 , 0.00138782 , 0.0010622 , 0.00081576 , 0.000676529 , 0.0004928 , 0.000393278 , 0.000318816 , 0.000227351 , 0.0001972374 , 0.0001564301 , 0.0001505792 , 0.000144573 , 0.0001402556 , 0.00013810728 , 0.0003997824 , 0.0004022879 , 0.000418506 , 0.0004337408 , 0.0004527691 , 0.000513857 , 0.000564994 , 0.000718648 , 0.000866987 , 0.001055936 , 0.001394913 , 0.00167376 , 0.0021338 , 0.00278426 , 0.003854 , 0.0049552 , 0.0070452 , 0.011088 , 0.02268 }; 
Double_t y_2sigma[38]={0.008505 , 0.004158 , 0.0026334 , 0.0018908 , 0.0014596 , 0.00102578 , 0.00078255 , 0.00060324 , 0.000499216 , 0.000361088 , 0.000285678 , 0.000231404 , 0.000158772 , 0.000135993 , 0.0001030971 , 9.8688e-05 , 9.52875e-05 , 9.24373e-05 , 9.102288e-05 , 0.00065847864 , 0.0006682364 , 0.000689304 , 0.0007153152 , 0.0007457798 , 0.0008167188 , 0.000876579 , 0.001063048 , 0.001257037 , 0.00150752 , 0.001950443 , 0.00233244 , 0.00293515 , 0.00378849 , 0.0052234 , 0.0066667 , 0.0097128 , 0.015246 , 0.030051 }; 




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
 legend->AddEntry(p3,"CMS exclusion (19.7 fb^{-1}, 8 TeV)","f");

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

 l1.DrawLatex(0.14,0.93,"CMS #it{Preliminary}          #sqrt{s} = 8 TeV         19.7 fb^{-1}");
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
