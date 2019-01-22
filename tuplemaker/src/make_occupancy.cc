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
    intVars.push_back(make_pair("Spill.spillID","spillID"));
    intVars.push_back(make_pair("Spill.targetPos","targetPos"));
    intVars.push_back(make_pair("Spill.dataQuality","dataQuality"));
    intVars.push_back(make_pair("Event.eventID","eventID"));
    intVars.push_back(make_pair("Event.runID","runID"));
    intVars.push_back(make_pair("Event.NIM1","NIM1"));
    intVars.push_back(make_pair("Event.NIM3","NIM3"));
    intVars.push_back(make_pair("Event.MATRIX1","MATRIX1"));
    intVars.push_back(make_pair("Event.MATRIX2","MATRIX2"));
    intVars.push_back(make_pair("Event.MATRIX3","MATRIX3"));
    intVars.push_back(make_pair("Occupancy.D1","D1"));
    intVars.push_back(make_pair("Occupancy.D2","D2"));
    intVars.push_back(make_pair("Occupancy.D3","D3"));
    intVars.push_back(make_pair("BeamDAQ.Inh_thres","Inh_thres"));
    //intVars.push_back(make_pair("QIE.`RF-16`","RFm16"));
    //intVars.push_back(make_pair("QIE.`RF-15`","RFm15"));
    //intVars.push_back(make_pair("QIE.`RF-14`","RFm14"));
    //intVars.push_back(make_pair("QIE.`RF-13`","RFm13"));
    //intVars.push_back(make_pair("QIE.`RF-12`","RFm12"));
    //intVars.push_back(make_pair("QIE.`RF-11`","RFm11"));
    //intVars.push_back(make_pair("QIE.`RF-10`","RFm10"));
    intVars.push_back(make_pair("QIE.`RF-09`","RFm09"));
    intVars.push_back(make_pair("QIE.`RF-08`","RFm08"));
    intVars.push_back(make_pair("QIE.`RF-07`","RFm07"));
    intVars.push_back(make_pair("QIE.`RF-06`","RFm06"));
    intVars.push_back(make_pair("QIE.`RF-05`","RFm05"));
    intVars.push_back(make_pair("QIE.`RF-04`","RFm04"));
    intVars.push_back(make_pair("QIE.`RF-03`","RFm03"));
    intVars.push_back(make_pair("QIE.`RF-02`","RFm02"));
    intVars.push_back(make_pair("QIE.`RF-01`","RFm01"));
    intVars.push_back(make_pair("QIE.`RF+00`","RF00"));
    intVars.push_back(make_pair("QIE.`RF+01`","RFp01"));
    intVars.push_back(make_pair("QIE.`RF+02`","RFp02"));
    intVars.push_back(make_pair("QIE.`RF+03`","RFp03"));
    intVars.push_back(make_pair("QIE.`RF+04`","RFp04"));
    intVars.push_back(make_pair("QIE.`RF+05`","RFp05"));
    intVars.push_back(make_pair("QIE.`RF+06`","RFp06"));
    intVars.push_back(make_pair("QIE.`RF+07`","RFp07"));
    intVars.push_back(make_pair("QIE.`RF+08`","RFp08"));
    intVars.push_back(make_pair("QIE.`RF+09`","RFp09"));
    intVars.push_back(make_pair("GREATEST(QIE.`RF-08`,QIE.`RF-07`,QIE.`RF-06`,QIE.`RF-05`,QIE.`RF-04`,QIE.`RF-03`,QIE.`RF-02`,QIE.`RF-01`,QIE.`RF+00`,QIE.`RF+01`,QIE.`RF+02`,QIE.`RF+03`,QIE.`RF+04`,QIE.`RF+05`,QIE.`RF+06`,QIE.`RF+07`,QIE.`RF+08`)","RFmax"));
    //"QIE.`RF-08`,QIE.`RF-07`,QIE.`RF-06`,QIE.`RF-05`,QIE.`RF-04`,QIE.`RF-03`,QIE.`RF-02`,QIE.`RF-01`,QIE.`RF+00`,QIE.`RF+01`,QIE.`RF+02`,QIE.`RF+03`,QIE.`RF+04`,QIE.`RF+05`,QIE.`RF+06`,QIE.`RF+07`,QIE.`RF+08`"
    //intVars.push_back(make_pair("QIE.`RF+10`","RFp10"));
    //intVars.push_back(make_pair("QIE.`RF+11`","RFp11"));
    //intVars.push_back(make_pair("QIE.`RF+12`","RFp12"));
    //intVars.push_back(make_pair("QIE.`RF+13`","RFp13"));
    //intVars.push_back(make_pair("QIE.`RF+14`","RFp14"));
    //intVars.push_back(make_pair("QIE.`RF+15`","RFp15"));
    //intVars.push_back(make_pair("QIE.`RF+16`","RFp16"));
    //intVars.push_back(make_pair("QIE.sum_0","sum_0"));//empty
    //intVars.push_back(make_pair("QIE.sum_1","sum_1"));//empty
    //intVars.push_back(make_pair("QIE.sum_2","sum_2"));//empty
    //intVars.push_back(make_pair("QIE.sum_3","sum_3"));//empty
    //intVars.push_back(make_pair("",""));

    vector <pair<string,string> > doubleVars;
    //doubleVars.push_back(make_pair("QIE.Intensity","Intensity"));
    doubleVars.push_back(make_pair("QIE.PotPerQie","PotPerQie"));
    //doubleVars.push_back(make_pair("QIE.Intensity_p","Intensity_p"));
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
        //if (i<intVars.size()-1)
        querystring+= ", ";//no comma after last var
        save->Branch(intVars[i].second.c_str(),&(intVarVals[i]),(intVars[i].second+"/I").c_str());
    }

    double* doubleVarVals = new double[doubleVars.size()];
    for (int i=0;i<doubleVars.size();i++) {
        querystring += doubleVars[i].first + " AS " + doubleVars[i].second;
        if (i<doubleVars.size()-1) querystring+= ", ";//no comma after last var
        save->Branch(doubleVars[i].second.c_str(),&(doubleVarVals[i]),(doubleVars[i].second+"/D").c_str());
    }

    querystring += " FROM run_RUNNUM_R007.Event Event";
    querystring += " JOIN run_RUNNUM_R007.Occupancy Occupancy ON Event.eventID = Occupancy.eventID";
    querystring += " JOIN run_RUNNUM_R007.Spill Spill ON Event.spillID = Spill.spillID";
    querystring += " JOIN run_RUNNUM_R007.BeamDAQ BeamDAQ ON Event.spillID = BeamDAQ.spillID";
    querystring += " JOIN run_RUNNUM_R007.QIE QIE ON Event.eventID = QIE.eventID";

    querystring += " WHERE Spill.dataQuality=0 AND (Event.eventID%100=0 OR Event.NIM3)"; //prescale non-NIM3 events by 100
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

