#include <iostream>
#include <memory>
#include <string>
#include <optional>

#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/grpcpp.h>
#include <grpcpp/health_check_service_interface.h>
#include <argparse/argparse.hpp>

#include "core-people.grpc.pb.h"

#include "processRequest.hpp"
#include "PeopleDetector.hpp"


bool isNumber(const std::string& str)
{
    for(char const& c : str) {
        if(!std::isdigit(c))
            return false;
    }
    return true;
}

class PeopleServiceImpl final : public People::Service {
public:
    PeopleServiceImpl(const cv::FileStorage& cascadeFile) : cascadeFile(cascadeFile) {}

private:
    grpc::Status get_result(grpc::ServerContext* context,
                            const PeopleRequest* request,
                            PeopleResponse* reply) override {
        std::cout << "new request\n";
        processRequest(cascadeFile, request, reply);
        return grpc::Status::OK;
    }

    const cv::FileStorage& cascadeFile;
};

int main(int argc, char** argv) {
    // parse args
    argparse::ArgumentParser program("peopleServer");
    program.add_argument("--port")
        .default_value(std::string{"50060"})
        .help("specify server port");

    try {
        program.parse_args(argc, argv);
    }
    catch (const std::runtime_error& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        std::exit(1);
    }

    auto port = program.get<std::string>("--port");
    if(!isNumber(port)){
        std::cerr << "port must be a number" << std::endl;
        std::exit(1);
    }
    std::string serverAddress("localhost:" + port);

    // open cascade file
    const std::string cascadePath = "cascades/haarcascade_frontalface_default.xml";
    cv::FileStorage cascadeFile(cascadePath, cv::FileStorage::READ);
    if(!cascadeFile.isOpened()){
        std::cerr << "could not open " << cascadePath << " file\n";
        std::exit(1);
    }

    // start grpc server
    grpc::EnableDefaultHealthCheckService(true);
    grpc::reflection::InitProtoReflectionServerBuilderPlugin();

    PeopleServiceImpl service(cascadeFile);
    int selectedPort = 0;
    grpc::ServerBuilder builder;
    builder.AddListeningPort(serverAddress, grpc::InsecureServerCredentials(), &selectedPort);
    builder.RegisterService(&service);

    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    if(!server){
        std::cerr << "Could not start server" << std::endl;
        std::exit(1);
    }
    std::cout << "Server listening on localhost:" << selectedPort << std::endl;

    server->Wait();

    return 0;
}
