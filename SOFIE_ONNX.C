{
   std::string inputName = "out/model_19.onnx";
   using namespace TMVA::Experimental;
   SOFIE::RModelParser_ONNX parser;
   std::cout << "parsing file " << inputName << std::endl;
   SOFIE::RModel model = parser.Parse(inputName);
   model.Generate();
   model.OutputGenerated();//outputName);
   std::cout << "output written " << std::endl;
}