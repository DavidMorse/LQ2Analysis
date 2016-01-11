#include <TCanvas>
#include <TH1>
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

void plotRPV(){

  using namespace std;

  gStyle->SetOptStat(0);

  gStyle->SetPaintTextFormat("4.2f");
 
  TCanvas *c1 = new TCanvas("c1","",1400,1000);
  c1->cd();


  TFile f_200("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj200.root","READ");
  TFile f_250("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj250.root","READ");
  TFile f_300("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj300.root","READ");
  TFile f_350("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj350.root","READ");
  TFile f_400("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj400.root","READ");
  TFile f_450("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj450.root","READ");
  TFile f_500("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj500.root","READ");
  TFile f_550("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj550.root","READ");
  TFile f_600("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj600.root","READ");
  TFile f_650("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj650.root","READ");
  TFile f_700("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj700.root","READ");
  TFile f_750("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj750.root","READ");
  TFile f_800("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj800.root","READ");
  TFile f_850("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj850.root","READ");
  TFile f_900("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj900.root","READ");
  TFile f_950("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj950.root","READ");
  TFile f_1000("NTupleAnalyzer_FullJuly24_2014_07_24_17_24_05/SummaryFiles/RVuujj1000.root","READ");


  TTree* trees[17]={(TTree*)f_200.Get("PhysicalVariables"),
		    (TTree*)f_250.Get("PhysicalVariables"),
		    (TTree*)f_300.Get("PhysicalVariables"),
		    (TTree*)f_350.Get("PhysicalVariables"),
		    (TTree*)f_400.Get("PhysicalVariables"),
		    (TTree*)f_450.Get("PhysicalVariables"),
		    (TTree*)f_500.Get("PhysicalVariables"),
		    (TTree*)f_550.Get("PhysicalVariables"),
		    (TTree*)f_600.Get("PhysicalVariables"),
		    (TTree*)f_650.Get("PhysicalVariables"),
		    (TTree*)f_700.Get("PhysicalVariables"),
		    (TTree*)f_750.Get("PhysicalVariables"),
		    (TTree*)f_800.Get("PhysicalVariables"),
		    (TTree*)f_850.Get("PhysicalVariables"),
		    (TTree*)f_900.Get("PhysicalVariables"),
		    (TTree*)f_950.Get("PhysicalVariables"),
		    (TTree*)f_1000.Get("PhysicalVariables")};
  

  float L_int=19600.;

  TCut cuts[18]={"(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>0)&&(St_uujj>0)&&(M_uujj2>0)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>100)&&(St_uujj>0)&&(M_uujj2>0)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>100)&&(St_uujj>380)&&(M_uujj2>0)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>100)&&(St_uujj>380)&&(M_uujj2>115)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>115)&&(St_uujj>460)&&(M_uujj2>115)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>125)&&(St_uujj>540)&&(M_uujj2>120)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>140)&&(St_uujj>615)&&(M_uujj2>135)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>150)&&(St_uujj>685)&&(M_uujj2>155)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>165)&&(St_uujj>755)&&(M_uujj2>180)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>175)&&(St_uujj>820)&&(M_uujj2>210)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>185)&&(St_uujj>880)&&(M_uujj2>250)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>195)&&(St_uujj>935)&&(M_uujj2>295)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>205)&&(St_uujj>990)&&(M_uujj2>345)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>215)&&(St_uujj>1040)&&(M_uujj2>400)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>220)&&(St_uujj>1090)&&(M_uujj2>465)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>230)&&(St_uujj>1135)&&(M_uujj2>535)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>235)&&(St_uujj>1175)&&(M_uujj2>610)",
		 "(abs(Eta_muon1)<2.1)&&(abs(Eta_muon2)<2.1)&&(abs(Eta_jet1)<2.4)&&(abs(Eta_jet2)<2.4)&&(DR_muon1jet1>0.3)&&(DR_muon1jet2>0.3)&&(DR_muon2jet1>0.3)&&(DR_muon2jet2>0.3)&&(Pt_muon1>45)&&(Pt_muon2>45)&&(Pt_jet1>125)&&(Pt_jet2>45)&&(St_uujj>300)&&(M_uu>50)&&(DR_muon1muon2>0.3)&&(M_uu>245)&&(St_uujj>1210)&&(M_uujj2>690)"};
  
  float bgs[18]={13952.41,
		 2783.1,
		 0.,
		 1583.,
		 819.,
		 434.3,
		 234.7,
		 142.6,
		 77.,
		 47.4,
		 31.,
		 20.3,
		 10.18,
		 5.7,
		 2.71,
		 1.38,
		 0.87,
                 0.41};


  TH2F* h_eff = new TH2F("h_eff",";stop mass;LQ2 optimization cut mass",17,200,1500,18,150,1050);
  TH2F* h_sOverSplusB = new TH2F("h_sOverSplusB",";stop mass;LQ2 optimization cut mass",17,200,1050,18,150,1050);
  TH2F* h_yields = new TH2F("h_yields",";stop mass;LQ2 optimization cut mass",17,200,1050,18,150,1050);
  
  
  //for(int i=0;i<16;++i){
   
    for(int j=0;j<17;++j){

      trees[j]->Draw("weight_nopu");
      TH1F *h_w = (TH1F*)trees[j]->GetHistogram();
      float weight = h_w->GetMean(1)*L_int;
      h_w->Delete();
      
      for(int k=1;k<=18;++k){
     	if(k==3)continue;
	cout<<"j:"<<j<<" k:"<<k<<endl;
	trees[j]->Draw("St_uujj",cuts[k-1],"");
	TH1F *h_St = (TH1F*)trees[j]->GetHistogram();
	float yield = h_St->Integral(0,-1);
	
	/*if(j==0) h_eff->Fill(150+50*(j+1),100+50*k,yield/9500.);
	else if(j==6)h_eff->Fill(150+50*(j+1),100+50*k,yield/9480.);
	else h_eff->Fill(150+50*(j+1),100+50*k,yield/50.);*/
	h_eff->Fill(150+50*(j+1),100+50*k,yield/30000.);
	
	float tot = yield*weight;
	cout<<"xbin:"<<150+50*(j+1)<<"  ybin:"<<100+50*k<<"  tot:"<<tot<<"  bg:"<<bgs[k-1]<<endl;
	h_sOverSplusB->Fill(150+50*(j+1),100+50*k,tot/sqrt(tot+bgs[k-1]));
	h_yields->Fill(150+50*(j+1),100+50*k,tot);
	h_St->Delete();
      }
    }
    //  }
    
    int y=200;
    h_yields->GetYaxis()->SetBinLabel(1,"Preselection");
    h_yields->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
    h_eff->GetYaxis()->SetBinLabel(1,"Preselection");
    h_eff->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
    h_sOverSplusB->GetYaxis()->SetBinLabel(1,"Preselection");
    h_sOverSplusB->GetYaxis()->SetBinLabel(2,"Presel. + m_{#mu#mu}>100");
    for(int b=1;b<=18;b++){
      stringstream ss;ss <<y;
      string str=ss.str();
      cout<<"str: "<<str<<endl;
      h_yields->GetXaxis()->SetBinLabel(b,str.c_str());
      h_eff->GetXaxis()->SetBinLabel(b,str.c_str());
      h_sOverSplusB->GetXaxis()->SetBinLabel(b,str.c_str());
      if(b>=3){
      h_yields->GetYaxis()->SetBinLabel(b+1,str.c_str());
      h_eff->GetYaxis()->SetBinLabel(b+1,str.c_str());
      h_sOverSplusB->GetYaxis()->SetBinLabel(b+1,str.c_str());
      }
      y+=50;
    }
    //h_eff->GetZaxis()->SetRangeUser(0.,1.);
    h_eff->GetYaxis()->SetTitleSize(0.05);
    h_eff->Draw("colztext");
    c1->Print("Plots/efficiencyTable.png");
    c1->Print("Plots/efficiencyTable.pdf");
    
    h_sOverSplusB->GetYaxis()->SetTitleSize(0.05);
    h_sOverSplusB->GetZaxis()->SetRangeUser(.077,140);
    gPad->SetLogz(1);
    h_sOverSplusB->Draw("colztext");
    c1->Print("Plots/sOverSqrtSplusB.png");
    c1->Print("Plots/sOverSqrtSplusB.pdf");
    
    gStyle->SetPaintTextFormat("4.0f");
    //gPad->SetLogz(0);
    h_yields->GetYaxis()->SetTitleSize(0.05);
    h_yields->Draw("colztext");
    c1->Print("Plots/yields.png");
    c1->Print("Plots/yields.pdf");
    


  TH1F* h_xsecs = new TH1F("h_xsecs",";stop mass;#tilde{t}  #tilde{t}   #sigma [pb]",16,200,1000);
  float xsecs[34]={18.5245,.149147,
		   5.57596,.147529,
		   1.99608,.146905,
		   0.807323,.143597,
		   0.35683,.142848,
		   0.169668,.142368,
		   0.0855847,.149611,
		   0.0452067,.158177,
		   0.0248009,.166406,
		   0.0139566,.1756,
		   0.0081141,.184146,
		   0.00480639,.194088,
		   0.00289588,.20516,
		   0.00176742,.21836,
		   0.00109501,.239439,
		   0.000687022,.25834,
		   0.000435488,.276595};
  
  
  for(int i=0;i<17;i++){
    h_xsecs->SetBinContent(i+1,xsecs[2*i]);
    h_xsecs->SetBinError(i+1,xsecs[2*i]*xsecs[2*i+1]);
  }
  c1->SetLogy(1);
  h_xsecs->GetYaxis()->SetRangeUser(4.5e-4,30);
  h_xsecs->Draw("pe");
  h_xsecs->Draw("c hist sames");
  c1->Print("Plots/stopXsecs.png");
  c1->Print("Plots/stopXsecs.pdf");
    
    
    
}
