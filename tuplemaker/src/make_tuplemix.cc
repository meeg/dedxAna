#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include <unistd.h>

#include <TFile.h>
#include <TTree.h>

#include <boost/algorithm/string/replace.hpp>

#include <stdint.h>
#include "mysql_connection.h"
#include "mysql_driver.h"

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>

using namespace std;

void add_var(vector <pair<string,string> > &vars, string table, string column)
{
    vars.push_back(make_pair(table+"."+column, column));
}

void add_trackvar(vector <pair<string,string> > &vars, string table, string column)
{
    vars.push_back(make_pair("p"+table+"."+column, "p"+column));
    vars.push_back(make_pair("n"+table+"."+column, "n"+column));
}

// tsv, database, port, roadset, password, output filename
int main(int argc,char** argv)
{
    vector <pair<string,string> > intVars;
    add_var(intVars,"kDimuon","dimuonID");
    add_var(intVars,"kDimuon","runID");
    add_var(intVars,"kDimuon","eventID");

    add_trackvar(intVars,"Track","trackID");
    add_trackvar(intVars,"Track","charge");
    add_trackvar(intVars,"Track","numHits");
    add_trackvar(intVars,"Track","numHitsSt1");
    add_trackvar(intVars,"Track","numHitsSt2");
    add_trackvar(intVars,"Track","numHitsSt3");
    add_trackvar(intVars,"Track","roadID");
    add_var(intVars,"kDimuon","targetPos");
    add_trackvar(intVars,"Spill","spillID");
    add_trackvar(intVars,"Spill","dataQuality");
    add_trackvar(intVars,"Event","NIM1");
    add_trackvar(intVars,"Event","NIM3");
    add_trackvar(intVars,"Event","MATRIX1");
    add_trackvar(intVars,"Event","MATRIX2");
    add_trackvar(intVars,"Event","MATRIX3");
    add_trackvar(intVars,"Occupancy","D1");
    add_trackvar(intVars,"Occupancy","D2");
    add_trackvar(intVars,"Occupancy","D3");
    add_trackvar(intVars,"BeamDAQ","Inh_thres");
    intVars.push_back(make_pair("pQIE.`RF+00`","pRF00"));
    intVars.push_back(make_pair("nQIE.`RF+00`","nRF00"));
    //intVars.push_back(make_pair("",""));

    vector <pair<string,string> > doubleVars;
    add_var(doubleVars,"kDimuon","mass");
    add_var(doubleVars,"kDimuon","xF");
    add_var(doubleVars,"kDimuon","xB");
    add_var(doubleVars,"kDimuon","xT");
    add_var(doubleVars,"kDimuon","costh");
    add_var(doubleVars,"kDimuon","dx");
    add_var(doubleVars,"kDimuon","dy");
    add_var(doubleVars,"kDimuon","dz");
    add_var(doubleVars,"kDimuon","dpx");
    add_var(doubleVars,"kDimuon","dpy");
    add_var(doubleVars,"kDimuon","dpz");
    add_var(doubleVars,"kDimuon","trackSeparation");
    add_var(doubleVars,"kDimuon","chisq_dimuon");

    add_trackvar(doubleVars,"Track","chisq");
    add_trackvar(doubleVars,"Track","chisq_target");
    add_trackvar(doubleVars,"Track","chisq_dump");
    add_trackvar(doubleVars,"Track","chisq_upstream");
    add_trackvar(doubleVars,"Track","px1");
    add_trackvar(doubleVars,"Track","py1");
    add_trackvar(doubleVars,"Track","pz1");
    add_trackvar(doubleVars,"Track","px3");
    add_trackvar(doubleVars,"Track","py3");
    add_trackvar(doubleVars,"Track","pz3");
    add_trackvar(doubleVars,"Track","xT");
    add_trackvar(doubleVars,"Track","xD");
    add_trackvar(doubleVars,"Track","yT");
    add_trackvar(doubleVars,"Track","yD");
    add_trackvar(doubleVars,"Track","z0");
    add_trackvar(doubleVars,"Track","y1");
    add_trackvar(doubleVars,"Track","y3");
    add_trackvar(doubleVars,"QIE","PotPerQie");
    //doubleVars.push_back(make_pair("",""));

    /*
       int c;
       while ((c = getopt(argc,argv,"h")) !=-1)
       switch (c)
       {
       case 'h':
       printf("-h: print this help\n");
       return(0);
       break;
       case 'Z':
       max_vz = atof(optarg);
       break;
       case 'c':
       cut_on_acceptance = true;;
       break;
       case '?':
       printf("Invalid option or missing option argument; -h to list options\n");
       return(1);
       default:
       abort();
       }
       if ( argc-optind < 2 )
       {
       printf("<input stdhep filename> <output stdhep filename>\n");
       return 1;
       }
       */

    const string user = "seaguest";
    const string pass = argv[5];
    FILE * runfile = fopen(argv[1],"r");
    const string host = argv[2];
    const string port = argv[3];
    string url = host+":"+port;
    const int roadset = atoi(argv[4]);
    TFile* saveFile = new TFile(argv[6], "recreate");
    TTree* save = new TTree("save", "save");

    sql::Driver * driver = sql::mysql::get_driver_instance();
    std::auto_ptr< sql::Connection > con(driver->connect(url, user, pass));
    std::auto_ptr< sql::Statement > stmt(con->createStatement());

    string querystring = "SELECT ";

    int* intVarVals = new int[intVars.size()];
    for (int i=0;i<intVars.size();i++) {
        querystring += intVars[i].first + " AS " + intVars[i].second;
        querystring+= ", ";
        save->Branch(intVars[i].second.c_str(),&(intVarVals[i]),(intVars[i].second+"/I").c_str());
    }

    double* doubleVarVals = new double[doubleVars.size()];
    for (int i=0;i<doubleVars.size();i++) {
        querystring += doubleVars[i].first + " AS " + doubleVars[i].second;
        if (i<doubleVars.size()-1) querystring+= ", ";//no comma after last var
        save->Branch(doubleVars[i].second.c_str(),&(doubleVarVals[i]),(doubleVars[i].second+"/D").c_str());
    }

    
    querystring += " FROM run_RUNNUM_R008.kDimuonMix kDimuon";
    querystring += " JOIN run_RUNNUM_R008.kTrackMix pTrack ON kDimuon.posTrackID = pTrack.trackID";
    querystring += " JOIN run_RUNNUM_R008.kTrackMix nTrack ON kDimuon.negTrackID = nTrack.trackID";
    querystring += " JOIN run_RUNNUM_R008.kEventMix kEvent ON kDimuon.eventID = kEvent.eventID";
    
    querystring += " JOIN run_RUNNUM_R007.Event pEvent ON kEvent.source1 = pEvent.eventID";
    querystring += " JOIN run_RUNNUM_R007.Occupancy pOccupancy ON kEvent.source1 = pOccupancy.eventID";
    querystring += " JOIN run_RUNNUM_R007.QIE pQIE ON kEvent.source1 = pQIE.eventID";
    querystring += " JOIN run_RUNNUM_R007.Spill pSpill ON pEvent.spillID = pSpill.spillID";
    querystring += " JOIN run_RUNNUM_R007.BeamDAQ pBeamDAQ ON pEvent.spillID = pBeamDAQ.spillID";

    querystring += " JOIN run_RUNNUM_R007.Event nEvent ON kEvent.source2 = nEvent.eventID";
    querystring += " JOIN run_RUNNUM_R007.Occupancy nOccupancy ON kEvent.source2 = nOccupancy.eventID";
    querystring += " JOIN run_RUNNUM_R007.QIE nQIE ON kEvent.source2 = nQIE.eventID";
    querystring += " JOIN run_RUNNUM_R007.Spill nSpill ON nEvent.spillID = nSpill.spillID";
    querystring += " JOIN run_RUNNUM_R007.BeamDAQ nBeamDAQ ON nEvent.spillID = nBeamDAQ.spillID";

    querystring += " WHERE pSpill.dataQuality=0 AND nSpill.dataQuality=0 AND chisq_dimuon<25 AND pTrack.chisq_target<20 AND nTrack.chisq_target<20";
    //printf("%s \n",querystring.c_str());


    char line[1000];
    char thisrunstr[100];
    char thishost[100];
    int thisroadset;
    int numvals;
    while (fgets(line,1000,runfile)!=NULL) {
        numvals = sscanf(line," %s %*d %s %*d %d %*s %*d", &thisrunstr, &thishost, &thisroadset);
        if (numvals==3 && host==thishost && roadset==thisroadset) {
            //printf("%s, %s, %d\n",thisrunstr, thishost, thisroadset);
            printf(line);
            string newquery = boost::replace_all_copy(querystring,"RUNNUM",thisrunstr);
            //printf("%s\n",newquery.c_str());

            try {
                con->reconnect();
                std::auto_ptr< sql::ResultSet > res(stmt->executeQuery(newquery));
                //std::auto_ptr< sql::ResultSet > res(stmt->executeQuery("SELECT dimuonID FROM run_015789_R008.kDimuon"));

                while (res->next()) {
                    for (int i=0;i<intVars.size();i++)
                        intVarVals[i] = res->getInt(intVars[i].second);
                    for (int i=0;i<doubleVars.size();i++)
                        doubleVarVals[i] = res->getDouble(doubleVars[i].second);
                    save->Fill();
                }
            } catch (sql::SQLException &e) {
                printf("SQLException: %s\nquery:\n%s\n",e.what(),newquery.c_str());
            }
        }
    }

    //save->Write();
    saveFile->Write();
    saveFile->Close();
}

