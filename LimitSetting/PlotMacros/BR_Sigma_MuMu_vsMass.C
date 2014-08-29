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
Double_t xsTh[101] = {17.4,13.4,10.5,8.27,6.57,5.26,4.24,3.44,2.8,2.3,1.89,1.57,1.3,1.09,0.914,0.77,0.65,0.551,0.469,0.4,0.342,0.294,0.253,0.218,0.188,0.163,0.142,0.123,0.107,0.0937,0.082,0.0719,0.0631,0.0555,0.0489,0.0431,0.0381,0.0337,0.0298,0.0265,0.0235,0.0209,0.0186,0.0166,0.0148,0.0132,0.0118,0.0106,0.00946,0.00848,0.00761,0.00683,0.00614,0.00552,0.00497,0.00448,0.00404,0.00364,0.00329,0.00297,0.00269,0.00243,0.0022,0.00199,0.00181,0.00164,0.00149,0.00135,0.00123,0.00111,0.00101,0.000922,0.000839,0.000764,0.000696,0.000634,0.000578,0.000527,0.000481,0.000439,0.000401,0.000366,0.000335,0.000306,0.00028,0.000256,0.000234,0.000214,0.000196,0.00018,0.000165,0.000151,0.000138,0.000127,0.000116,0.000107,9.8e-05,8.99e-05,8.25e-05,7.58e-05,6.96e-05};
Double_t x_pdf[202] = {200.0,210.0,220.0,230.0,240.0,250.0,260.0,270.0,280.0,290.0,300.0,310.0,320.0,330.0,340.0,350.0,360.0,370.0,380.0,390.0,400.0,410.0,420.0,430.0,440.0,450.0,460.0,470.0,480.0,490.0,500.0,510.0,520.0,530.0,540.0,550.0,560.0,570.0,580.0,590.0,600.0,610.0,620.0,630.0,640.0,650.0,660.0,670.0,680.0,690.0,700.0,710.0,720.0,730.0,740.0,750.0,760.0,770.0,780.0,790.0,800.0,810.0,820.0,830.0,840.0,850.0,860.0,870.0,880.0,890.0,900.0,910.0,920.0,930.0,940.0,950.0,960.0,970.0,980.0,990.0,1000.0,1010.0,1020.0,1030.0,1040.0,1050.0,1060.0,1070.0,1080.0,1090.0,1100.0,1110.0,1120.0,1130.0,1140.0,1150.0,1160.0,1170.0,1180.0,1190.0,1200.0,1200.0,1190.0,1180.0,1170.0,1160.0,1150.0,1140.0,1130.0,1120.0,1110.0,1100.0,1090.0,1080.0,1070.0,1060.0,1050.0,1040.0,1030.0,1020.0,1010.0,1000.0,990.0,980.0,970.0,960.0,950.0,940.0,930.0,920.0,910.0,900.0,890.0,880.0,870.0,860.0,850.0,840.0,830.0,820.0,810.0,800.0,790.0,780.0,770.0,760.0,750.0,740.0,730.0,720.0,710.0,700.0,690.0,680.0,670.0,660.0,650.0,640.0,630.0,620.0,610.0,600.0,590.0,580.0,570.0,560.0,550.0,540.0,530.0,520.0,510.0,500.0,490.0,480.0,470.0,460.0,450.0,440.0,430.0,420.0,410.0,400.0,390.0,380.0,370.0,360.0,350.0,340.0,330.0,320.0,310.0,300.0,290.0,280.0,270.0,260.0,250.0,240.0,230.0,220.0,210.0,200.0};
Double_t y_pdf[202] = {20.012967661,15.464000969,12.13163844,9.563257902,7.607863671,6.096402415,4.918011799,3.999746371,3.26479673,2.682883794,2.211552484,1.841088546,1.532086191,1.285181966,1.07946903,0.91007141,0.770943003,0.655432993,0.558801392,0.477566036,0.409475922,0.35217637,0.30384378,0.262601009,0.22752164,0.197246752,0.171984829,0.149544491,0.131005208,0.114447289,0.100555053,0.088321023,0.077802721,0.068569813,0.060562487,0.053535751,0.047404348,0.042052748,0.037337911,0.033234011,0.029590156,0.02634136,0.023502948,0.021047066,0.018826475,0.016841209,0.015082743,0.013551694,0.012170295,0.010921823,0.009832814,0.008851584,0.007978396,0.007192872,0.006495418,0.005867083,0.005306254,0.004803615,0.004347382,0.003936207,0.003572383,0.00323898,0.002940176,0.002670827,0.002432154,0.002211077,0.002014619,0.001830953,0.001670114,0.001519547,0.001384178,0.001266651,0.001155623,0.001055563,0.000964732,0.000881194,0.000805882,0.00073744,0.000675288,0.000618075,0.000566148,0.000519444,0.000476397,0.000436633,0.000400814,0.000367328,0.000337164,0.000309708,0.000284487,0.00026165,0.000240705,0.000221045,0.000203176,0.000187273,0.000172068,0.000158736,0.000146099,0.000134583,0.000123896,0.000114225,0.000105274,3.3578e-05,3.6993e-05,4.0687e-05,4.4858e-05,4.9379e-05,5.4542e-05,5.9569e-05,6.6067e-05,7.2153e-05,7.9956e-05,8.8291e-05,9.6989e-05,0.000106485,0.000117248,0.00012945,0.000142912,0.00015744,0.000173599,0.000191456,0.000210758,0.000233307,0.000257,0.000283769,0.000313229,0.000346375,0.000382284,0.000422354,0.000466706,0.000516221,0.000571093,0.000630362,0.000697262,0.000778115,0.000857033,0.000953227,0.001056708,0.001171348,0.001296729,0.001443256,0.00159997,0.001782145,0.001978054,0.002206831,0.002450378,0.002738232,0.00305294,0.003404114,0.003801716,0.004246934,0.004748534,0.00531285,0.005958374,0.006677879,0.007509595,0.008421184,0.00946123,0.010623578,0.012003654,0.013497167,0.015256561,0.017203175,0.019507368,0.021998071,0.025030029,0.02836702,0.032285431,0.03674255,0.041875757,0.04777812,0.05473958,0.06263999,0.07185967,0.0825196,0.095276184,0.110218087,0.12691898,0.147232856,0.170869861,0.198962143,0.232603827,0.271907204,0.318437202,0.375147509,0.442453927,0.523496206,0.622172398,0.741373235,0.88752531,1.067913809,1.283837459,1.553256774,1.89392119,2.319546048,2.856376834,3.529718366,4.390765279,5.507144883,6.951358275,8.842548945,11.335999031,14.698592959};



 // filename for the final plot (NB: changing the name extension changes the file format)
 string fileName2 = "BR_Sigma_MuMu.pdf";
 string fileName3 = "BR_Sigma_MuMu.png";
 string fileName1 = "BR_Sigma_MuMu.eps";

 // axes labels for the final plot
 string title = ";M_{LQ} (GeV);#sigma#times#beta^{2} (pb)";

 // integrated luminosity
 string lint = "19.7 fb^{-1}";



