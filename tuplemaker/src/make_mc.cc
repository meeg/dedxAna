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

void add_trackvar(vector <pair<string,string> > &vars, string column)
{
    vars.push_back(make_pair("pTrack."+column, "p"+column));
    vars.push_back(make_pair("nTrack."+column, "n"+column));
}

// tsv, database, port, roadset, password, output filename
int main(int argc,char** argv)
{
    const string user = "seaguest";
    //FILE * runfile = fopen(argv[1],"r");
    const string dbname = argv[1];
    const string host = argv[2];
    const string port = argv[3];
    string url = host+":"+port;
    //const int roadset = atoi(argv[4]);
    const string pass = argv[4];
    TFile* saveFile = new TFile(argv[5], "recreate");
    TTree* save = new TTree("save", "save");

    //bool isMessy = (strstr(dbname,"messy") != NULL);
    bool isMessy = (dbname.find("messy") != string::npos);


    vector <pair<string,string> > intVars;
    add_var(intVars,"kDimuon","dimuonID");
    add_var(intVars,"kDimuon","runID");
    add_var(intVars,"kDimuon","eventID");

    add_var(intVars,"kDimuon","spillID");
    add_var(intVars,"kDimuon","targetPos");

    if (isMessy) {
        add_var(intVars,"kEmbed","eRunID");
        add_var(intVars,"kEmbed","eSpillID");
        add_var(intVars,"kEmbed","eEventID");
    }

    add_trackvar(intVars,"trackID");
    add_trackvar(intVars,"charge");
    add_trackvar(intVars,"numHits");
    add_trackvar(intVars,"numHitsSt1");
    add_trackvar(intVars,"numHitsSt2");
    add_trackvar(intVars,"numHitsSt3");
    add_trackvar(intVars,"roadID");
    //intVars.push_back(make_pair("Spill.spillID","spillID"));
    //intVars.push_back(make_pair("Spill.targetPos","targetPos"));
    //intVars.push_back(make_pair("Spill.dataQuality","dataQuality"));
    //intVars.push_back(make_pair("Event.NIM1","NIM1"));
    //intVars.push_back(make_pair("Event.NIM3","NIM3"));
    //intVars.push_back(make_pair("Event.MATRIX1","MATRIX1"));
    //intVars.push_back(make_pair("Event.MATRIX2","MATRIX2"));
    //intVars.push_back(make_pair("Event.MATRIX3","MATRIX3"));
    //intVars.push_back(make_pair("Occupancy.D1","D1"));
    //intVars.push_back(make_pair("Occupancy.D2","D2"));
    //intVars.push_back(make_pair("Occupancy.D3","D3"));
    //intVars.push_back(make_pair("BeamDAQ.Inh_thres","Inh_thres"));
    //intVars.push_back(make_pair("QIE.`RF+00`","RF00"));
    //intVars.push_back(make_pair("",""));

    vector <pair<string,string> > doubleVars;
    doubleVars.push_back(make_pair("kDimuon.mass","mass"));
    doubleVars.push_back(make_pair("kDimuon.xF","xF"));
    doubleVars.push_back(make_pair("kDimuon.xB","xB"));
    doubleVars.push_back(make_pair("kDimuon.xT","xT"));
    doubleVars.push_back(make_pair("kDimuon.costh","costh"));
    doubleVars.push_back(make_pair("kDimuon.dx","dx"));
    doubleVars.push_back(make_pair("kDimuon.dy","dy"));
    doubleVars.push_back(make_pair("kDimuon.dz","dz"));
    doubleVars.push_back(make_pair("kDimuon.dpx","dpx"));
    doubleVars.push_back(make_pair("kDimuon.dpy","dpy"));
    doubleVars.push_back(make_pair("kDimuon.dpz","dpz"));
    doubleVars.push_back(make_pair("kDimuon.trackSeparation","trackSeparation"));
    doubleVars.push_back(make_pair("kDimuon.chisq_dimuon","chisq_dimuon"));

    add_trackvar(doubleVars,"chisq");
    add_trackvar(doubleVars,"chisq_target");
    add_trackvar(doubleVars,"chisq_dump");
    add_trackvar(doubleVars,"chisq_upstream");
    add_trackvar(doubleVars,"px1");
    add_trackvar(doubleVars,"py1");
    add_trackvar(doubleVars,"pz1");
    add_trackvar(doubleVars,"px3");
    add_trackvar(doubleVars,"py3");
    add_trackvar(doubleVars,"pz3");
    add_trackvar(doubleVars,"xT");
    add_trackvar(doubleVars,"xD");
    add_trackvar(doubleVars,"yT");
    add_trackvar(doubleVars,"yD");
    add_trackvar(doubleVars,"z0");
    add_trackvar(doubleVars,"y1");
    add_trackvar(doubleVars,"y3");
    //doubleVars.push_back(make_pair("pTrack.chisq","pchisq"));
    //doubleVars.push_back(make_pair("pTrack.chisq_target","pchisq_target"));
    //doubleVars.push_back(make_pair("pTrack.chisq_dump","pchisq_dump"));
    //doubleVars.push_back(make_pair("pTrack.chisq_upstream","pchisq_upstream"));
    //doubleVars.push_back(make_pair("nTrack.chisq","nchisq"));
    //doubleVars.push_back(make_pair("nTrack.chisq_target","nchisq_target"));
    //doubleVars.push_back(make_pair("nTrack.chisq_dump","nchisq_dump"));
    //doubleVars.push_back(make_pair("nTrack.chisq_upstream","nchisq_upstream"));
    //doubleVars.push_back(make_pair("QIE.PotPerQie","PotPerQie"));
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

    querystring += " FROM DBNAME.kDimuon kDimuon";
    querystring += " JOIN DBNAME.kTrack pTrack ON kDimuon.posTrackID = pTrack.trackID";
    querystring += " JOIN DBNAME.kTrack nTrack ON kDimuon.negTrackID = nTrack.trackID";
    //querystring += " JOIN DBNAME.Spill Spill ON kDimuon.spillID = Spill.spillID";
    //querystring += " JOIN DBNAME.BeamDAQ BeamDAQ ON kDimuon.spillID = BeamDAQ.spillID";
    //querystring += " JOIN DBNAME.kEvent kEvent ON kDimuon.eventID = kEvent.eventID";
    //querystring += " JOIN DBNAME.Occupancy Occupancy ON kDimuon.eventID = Occupancy.eventID";
    //querystring += " JOIN DBNAME.QIE QIE ON kDimuon.eventID = QIE.eventID";
    if (isMessy) {
        querystring += " JOIN DBNAME.kEmbed kEmbed ON kDimuon.eventID = kEmbed.eventID";
    }

    //querystring += " WHERE Spill.dataQuality=0 AND chisq_dimuon<25 AND pTrack.chisq_target<20 AND nTrack.chisq_target<20";
    //printf("%s \n",querystring.c_str());


    char line[1000];
    char thisrunstr[100];
    char thishost[100];
    int thisroadset;
    int numvals;
    string newquery = boost::replace_all_copy(querystring,"DBNAME",dbname);
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

    //save->Write();
    saveFile->Write();
    saveFile->Close();
}

