using namespace TMVA::Experimental;

void TMVA_SOFIE_ONNX(std::string inputFile = ""){
   if (inputFile.empty() )
      inputFile = std::string(gROOT->GetTutorialsDir()) + "/tmva/Linear_16.onnx";

    //Creating parser object to parse ONNX files
    SOFIE::RModelParser_ONNX parser;
    SOFIE::RModel model = parser.Parse(inputFile);

    //Generating inference code
    model.Generate();
    // write the code in a file (by default Linear_16.hxx and Linear_16.dat
    model.OutputGenerated();

    //Printing required input tensors
    model.PrintRequiredInputTensors();

    //Printing initialized tensors (weights)
    std::cout<<"\n\n";
    model.PrintInitializedTensors();

    //Printing intermediate tensors
    std::cout<<"\n\n";
    model.PrintIntermediateTensors();

    //Printing generated inference code
    std::cout<<"\n\n";
    model.PrintGenerated();
}