Double_t mData[19] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 }; 
Double_t x_shademasses[38] = {300.0 , 350.0 , 400.0 , 450.0 , 500.0 , 550.0 , 600.0 , 650.0 , 700.0 , 750.0 , 800.0 , 850.0 , 900.0 , 950.0 , 1000.0 , 1050.0 , 1100.0 , 1150.0 , 1200.0 , 1200.0 , 1150.0 , 1100.0 , 1050.0 , 1000.0 , 950.0 , 900.0 , 850.0 , 800.0 , 750.0 , 700.0 , 650.0 , 600.0 , 550.0 , 500.0 , 450.0 , 400.0 , 350.0 , 300.0 }; 
Double_t xsUp_expected[19] = {0.01615700142 , 0.00797978797 , 0.005081128542 , 0.003488222331 , 0.002728730892 , 0.0019545400467 , 0.001485589677 , 0.0011632183992 , 0.00096118025095 , 0.00071524874624 , 0.00057572766695 , 0.00047206181808 , 0.00035209767863 , 0.000311429227128 , 0.000260314366208 , 0.000251180541952 , 0.000240701029305 , 0.000232385369802 , 0.000229931261986 }; 
Double_t xsUp_observed[19] = {0.02414776833 , 0.00681650585 , 0.0053910999 , 0.003399945932 , 0.002229052658 , 0.0024274091969 , 0.0014807654325 , 0.000819367956 , 0.00066967153007 , 0.00076607752704 , 0.00084817322608 , 0.00065499845364 , 0.00052260284358 , 0.000326210067914 , 0.00020897351897 , 0.000200503079936 , 0.000193022879115 , 0.000186683641831 , 0.000184584485424 }; 
Double_t y_1sigma[38]={0.01160902449 , 0.00571446876 , 0.003626514306 , 0.002495982325 , 0.001947555842 , 0.0013867224585 , 0.001054960026 , 0.0008175063468 , 0.00067318257099 , 0.00049297222912 , 0.00039327391389 , 0.0003188412396 , 0.00022754774699 , 0.000196755551758 , 0.00015660131898 , 0.000150782684416 , 0.00014480222229 , 0.000139799641007 , 0.000138323292718 , 0.00040040320931 , 0.000404676813137 , 0.0004172388231 , 0.000433401916416 , 0.000453312461817 , 0.000512531214704 , 0.00056261916478 , 0.00071855909068 , 0.00086717680371 , 0.00105451919552 , 0.00139411777022 , 0.0016778853036 , 0.002131046787 , 0.0027725823998 , 0.003849045396 , 0.004948163616 , 0.007167248856 , 0.01125598936 , 0.02253284838 }; 
Double_t y_2sigma[38]={0.00874118952 , 0.00428601866 , 0.002709273726 , 0.00185993106 , 0.001454967902 , 0.0010345319291 , 0.000783416445 , 0.0006066002316 , 0.00049748588933 , 0.00036181529216 , 0.0002856148926 , 0.00023142091824 , 0.00015885657538 , 0.000135642028378 , 0.000103210578589 , 9.9098571776e-05 , 9.5434193085e-05 , 9.2137166177e-05 , 9.11641562376e-05 , 0.00065950509565 , 0.000666544133154 , 0.00069014088396 , 0.000714759399424 , 0.000746652100112 , 0.000814630271494 , 0.00087618650592 , 0.00106301286628 , 0.00125717111533 , 0.0015053243072 , 0.00194946258087 , 0.0023242798392 , 0.0029420547465 , 0.0038006439845 , 0.005221863894 , 0.006694499161 , 0.009658837188 , 0.01516896689 , 0.03011750154 }; 




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
   if(( pow(10.0,xsData_vs_m_observed_log->Eval(mtest))/pow(10.0,xsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,xsData_vs_m_observed_log->Eval(mtest+0.1))/pow(10.0,xsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) obslim = mtest; 
  }
  std::cout<<"## LLJJ expected limit: "<<exlim<<" GeV"<<std::endl;
  std::cout<<"## LLJJ observed limit: "<<obslim<<" GeV"<<std::endl;

 // region excluded by Tevatron limits
 Double_t x_shaded[5] = {675,840,840,675,675};// CHANGED FOR LQ2
 Double_t y_shaded[5] = {0.00001,0.00001,50,50,0.00001};// CHANGED FOR LQ2

 Double_t x_shaded2[5] = {300,675,675,300,300};// CHANGED FOR LQ2
 Double_t y_shaded2[5] = {0.00001,0.00001,50,50,0.00001};// CHANGED FOR LQ2

 Double_t x_shaded3[5] = {840,obslim,obslim,840,840};// CHANGED FOR LQ2
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
