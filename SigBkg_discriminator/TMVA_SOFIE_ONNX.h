using namespace TMVA::Experimental;

void TMVA_SOFIE_ONNX(std::string inputFile = ""){
    //Creating parser object to parse ONNX files
    SOFIE::RModelParser_ONNX parser;
    SOFIE::RModel model = parser.Parse(inputFile);

    //Generating inference code
    model.Generate();
    // write the code in a file
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