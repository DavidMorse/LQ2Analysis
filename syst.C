void syst(){

  double obs=36.;
  //double obs=32.;
  double totBG = 0.;
  
  double rate[6]={44.624561372,7.96911718752,1.70575867382,13.955665047,0.458642547066,2.1800948954};
  double MES[6]={1.00190782086,1.04244839913,1.57711169487,1.22531446612,2.98083352034,1.05447506672};
  double LUMI[6]={1.026,1.00151708056,1.00046881486,1.00204231074,1.026,1.026};
  double PU[6]={1.00057715341,1.03000048706,1.09230441354,1.0113784605,1.04231165348,1.06239793394};
  double JER[6]={1.00783079009,1.06211338189,1.1398220727,1.01369892376,1,1.00950855018};
  double SHAPEW[6]={1,1.000058662,1.00002736211,1.23762379139,1,1};
  double ALIGN[6]={1.01,1.04477205989,1.04520466244,1.04553818218,1.04518,1.04518};
  double SHAPEZ[6]={1,1.0002711989,1.2262706629,1.00014148749,1,1};
  double MUONHLT[6]={1.01,1.00065059095,1.0002794774,1.00028558105,1.01,1.01};
  double SHAPETT[6]={1,1.04688563403,1.00003266353,1.00006632929,1,1};
  double JES[6]={1.00024463039,1.01946829683,1.08100582563,1.02753375339,1,1.09702122746};
  double MUONIDISO[6]={1.02,1.00077290141,1.00033303879,1.00116397879,1.02,1.02};
  double TTNORM[6]={1,1.01970295489,1.00012758861,1.00036753869,1,1};
  double ZNORM[6]={1,1.00030302069,1.01092601446,1.00027812795,1,1};
  double MER[6]={1.00149615724,1.01765090028,1.39154786266,1.02706090571,1.92831574476,1.11596502223};
  double WNORM[6]={1,1.00039768846,1.00001898333,1.01192609311,1,1};
  double PDF[6]={1.03,1.14290994488,1.03476734171,1.04763195924,1.0878,1.0403};
  /*

  double rate[6]={43.1768540374,7.47593531023,1.45166013679,12.1165062831,0.461221018893,2.06878905456};
  double JER[6]={1.0078880033,1.0557933371,1.19589481162,1.01544506083,1,1.01904437277};
  double LUMI[6]={1.044,1.00209428349,1.00129046527,1.00332795684,1.044,1.044};
  double JES[6]={1.00080201251,1.04720740441,1.09206802903,1.03457501753,1,1.07419327157};
  double ZNORM[6]={1,1.00020729012,1.01165056071,1.00016274297,1,1};
  double ALIGN[6]={1.01,1.04522715582,1.04513229611,1.04533215843,1.04518,1.04518};
  double PU[6]={1.0008661235,1.02753612814,1.08572200493,1.01728515855,1.04231165348,1.08836795804};
  double SHAPEZ[6]={1,1.00024275051,1.03317996447,1.00010029178,1,1};
  double MES[6]={1.00195709603,1.02417104074,1.32248472877,1.19055044808,1.92950558807,1};
  double SHAPEW[6]={1,1.00007987269,1.00012480221,1.09124174984,1,1};
  double MUONHLT[6]={1.01,1.00040411374,1.00046722897,1.00072177853,1.01,1.01};
  double SHAPETT[6]={1,1.19925138229,1.00002165101,1.00010511708,1,1};
  double PDF[6]={1.02,1.04985978792,1.0191654116,1.10535700924,1.128,1.0227};
  double TTNORM[6]={1,1.01978230091,1.0001594937,1.0001299035,1,1};
  double WNORM[6]={1,1.00020597309,1.00015206936,1.0119602991,1,1};
  double MUONIDISO[6]={1.02,1.00072748501,1.0005256945,1.00139483838,1.02,1.02};
  double MER[6]={1.00250470296,1.04925222346,1.19368462912,1.01245243891,2.05251777557,1.04727797388 };
  */
   for(int i=1;i<6;i++){
    totBG+=rate[i];
  }
  cout<<"totBG: "<<totBG<<endl;

  double totMES=0.,totLUMI=0.,totPU=0.,totJER=0.,totSHAPEW=0.,totALIGN=0.,totSHAPEZ=0.,totMUONHLT=0.,totSHAPETT=0.,totJES=0.,totMUONIDISO=0.,totTTNORM=0.,totZNORM=0.,totMER=0.,totWNORM=0.,totPDF=0.;
  for(int i=1;i<6;i++){
    totMES+=rate[i]*(1.-MES[i])*rate[i]*(1.-MES[i]);
    totLUMI+=rate[i]*(1.-LUMI[i])*rate[i]*(1.-LUMI[i]);
    totPU+=rate[i]*(1.-PU[i])*rate[i]*(1.-PU[i]);
    totJER+=rate[i]*(1.-JER[i])*rate[i]*(1.-JER[i]);
    totSHAPEW+=rate[i]*(1.-SHAPEW[i])*rate[i]*(1.-SHAPEW[i]);
    totALIGN+=rate[i]*(1.-ALIGN[i])*rate[i]*(1.-ALIGN[i]);
    totSHAPEZ+=rate[i]*(1.-SHAPEZ[i])*rate[i]*(1.-SHAPEZ[i]);
    totMUONHLT+=rate[i]*(1.-MUONHLT[i])*rate[i]*(1.-MUONHLT[i]);
    totSHAPETT+=rate[i]*(1.-SHAPETT[i])*rate[i]*(1.-SHAPETT[i]);
    totJES+=rate[i]*(1.-JES[i])*rate[i]*(1.-JES[i]);
    totMUONIDISO+=rate[i]*(1.-MUONIDISO[i])*rate[i]*(1.-MUONIDISO[i]);
    totTTNORM+=rate[i]*(1.-TTNORM[i])*rate[i]*(1.-TTNORM[i]);
    totZNORM+=rate[i]*(1.-ZNORM[i])*rate[i]*(1.-ZNORM[i]);
    totMER+=rate[i]*(1.-MER[i])*rate[i]*(1.-MER[i]);
    totWNORM+=rate[i]*(1.-WNORM[i])*rate[i]*(1.-WNORM[i]);
    totPDF+=rate[i]*(1.-PDF[i])*rate[i]*(1.-PDF[i]);
  }
  double totMES2=sqrt(totMES)/totBG;
  double totLUMI2=sqrt(totLUMI)/totBG;
  double totPU2=sqrt(totPU)/totBG;
  double totJER2=sqrt(totJER)/totBG;
  double totSHAPEW2=sqrt(totSHAPEW)/totBG;
  double totALIGN2=sqrt(totALIGN)/totBG;
  double totSHAPEZ2=sqrt(totSHAPEZ)/totBG;
  double totMUONHLT2=sqrt(totMUONHLT)/totBG;
  double totSHAPETT2=sqrt(totSHAPETT)/totBG;
  double totJES2=sqrt(totJES)/totBG;
  double totMUONIDISO2=sqrt(totMUONIDISO)/totBG;
  double totTTNORM2=sqrt(totTTNORM)/totBG;
  double totZNORM2=sqrt(totZNORM)/totBG;
  double totMER2=sqrt(totMER)/totBG;
  double totWNORM2=sqrt(totWNORM)/totBG;
  double totPDF2=sqrt(totPDF)/totBG;

  cout<<"totMES=       "<<totMES2<<endl;
  cout<<"totLUMI=      "<<totLUMI2<<endl;
  cout<<"totPU=        "<<totPU2<<endl;
  cout<<"totJER=       "<<totJER2<<endl;
  cout<<"totSHAPEW=    "<<totSHAPEW2<<endl;
  cout<<"totALIGN=     "<<totALIGN2<<endl;
  cout<<"totSHAPEZ=    "<<totSHAPEZ2<<endl;
  cout<<"totMUONHLT=   "<<totMUONHLT2<<endl;
  cout<<"totSHAPETT=   "<<totSHAPETT2<<endl;
  cout<<"totJES=       "<<totJES2<<endl;
  cout<<"totMUONIDISO= "<<totMUONIDISO2<<endl;
  cout<<"totTTNORM=    "<<totTTNORM2<<endl;
  cout<<"totZNORM=     "<<totZNORM2<<endl;
  cout<<"totMER=       "<<totMER2<<endl;
  cout<<"totWNORM=     "<<totWNORM2<<endl;
  cout<<"totPDF=       "<<totPDF2<<endl;

  double totErr = sqrt(totMES+totLUMI+totPU+totJER+totSHAPEW+totALIGN+totSHAPEZ+totMUONHLT+totSHAPETT+totJES+totMUONIDISO+totTTNORM+totZNORM+totMER+totWNORM+totPDF)/totBG;

  cout<<"totErr=       "<<totErr<<endl;
  cout<<"totErr=       "<<totErr*totBG<<endl;



  return;
}
