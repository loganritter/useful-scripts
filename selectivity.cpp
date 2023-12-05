#include <iomanip>
#include <iostream>
#include <cstdlib>
#include <fstream>

int main(int argc, char * argv[])
{
    if( argc != 6) {
        std::cout<< "Usage:\n"<< argv[0] << " <P> <A> <B> <fileA> <fileB>\n";
        std::cout<< "P     - Pressure\n";
        std::cout<< "A     - moles of species A per unit volume in bulk phase.\n";
        std::cout<< "B     - moles of species B per unit volume in bulk phase.\n";
        std::cout<< "fileA - filename of text file whose contents is a single number: the\n        avg moles sorbed of species A.\n";
        std::cout<< "fileB - filename of text file whose contents is a single number: the\n        avg moles sorbed of species B.\n";
        exit(0);
    }

    double P = atof(argv[1]);
    double A = atof(argv[2]);
    double B = atof(argv[3]);
    double Total = A + B;
    double yA = A / Total;
    double yB = B / Total;

    double xA = 0;
    double xB = 0;

    std::fstream Afile(argv[4], std::ios_base::in);
    Afile >> A;
    std::fstream Bfile(argv[5], std::ios_base::in);
    Bfile >> B;

    Total = A + B;
    xA = A / Total;
    xB = B / Total;

    Afile.close();
    Bfile.close();
    std::cout<< std::fixed << std::setprecision(5);
    std::cout << std::setw(10) << P << "\t " << std::setw(10) << (xA/yA)/(xB/yB) <<"\n";

    return 0;
}
