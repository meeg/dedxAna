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

// tsv, database, port, roadset, password, output filename
int main(int argc,char** argv)
{
    vector <pair<string,string> > intVars;
    intVars.push_back(make_pair("kDimuon.dimuonID","dimuonID"));
    intVars.push_back(make_pair("kDimuon.runID","runID"));
    intVars.push_back(make_pair("kDimuon.eventID","eventID"));
    intVars.push_back(make_pair("pTrack.trackID","ptrackID"));
    intVars.push_back(make_pair("pTrack.charge","pcharge"));
    intVars.push_back(make_pair("pTrack.numHits","pnumHits"));
    intVars.push_back(make_pair("nTrack.trackID","ntrackID"));
    intVars.push_back(make_pair("nTrack.charge","ncharge"));
    intVars.push_back(make_pair("nTrack.numHits","nnumHits"));
    intVars.push_back(make_pair("Spill.spillID","spillID"));
    intVars.push_back(make_pair("Spill.targetPos","targetPos"));
    intVars.push_back(make_pair("Spill.dataQuality","dataQuality"));
    intVars.push_back(make_pair("Event.NIM1","NIM1"));
    intVars.push_back(make_pair("Event.NIM3","NIM3"));
    intVars.push_back(make_pair("Event.MATRIX1","MATRIX1"));
    intVars.push_back(make_pair("Event.MATRIX2","MATRIX2"));
    intVars.push_back(make_pair("Event.MATRIX3","MATRIX3"));
    intVars.push_back(make_pair("Occupancy.D1","D1"));
    intVars.push_back(make_pair("Occupancy.D2","D2"));
    intVars.push_back(make_pair("Occupancy.D3","D3"));
    intVars.push_back(make_pair("QIE.`RF+00`","RF00"));
    //intVars.push_back(make_pair("",""));

    vector <pair<string,string> > doubleVars;
    doubleVars.push_back(make_pair("kDimuon.mass","mass"));
    doubleVars.push_back(make_pair("kDimuon.xF","xF"));
    doubleVars.push_back(make_pair("kDimuon.xB","xB"));
    doubleVars.push_back(make_pair("kDimuon.xT","xT"));
    doubleVars.push_back(make_pair("kDimuon.chisq_dimuon","chisq_dimuon"));
    doubleVars.push_back(make_pair("pTrack.chisq","pchisq"));
    doubleVars.push_back(make_pair("pTrack.chisq_target","pchisq_target"));
    doubleVars.push_back(make_pair("pTrack.chisq_dump","pchisq_dump"));
    doubleVars.push_back(make_pair("pTrack.chisq_upstream","pchisq_upstream"));
    doubleVars.push_back(make_pair("nTrack.chisq","nchisq"));
    doubleVars.push_back(make_pair("nTrack.chisq_target","nchisq_target"));
    doubleVars.push_back(make_pair("nTrack.chisq_dump","nchisq_dump"));
    doubleVars.push_back(make_pair("nTrack.chisq_upstream","nchisq_upstream"));
    doubleVars.push_back(make_pair("QIE.PotPerQie","PotPerQie"));
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

    querystring += " FROM run_RUNNUM_R008.kDimuon kDimuon";
    querystring += " JOIN run_RUNNUM_R008.kTrack pTrack ON kDimuon.posTrackID = pTrack.trackID";
    querystring += " JOIN run_RUNNUM_R008.kTrack nTrack ON kDimuon.negTrackID = nTrack.trackID";
    querystring += " JOIN run_RUNNUM_R007.Spill Spill ON kDimuon.spillID = Spill.spillID";
    querystring += " JOIN run_RUNNUM_R007.Event Event ON kDimuon.eventID = Event.eventID";
    querystring += " JOIN run_RUNNUM_R007.Occupancy Occupancy ON kDimuon.eventID = Occupancy.eventID";
    querystring += " JOIN run_RUNNUM_R007.QIE QIE ON Event.eventID = QIE.eventID";

    querystring += " WHERE chisq_dimuon<25 AND pTrack.chisq_target<20 AND nTrack.chisq_target<20";
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

